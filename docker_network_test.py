#!/usr/bin/env python3
"""
Docker Network Test for Telegram Connectivity
Tests network connectivity from within Docker container to Telegram API.
"""

import asyncio
import os
import sys
import json
import socket
import ssl
import urllib.request
import urllib.error
from typing import Optional


class DockerNetworkTester:
    """Test network connectivity from Docker container."""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
    async def run_network_tests(self):
        """Run comprehensive network tests."""
        print("🐳 Docker Network Test for Telegram")
        print("=" * 50)
        
        # Test 1: Basic network connectivity
        await self._test_basic_connectivity()
        
        # Test 2: DNS resolution
        await self._test_dns_resolution()
        
        # Test 3: HTTPS connectivity
        await self._test_https_connectivity()
        
        # Test 4: Telegram API connectivity
        await self._test_telegram_api_connectivity()
        
        # Test 5: Python telegram-bot library
        await self._test_telegram_bot_library()
        
        # Test 6: Full MCP integration
        await self._test_mcp_integration()
        
        print("\n🎯 Network Test Summary")
        print("=" * 50)
        print("If all tests pass, the network configuration is correct.")
        print("If tests fail, check Docker network settings and firewall rules.")
    
    async def _test_basic_connectivity(self):
        """Test basic network connectivity."""
        print("\n🌐 Basic Network Connectivity:")
        
        # Test internet connectivity
        try:
            response = urllib.request.urlopen('https://www.google.com', timeout=10)
            if response.getcode() == 200:
                print("✅ Internet connectivity: Working")
            else:
                print(f"⚠️ Internet connectivity: HTTP {response.getcode()}")
        except Exception as e:
            print(f"❌ Internet connectivity: Failed - {e}")
        
        # Test specific Telegram domain
        try:
            response = urllib.request.urlopen('https://api.telegram.org', timeout=10)
            print("✅ Telegram API domain: Reachable")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("✅ Telegram API domain: Reachable (404 expected for root)")
            else:
                print(f"⚠️ Telegram API domain: HTTP {e.code}")
        except Exception as e:
            print(f"❌ Telegram API domain: Failed - {e}")
    
    async def _test_dns_resolution(self):
        """Test DNS resolution."""
        print("\n🔍 DNS Resolution:")
        
        domains = [
            'api.telegram.org',
            'core.telegram.org',
            'web.telegram.org'
        ]
        
        for domain in domains:
            try:
                ip = socket.gethostbyname(domain)
                print(f"✅ {domain}: {ip}")
            except Exception as e:
                print(f"❌ {domain}: Failed - {e}")
    
    async def _test_https_connectivity(self):
        """Test HTTPS connectivity and SSL."""
        print("\n🔒 HTTPS/SSL Connectivity:")
        
        try:
            # Test SSL connection to Telegram API
            context = ssl.create_default_context()
            with socket.create_connection(('api.telegram.org', 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname='api.telegram.org') as ssock:
                    print(f"✅ SSL connection: {ssock.version()}")
                    print(f"✅ SSL cipher: {ssock.cipher()[0]}")
        except Exception as e:
            print(f"❌ SSL connection: Failed - {e}")
    
    async def _test_telegram_api_connectivity(self):
        """Test direct Telegram API connectivity."""
        print("\n📡 Telegram API Connectivity:")
        
        if not self.bot_token:
            print("⚠️ No bot token provided, skipping API tests")
            return
        
        # Test getMe endpoint
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = urllib.request.urlopen(url, timeout=10)
            data = json.loads(response.read().decode())
            
            if data.get('ok'):
                bot_info = data['result']
                print(f"✅ Bot API: @{bot_info.get('username')} ({bot_info.get('first_name')})")
            else:
                print(f"❌ Bot API: {data.get('description', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Bot API: Failed - {e}")
        
        # Test sendMessage endpoint if chat_id is provided
        if self.chat_id:
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                data = {
                    'chat_id': self.chat_id,
                    'text': '🐳 Docker network test - please ignore'
                }
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={'Content-Type': 'application/json'}
                )
                
                response = urllib.request.urlopen(req, timeout=10)
                result = json.loads(response.read().decode())
                
                if result.get('ok'):
                    print(f"✅ Send message: Message sent (ID: {result['result']['message_id']})")
                else:
                    print(f"❌ Send message: {result.get('description', 'Unknown error')}")
            except Exception as e:
                print(f"❌ Send message: Failed - {e}")
    
    async def _test_telegram_bot_library(self):
        """Test python-telegram-bot library."""
        print("\n📚 Python Telegram Bot Library:")
        
        try:
            import telegram
            print(f"✅ Library version: {telegram.__version__}")
        except ImportError:
            print("❌ Library not installed")
            return
        
        if not self.bot_token:
            print("⚠️ No bot token provided, skipping library tests")
            return
        
        try:
            from telegram import Bot
            bot = Bot(token=self.bot_token)
            
            # Test getMe
            me = await bot.get_me()
            print(f"✅ Bot object: @{me.username} ({me.first_name})")
            
            # Test sendMessage if chat_id is provided
            if self.chat_id:
                message = await bot.send_message(
                    chat_id=self.chat_id,
                    text="🐳 Docker library test - please ignore"
                )
                print(f"✅ Library message: Sent (ID: {message.message_id})")
                
        except Exception as e:
            print(f"❌ Library test: Failed - {e}")
            import traceback
            traceback.print_exc()
    
    async def _test_mcp_integration(self):
        """Test MCP server integration."""
        print("\n🖥️  MCP Integration:")
        
        try:
            from mcp_your_turn_server import MCPServer
            server = MCPServer()
            print("✅ MCP Server: Created")
            
            if server.telegram_notifier and server.telegram_notifier.is_enabled():
                print("✅ Telegram notifier: Enabled")
                
                # Test notification
                request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {
                        "name": "your_turn_notify",
                        "arguments": {"reason": "Docker network test"}
                    }
                }
                
                response = await server.handle_request(request)
                
                if 'result' in response:
                    print("✅ MCP notification: Working")
                else:
                    print(f"❌ MCP notification: {response.get('error', 'Unknown error')}")
                
                # Test interactive mode
                interactive_request = {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "your_turn_interactive",
                        "arguments": {
                            "message": "🐳 Docker interactive test - please respond with 'DOCKER OK'",
                            "interactive": True,
                            "timeout_seconds": 30
                        }
                    }
                }
                
                print("📤 Testing interactive mode...")
                response = await server.handle_request(interactive_request)
                
                if 'result' in response:
                    print("✅ MCP interactive: Question sent")
                    content = response['result']['content'][0]['text']
                    if 'DOCKER OK' in content:
                        print("✅ MCP interactive: Response received!")
                    else:
                        print("⏰ MCP interactive: No response (timeout or no interaction)")
                else:
                    print(f"❌ MCP interactive: {response.get('error', 'Unknown error')}")
            else:
                print("⚠️ Telegram notifier: Not enabled")
                
        except Exception as e:
            print(f"❌ MCP integration: Failed - {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Run the Docker network test."""
    print("🐳 Docker Network Test for Telegram Connectivity")
    print("This tool tests network connectivity from within the Docker container.")
    print()
    
    # Show environment
    print("📋 Environment:")
    print(f"  TELEGRAM_BOT_TOKEN: {'SET' if os.getenv('TELEGRAM_BOT_TOKEN') else 'NOT SET'}")
    print(f"  TELEGRAM_CHAT_ID: {os.getenv('TELEGRAM_CHAT_ID', 'NOT SET')}")
    print(f"  Python version: {sys.version}")
    print()
    
    tester = DockerNetworkTester()
    
    try:
        await tester.run_network_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
