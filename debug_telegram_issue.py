#!/usr/bin/env python3
"""
Debug Telegram Issue Tool
Comprehensive debugging for Telegram connection and message handling issues.
"""

import asyncio
import os
import sys
import logging
import json
from typing import Optional

# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramDebugger:
    """Comprehensive Telegram debugging tool."""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    async def run_full_debug(self):
        """Run comprehensive debugging."""
        print("🔍 Telegram Connection Debug Tool")
        print("=" * 50)
        
        # Step 1: Environment check
        self._check_environment()
        
        # Step 2: Dependencies check
        self._check_dependencies()
        
        # Step 3: Basic Telegram API test
        if await self._test_basic_telegram_api():
            print("✅ Basic Telegram API working")
        else:
            print("❌ Basic Telegram API failed")
            return
        
        # Step 4: MCP Server integration test
        await self._test_mcp_integration()
        
        # Step 5: Interactive mode test
        await self._test_interactive_mode()
        
        # Step 6: Full end-to-end test
        await self._test_end_to_end()
    
    def _check_environment(self):
        """Check environment variables."""
        print("\n🔧 Environment Variables:")
        
        if self.bot_token:
            print(f"✅ TELEGRAM_BOT_TOKEN: {self.bot_token[:10]}...")
        else:
            print("❌ TELEGRAM_BOT_TOKEN: Not set")
            
        if self.chat_id:
            print(f"✅ TELEGRAM_CHAT_ID: {self.chat_id}")
        else:
            print("❌ TELEGRAM_CHAT_ID: Not set")
    
    def _check_dependencies(self):
        """Check required dependencies."""
        print("\n📦 Dependencies:")
        
        try:
            import telegram
            print(f"✅ python-telegram-bot: {telegram.__version__}")
        except ImportError:
            print("❌ python-telegram-bot: Not installed")
            print("💡 Install with: pip install python-telegram-bot")
            return False
        
        try:
            import asyncio
            print("✅ asyncio: Available")
        except ImportError:
            print("❌ asyncio: Not available")
            return False
        
        return True
    
    async def _test_basic_telegram_api(self) -> bool:
        """Test basic Telegram API connectivity."""
        print("\n🌐 Basic Telegram API Test:")
        
        if not self.bot_token or not self.chat_id:
            print("❌ Missing credentials")
            return False
        
        try:
            from telegram import Bot
            
            bot = Bot(token=self.bot_token)
            print("✅ Bot object created")
            
            # Test get_me
            me = await bot.get_me()
            print(f"✅ Bot info: @{me.username} ({me.first_name})")
            
            # Test send_message
            message = await bot.send_message(
                chat_id=self.chat_id,
                text="🧪 Debug test message - please ignore"
            )
            print(f"✅ Test message sent (ID: {message.message_id})")
            
            return True
            
        except Exception as e:
            print(f"❌ Basic API test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _test_mcp_integration(self):
        """Test MCP server integration."""
        print("\n🖥️  MCP Integration Test:")
        
        try:
            from mcp_your_turn_server import MCPServer
            server = MCPServer()
            print("✅ MCP Server created")
            
            if server.telegram_notifier:
                print("✅ Telegram notifier available")
                
                if server.telegram_notifier.is_enabled():
                    print("✅ Telegram notifier enabled")
                else:
                    print("❌ Telegram notifier not enabled")
                    return
            else:
                print("❌ Telegram notifier not available")
                return
            
            # Test notification
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_notify",
                    "arguments": {"reason": "MCP integration test"}
                }
            }
            
            response = await server.handle_request(request)
            
            if 'result' in response:
                print("✅ MCP notification tool works")
            else:
                print(f"❌ MCP notification failed: {response.get('error')}")
                
        except Exception as e:
            print(f"❌ MCP integration test failed: {e}")
            import traceback
            traceback.print_exc()
    
    async def _test_interactive_mode(self):
        """Test interactive mode functionality."""
        print("\n🔄 Interactive Mode Test:")
        
        try:
            from mcp_your_turn_server import MCPServer
            server = MCPServer()
            
            # Test interactive tool
            request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "🧪 Interactive debug test - please respond with 'DEBUG OK'",
                        "interactive": True,
                        "timeout_seconds": 60
                    }
                }
            }
            
            print("📤 Sending interactive question...")
            response = await server.handle_request(request)
            
            if 'result' in response:
                print("✅ Interactive question sent")
                content = response['result']['content'][0]['text']
                if 'User Response Received' in content:
                    print(f"✅ Response received: {content}")
                elif 'No response received' in content:
                    print("⏰ No response received (timeout)")
                else:
                    print(f"ℹ️ Response: {content}")
            else:
                print(f"❌ Interactive question failed: {response.get('error')}")
                
        except Exception as e:
            print(f"❌ Interactive mode test failed: {e}")
            import traceback
            traceback.print_exc()
    
    async def _test_end_to_end(self):
        """Test complete end-to-end functionality."""
        print("\n🎯 End-to-End Test:")
        
        try:
            from mcp_your_turn_server import MCPServer
            from telegram_notifier import TelegramNotifier
            
            # Create notifier directly
            notifier = TelegramNotifier(self.bot_token, self.chat_id)
            
            if not notifier.is_enabled():
                print("❌ Direct notifier not enabled")
                return
            
            # Test connection
            connection_ok = await notifier._test_connection()
            if connection_ok:
                print("✅ Direct connection test passed")
            else:
                print("❌ Direct connection test failed")
                return
            
            # Test notification
            success = await notifier.send_notification("End-to-end debug test")
            if success:
                print("✅ Direct notification sent")
            else:
                print("❌ Direct notification failed")
            
            # Test interactive mode setup
            if await notifier.enable_interactive_mode():
                print("✅ Interactive mode enabled")
                
                # Start interactive mode
                await notifier.start_interactive_mode()
                
                if notifier._running:
                    print("✅ Interactive polling started")
                    
                    # Send test question
                    from interactive_session import create_interactive_session
                    session = await create_interactive_session(
                        message="🧪 End-to-end test - please respond",
                        chat_id=self.chat_id,
                        timeout_seconds=30
                    )
                    
                    question_sent = await notifier.send_interactive_question(session)
                    if question_sent:
                        print("✅ Interactive question sent")
                        print("💡 Check your Telegram and respond to test full functionality")
                    else:
                        print("❌ Interactive question failed")
                    
                    # Clean up
                    await notifier.stop_interactive_mode()
                    print("🧹 Cleaned up interactive mode")
                else:
                    print("❌ Interactive polling failed to start")
            else:
                print("❌ Failed to enable interactive mode")
                
        except Exception as e:
            print(f"❌ End-to-end test failed: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Run the debug tool."""
    debugger = TelegramDebugger()
    
    print("🧪 Telegram Connection Debug Tool")
    print("This tool will comprehensively test all Telegram functionality.")
    print("Make sure you have TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID set!")
    print("Also ensure python-telegram-bot is installed: pip install python-telegram-bot")
    print()
    
    try:
        await debugger.run_full_debug()
        print("\n🎉 Debug session completed!")
        print("Check the output above for any issues.")
    except KeyboardInterrupt:
        print("\n⏹️ Debug interrupted by user")
    except Exception as e:
        print(f"\n❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
