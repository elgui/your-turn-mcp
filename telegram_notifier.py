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
        self._last_activity = None
        self._monitoring_task = None

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

            # Note: Connection testing will happen when first used
            # to avoid event loop issues during initialization

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

    async def _test_connection(self) -> bool:
        """Test Telegram connection."""
        if self._connection_tested or not self.enabled:
            return self._connection_tested

        try:
            logger.debug("🔍 Testing Telegram connection...")
            me = await self.bot.get_me()
            logger.info(f"✅ Connected to Telegram bot: @{me.username} ({me.first_name})")
            self._connection_tested = True
            return True
        except Exception as e:
            logger.warning(f"⚠️ Telegram connection test failed: {e}")
            logger.warning("💡 This might be a network issue or invalid token")
            return False

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

            # Add callback query handler for inline keyboard buttons
            from telegram.ext import CallbackQueryHandler
            callback_handler = CallbackQueryHandler(self._handle_callback_query)
            self.application.add_handler(callback_handler)

            self.interactive_mode = True
            self._log_info("Interactive mode enabled")
            return True

        except Exception as e:
            self._log_error(f"Failed to enable interactive mode: {e}")
            return False

    async def start_interactive_mode(self) -> None:
        """Start the interactive mode (polling for updates)."""
        if not self.interactive_mode or not self.application:
            logger.error("Cannot start interactive mode: not enabled or no application")
            return

        if self._running:
            logger.info("Interactive mode already running")
            return

        try:
            logger.info("🔄 Initializing Telegram application...")
            self._running = True

            # Initialize the application
            await self.application.initialize()
            logger.info("✅ Application initialized")

            # Start the application
            await self.application.start()
            logger.info("✅ Application started")

            # Start polling for updates
            logger.info("🔄 Starting polling for updates...")
            await self.application.updater.start_polling(
                poll_interval=1.0,      # Poll every second
                timeout=10,             # 10 second timeout for each poll
                bootstrap_retries=5,    # Retry 5 times on startup
                drop_pending_updates=True  # Drop any pending updates on startup
            )

            logger.info("✅ Interactive mode started successfully - now listening for messages!")
            self._log_info("🤖 Telegram bot is now actively listening for your responses")

            # Start connection monitoring
            self._start_connection_monitoring()

        except Exception as e:
            logger.error(f"❌ Failed to start interactive mode: {e}")
            import traceback
            logger.debug(f"Full traceback: {traceback.format_exc()}")
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
        finally:
            # Stop monitoring
            self._stop_connection_monitoring()

    def _start_connection_monitoring(self) -> None:
        """Start monitoring the connection."""
        if self._monitoring_task:
            return

        logger.info("🔍 Starting connection monitoring...")
        self._monitoring_task = asyncio.create_task(self._monitor_connection())

    def _stop_connection_monitoring(self) -> None:
        """Stop monitoring the connection."""
        if self._monitoring_task:
            logger.info("🛑 Stopping connection monitoring...")
            self._monitoring_task.cancel()
            self._monitoring_task = None

    async def _monitor_connection(self) -> None:
        """Monitor the connection and log activity."""
        import datetime

        while self._running:
            try:
                current_time = datetime.datetime.now()

                # Log periodic status
                if not self._last_activity:
                    self._last_activity = current_time

                time_since_activity = current_time - self._last_activity

                # Log status every 30 seconds
                if time_since_activity.total_seconds() > 30:
                    logger.info(f"🤖 Bot status: Running for {time_since_activity.total_seconds():.0f}s, waiting for messages...")
                    self._last_activity = current_time

                # Wait before next check
                await asyncio.sleep(30)

            except asyncio.CancelledError:
                logger.info("🛑 Connection monitoring stopped")
                break
            except Exception as e:
                logger.error(f"❌ Connection monitoring error: {e}")
                await asyncio.sleep(10)  # Wait before retrying

    async def _handle_message(self, update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
        """Handle incoming messages from users."""
        if not update.message or not update.message.text:
            logger.debug("Received update without message or text")
            return

        chat_id = str(update.effective_chat.id)
        message_text = update.message.text.strip()
        user_id = update.message.from_user.id
        username = update.message.from_user.username or "Unknown"

        logger.info(f"📨 Received message from user {username} ({user_id}) in chat {chat_id}: '{message_text}'")

        # Update activity timestamp
        import datetime
        self._last_activity = datetime.datetime.now()

        # Check if this is the configured chat
        if chat_id != str(self.chat_id):
            logger.warning(f"⚠️ Message from unauthorized chat {chat_id}, expected {self.chat_id}")
            return

        # Get session manager and find active sessions for this chat
        session_manager = get_session_manager()
        active_sessions = session_manager.get_sessions_for_chat(chat_id)

        logger.info(f"🔍 Found {len(active_sessions)} active sessions for chat {chat_id}")

        if not active_sessions:
            # No active sessions, send help message
            logger.info("ℹ️ No active sessions found, sending help message")
            await self._send_help_message(chat_id)
            return

        # Find the most recent active session
        latest_session = max(active_sessions.values(), key=lambda s: s.created_at)
        logger.info(f"🎯 Using latest session: {latest_session.session_id}")

        # Submit the response
        logger.info(f"📝 Submitting response to session {latest_session.session_id}: '{message_text}'")
        success = session_manager.submit_response(latest_session.session_id, message_text)

        if success:
            logger.info(f"✅ Response successfully submitted for session {latest_session.session_id}")
            await self._send_confirmation_message(chat_id, message_text)
        else:
            logger.error(f"❌ Failed to submit response for session {latest_session.session_id}")
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

    async def _handle_callback_query(self, update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
        """Handle callback queries from inline keyboard buttons."""
        query = update.callback_query
        if not query:
            logger.debug("Received update without callback query")
            return

        await query.answer()  # Acknowledge the callback query

        chat_id = str(query.message.chat_id)
        callback_data = query.data
        user_id = query.from_user.id
        username = query.from_user.username or "Unknown"

        logger.info(f"🔘 Received button click from user {username} ({user_id}) in chat {chat_id}: '{callback_data}'")

        # Update activity timestamp
        import datetime
        self._last_activity = datetime.datetime.now()

        # Check if this is the configured chat
        if chat_id != str(self.chat_id):
            logger.warning(f"⚠️ Callback query from unauthorized chat {chat_id}, expected {self.chat_id}")
            return

        # Parse callback data
        if callback_data.startswith("response:"):
            # Format: response:session_id:response_type
            parts = callback_data.split(":", 2)
            if len(parts) == 3:
                _, session_id, response_type = parts
                logger.info(f"🎯 Processing quick response: {response_type} for session {session_id}")
                await self._handle_quick_response(query, session_id, response_type)
            else:
                logger.error(f"❌ Invalid response callback data format: {callback_data}")
        elif callback_data.startswith("custom:"):
            # Format: custom:session_id
            parts = callback_data.split(":", 1)
            if len(parts) == 2:
                _, session_id = parts
                logger.info(f"💬 Processing custom response request for session {session_id}")
                await self._handle_custom_response_request(query, session_id)
            else:
                logger.error(f"❌ Invalid custom callback data format: {callback_data}")
        else:
            logger.warning(f"⚠️ Unknown callback data format: {callback_data}")

    async def _handle_quick_response(self, query, session_id: str, response_type: str) -> None:
        """Handle quick response button presses."""
        # Map response types to user-friendly messages
        response_map = {
            "complete": "✅ Task completed successfully",
            "progress": "🔄 Task is in progress",
            "help": "❌ Need help with this task",
            "pause": "⏸️ Task paused for now",
            "default": "📝 Send default message (no user input)"
        }

        response_text = response_map.get(response_type, f"Selected: {response_type}")
        logger.info(f"📝 Quick response mapped: {response_type} -> '{response_text}'")

        # Find the session and set response
        session_manager = get_session_manager()
        logger.info(f"🔍 Submitting quick response to session {session_id}: '{response_text}'")
        success = session_manager.submit_response(session_id, response_text)

        if success:
            logger.info(f"✅ Quick response successfully submitted for session {session_id}: {response_text}")

            # Edit the original message to show the response
            try:
                logger.info(f"🔄 Updating message to show response...")
                await query.edit_message_text(
                    text=f"❓ Question completed\n\n"
                         f"✅ Your response: {response_text}\n\n"
                         f"🆔 Session {session_id[:8]}... completed."
                    # No parse_mode - send as plain text to avoid formatting errors
                )
                logger.info(f"✅ Message updated successfully")
            except Exception as e:
                logger.error(f"❌ Failed to edit message: {e}")
        else:
            logger.error(f"❌ Failed to submit quick response for session {session_id}")
            # Session not found or already completed
            try:
                await query.edit_message_text(
                    text="⚠️ This session has expired or already been completed."
                    # No parse_mode - send as plain text to avoid formatting errors
                )
                logger.info("⚠️ Updated message to show session expired")
            except Exception as e:
                logger.error(f"❌ Failed to edit expired message: {e}")

    async def _handle_custom_response_request(self, query, session_id: str) -> None:
        """Handle custom response button press."""
        try:
            await query.edit_message_text(
                text=f"💬 Please type your custom response below.\n\n"
                     f"🆔 Session: {session_id[:8]}...\n\n"
                     f"Just send a regular message with your answer."
                # No parse_mode - send as plain text to avoid formatting errors
            )
        except Exception as e:
            logger.error(f"Failed to edit message for custom response: {e}")

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
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

            # Add instructions
            message += "\n\n💬 You can:"
            message += "\n• Type a custom response"
            message += "\n• Use the quick response buttons below"

            # Create inline keyboard with quick response options
            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ Task Complete",
                        callback_data=f"response:{session.session_id}:complete"
                    ),
                    InlineKeyboardButton(
                        "🔄 In Progress",
                        callback_data=f"response:{session.session_id}:progress"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Need Help",
                        callback_data=f"response:{session.session_id}:help"
                    ),
                    InlineKeyboardButton(
                        "⏸️ Pause",
                        callback_data=f"response:{session.session_id}:pause"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 Send Default Message",
                        callback_data=f"response:{session.session_id}:default"
                    ),
                    InlineKeyboardButton(
                        "💬 Custom Response",
                        callback_data=f"custom:{session.session_id}"
                    )
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            # Send the message with timeout (plain text to avoid parsing errors)
            await asyncio.wait_for(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    # No parse_mode - send as plain text to avoid formatting errors
                    reply_markup=reply_markup
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

        # Test connection if not already tested
        if not self._connection_tested:
            connection_ok = await self._test_connection()
            if not connection_ok:
                logger.error("❌ Telegram connection test failed, notification may not work")

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
            
            # Send the message with timeout (plain text to avoid parsing errors)
            await asyncio.wait_for(
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message
                    # No parse_mode - send as plain text to avoid formatting errors
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
