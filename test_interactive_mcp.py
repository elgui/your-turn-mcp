import asyncio
import json
import logging
from mcp_your_turn_server import MCPServer

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_interactive_tool():
    print("🧪 Testing Interactive Tool MCP Protocol Compliance")
    print("=" * 60)
    
    server = MCPServer()
    
    # Test interactive tool
    request = {
        "jsonrpc": "2.0",
        "id": 123,
        "method": "tools/call",
        "params": {
            "name": "your_turn_interactive",
            "arguments": {
                "message": "Test interactive question - please respond with 'TEST OK'",
                "interactive": True,
                "timeout_seconds": 10  # Short timeout for testing
            }
        }
    }
    
    print("📤 Sending interactive tool request...")
    print(f"Request: {json.dumps(request, indent=2)}")
    print()
    
    try:
        response = await server.handle_request(request)
        
        print("📥 Received response:")
        print(json.dumps(response, indent=2))
        print()
        
        # Validate MCP protocol compliance
        print("🔍 MCP Protocol Validation:")
        
        if "jsonrpc" in response and response["jsonrpc"] == "2.0":
            print("✅ JSON-RPC version correct")
        else:
            print("❌ JSON-RPC version missing or incorrect")
        
        if "id" in response and response["id"] == 123:
            print("✅ Request ID correctly echoed")
        else:
            print("❌ Request ID missing or incorrect")
        
        if "result" in response:
            print("✅ Result field present")
            
            result = response["result"]
            if "content" in result and isinstance(result["content"], list):
                print("✅ Content field is array")
                
                if len(result["content"]) > 0:
                    content_item = result["content"][0]
                    if "type" in content_item and content_item["type"] == "text":
                        print("✅ Content type is 'text'")
                    else:
                        print("❌ Content type missing or not 'text'")
                    
                    if "text" in content_item:
                        print("✅ Text field present")
                        print(f"📝 Response text: {content_item['text'][:100]}...")
                    else:
                        print("❌ Text field missing")
                else:
                    print("❌ Content array is empty")
            else:
                print("❌ Content field missing or not array")
        elif "error" in response:
            print("⚠️ Error response received")
            error = response["error"]
            print(f"   Code: {error.get('code')}")
            print(f"   Message: {error.get('message')}")
        else:
            print("❌ Neither result nor error field present")
        
        print("\n🎯 Summary:")
        if "result" in response and "content" in response["result"]:
            print("✅ Interactive tool follows MCP protocol correctly")
        else:
            print("❌ Interactive tool has MCP protocol issues")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_interactive_tool())
