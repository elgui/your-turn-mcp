#!/usr/bin/env python3
"""
Enhanced MCP server with notification tools.
Provides both simple notifications and interactive user input capabilities.
Supports sound notifications and optional Telegram bot integration.
"""

import asyncio
import json
import sys
import os
import argparse
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass

# Debugging environment variables
print(f"DEBUG: TELEGRAM_BOT_TOKEN from os.getenv: {os.getenv('TELEGRAM_BOT_TOKEN')}", file=sys.stderr)
print(f"DEBUG: TELEGRAM_CHAT_ID from os.getenv: {os.getenv('TELEGRAM_CHAT_ID')}", file=sys.stderr)

# Import our custom modules
try:
    from config import config
    from telegram_notifier import TelegramNotifier
    from sound_manager import play_notification_sound
    from interactive_session import (
        create_interactive_session,
        wait_for_user_response
    )
except ImportError as e:
    print(f"[WARNING] Could not import custom modules: {e}", file=sys.stderr)
    print("[WARNING] Some features will be disabled", file=sys.stderr)
    config = None
    TelegramNotifier = None
    play_notification_sound = None
    create_interactive_session = None
    wait_for_user_response = None
    get_session_manager = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ResponseResult:
    """
    Result of user response collection process.

    This encapsulates the outcome of attempting to collect a user response,
    including metadata about what was attempted and any errors encountered.
    """
    user_response: Optional[str]
    telegram_attempted: bool
    error: Optional[str]

class MCPServer:
    def __init__(self, telegram_bot_token: Optional[str] = None, telegram_chat_id: Optional[str] = None):
        # Define single tool - simplified back to original behavior
        self.tools = {
            "your_turn": {
                "name": "your_turn",
                "description": "Send notification and wait for user response via Telegram. Plays sound and waits up to timeout_seconds (default 300).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Optional reason for the notification (e.g., 'mission completed', 'need user input')"
                        },
                        "timeout_seconds": {
                            "type": "number",
                            "description": "Optional override for wait timeout in seconds (min 10, max 7200). Default 300."
                        }
                    },
                    "additionalProperties": False
                }
            }
        }

        # Initialize Telegram notifier
        self.telegram_notifier = None

        # Priority: command-line args > environment variables > config file
        # Priority: environment variables > command-line args > config file
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        # Fall back to command-line args if not provided via environment variables
        if not bot_token:
            bot_token = telegram_bot_token
        if not chat_id:
            chat_id = telegram_chat_id

        # Fall back to config file if available
        if not bot_token or not chat_id:
            if config and hasattr(config, 'get_telegram_config'):
                config_token, config_chat_id = config.get_telegram_config()
                if not bot_token:
                    bot_token = config_token
                if not chat_id:
                    chat_id = config_chat_id

        # Create Telegram notifier if we have credentials
        if bot_token and chat_id and TelegramNotifier:
            self.telegram_notifier = TelegramNotifier(bot_token, chat_id)
            print(f"[TELEGRAM] Initialized with chat ID: {chat_id}", file=sys.stderr)
        elif bot_token or chat_id:
            print(f"[TELEGRAM] Incomplete configuration - missing {'chat_id' if not chat_id else 'bot_token'}", file=sys.stderr)
        else:
            print("[TELEGRAM] No configuration found - sound notifications only", file=sys.stderr)

    def play_notification_sound(self):
        """Play a notification sound using the sound manager."""
        try:
            if play_notification_sound:
                # Use the new sound manager
                success = play_notification_sound()
                if not success:
                    logger.warning("Sound manager failed, using fallback")
                    # IMPORTANT: write bell to stderr to avoid corrupting MCP JSON on stdout
                    print("\a", file=sys.stderr, flush=True)  # ASCII bell fallback to stderr
            else:
                # Fallback if sound manager not available
                print("\a", file=sys.stderr, flush=True)  # ASCII bell character to stderr
        except Exception as e:
            logger.error(f"Sound notification failed: {e}")
            # IMPORTANT: write any fallback bell/notice to stderr to avoid corrupting MCP JSON on stdout
            print(f"\a[NOTIFICATION: sound failed - {e}]", file=sys.stderr, flush=True)

    async def _ensure_interactive_mode(self) -> bool:
        """Ensure Telegram interactive mode is running."""
        if not self.telegram_notifier:
            logger.error("No Telegram notifier available")
            return False

        try:
            # Test connection first
            logger.info("🔍 Testing Telegram connection...")
            connection_ok = await self.telegram_notifier._test_connection()
            if not connection_ok:
                logger.error("❌ Telegram connection test failed")
                return False

            # Check if interactive mode is already running
            if self.telegram_notifier.interactive_mode and self.telegram_notifier._running:
                logger.info("✅ Interactive mode already running")
                return True

            logger.info("🚀 Starting Telegram interactive mode...")

            # Enable interactive mode
            if not self.telegram_notifier.interactive_mode:
                logger.info("📱 Enabling interactive mode...")
                success = await self.telegram_notifier.enable_interactive_mode()
                if not success:
                    logger.error("❌ Failed to enable interactive mode")
                    return False
                logger.info("✅ Interactive mode enabled")

            # Start interactive mode (polling)
            if not self.telegram_notifier._running:
                logger.info("🔄 Starting interactive polling...")
                await self.telegram_notifier.start_interactive_mode()

                # Give it a moment to start
                import asyncio
                await asyncio.sleep(2)

                if self.telegram_notifier._running:
                    logger.info("✅ Interactive polling started successfully")
                    return True
                else:
                    logger.error("❌ Interactive polling failed to start")
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ Failed to ensure interactive mode: {e}")
            import traceback
            logger.debug(f"Full traceback: {traceback.format_exc()}")
            return False

    async def _handle_your_turn_tool(self, request: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the your_turn tool - simplified approach based on old server architecture.

        This tool:
        1. Plays notification sound
        2. Attempts to get user response via Telegram (with timeout)
        3. ALWAYS returns the pre-written message with any user response included
        """
        reason = arguments.get("reason", "")
        # Allow MCP clients to override timeout (defaults to 300)
        try:
            timeout_seconds = int(float(arguments.get("timeout_seconds", 300)))
        except Exception:
            timeout_seconds = 300
        timeout_seconds = max(10, min(timeout_seconds, 7200))
        logger.info(f"🔔 Your Turn tool called with reason: {reason} (timeout_seconds={timeout_seconds})")

        # Play notification sound
        self.play_notification_sound()

        # Try to get user response via Telegram (simplified approach)
        user_response = None
        telegram_attempted = False

        if self.telegram_notifier and self.telegram_notifier.is_enabled():
            telegram_attempted = True
            try:
                logger.info("🤖 Attempting to get user response via Telegram...")

                # Ensure interactive mode is active
                interactive_started = await self._ensure_interactive_mode()
                if interactive_started:
                    # Create session
                    session = await create_interactive_session(
                        message=f"🔔 Notification: {reason}\n\nPlease respond if you have any input, or I'll continue automatically in {timeout_seconds//60 if timeout_seconds>=60 else timeout_seconds} {'minutes' if timeout_seconds>=60 else 'seconds' }.",
                        chat_id=self.telegram_notifier.chat_id,
                        timeout_seconds=timeout_seconds
                    )

                    # Send question
                    question_sent = await self.telegram_notifier.send_interactive_question(session)
                    if question_sent:
                        logger.info(f"⏳ Waiting for user response ({timeout_seconds} seconds max)...")

                        # Wait for response with guaranteed timeout
                        try:
                            user_response = await asyncio.wait_for(
                                wait_for_user_response(session),
                                timeout=timeout_seconds + 5  # small buffer
                            )
                        except asyncio.TimeoutError:
                            logger.info("⏰ Timeout reached - no user response")
                            user_response = None

                        # Final check for race conditions
                        if not user_response and hasattr(session, 'response') and session.response:
                            logger.warning(f"🔄 Using session response: '{session.response}'")
                            user_response = session.response

                        if user_response:
                            logger.info(f"✅ User response received: '{user_response}'")
                        else:
                            logger.info("⏰ No user response received")
                    else:
                        logger.error("❌ Failed to send Telegram question")
                else:
                    logger.error("❌ Failed to start interactive mode")

            except Exception as e:
                logger.error(f"❌ Error in Telegram interaction: {e}")

        # Build response message (prefer configurable templates if available)
        msgs = getattr(config, 'messages', {}).get('messages', {}) if config else {}
        default_prefix = msgs.get('default_prefix', "🔔 Notification sent! The user has been alerted.")
        default_reason_prefix = msgs.get('default_reason_prefix', "📝 Reason: ")
        response_prefix = msgs.get('response_prefix', "✅ User Response: ")
        no_response_suffix = msgs.get('no_response_suffix', f"⏰ No user response received (timeout)")
        sound_only_suffix = msgs.get('sound_only_suffix', "🔊 Sound notification only (Telegram not configured)")
        post_instructions = msgs.get('post_instructions', "")

        message = default_prefix

        if reason:
            message += f"\n\n{default_reason_prefix}{reason}"

        # Add user response if we got one
        if user_response:
            message += f"\n\n{response_prefix}\"{user_response}\""
        else:
            # Add status message only if no user response
            message += f"\n\n{no_response_suffix}" if telegram_attempted else f"\n\n{sound_only_suffix}"

        # Add the configurable post-instructions
        if post_instructions:
            message += f"{post_instructions}"

        logger.info(f"📤 Returning response (user_response: {user_response is not None})")

        response = {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        }

        # Log the exact response being returned
        logger.info(f"🚀 Response ready - ID: {request.get('id')}, content length: {len(message)}")

        return response



    async def _handle_notification_tool(self, request: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the notification tools (your_turn and your_turn_notify)."""
        reason = arguments.get("reason", "")

        # Play notification sound
        self.play_notification_sound()

        # Send Telegram notification if available
        telegram_sent = False
        if self.telegram_notifier and self.telegram_notifier.is_enabled():
            try:
                telegram_sent = await self.telegram_notifier.send_notification(reason)
            except Exception as e:
                logger.error(f"Failed to send Telegram notification: {e}")

        # Prepare response message (use config templates)
        msgs = getattr(config, 'messages', {}).get('messages', {}) if config else {}
        default_prefix = msgs.get('default_prefix', "🔔 Notification sent! The user has been alerted.")
        default_reason_prefix = msgs.get('default_reason_prefix', "📝 Reason: ")
        sound_only_suffix = msgs.get('sound_only_suffix', "🔊 Sound notification only (Telegram not configured)")

        message = default_prefix
        if reason:
            message += f"\n\n{default_reason_prefix}{reason}"

        # Add notification status to message
        if telegram_sent:
            message += "\n\n✅ Telegram notification sent successfully"
        elif self.telegram_notifier:
            message += "\n\n⚠️ Telegram notification failed (check logs)"
        else:
            message += f"\n\n{sound_only_suffix}"

        message += "\n\n💡 **Default Guidance:**\n\n"
        message += "From the accumulated context, identify the most critical area for improvement, and create a detailed set of instructions, containing details and file references (code and documentation).\n\n"
        message += "**Key areas to consider:**\n"
        message += "• Code quality and architecture improvements\n"
        message += "• Documentation completeness and accuracy\n"
        message += "• Testing coverage and reliability\n"
        message += "• Performance optimizations\n"
        message += "• Security considerations\n"
        message += "• User experience enhancements\n\n"
        message += "Please provide specific file references and actionable recommendations."
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        }

    async def _handle_interactive_tool(self, request: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle the interactive tool (your_turn_interactive)."""
        message = arguments.get("message", "")
        interactive = arguments.get("interactive", False)
        timeout_seconds = arguments.get("timeout_seconds", 20000)

        if not message:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32602,
                    "message": "Missing required parameter: message"
                }
            }

        if not interactive:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32602,
                    "message": "Interactive mode must be enabled (set interactive=True)"
                }
            }

        # Check if interactive functionality is available
        if not create_interactive_session or not wait_for_user_response:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Interactive functionality not available (missing dependencies)"
                }
            }

        # Check if Telegram is configured for interactive mode
        if not self.telegram_notifier or not self.telegram_notifier.is_enabled():
            logger.error("Interactive mode requires Telegram configuration")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Interactive mode requires Telegram configuration"
                }
            }

        # Ensure interactive mode is started
        logger.info("🤖 Ensuring Telegram interactive mode is active...")
        interactive_started = await self._ensure_interactive_mode()
        if not interactive_started:
            logger.error("Failed to start Telegram interactive mode")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Failed to start Telegram interactive mode"
                }
            }

        try:
            # Create interactive session
            session = await create_interactive_session(
                message=message,
                chat_id=self.telegram_notifier.chat_id,
                timeout_seconds=timeout_seconds
            )

            # Play notification sound
            self.play_notification_sound()

            # Send interactive question via Telegram
            question_sent = await self.telegram_notifier.send_interactive_question(session)

            if not question_sent:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": "Failed to send interactive question via Telegram"
                    }
                }

            # Wait for user response
            logger.info(f"Waiting for user response to session {session.session_id}")
            user_response = await wait_for_user_response(session)

            if user_response:
                response_message = f"✅ **User Response Received:**\n\n\"{user_response}\"\n\n🆔 Session: {session.session_id[:8]}..."
            else:
                response_message = f"⏰ **No response received** (timeout after {timeout_seconds} seconds)\n\n🆔 Session: {session.session_id[:8]}..."

            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": response_message
                        }
                    ]
                }
            }

        except Exception as e:
            logger.error(f"Interactive tool error: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Interactive tool failed: {str(e)}"
                }
            }

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests."""
        method = request.get("method")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "your-turn-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "tools": list(self.tools.values())
                }
            }
        
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "your_turn":
                return await self._handle_your_turn_tool(request, arguments)

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }

    async def run(self):
        """Main server loop - reads from stdin and writes to stdout."""
        while True:
            try:
                # Read line from stdin
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON request
                try:
                    # Log raw line for debugging (stderr via logger)
                    logger.info(f"🧾 Raw stdin line: {line!r}")
                    request = json.loads(line)
                    logger.info(f"📥 Received request: {request.get('method')} (ID: {request.get('id')})")
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ Received invalid JSON, ignoring. Error: {e}. Raw: {line!r}")
                    continue
                
                # Handle request
                response = await self.handle_request(request)

                # Log before sending response
                logger.info(f"🔄 Sending response for request ID {request.get('id')}: {response.get('result', {}).get('content', [{}])[0].get('text', '')[:100]}...")

                # Send response
                response_json = json.dumps(response)
                print(response_json, flush=True)

                # Force flush all output streams immediately
                sys.stdout.flush()
                sys.stderr.flush()

                # Log after sending
                logger.info(f"✅ Response sent successfully (length: {len(response_json)} chars)")
                logger.info(f"🔍 Response ID: {response.get('id')}, Method: {request.get('method')}")

                # Additional delay to ensure response is fully transmitted
                await asyncio.sleep(0.2)

                # Log that we're ready for the next request
                logger.info(f"🔄 Ready for next request...")

                # Ensure we stay alive and don't exit prematurely
                await asyncio.sleep(0.5)

            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal - shutting down gracefully")
                break
            except Exception as e:
                # Send error response if we have a request ID
                request_id = request.get('id') if 'request' in locals() else None
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
                logger.error(f"❌ Error handling request: {e}")
                import traceback
                logger.debug(f"Full traceback: {traceback.format_exc()}")

                # Continue running after error
                logger.info("🔄 Continuing to listen for requests...")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Enhanced MCP Your Turn Server - Notification and interactive response server for LLM interactions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (sound only)
  python3 mcp_your_turn_server.py

  # With Telegram notifications and interactive mode
  python3 mcp_your_turn_server.py --telegram-token "123:ABC" --telegram-chat-id "456789"

  # Docker usage
  docker run your-turn-server --telegram-token "123:ABC" --telegram-chat-id "456789"

Tools available:
  - your_turn_notify: Simple notification (sound + optional Telegram)
  - your_turn_interactive: Ask user a question and wait for response via Telegram
  - your_turn: Legacy tool (same as your_turn_notify)
        """
    )

    parser.add_argument(
        '--telegram-token', '--telegram-bot-token',
        type=str,
        help='Telegram bot token (from @BotFather)'
    )

    parser.add_argument(
        '--telegram-chat-id',
        type=str,
        help='Telegram chat ID for notifications'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Enhanced MCP Your Turn Server 2.0.0'
    )

    return parser.parse_args()

def main():
    """Entry point."""
    args = parse_args()

    server = MCPServer(
        telegram_bot_token=args.telegram_token,
        telegram_chat_id=args.telegram_chat_id
    )

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
