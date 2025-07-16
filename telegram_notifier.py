"""
Telegram bot notification handler for the MCP Your Turn server.
Sends notifications via Telegram when the your_turn tool is called.
Supports both simple notifications and interactive sessions.
"""

import asyncio
import sys
import logging
from typing import Optional, Dict, Any

try:
    from telegram import Bot, Update
    from telegram.ext import Application, MessageHandler, filters, ContextTypes
    from telegram.error import TelegramError, NetworkError, TimedOut
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    Bot = None
    Update = None
    Application = None
    MessageHandler = None
    filters = None
    ContextTypes = None
    TelegramError = Exception
    NetworkError = Exception
    TimedOut = Exception

from interactive_session import get_session_manager, InteractiveSession

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles sending notifications via Telegram bot with interactive support."""

    def __init__(self, bot_token: Optional[str], chat_id: Optional[str]):
        """
        Initialize the Telegram notifier.

        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Target chat ID for notifications
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = None  # Will be Bot instance if available
        self.application = None  # Will be Application instance for interactive mode
        self.enabled = False
        self.interactive_mode = False
        self._running = False
        self._connection_tested = False

        logger.info("🤖 Initializing Telegram notifier...")

        if not TELEGRAM_AVAILABLE:
            self._log_error("python-telegram-bot not installed. Install with: pip install python-telegram-bot")
            return

        # Validate inputs
        if not self._validate_credentials(bot_token, chat_id):
            return

        try:
            logger.debug(f"🔑 Creating Telegram bot with token: {bot_token[:10]}...")
            self.bot = Bot(token=bot_token)
            self.enabled = True
            logger.info("✅ Telegram notifier initialized successfully")

            # Test connection in background (don't block initialization)
            asyncio.create_task(self._test_connection())

        except Exception as e:
            self._log_error(f"Failed to initialize Telegram bot: {e}")

    def _validate_credentials(self, bot_token: Optional[str], chat_id: Optional[str]) -> bool:
        """Validate Telegram credentials."""
        if not bot_token:
            self._log_error("Missing TELEGRAM_BOT_TOKEN - get one from @BotFather")
            return False

        if not chat_id:
            self._log_error("Missing TELEGRAM_CHAT_ID - send a message to your bot and check logs")
            return False

        # Basic token format validation
        if not bot_token.count(':') == 1:
            self._log_error("Invalid bot token format - should be like '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'")
            return False

        # Basic chat ID validation
        try:
            int(chat_id)
        except ValueError:
            self._log_error("Invalid chat ID format - should be a number like '123456789'")
            return False

        logger.debug("✅ Telegram credentials validation passed")
        return True

    async def _test_connection(self) -> None:
        """Test Telegram connection in background."""
        if self._connection_tested or not self.enabled:
            return

        try:
            logger.debug("🔍 Testing Telegram connection...")
            me = await self.bot.get_me()
            logger.info(f"✅ Connected to Telegram bot: @{me.username} ({me.first_name})")
            self._connection_tested = True
        except Exception as e:
            logger.warning(f"⚠️ Telegram connection test failed: {e}")
            logger.warning("💡 This might be a network issue or invalid token")

    async def enable_interactive_mode(self) -> bool:
        """
        Enable interactive mode for receiving user responses.

        Returns:
            bool: True if interactive mode was enabled successfully
        """
        if not self.enabled or not TELEGRAM_AVAILABLE:
            return False

        try:
            # Create application for handling updates
            self.application = Application.builder().token(self.bot_token).build()

            # Add message handler for user responses
            message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message)
            self.application.add_handler(message_handler)

            self.interactive_mode = True
            self._log_info("Interactive mode enabled")
            return True

        except Exception as e:
            self._log_error(f"Failed to enable interactive mode: {e}")
            return False

    async def start_interactive_mode(self) -> None:
        """Start the interactive mode (polling for updates)."""
        if not self.interactive_mode or not self.application:
            return

        try:
            self._running = True
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            self._log_info("Interactive mode started")

        except Exception as e:
            self._log_error(f"Failed to start interactive mode: {e}")
            self._running = False

    async def stop_interactive_mode(self) -> None:
        """Stop the interactive mode."""
        if not self._running or not self.application:
            return

        try:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            self._running = False
            self._log_info("Interactive mode stopped")

        except Exception as e:
            self._log_error(f"Failed to stop interactive mode: {e}")

    async def _handle_message(self, update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
        """Handle incoming messages from users."""
        if not update.message or not update.message.text:
            return

        chat_id = str(update.effective_chat.id)
        message_text = update.message.text.strip()

        # Get session manager and find active sessions for this chat
        session_manager = get_session_manager()
        active_sessions = session_manager.get_sessions_for_chat(chat_id)

        if not active_sessions:
            # No active sessions, send help message
            await self._send_help_message(chat_id)
            return

        # Find the most recent active session
        latest_session = max(active_sessions.values(), key=lambda s: s.created_at)

        # Submit the response
        success = session_manager.submit_response(latest_session.session_id, message_text)

        if success:
            await self._send_confirmation_message(chat_id, message_text)
        else:
            await self._send_error_message(chat_id, "Failed to process your response")

    async def _send_help_message(self, chat_id: str) -> None:
        """Send a help message when no active sessions are found."""
        message = "ℹ️ No active questions found. I'll notify you when the LLM needs your input!"
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            self._log_error(f"Failed to send help message: {e}")

    async def _send_confirmation_message(self, chat_id: str, response: str) -> None:
        """Send a confirmation message after receiving a response."""
        message = f"✅ Got it! Your response: \"{response[:50]}{'...' if len(response) > 50 else ''}\""
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            self._log_error(f"Failed to send confirmation message: {e}")

    async def _send_error_message(self, chat_id: str, error: str) -> None:
        """Send an error message."""
        message = f"❌ {error}"
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            self._log_error(f"Failed to send error message: {e}")
    
    def _log_info(self, message: str) -> None:
        """Log info message to stderr."""
        print(f"[TELEGRAM] {message}", file=sys.stderr)
    
    def _log_error(self, message: str) -> None:
        """Log error message to stderr."""
        print(f"[TELEGRAM ERROR] {message}", file=sys.stderr)
    
    async def send_interactive_question(self, session: "InteractiveSession") -> bool:
        """
        Send an interactive question via Telegram.

        Args:
            session: The interactive session containing the question

        Returns:
            bool: True if question was sent successfully, False otherwise
        """
        if not self.enabled or not self.bot:
            return False

        try:
            # Format the interactive message
            message = f"❓ *Question for you:*\n\n{session.message}"

            # Add session info
            message += f"\n\n🆔 Session: `{session.session_id[:8]}...`"

            # Add timeout info
            timeout_minutes = session.timeout_seconds // 60
            if timeout_minutes > 0:
                message += f"\n⏱️ Timeout: {timeout_minutes} minutes"

            # Add timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            message += f"\n⏰ {timestamp}"

            message += "\n\n💬 *Please reply with your answer.*"

            # Send the message with timeout
            await asyncio.wait_for(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                ),
                timeout=10.0  # 10 second timeout
            )

            self._log_info(f"Interactive question sent for session {session.session_id}")
            return True

        except Exception as e:
            self._log_error(f"Failed to send interactive question: {e}")
            return False

    async def send_notification(self, reason: Optional[str] = None) -> bool:
        """
        Send a notification via Telegram.
        
        Args:
            reason: Optional reason for the notification
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        if not self.enabled or not self.bot:
            logger.debug("❌ Telegram not enabled or bot not initialized")
            return False

        logger.info("📤 Sending Telegram notification...")

        try:
            # Format the message
            message = "🔔 *Your Turn!*\n\nThe LLM is waiting for your response."
            if reason:
                message += f"\n\n📝 *Reason:* {reason}"

            # Add timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            message += f"\n\n⏰ {timestamp}"

            logger.debug(f"📝 Sending message to chat {self.chat_id}: {message[:50]}...")
            
            # Send the message with timeout
            await asyncio.wait_for(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode='Markdown'
                ),
                timeout=10.0  # 10 second timeout
            )
            
            logger.info("✅ Telegram notification sent successfully")
            return True

        except asyncio.TimeoutError:
            self._log_error("⏰ Telegram notification timed out (10 seconds)")
            return False
        except TimedOut:
            self._log_error("⏰ Telegram API timeout")
            return False
        except NetworkError as e:
            self._log_error(f"🌐 Telegram network error: {e}")
            self._log_error("💡 Check your internet connection")
            return False
        except TelegramError as e:
            if "Unauthorized" in str(e):
                self._log_error(f"🔐 Telegram authorization error: {e}")
                self._log_error("💡 Check your bot token - get a new one from @BotFather if needed")
            elif "Chat not found" in str(e):
                self._log_error(f"💬 Telegram chat error: {e}")
                self._log_error("💡 Make sure you've sent a message to your bot first")
            else:
                self._log_error(f"🤖 Telegram API error: {e}")
            return False
        except Exception as e:
            self._log_error(f"❌ Unexpected error sending Telegram notification: {e}")
            import traceback
            logger.debug(f"Full traceback: {traceback.format_exc()}")
            return False
    
    def is_enabled(self) -> bool:
        """Check if Telegram notifications are enabled."""
        return self.enabled


# Factory function to create a TelegramNotifier instance
def create_telegram_notifier(bot_token: Optional[str], chat_id: Optional[str]) -> TelegramNotifier:
    """
    Create a TelegramNotifier instance.
    
    Args:
        bot_token: Telegram bot token
        chat_id: Target chat ID
        
    Returns:
        TelegramNotifier instance
    """
    return TelegramNotifier(bot_token, chat_id)
