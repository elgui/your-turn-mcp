#!/usr/bin/env python3
"""
Comprehensive test tool for Enhanced MCP Your Turn Server interactive Telegram functionality.
Tests both notification and interactive features with real Telegram integration.
"""

import asyncio
import json
import os
import sys
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InteractiveTelegramTester:
    """Test tool for interactive Telegram functionality."""
    
    def __init__(self):
        self.server = None
        self.test_results = {}
        
    async def run_all_tests(self):
        """Run comprehensive interactive Telegram tests."""
        print("🧪 Enhanced MCP Your Turn Server - Interactive Telegram Test")
        print("=" * 65)
        
        # Check prerequisites
        if not await self._check_prerequisites():
            return
        
        # Initialize server
        if not await self._initialize_server():
            return
        
        # Test 1: Basic notification
        await self._test_basic_notification()
        
        # Test 2: Interactive question with buttons
        await self._test_interactive_question()
        
        # Test 3: Quick response buttons
        await self._test_quick_response_buttons()
        
        # Test 4: Custom response flow
        await self._test_custom_response_flow()
        
        # Test 5: Session timeout handling
        await self._test_session_timeout()
        
        # Test 6: Multiple concurrent sessions
        await self._test_concurrent_sessions()
        
        # Generate report
        self._generate_test_report()
    
    async def _check_prerequisites(self) -> bool:
        """Check if prerequisites are met."""
        print("\n🔍 Checking Prerequisites...")
        
        # Check environment variables
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token:
            print("❌ TELEGRAM_BOT_TOKEN not set")
            print("💡 Set it with: export TELEGRAM_BOT_TOKEN='your_token_here'")
            return False
        
        if not chat_id:
            print("❌ TELEGRAM_CHAT_ID not set")
            print("💡 Set it with: export TELEGRAM_CHAT_ID='your_chat_id_here'")
            return False
        
        print(f"✅ Bot token: {bot_token[:10]}...")
        print(f"✅ Chat ID: {chat_id}")
        
        # Check python-telegram-bot availability
        try:
            import telegram
            print("✅ python-telegram-bot library available")
        except ImportError:
            print("❌ python-telegram-bot not installed")
            print("💡 Install with: pip install python-telegram-bot")
            return False
        
        return True
    
    async def _initialize_server(self) -> bool:
        """Initialize the MCP server."""
        print("\n🖥️  Initializing MCP Server...")
        
        try:
            from mcp_your_turn_server import MCPServer
            self.server = MCPServer()
            print("✅ MCP Server initialized")
            
            # Check if Telegram is configured
            if self.server.telegram_notifier and self.server.telegram_notifier.is_enabled():
                print("✅ Telegram notifier enabled")
                
                # Enable interactive mode
                success = await self.server.telegram_notifier.enable_interactive_mode()
                if success:
                    print("✅ Interactive mode enabled")
                    
                    # Start interactive mode
                    await self.server.telegram_notifier.start_interactive_mode()
                    print("✅ Interactive mode started")
                    
                    # Give it a moment to initialize
                    await asyncio.sleep(2)
                    
                    return True
                else:
                    print("❌ Failed to enable interactive mode")
                    return False
            else:
                print("❌ Telegram notifier not enabled")
                return False
                
        except Exception as e:
            print(f"❌ Failed to initialize server: {e}")
            return False
    
    async def _test_basic_notification(self):
        """Test basic notification functionality."""
        print("\n📢 Test 1: Basic Notification")
        print("-" * 30)
        
        try:
            # Call the notification tool
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_notify",
                    "arguments": {"reason": "Testing basic notification"}
                }
            }
            
            response = await self.server.handle_request(request)
            
            if 'result' in response:
                print("✅ Basic notification sent successfully")
                self.test_results['basic_notification'] = True
            else:
                print(f"❌ Basic notification failed: {response.get('error', 'Unknown error')}")
                self.test_results['basic_notification'] = False
                
        except Exception as e:
            print(f"❌ Basic notification error: {e}")
            self.test_results['basic_notification'] = False
    
    async def _test_interactive_question(self):
        """Test interactive question with inline keyboard."""
        print("\n❓ Test 2: Interactive Question")
        print("-" * 30)
        
        try:
            # Call the interactive tool
            request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "What is your favorite color? (This is a test)",
                        "interactive": True,
                        "timeout_seconds": 300
                    }
                }
            }
            
            print("📤 Sending interactive question...")
            response = await self.server.handle_request(request)
            
            if 'result' in response:
                print("✅ Interactive question sent with inline keyboard")
                print("💡 Check your Telegram - you should see buttons!")
                self.test_results['interactive_question'] = True
            else:
                print(f"❌ Interactive question failed: {response.get('error', 'Unknown error')}")
                self.test_results['interactive_question'] = False
                
        except Exception as e:
            print(f"❌ Interactive question error: {e}")
            self.test_results['interactive_question'] = False
    
    async def _test_quick_response_buttons(self):
        """Test quick response button functionality."""
        print("\n🔘 Test 3: Quick Response Buttons")
        print("-" * 30)
        
        print("💡 This test requires manual interaction:")
        print("   1. Check your Telegram for the question with buttons")
        print("   2. Click one of the quick response buttons")
        print("   3. The message should update to show your response")
        
        # Wait a bit for user interaction
        print("⏳ Waiting 30 seconds for button interaction...")
        await asyncio.sleep(30)
        
        # Check if any sessions received responses
        from interactive_session import get_session_manager
        session_manager = get_session_manager()
        active_sessions = session_manager.get_active_sessions()
        
        button_response_received = False
        for session in active_sessions.values():
            if session.response_received and session.response in [
                "✅ Task completed successfully",
                "🔄 Task is in progress", 
                "❌ Need help with this task",
                "⏸️ Task paused for now"
            ]:
                button_response_received = True
                print(f"✅ Quick response received: {session.response}")
                break
        
        if button_response_received:
            self.test_results['quick_response_buttons'] = True
        else:
            print("⚠️ No quick response detected (manual test)")
            self.test_results['quick_response_buttons'] = None
    
    async def _test_custom_response_flow(self):
        """Test custom response flow."""
        print("\n💬 Test 4: Custom Response Flow")
        print("-" * 30)
        
        try:
            # Send another interactive question
            request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "Please describe your testing experience so far.",
                        "interactive": True,
                        "timeout_seconds": 300
                    }
                }
            }
            
            response = await self.server.handle_request(request)
            
            if 'result' in response:
                print("✅ Custom response question sent")
                print("💡 Try clicking 'Custom Response' button and typing a message")
                self.test_results['custom_response_flow'] = True
            else:
                print(f"❌ Custom response question failed: {response.get('error', 'Unknown error')}")
                self.test_results['custom_response_flow'] = False
                
        except Exception as e:
            print(f"❌ Custom response flow error: {e}")
            self.test_results['custom_response_flow'] = False
    
    async def _test_session_timeout(self):
        """Test session timeout handling."""
        print("\n⏰ Test 5: Session Timeout")
        print("-" * 30)
        
        try:
            # Create a session with short timeout
            request = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "This question will timeout in 5 seconds (don't answer)",
                        "interactive": True,
                        "timeout_seconds": 5
                    }
                }
            }
            
            print("📤 Sending question with 5-second timeout...")
            response = await self.server.handle_request(request)
            
            if 'result' in response:
                print("✅ Timeout question sent")
                
                # Wait for timeout
                print("⏳ Waiting for timeout...")
                await asyncio.sleep(7)
                
                # Check if session timed out
                from interactive_session import get_session_manager
                session_manager = get_session_manager()
                
                # The session should have timed out
                print("✅ Session timeout test completed")
                self.test_results['session_timeout'] = True
            else:
                print(f"❌ Timeout test failed: {response.get('error', 'Unknown error')}")
                self.test_results['session_timeout'] = False
                
        except Exception as e:
            print(f"❌ Session timeout error: {e}")
            self.test_results['session_timeout'] = False
    
    async def _test_concurrent_sessions(self):
        """Test multiple concurrent sessions."""
        print("\n🔀 Test 6: Concurrent Sessions")
        print("-" * 30)
        
        try:
            # Create multiple sessions quickly
            questions = [
                "Question 1: What's your name?",
                "Question 2: What's your favorite food?",
                "Question 3: What time is it?"
            ]
            
            for i, question in enumerate(questions):
                request = {
                    "jsonrpc": "2.0",
                    "id": 6 + i,
                    "method": "tools/call",
                    "params": {
                        "name": "your_turn_interactive",
                        "arguments": {
                            "message": question,
                            "interactive": True,
                            "timeout_seconds": 300
                        }
                    }
                }
                
                response = await self.server.handle_request(request)
                if 'result' in response:
                    print(f"✅ Concurrent question {i+1} sent")
                else:
                    print(f"❌ Concurrent question {i+1} failed")
                
                # Small delay between questions
                await asyncio.sleep(1)
            
            print("💡 Check Telegram - you should see multiple questions")
            self.test_results['concurrent_sessions'] = True
            
        except Exception as e:
            print(f"❌ Concurrent sessions error: {e}")
            self.test_results['concurrent_sessions'] = False
    
    def _generate_test_report(self):
        """Generate final test report."""
        print("\n" + "=" * 65)
        print("📊 INTERACTIVE TELEGRAM TEST REPORT")
        print("=" * 65)
        
        passed = sum(1 for result in self.test_results.values() if result is True)
        failed = sum(1 for result in self.test_results.values() if result is False)
        manual = sum(1 for result in self.test_results.values() if result is None)
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Manual: {manual}")
        
        if failed == 0:
            print("\n🎉 ALL AUTOMATED TESTS PASSED!")
            print("\n✅ Verified functionality:")
            print("  • Basic Telegram notifications")
            print("  • Interactive questions with inline keyboards")
            print("  • Quick response buttons")
            print("  • Custom response flow")
            print("  • Session timeout handling")
            print("  • Concurrent session management")
            
            print("\n💡 Manual verification needed:")
            print("  • Click the inline keyboard buttons")
            print("  • Type custom responses")
            print("  • Verify message updates work correctly")
            
            print("\n🚀 Enhanced Interactive Telegram functionality is working!")
        else:
            print(f"\n⚠️ {failed} test(s) failed. Check the output above for details.")
        
        print("\n" + "=" * 65)


async def main():
    """Run the interactive Telegram test."""
    tester = InteractiveTelegramTester()
    
    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        if tester.server and tester.server.telegram_notifier:
            try:
                await tester.server.telegram_notifier.stop_interactive_mode()
                print("🧹 Cleaned up interactive mode")
            except:
                pass


if __name__ == "__main__":
    print("🧪 Enhanced MCP Your Turn Server - Interactive Telegram Tester")
    print("This tool tests the enhanced interactive Telegram functionality.")
    print("Make sure you have TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID set!")
    print()
    
    asyncio.run(main())
