"""
Configuration management for the MCP Your Turn server.
Handles environment variables and settings.
"""

import os
import sys
from typing import Optional

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass


class Config:
    """Configuration class for managing environment variables and settings."""
    
    def __init__(self):
        """Initialize configuration with environment variables."""
        self.telegram_bot_token: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id: Optional[str] = os.getenv('TELEGRAM_CHAT_ID')
        self.telegram_enabled: bool = self._parse_bool(os.getenv('TELEGRAM_ENABLED', 'true'))
        
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
