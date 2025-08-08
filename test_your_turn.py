#!/usr/bin/env python3
"""
Test script to verify the your_turn tool works correctly.
"""

import json
import asyncio
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp_your_turn_server import YourTurnServer

async def test_your_turn_tool():
    """Test the your_turn tool to ensure it properly captures user responses."""
    
    # Create server instance
    server = YourTurnServer()
    
    # Create a test request
    test_request = {
        "jsonrpc": "2.0",
        "id": "test-123",
        "method": "tools/call",
        "params": {
            "name": "your_turn",
            "arguments": {
                "reason": "Testing user response transmission"
            }
        }
    }
    
    print("🧪 Testing your_turn tool...")
    print(f"📤 Sending request: {json.dumps(test_request, indent=2)}")
    
    try:
        # Handle the request
        response = await server.handle_request(test_request)
        
        print(f"📥 Received response: {json.dumps(response, indent=2)}")
        
        # Check if the response contains user input
        if "result" in response and "content" in response["result"]:
            content = response["result"]["content"][0]["text"]
            if "User Response:" in content:
                print("✅ SUCCESS: User response was captured and included in the response!")
            else:
                print("❌ ISSUE: User response was not included in the response")
                print(f"Response content: {content}")
        else:
            print("❌ ERROR: Invalid response format")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_your_turn_tool())
