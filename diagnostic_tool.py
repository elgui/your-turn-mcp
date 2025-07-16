#!/usr/bin/env python3
"""
Comprehensive diagnostic tool for MCP Your Turn Server.
Tests sound notifications and Telegram functionality with detailed reporting.
"""

import os
import sys
import asyncio
import logging
import platform
import subprocess
from typing import Optional, Dict, Any, List, Tuple

# Set up logging for diagnostics
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiagnosticTool:
    """Comprehensive diagnostic tool for troubleshooting."""
    
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.platform = platform.system().lower()
        
    async def run_all_diagnostics(self) -> Dict[str, Any]:
        """Run all diagnostic tests."""
        print("🔍 MCP Your Turn Server Diagnostic Tool")
        print("=" * 50)
        
        # System information
        await self._test_system_info()
        
        # Environment variables
        await self._test_environment_variables()
        
        # Python dependencies
        await self._test_python_dependencies()
        
        # Sound system
        await self._test_sound_system()
        
        # Telegram functionality
        await self._test_telegram_functionality()
        
        # MCP server functionality
        await self._test_mcp_server()
        
        # Generate report
        self._generate_report()
        
        return self.results
    
    async def _test_system_info(self):
        """Test and report system information."""
        print("\n🖥️  System Information")
        print("-" * 30)
        
        info = {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture()[0]
        }
        
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        self.results['system_info'] = info
    
    async def _test_environment_variables(self):
        """Test environment variable configuration."""
        print("\n🔧 Environment Variables")
        print("-" * 30)
        
        env_vars = {
            'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
            'TELEGRAM_CHAT_ID': os.getenv('TELEGRAM_CHAT_ID'),
            'TELEGRAM_ENABLED': os.getenv('TELEGRAM_ENABLED', 'true')
        }
        
        results = {}
        for var, value in env_vars.items():
            if value:
                if var == 'TELEGRAM_BOT_TOKEN':
                    display_value = f"{value[:10]}..." if len(value) > 10 else value
                    print(f"  ✅ {var}: {display_value}")
                    results[var] = {'set': True, 'valid_format': ':' in value}
                else:
                    print(f"  ✅ {var}: {value}")
                    results[var] = {'set': True, 'value': value}
            else:
                print(f"  ❌ {var}: Not set")
                results[var] = {'set': False}
        
        self.results['environment_variables'] = results
    
    async def _test_python_dependencies(self):
        """Test Python dependencies."""
        print("\n📦 Python Dependencies")
        print("-" * 30)
        
        dependencies = [
            ('python-telegram-bot', 'telegram'),
            ('python-dotenv', 'dotenv'),
            ('asyncio', 'asyncio')
        ]
        
        results = {}
        for dep_name, import_name in dependencies:
            try:
                __import__(import_name)
                print(f"  ✅ {dep_name}: Available")
                results[dep_name] = {'available': True}
            except ImportError as e:
                print(f"  ❌ {dep_name}: Not available ({e})")
                results[dep_name] = {'available': False, 'error': str(e)}
        
        self.results['dependencies'] = results
    
    async def _test_sound_system(self):
        """Test sound system functionality."""
        print("\n🔊 Sound System")
        print("-" * 30)
        
        try:
            from sound_manager import SoundManager
            manager = SoundManager()
            
            # Test each sound strategy
            strategies = [
                ('System Sound', manager._play_system_sound),
                ('External Sound', manager._play_external_sound),
                ('Embedded Sound', manager._play_embedded_sound),
                ('ASCII Bell', manager._play_ascii_bell)
            ]
            
            results = {}
            for strategy_name, strategy_func in strategies:
                try:
                    print(f"  🎵 Testing {strategy_name}...")
                    success = strategy_func()
                    if success:
                        print(f"    ✅ {strategy_name}: Working")
                        results[strategy_name] = {'working': True}
                    else:
                        print(f"    ❌ {strategy_name}: Failed")
                        results[strategy_name] = {'working': False}
                except Exception as e:
                    print(f"    ❌ {strategy_name}: Error - {e}")
                    results[strategy_name] = {'working': False, 'error': str(e)}
            
            # Test overall sound manager
            print(f"  🔊 Testing overall sound notification...")
            overall_success = manager.play_notification_sound()
            print(f"    {'✅' if overall_success else '❌'} Overall sound: {'Working' if overall_success else 'Failed'}")
            results['overall'] = {'working': overall_success}
            
            self.results['sound_system'] = results
            
        except ImportError as e:
            print(f"  ❌ Sound manager not available: {e}")
            self.results['sound_system'] = {'available': False, 'error': str(e)}
    
    async def _test_telegram_functionality(self):
        """Test Telegram functionality."""
        print("\n🤖 Telegram Functionality")
        print("-" * 30)
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            print("  ❌ Telegram credentials not configured")
            self.results['telegram'] = {'configured': False}
            return
        
        try:
            from telegram_notifier import TelegramNotifier
            notifier = TelegramNotifier(bot_token, chat_id)
            
            results = {
                'configured': True,
                'initialized': notifier.is_enabled()
            }
            
            if notifier.is_enabled():
                print("  ✅ Telegram notifier initialized")
                
                # Test connection
                try:
                    print("  🔍 Testing Telegram connection...")
                    me = await notifier.bot.get_me()
                    print(f"    ✅ Connected to bot: @{me.username}")
                    results['connection_test'] = {'success': True, 'bot_username': me.username}
                except Exception as e:
                    print(f"    ❌ Connection test failed: {e}")
                    results['connection_test'] = {'success': False, 'error': str(e)}
                
                # Test notification (optional)
                print("  📤 Testing notification send (optional)...")
                try:
                    success = await notifier.send_notification("Diagnostic test")
                    if success:
                        print("    ✅ Test notification sent successfully")
                        results['notification_test'] = {'success': True}
                    else:
                        print("    ❌ Test notification failed")
                        results['notification_test'] = {'success': False}
                except Exception as e:
                    print(f"    ❌ Notification test error: {e}")
                    results['notification_test'] = {'success': False, 'error': str(e)}
            else:
                print("  ❌ Telegram notifier failed to initialize")
                results['initialization_error'] = True
            
            self.results['telegram'] = results
            
        except ImportError as e:
            print(f"  ❌ Telegram dependencies not available: {e}")
            self.results['telegram'] = {'available': False, 'error': str(e)}
    
    async def _test_mcp_server(self):
        """Test MCP server functionality."""
        print("\n🖥️  MCP Server")
        print("-" * 30)
        
        try:
            from mcp_your_turn_server import MCPServer
            server = MCPServer()
            
            # Test initialization
            print("  ✅ MCP Server initialized")
            
            # Test tools
            tools = list(server.tools.keys())
            print(f"  📋 Available tools: {', '.join(tools)}")
            
            # Test basic MCP protocol
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {}
            }
            
            response = await server.handle_request(init_request)
            if response.get('result', {}).get('protocolVersion'):
                print(f"  ✅ MCP protocol: {response['result']['protocolVersion']}")
            
            self.results['mcp_server'] = {
                'initialized': True,
                'tools': tools,
                'protocol_version': response.get('result', {}).get('protocolVersion')
            }
            
        except Exception as e:
            print(f"  ❌ MCP Server error: {e}")
            self.results['mcp_server'] = {'initialized': False, 'error': str(e)}
    
    def _generate_report(self):
        """Generate diagnostic report."""
        print("\n📊 Diagnostic Report")
        print("=" * 50)
        
        # Overall status
        issues = []
        
        # Check environment variables
        env_vars = self.results.get('environment_variables', {})
        if not env_vars.get('TELEGRAM_BOT_TOKEN', {}).get('set'):
            issues.append("TELEGRAM_BOT_TOKEN not set")
        if not env_vars.get('TELEGRAM_CHAT_ID', {}).get('set'):
            issues.append("TELEGRAM_CHAT_ID not set")
        
        # Check dependencies
        deps = self.results.get('dependencies', {})
        if not deps.get('python-telegram-bot', {}).get('available'):
            issues.append("python-telegram-bot not installed")
        
        # Check sound system
        sound = self.results.get('sound_system', {})
        if not sound.get('overall', {}).get('working'):
            issues.append("Sound system not working")
        
        # Check Telegram
        telegram = self.results.get('telegram', {})
        if not telegram.get('configured'):
            issues.append("Telegram not configured")
        elif not telegram.get('connection_test', {}).get('success'):
            issues.append("Telegram connection failed")
        
        if not issues:
            print("✅ All systems operational!")
        else:
            print("❌ Issues found:")
            for issue in issues:
                print(f"  • {issue}")
        
        print("\n💡 Recommendations:")
        if "TELEGRAM_BOT_TOKEN not set" in issues:
            print("  • Set TELEGRAM_BOT_TOKEN environment variable")
            print("  • Get a token from @BotFather on Telegram")
        if "TELEGRAM_CHAT_ID not set" in issues:
            print("  • Set TELEGRAM_CHAT_ID environment variable")
            print("  • Send a message to your bot and check the logs")
        if "python-telegram-bot not installed" in issues:
            print("  • Install with: pip install python-telegram-bot")
        if "Sound system not working" in issues:
            print("  • Check audio system configuration")
            print("  • Install audio utilities (paplay, aplay, etc.)")
        if "Telegram connection failed" in issues:
            print("  • Check internet connection")
            print("  • Verify bot token is correct")
            print("  • Make sure you've messaged the bot first")


async def main():
    """Run diagnostic tool."""
    diagnostic = DiagnosticTool()
    await diagnostic.run_all_diagnostics()


if __name__ == "__main__":
    asyncio.run(main())
