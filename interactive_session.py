"""
Interactive Session Manager for MCP Your Turn Server

This module manages interactive sessions where the server waits for user responses
via Telegram. It handles session state, timeouts, and response processing.
"""

import asyncio
import time
import uuid
import logging
from typing import Dict, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class SessionStatus(Enum):
    """Status of an interactive session."""
    PENDING = "pending"
    WAITING = "waiting"
    COMPLETED = "completed"
    TIMEOUT = "timeout"
    ERROR = "error"


@dataclass
class InteractiveSession:
    """Represents an interactive session waiting for user response."""
    
    session_id: str
    message: str
    chat_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    timeout_seconds: int = 300  # 5 minutes default
    status: SessionStatus = SessionStatus.PENDING
    response: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if the session has expired.
        A timeout_seconds <= 0 means infinite timeout (never expires).
        """
        if self.timeout_seconds <= 0:
            return False
        return time.time() - self.created_at > self.timeout_seconds

    @property
    def is_active(self) -> bool:
        """Check if the session is still active (pending or waiting)."""
        return self.status in [SessionStatus.PENDING, SessionStatus.WAITING]
    
    def mark_completed(self, response: str) -> None:
        """Mark the session as completed with a response."""
        self.response = response
        self.status = SessionStatus.COMPLETED
    
    def mark_timeout(self) -> None:
        """Mark the session as timed out."""
        self.status = SessionStatus.TIMEOUT
    
    def mark_error(self, error_message: str) -> None:
        """Mark the session as having an error."""
        self.error_message = error_message
        self.status = SessionStatus.ERROR


class InteractiveSessionManager:
    """Manages interactive sessions for user responses."""
    
    def __init__(self, cleanup_interval: int = 60):
        """
        Initialize the session manager.
        
        Args:
            cleanup_interval: How often to clean up expired sessions (seconds)
        """
        self.sessions: Dict[str, InteractiveSession] = {}
        self.cleanup_interval = cleanup_interval
        self._cleanup_task: Optional[asyncio.Task] = None
        self._response_callbacks: Dict[str, Callable[[str], Awaitable[None]]] = {}
        
    async def start(self) -> None:
        """Start the session manager and cleanup task."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
            logger.info("Interactive session manager started")
    
    async def stop(self) -> None:
        """Stop the session manager and cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
            logger.info("Interactive session manager stopped")
    
    def create_session(
        self,
        message: str,
        chat_id: Optional[str] = None,
        timeout_seconds: int = 300,
        metadata: Optional[Dict[str, Any]] = None
    ) -> InteractiveSession:
        """
        Create a new interactive session.
        
        Args:
            message: The message/question to send to the user
            chat_id: Telegram chat ID (if applicable)
            timeout_seconds: How long to wait for a response
            metadata: Additional metadata for the session
            
        Returns:
            InteractiveSession: The created session
        """
        session_id = str(uuid.uuid4())
        session = InteractiveSession(
            session_id=session_id,
            message=message,
            chat_id=chat_id,
            timeout_seconds=timeout_seconds,
            metadata=metadata or {}
        )
        
        self.sessions[session_id] = session
        logger.info(f"Created interactive session {session_id}")
        return session
    
    async def wait_for_response(
        self,
        session: InteractiveSession,
        poll_interval: float = 1.0
    ) -> Optional[str]:
        """
        Wait for a response to an interactive session.

        Args:
            session: The session to wait for
            poll_interval: How often to check for responses (seconds)

        Returns:
            Optional[str]: The user's response, or None if timeout/error
        """
        session.status = SessionStatus.WAITING
        logger.info(f"⏳ Starting wait for response to session {session.session_id}")

        poll_count = 0
        while True:
            poll_count += 1

            # Check if we have a response (check this first!)
            if session.status == SessionStatus.COMPLETED:
                logger.info(f"✅ Session {session.session_id} completed with response: '{session.response}' (after {poll_count} polls)")
                return session.response

            # Check for timeout
            if session.is_expired:
                # Do one final check for response before timing out (race condition fix)
                if session.status == SessionStatus.COMPLETED:
                    logger.info(f"✅ Session {session.session_id} completed just before timeout: '{session.response}' (after {poll_count} polls)")
                    return session.response

                session.mark_timeout()
                logger.warning(f"⏰ Session {session.session_id} timed out after {session.timeout_seconds} seconds ({poll_count} polls)")

                # Auto-submit default message if configured
                try:
                    from config import config as _cfg
                    msgs = getattr(_cfg, 'messages', {}).get('messages', {}) if _cfg else {}
                    pre = msgs.get('prewritten') or []
                    default_item = None
                    if isinstance(pre, list):
                        for it in pre:
                            if isinstance(it, dict) and it.get('default') is True:
                                default_item = it
                                break
                    if default_item is not None:
                        try:
                            text = _cfg.resolve_message_item(default_item)
                            if text:
                                old_status = session.status.value
                                session.mark_completed(text)
                                logger.info(f"✅ Auto-submitted default message on timeout for session {session.session_id} (was {old_status})")
                                return text
                        except Exception as e:
                            logger.error(f"Failed to resolve default prewritten message: {e}")
                except Exception as e:
                    logger.error(f"Default message lookup failed: {e}")

                break

            # Check if session is no longer active (but not completed)
            if not session.is_active and session.status != SessionStatus.COMPLETED:
                logger.warning(f"❌ Session {session.session_id} became inactive without completion (after {poll_count} polls)")
                break

            # Log periodic status updates (every 30 seconds)
            if poll_count % 30 == 0:
                logger.info(f"🔄 Still waiting for session {session.session_id} (poll #{poll_count}, status: {session.status.value})")

            # Wait before next check
            await asyncio.sleep(poll_interval)

        # Final check before returning None
        if session.status == SessionStatus.COMPLETED:
            logger.info(f"✅ Session {session.session_id} completed in final check: '{session.response}' (after {poll_count} polls)")
            return session.response

        logger.info(f"❌ Returning None for session {session.session_id} (after {poll_count} polls)")
        return None
    
    def submit_response(self, session_id: str, response: str) -> bool:
        """
        Submit a response for a session.

        Args:
            session_id: The session ID
            response: The user's response

        Returns:
            bool: True if response was accepted, False otherwise
        """
        logger.info(f"📥 Attempting to submit response for session {session_id}: '{response}'")

        session = self.sessions.get(session_id)
        if not session:
            logger.warning(f"❌ Attempted to submit response for unknown session {session_id}")
            return False

        if not session.is_active:
            logger.warning(f"❌ Attempted to submit response for inactive session {session_id} (status: {session.status.value})")
            return False

        if session.is_expired:
            session.mark_timeout()
            logger.warning(f"❌ Attempted to submit response for expired session {session_id}")
            return False

        # Mark as completed and log the change
        old_status = session.status.value
        session.mark_completed(response)
        logger.info(f"✅ Response submitted for session {session_id} (status changed from {old_status} to {session.status.value})")
        return True
    
    def get_session(self, session_id: str) -> Optional[InteractiveSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def get_active_sessions(self) -> Dict[str, InteractiveSession]:
        """Get all active sessions."""
        return {
            sid: session for sid, session in self.sessions.items()
            if session.is_active and not session.is_expired
        }
    
    def get_sessions_for_chat(self, chat_id: str) -> Dict[str, InteractiveSession]:
        """Get all sessions for a specific chat ID."""
        return {
            sid: session for sid, session in self.sessions.items()
            if session.chat_id == chat_id
        }
    
    async def _cleanup_loop(self) -> None:
        """Background task to clean up expired sessions."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                await self._cleanup_expired_sessions()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in session cleanup: {e}")
    
    async def _cleanup_expired_sessions(self) -> None:
        """Clean up expired sessions."""
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.is_expired and session.is_active:
                session.mark_timeout()
                expired_sessions.append(session_id)
        
        # Remove old completed/timeout/error sessions (older than 1 hour)
        cutoff_time = time.time() - 3600  # 1 hour
        old_sessions = [
            session_id for session_id, session in self.sessions.items()
            if session.created_at < cutoff_time and not session.is_active
        ]
        
        for session_id in old_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Marked {len(expired_sessions)} sessions as expired")
        
        if old_sessions:
            logger.info(f"Cleaned up {len(old_sessions)} old sessions")


# Global session manager instance
_session_manager: Optional[InteractiveSessionManager] = None


def get_session_manager() -> InteractiveSessionManager:
    """Get or create the global session manager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = InteractiveSessionManager()
    return _session_manager


async def create_interactive_session(
    message: str,
    chat_id: Optional[str] = None,
    timeout_seconds: int = 300,
    metadata: Optional[Dict[str, Any]] = None
) -> InteractiveSession:
    """
    Convenience function to create an interactive session.
    
    Args:
        message: The message/question to send to the user
        chat_id: Telegram chat ID (if applicable)
        timeout_seconds: How long to wait for a response
        metadata: Additional metadata for the session
        
    Returns:
        InteractiveSession: The created session
    """
    manager = get_session_manager()
    await manager.start()  # Ensure manager is started
    return manager.create_session(message, chat_id, timeout_seconds, metadata)


async def wait_for_user_response(
    session: InteractiveSession,
    poll_interval: float = 1.0
) -> Optional[str]:
    """
    Convenience function to wait for a user response.
    
    Args:
        session: The session to wait for
        poll_interval: How often to check for responses (seconds)
        
    Returns:
        Optional[str]: The user's response, or None if timeout/error
    """
    manager = get_session_manager()
    return await manager.wait_for_response(session, poll_interval)


def submit_user_response(session_id: str, response: str) -> bool:
    """
    Convenience function to submit a user response.
    
    Args:
        session_id: The session ID
        response: The user's response
        
    Returns:
        bool: True if response was accepted, False otherwise
    """
    manager = get_session_manager()
    return manager.submit_response(session_id, response)


if __name__ == "__main__":
    # Test the session manager
    async def test_session_manager():
        print("Testing interactive session manager...")
        
        manager = InteractiveSessionManager()
        await manager.start()
        
        # Create a test session
        session = manager.create_session(
            message="What is your favorite color?",
            timeout_seconds=10
        )
        
        print(f"Created session: {session.session_id}")
        print(f"Session status: {session.status}")
        
        # Simulate a response after 2 seconds
        async def simulate_response():
            await asyncio.sleep(2)
            manager.submit_response(session.session_id, "Blue")
        
        # Start the response simulation
        response_task = asyncio.create_task(simulate_response())
        
        # Wait for response
        response = await manager.wait_for_response(session)
        print(f"Received response: {response}")
        
        await response_task
        await manager.stop()
    
    asyncio.run(test_session_manager())
