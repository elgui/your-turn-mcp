"""
Configuration management for the MCP Your Turn server.
Handles environment variables and settings.
"""

import os
import sys
from typing import Optional, Dict, Any

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass
# Optional YAML support for message configuration
try:
    import yaml  # type: ignore
except Exception:
    yaml = None



class Config:
    """Configuration class for managing environment variables and settings."""

    def __init__(self):
        """Initialize configuration with environment variables."""
        self.telegram_bot_token: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id: Optional[str] = os.getenv('TELEGRAM_CHAT_ID')
        self.telegram_enabled: bool = self._parse_bool(os.getenv('TELEGRAM_ENABLED', 'true'))

        # Messages config (YAML file)
        self.messages: Dict[str, Any] = self._load_messages_yaml(os.getenv('MESSAGES_FILE', 'messages.yml'))

        # Validate Telegram configuration
        self.telegram_configured = self._validate_telegram_config()

    def _parse_bool(self, value: str) -> bool:
        """Parse a string value to boolean."""
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')

    def _validate_telegram_config(self) -> bool:
        """Validate if Telegram is properly configured."""
        if not self.telegram_enabled:
            return False

        if not self.telegram_bot_token:
            self._log_config_issue("TELEGRAM_BOT_TOKEN not set")
            return False

        if not self.telegram_chat_id:
            self._log_config_issue("TELEGRAM_CHAT_ID not set")
            return False

        return True

    def _log_config_issue(self, message: str) -> None:
        """Log configuration issues to stderr."""
        print(f"[CONFIG] Telegram disabled: {message}", file=sys.stderr)

    def _load_messages_yaml(self, path: str) -> Dict[str, Any]:
        """Load messages configuration from YAML if available; return dict with defaults otherwise."""
        defaults: Dict[str, Any] = {
            "messages": {
                "default_reason_prefix": "📝 Reason: ",
                "default_prefix": "🔔 Notification sent! The user has been alerted.",
                "no_response_suffix": "⏰ No user response received (5 minute timeout)",
                "sound_only_suffix": "🔊 Sound notification only (Telegram not configured)",
                "response_prefix": "✅ User Response: ",
                "post_instructions": (
                    "\n It appears that you haven't entirely completed your mission, have you ?\n\n"
                    "Once you have, please update : \n\n"
                    "- the right 'AI-CONTEXT.md' with tools and documentation data and references, and keep it clean!\n\n"
                    "And create a well designed, comprehensive prompt for a relevant new session, referencing files and passing sharp instructions for high quality job\n\n"
                    "The new session might be about valuable improvements, but because we aim at developing robust solutions, it might be a better idea to do an honest critic of what has been accompilshed in this session, and plan for a healthy checkup and quality improvements"
                ),
            }
        }
        if yaml is None:
            return defaults
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                # shallow-merge
                out = defaults.copy()
                if isinstance(data, dict):
                    out.update(data)
                return out
            return defaults
        except Exception as e:
            print(f"[CONFIG] Warning: failed to load messages YAML: {e}", file=sys.stderr)
            return defaults

    def get_telegram_config(self) -> tuple[Optional[str], Optional[str]]:
        """Get Telegram bot token and chat ID if configured."""
        if self.telegram_configured:
            return self.telegram_bot_token, self.telegram_chat_id
        return None, None

    def is_telegram_enabled(self) -> bool:
        """Check if Telegram notifications are enabled and configured."""
        return self.telegram_configured


# Global configuration instance
config = Config()
