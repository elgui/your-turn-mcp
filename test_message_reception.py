import asyncio
import json
import sys
import time
from datetime import datetime

async def test_message_reception():
    print("🧪 Testing Message Reception in Container")
    print("=" * 60)
    
    # Test the simplified your_turn tool
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "your_turn",
            "arguments": {
                "reason": "Testing message reception - I will send a test message to Telegram in 10 seconds"
            }
        }
    }
    
    print("📤 Sending your_turn request...")
    print(f"Request: {json.dumps(request, indent=2)}")
    print()
    
    print("⏰ The container will:")
    print("   1. Send notification to Telegram")
    print("   2. Wait 300 seconds for your response")
    print("   3. I will send a test message after 10 seconds")
    print("   4. Check if the container receives and processes it")
    print()
    
    # Send the request
    print(json.dumps(request))
    sys.stdout.flush()
    
    # The container should now be waiting for a response
    # We'll simulate sending a message after 10 seconds
    
    print("⏳ Waiting 10 seconds before sending test message...", file=sys.stderr)
    await asyncio.sleep(10)
    
    print("📨 Now I would send a test message to Telegram...", file=sys.stderr)
    print("   (In real test, you should send a message to the bot)", file=sys.stderr)
    print("   Message: 'TEST MESSAGE RECEIVED'", file=sys.stderr)
    print("   The container should log this message if it's listening", file=sys.stderr)
    
    # Wait a bit more to see if anything happens
    await asyncio.sleep(20)
    
    print("🔍 Check the container logs above for:", file=sys.stderr)
    print("   - 'Received message from user'", file=sys.stderr)
    print("   - 'Response successfully submitted'", file=sys.stderr)
    print("   - Any message processing activity", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(test_message_reception())
