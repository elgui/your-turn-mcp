#!/usr/bin/env python3
"""
Final integration test for Enhanced MCP Your Turn Server.
Tests all documented functionality to ensure everything works as promised.
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FinalIntegrationTest:
    """Comprehensive integration test suite."""
    
    def __init__(self):
        self.results = {}
        self.passed = 0
        self.failed = 0
    
    def test_result(self, test_name: str, success: bool, message: str = ""):
        """Record test result."""
        self.results[test_name] = {'success': success, 'message': message}
        if success:
            self.passed += 1
            print(f"✅ {test_name}: {message}")
        else:
            self.failed += 1
            print(f"❌ {test_name}: {message}")
    
    async def run_all_tests(self):
        """Run all integration tests."""
        print("🧪 Enhanced MCP Your Turn Server - Final Integration Test")
        print("=" * 60)
        
        # Test 1: Module imports
        await self.test_module_imports()
        
        # Test 2: Sound system
        await self.test_sound_system()
        
        # Test 3: Environment variables
        await self.test_environment_variables()
        
        # Test 4: MCP protocol
        await self.test_mcp_protocol()
        
        # Test 5: All three tools
        await self.test_all_tools()
        
        # Test 6: Docker functionality
        await self.test_docker_functionality()
        
        # Test 7: Documentation examples
        await self.test_documentation_examples()
        
        # Generate final report
        self.generate_final_report()
    
    async def test_module_imports(self):
        """Test that all modules can be imported."""
        modules = [
            'mcp_your_turn_server',
            'sound_manager',
            'telegram_notifier',
            'interactive_session',
            'config'
        ]
        
        for module in modules:
            try:
                __import__(module)
                self.test_result(f"Import {module}", True, "Module imported successfully")
            except ImportError as e:
                self.test_result(f"Import {module}", False, f"Import failed: {e}")
    
    async def test_sound_system(self):
        """Test the sound notification system."""
        try:
            from sound_manager import SoundManager, play_notification_sound
            
            # Test SoundManager class
            manager = SoundManager()
            self.test_result("SoundManager creation", True, "SoundManager created successfully")
            
            # Test sound notification
            success = manager.play_notification_sound()
            self.test_result("Sound notification", success, 
                           "Sound played successfully" if success else "Sound fallback used")
            
            # Test convenience function
            success = play_notification_sound()
            self.test_result("Convenience function", success,
                           "play_notification_sound() works")
            
            # Test cleanup
            manager.cleanup()
            self.test_result("Sound cleanup", True, "Cleanup completed")
            
        except Exception as e:
            self.test_result("Sound system", False, f"Error: {e}")
    
    async def test_environment_variables(self):
        """Test environment variable handling."""
        # Set test environment variables
        os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token_123:ABC'
        os.environ['TELEGRAM_CHAT_ID'] = '123456789'
        
        try:
            from config import config
            
            # Test config loading
            self.test_result("Config loading", True, "Config module loaded")
            
            # Test environment variable reading
            token_set = config.telegram_bot_token == 'test_token_123:ABC'
            self.test_result("Bot token reading", token_set, 
                           f"Token: {config.telegram_bot_token}")
            
            chat_id_set = config.telegram_chat_id == '123456789'
            self.test_result("Chat ID reading", chat_id_set,
                           f"Chat ID: {config.telegram_chat_id}")
            
            configured = config.telegram_configured
            self.test_result("Telegram configured", configured,
                           f"Configured: {configured}")
            
        except Exception as e:
            self.test_result("Environment variables", False, f"Error: {e}")
        finally:
            # Clean up environment variables
            os.environ.pop('TELEGRAM_BOT_TOKEN', None)
            os.environ.pop('TELEGRAM_CHAT_ID', None)
    
    async def test_mcp_protocol(self):
        """Test MCP protocol implementation."""
        try:
            from mcp_your_turn_server import MCPServer
            
            server = MCPServer()
            self.test_result("MCP Server creation", True, "Server created successfully")
            
            # Test initialize
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {}
            }
            
            response = await server.handle_request(init_request)
            protocol_version = response.get('result', {}).get('protocolVersion')
            self.test_result("MCP initialize", protocol_version == "2024-11-05",
                           f"Protocol version: {protocol_version}")
            
            # Test tools/list
            tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            response = await server.handle_request(tools_request)
            tools = [tool['name'] for tool in response.get('result', {}).get('tools', [])]
            expected_tools = ['your_turn_notify', 'your_turn_interactive', 'your_turn']
            
            all_tools_present = all(tool in tools for tool in expected_tools)
            self.test_result("Tools list", all_tools_present,
                           f"Tools: {tools}")
            
        except Exception as e:
            self.test_result("MCP protocol", False, f"Error: {e}")
    
    async def test_all_tools(self):
        """Test all three tools."""
        try:
            from mcp_your_turn_server import MCPServer
            
            server = MCPServer()
            
            # Test your_turn_notify
            notify_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_notify",
                    "arguments": {"reason": "Integration test"}
                }
            }
            
            response = await server.handle_request(notify_request)
            success = 'result' in response and 'error' not in response
            self.test_result("your_turn_notify tool", success,
                           "Notification tool works")
            
            # Test your_turn (legacy)
            legacy_request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "your_turn",
                    "arguments": {"reason": "Legacy test"}
                }
            }
            
            response = await server.handle_request(legacy_request)
            success = 'result' in response and 'error' not in response
            self.test_result("your_turn legacy tool", success,
                           "Legacy tool works")
            
            # Test your_turn_interactive (validation)
            interactive_request = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {
                    "name": "your_turn_interactive",
                    "arguments": {
                        "message": "Test question",
                        "interactive": False  # Should fail validation
                    }
                }
            }
            
            response = await server.handle_request(interactive_request)
            validation_works = 'error' in response
            self.test_result("Interactive tool validation", validation_works,
                           "Validation correctly rejects interactive=False")
            
        except Exception as e:
            self.test_result("Tool testing", False, f"Error: {e}")
    
    async def test_docker_functionality(self):
        """Test Docker build and run."""
        try:
            # Test Docker build (check if image exists)
            result = subprocess.run(['docker', 'images', 'your-turn-server', '--format', '{{.Repository}}'],
                                  capture_output=True, text=True, timeout=10)
            
            image_exists = 'your-turn-server' in result.stdout
            self.test_result("Docker image exists", image_exists,
                           "Docker image built successfully")
            
            if image_exists:
                # Test Docker run with version
                result = subprocess.run(['docker', 'run', '--rm', 'your-turn-server', '--version'],
                                      capture_output=True, text=True, timeout=15)
                
                version_works = result.returncode == 0 and '2.0.0' in result.stdout
                self.test_result("Docker version command", version_works,
                               f"Version output: {result.stdout.strip()}")
                
                # Test Docker with environment variables
                result = subprocess.run([
                    'docker', 'run', '--rm',
                    '-e', 'TELEGRAM_BOT_TOKEN=test_token',
                    '-e', 'TELEGRAM_CHAT_ID=123456',
                    'your-turn-server', '--version'
                ], capture_output=True, text=True, timeout=15)
                
                env_vars_work = result.returncode == 0 and 'test_token' in result.stderr
                self.test_result("Docker environment variables", env_vars_work,
                               "Environment variables passed correctly")
            
        except subprocess.TimeoutExpired:
            self.test_result("Docker functionality", False, "Docker commands timed out")
        except FileNotFoundError:
            self.test_result("Docker functionality", False, "Docker not available")
        except Exception as e:
            self.test_result("Docker functionality", False, f"Error: {e}")
    
    async def test_documentation_examples(self):
        """Test examples from documentation."""
        try:
            # Test diagnostic tool
            result = subprocess.run(['python3', 'diagnostic_tool.py'],
                                  capture_output=True, text=True, timeout=30)
            
            diagnostic_works = result.returncode == 0 and 'Diagnostic Report' in result.stdout
            self.test_result("Diagnostic tool", diagnostic_works,
                           "Diagnostic tool runs successfully")
            
            # Test enhanced server test
            result = subprocess.run(['python3', 'test_enhanced_server.py'],
                                  capture_output=True, text=True, timeout=20)
            
            test_works = result.returncode == 0 and 'All tests completed' in result.stdout
            self.test_result("Enhanced server test", test_works,
                           "Enhanced server test passes")
            
        except subprocess.TimeoutExpired:
            self.test_result("Documentation examples", False, "Examples timed out")
        except Exception as e:
            self.test_result("Documentation examples", False, f"Error: {e}")
    
    def generate_final_report(self):
        """Generate final test report."""
        print("\n" + "=" * 60)
        print("📊 FINAL INTEGRATION TEST REPORT")
        print("=" * 60)
        
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! The Enhanced MCP Your Turn Server is fully functional.")
            print("\n✅ Verified functionality:")
            print("  • Sound notifications with multiple fallbacks")
            print("  • Environment variable handling")
            print("  • MCP protocol implementation")
            print("  • All three tools (notify, interactive, legacy)")
            print("  • Docker build and execution")
            print("  • Documentation examples")
            
            print("\n🚀 Ready for production use!")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Review the issues above.")
            
            print("\n❌ Failed tests:")
            for test_name, result in self.results.items():
                if not result['success']:
                    print(f"  • {test_name}: {result['message']}")
        
        print("\n" + "=" * 60)


async def main():
    """Run the final integration test."""
    test_suite = FinalIntegrationTest()
    await test_suite.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
