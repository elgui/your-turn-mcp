#!/usr/bin/env python3
"""
Test script for Telegram bot configuration.
Use this to verify your Telegram setup before using the MCP server.
"""

import asyncio
import sys
import os

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ Loaded .env file")
except ImportError:
    print("⚠ python-dotenv not installed, using system environment variables only")

# Try to import telegram bot
try:
    from telegram import Bot
    from telegram.error import TelegramError
    print("✓ python-telegram-bot is installed")
except ImportError:
    print("✗ python-telegram-bot not installed")
    print("Install with: pip install python-telegram-bot")
    sys.exit(1)


async def test_telegram_config():
    """Test Telegram bot configuration."""
    
    # Get environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print("\n=== Telegram Configuration Test ===")
    
    # Check if variables are set
    if not bot_token:
        print("✗ TELEGRAM_BOT_TOKEN not set")
        print("Set it with: export TELEGRAM_BOT_TOKEN='your_token_here'")
        return False
    else:
        print(f"✓ TELEGRAM_BOT_TOKEN is set (ends with: ...{bot_token[-10:]})")
    
    if not chat_id:
        print("✗ TELEGRAM_CHAT_ID not set")
        print("Set it with: export TELEGRAM_CHAT_ID='your_chat_id_here'")
        return False
    else:
        print(f"✓ TELEGRAM_CHAT_ID is set: {chat_id}")
    
    # Test bot connection
    try:
        bot = Bot(token=bot_token)
        print("\n=== Testing Bot Connection ===")
        
        # Get bot info
        bot_info = await bot.get_me()
        print(f"✓ Bot connected successfully!")
        print(f"  Bot name: {bot_info.first_name}")
        print(f"  Bot username: @{bot_info.username}")
        
        # Test sending a message
        print("\n=== Testing Message Sending ===")
        test_message = "🧪 Test message from MCP Your Turn Server setup!\n\nIf you see this, your Telegram configuration is working correctly! 🎉"
        
        await bot.send_message(
            chat_id=chat_id,
            text=test_message,
            parse_mode='Markdown'
        )
        
        print("✓ Test message sent successfully!")
        print(f"Check your Telegram chat (ID: {chat_id}) for the test message.")
        
        return True
        
    except TelegramError as e:
        print(f"✗ Telegram API error: {e}")
        if "Unauthorized" in str(e):
            print("  → Check your bot token")
        elif "chat not found" in str(e).lower():
            print("  → Check your chat ID")
        elif "Bad Request" in str(e):
            print("  → Check your chat ID format")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def print_help():
    """Print help information."""
    print("\n=== Setup Help ===")
    print("1. Create a bot with @BotFather on Telegram")
    print("2. Get your chat ID by messaging your bot, then visiting:")
    print("   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
    print("3. Set environment variables:")
    print("   export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
    print("   export TELEGRAM_CHAT_ID='your_chat_id_here'")
    print("4. Or create a .env file with these variables")


async def main():
    """Main function."""
    print("MCP Your Turn Server - Telegram Configuration Test")
    print("=" * 50)
    
    success = await test_telegram_config()
    
    if success:
        print("\n🎉 All tests passed! Your Telegram configuration is ready.")
        print("You can now use the MCP server with Telegram notifications.")
    else:
        print("\n❌ Configuration test failed.")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
