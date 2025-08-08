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

class MCPServer:
    def __init__(self, telegram_bot_token: Optional[str] = None, telegram_chat_id: Optional[str] = None):
        # Define both tools: simple notification and interactive
        self.tools = {
            "your_turn_notify": {
                "name": "your_turn_notify",
                "description": "Send a simple notification to the user. Plays sound and optionally sends Telegram message.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Optional reason for the notification (e.g., 'mission completed', 'need user input')"
                        }
                    },
                    "additionalProperties": False
                }
            },
            "your_turn_interactive": {
                "name": "your_turn_interactive",
                "description": "Ask the user a question and wait for their response. Requires interactive=True parameter.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The question or message to send to the user"
                        },
                        "interactive": {
                            "type": "boolean",
                            "description": "Must be set to True to enable interactive mode"
                        },
                        "timeout_seconds": {
                            "type": "integer",
                            "description": "How long to wait for a response (default: 300 seconds)",
                            "default": 300
                        }
                    },
                    "required": ["message", "interactive"],
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
                    print("\a", flush=True)  # ASCII bell fallback
            else:
                # Fallback if sound manager not available
                print("\a", flush=True)  # ASCII bell character
        except Exception as e:
            logger.error(f"Sound notification failed: {e}")
            print(f"\a[NOTIFICATION: sound failed - {e}]", flush=True)

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

        # Prepare response message
        message = "🔔 Notification sent! The user has been alerted."
        if reason:
            message += f"\n\n📝 Reason: {reason}"

        # Add notification status to message
        if telegram_sent:
            message += "\n\n✅ Telegram notification sent successfully"
        elif self.telegram_notifier:
            message += "\n\n⚠️ Telegram notification failed (check logs)"
        else:
            message += "\n\n🔊 Sound notification only (Telegram not configured)"

        message += "\n\n It appears that you haven't entirely completed your mission, have you ?\n\n"
        message += "Once you have, please update : \n\n"
        message += "- the right 'AI-ENTRYPOINT.md' with tools and documentation data and references, and keep it clean!\n\n"
        message += "And create a well designed, comprehensive prompt for a relevant new session, referencing files and passing sharp instructions for high quality job\n\n"
        message += "The new session might be about valuable improvements, but because we aim at developing robust solutions, it might be a better idea to do an honest critic of what has been accompilshed in this session, and plan for a healthy checkup and quality improvements"
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
        timeout_seconds = arguments.get("timeout_seconds", 300)

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
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Interactive mode requires Telegram configuration"
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

            if tool_name in ["your_turn", "your_turn_notify"]:
                return await self._handle_notification_tool(request, arguments)

            elif tool_name == "your_turn_interactive":
                return await self._handle_interactive_tool(request, arguments)

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
                    request = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                # Handle request
                response = await self.handle_request(request)
                
                # Send response
                print(json.dumps(response), flush=True)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                # Send error response if we have a request ID
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)

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
