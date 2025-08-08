#!/usr/bin/env python3
"""
Enhanced Telegram Connection Test Tool
Tests the critical connection and message handling functionality.
"""

import asyncio
import os
import sys
import logging
import time
from typing import Optional

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TelegramConnectionTester:
    """Test Telegram connection and message handling."""
    
    def __init__(self):
        self.server = None
        self.telegram_notifier = None
        
    async def run_connection_test(self):
        """Run comprehensive connection test."""
        print("🔗 Enhanced Telegram Connection Test")
        print("=" * 50)
        
        # Check prerequisites
        if not self._check_prerequisites():
            return False
        
        # Initialize components
        if not await self._initialize_components():
            return False
        
        # Test connection establishment
        if not await self._test_connection_establishment():
            return False
        
        # Test interactive session creation
        if not await self._test_interactive_session():
            return False
        
        # Monitor for responses
        await self._monitor_for_responses()
        
        return True
    
    def _check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        print("\n🔍 Checking Prerequisites...")
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token:
            print("❌ TELEGRAM_BOT_TOKEN not set")
            return False
        
        if not chat_id:
            print("❌ TELEGRAM_CHAT_ID not set")
            return False
        
        print(f"✅ Bot token: {bot_token[:10]}...")
        print(f"✅ Chat ID: {chat_id}")
        
        # Check python-telegram-bot
        try:
            import telegram
            print("✅ python-telegram-bot available")
        except ImportError:
            print("❌ python-telegram-bot not installed")
            print("💡 Install with: pip install python-telegram-bot")
            return False
        
        return True
    
    async def _initialize_components(self) -> bool:
        """Initialize MCP server and Telegram components."""
        print("\n🚀 Initializing Components...")
        
        try:
            from mcp_your_turn_server import MCPServer
            self.server = MCPServer()
            print("✅ MCP Server initialized")
            
            if not self.server.telegram_notifier:
                print("❌ Telegram notifier not available")
                return False
            
            self.telegram_notifier = self.server.telegram_notifier
            
            if not self.telegram_notifier.is_enabled():
                print("❌ Telegram notifier not enabled")
                return False
            
            print("✅ Telegram notifier enabled")
            return True
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _test_connection_establishment(self) -> bool:
        """Test establishing the Telegram connection."""
        print("\n🔌 Testing Connection Establishment...")
        
        try:
            # Enable interactive mode
            print("📱 Enabling interactive mode...")
            success = await self.telegram_notifier.enable_interactive_mode()
            if not success:
                print("❌ Failed to enable interactive mode")
                return False
            print("✅ Interactive mode enabled")
            
            # Start interactive mode (this should start polling)
            print("🔄 Starting interactive polling...")
            await self.telegram_notifier.start_interactive_mode()
            
            # Give it time to start
            await asyncio.sleep(3)
            
            # Check if it's running
            if self.telegram_notifier._running:
                print("✅ Interactive polling started successfully")
                print("🤖 Bot is now listening for messages!")
                return True
            else:
                print("❌ Interactive polling failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Connection establishment failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _test_interactive_session(self) -> bool:
        """Test creating an interactive session."""
        print("\n❓ Testing Interactive Session Creation...")
        
        try:
            # Create an interactive session via MCP
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "🧪 CONNECTION TEST: Please respond with 'TEST OK' to verify the connection is working",
                        "interactive": True,
                        "timeout_seconds": 300
                    }
                }
            }
            
            print("📤 Sending interactive question...")
            
            # This should trigger the auto-start of interactive mode
            response = await self.server.handle_request(request)
            
            if 'result' in response:
                print("✅ Interactive question sent successfully")
                print("📱 Check your Telegram - you should see the test question with buttons!")
                return True
            else:
                print(f"❌ Interactive question failed: {response.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Interactive session test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def _monitor_for_responses(self):
        """Monitor for incoming responses."""
        print("\n👀 Monitoring for Responses...")
        print("💡 Instructions:")
        print("   1. Check your Telegram for the test question")
        print("   2. Either click a button OR type 'TEST OK'")
        print("   3. Watch the logs below for activity")
        print("   4. Press Ctrl+C to stop monitoring")
        print()
        
        try:
            # Monitor for 5 minutes or until interrupted
            start_time = time.time()
            last_status = time.time()
            
            while time.time() - start_time < 300:  # 5 minutes
                # Print status every 30 seconds
                if time.time() - last_status > 30:
                    elapsed = int(time.time() - start_time)
                    print(f"⏰ Monitoring... {elapsed}s elapsed (press Ctrl+C to stop)")
                    
                    # Check if bot is still running
                    if self.telegram_notifier._running:
                        print("✅ Bot is still running and listening")
                    else:
                        print("❌ Bot stopped running!")
                        break
                    
                    last_status = time.time()
                
                # Check for responses
                from interactive_session import get_session_manager
                session_manager = get_session_manager()
                active_sessions = session_manager.get_active_sessions()
                
                for session in active_sessions.values():
                    if session.response_received:
                        print(f"🎉 RESPONSE RECEIVED: '{session.response}'")
                        print(f"✅ Session {session.session_id} completed successfully!")
                        return
                
                await asyncio.sleep(1)
            
            print("⏰ Monitoring timeout reached (5 minutes)")
            
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Monitoring error: {e}")
        finally:
            # Clean up
            try:
                await self.telegram_notifier.stop_interactive_mode()
                print("🧹 Cleaned up interactive mode")
            except:
                pass


async def main():
    """Run the connection test."""
    tester = TelegramConnectionTester()
    
    print("🧪 Enhanced Telegram Connection Tester")
    print("This tool tests the critical connection and message handling.")
    print("Make sure you have TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID set!")
    print()
    
    try:
        success = await tester.run_connection_test()
        
        if success:
            print("\n🎉 Connection test completed!")
            print("If you saw response activity in the logs, the connection is working!")
        else:
            print("\n❌ Connection test failed!")
            print("Check the error messages above for troubleshooting.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
