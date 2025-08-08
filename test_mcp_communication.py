import asyncio
import json
import sys
from mcp_your_turn_server import MCPServer

async def test_mcp_communication():
    print("🧪 Testing MCP Communication")
    print("=" * 50)
    
    server = MCPServer()
    
    # Test notification tool (what you're actually using)
    print("📢 Testing notification tool...")
    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "your_turn_notify",
            "arguments": {
                "reason": "Test notification from MCP communication test"
            }
        }
    }
    
    print("📤 Sending request:")
    print(json.dumps(request, indent=2))
    print()
    
    try:
        response = await server.handle_request(request)
        
        print("📥 Received response:")
        print(json.dumps(response, indent=2))
        print()
        
        # Check if response is properly formatted
        if response.get("jsonrpc") == "2.0" and response.get("id") == 2:
            if "result" in response:
                print("✅ Response properly formatted and should be received by MCP client")
                return True
            elif "error" in response:
                print("⚠️ Error response (but properly formatted)")
                return True
        else:
            print("❌ Response not properly formatted for MCP protocol")
            return False
            
    except Exception as e:
        print(f"❌ Exception during request handling: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_mcp_communication())
    sys.exit(0 if success else 1)
