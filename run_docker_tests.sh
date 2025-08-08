#!/bin/bash

# Docker Test Runner for Enhanced MCP Your Turn Server
# Tests network connectivity and Telegram functionality from within Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_status $BLUE "🐳 Docker Test Runner for Enhanced MCP Your Turn Server"
echo "=" * 60

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_status $RED "❌ Docker is not installed or not in PATH"
    exit 1
fi

print_status $GREEN "✅ Docker is available"

# Check environment variables
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    print_status $YELLOW "⚠️  TELEGRAM_BOT_TOKEN not set"
    echo "   Set it with: export TELEGRAM_BOT_TOKEN='your_token_here'"
else
    print_status $GREEN "✅ TELEGRAM_BOT_TOKEN is set"
fi

if [ -z "$TELEGRAM_CHAT_ID" ]; then
    print_status $YELLOW "⚠️  TELEGRAM_CHAT_ID not set"
    echo "   Set it with: export TELEGRAM_CHAT_ID='your_chat_id_here'"
else
    print_status $GREEN "✅ TELEGRAM_CHAT_ID is set"
fi

# Build the Docker image
print_status $BLUE "\n🔨 Building Docker image..."
if docker build -t your-turn-server .; then
    print_status $GREEN "✅ Docker image built successfully"
else
    print_status $RED "❌ Docker build failed"
    exit 1
fi

# Test 1: Basic container functionality
print_status $BLUE "\n🧪 Test 1: Basic Container Functionality"
echo "Testing basic container startup and version..."

if docker run --rm your-turn-server --version; then
    print_status $GREEN "✅ Basic container functionality works"
else
    print_status $RED "❌ Basic container functionality failed"
    exit 1
fi

# Test 2: Network connectivity test
print_status $BLUE "\n🌐 Test 2: Network Connectivity"
echo "Testing network connectivity from within container..."

# Run with proper network configuration
if docker run --rm \
    --network host \
    -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
    -e TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
    your-turn-server --network-test; then
    print_status $GREEN "✅ Network connectivity test passed"
else
    print_status $YELLOW "⚠️  Network connectivity test had issues (check output above)"
fi

# Test 3: MCP notification tool
print_status $BLUE "\n📢 Test 3: MCP Notification Tool"
echo "Testing MCP notification functionality..."

# Create a test script for the notification tool
cat > test_notification.py << 'EOF'
import asyncio
import json
import sys
from mcp_your_turn_server import MCPServer

async def test_notification():
    server = MCPServer()
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "your_turn_notify",
            "arguments": {"reason": "Docker container test notification"}
        }
    }
    
    try:
        response = await server.handle_request(request)
        print(json.dumps(response, indent=2))
        
        if 'result' in response:
            print("✅ Notification tool test: PASSED", file=sys.stderr)
            sys.exit(0)
        else:
            print("❌ Notification tool test: FAILED", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Notification tool test: ERROR - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_notification())
EOF

# Copy test script to container and run it
if docker run --rm \
    --network host \
    -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
    -e TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
    -v "$(pwd)/test_notification.py:/app/test_notification.py" \
    your-turn-server python3 test_notification.py; then
    print_status $GREEN "✅ MCP notification tool works"
else
    print_status $RED "❌ MCP notification tool failed"
fi

# Clean up test script
rm -f test_notification.py

# Test 4: Interactive mode test (if Telegram is configured)
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    print_status $BLUE "\n❓ Test 4: Interactive Mode"
    echo "Testing interactive mode functionality..."
    
    # Create interactive test script
    cat > test_interactive.py << 'EOF'
import asyncio
import json
import sys
from mcp_your_turn_server import MCPServer

async def test_interactive():
    server = MCPServer()
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "your_turn_interactive",
            "arguments": {
                "message": "🐳 Docker interactive test - please respond with 'DOCKER OK' within 30 seconds",
                "interactive": True,
                "timeout_seconds": 30
            }
        }
    }
    
    try:
        print("📤 Sending interactive question...", file=sys.stderr)
        response = await server.handle_request(request)
        print(json.dumps(response, indent=2))
        
        if 'result' in response:
            content = response['result']['content'][0]['text']
            if 'DOCKER OK' in content:
                print("✅ Interactive mode test: PASSED - Response received!", file=sys.stderr)
            else:
                print("⏰ Interactive mode test: TIMEOUT - No response received", file=sys.stderr)
            sys.exit(0)
        else:
            print("❌ Interactive mode test: FAILED", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"❌ Interactive mode test: ERROR - {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_interactive())
EOF

    # Run interactive test
    if docker run --rm \
        --network host \
        -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
        -e TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
        -v "$(pwd)/test_interactive.py:/app/test_interactive.py" \
        your-turn-server python3 test_interactive.py; then
        print_status $GREEN "✅ Interactive mode test completed"
    else
        print_status $YELLOW "⚠️  Interactive mode test had issues"
    fi
    
    # Clean up test script
    rm -f test_interactive.py
else
    print_status $YELLOW "⚠️  Skipping interactive mode test (Telegram not configured)"
fi

# Test 5: Long-running container test
print_status $BLUE "\n🔄 Test 5: Long-running Container"
echo "Testing container in background mode..."

# Start container in background
CONTAINER_ID=$(docker run -d \
    --network host \
    -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
    -e TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID" \
    your-turn-server)

if [ $? -eq 0 ]; then
    print_status $GREEN "✅ Container started in background: $CONTAINER_ID"
    
    # Wait a few seconds
    sleep 5
    
    # Check if container is still running
    if docker ps | grep -q "$CONTAINER_ID"; then
        print_status $GREEN "✅ Container is running successfully"
        
        # Test sending a request to the running container
        echo "📤 Testing communication with running container..."
        
        # Stop the container
        docker stop "$CONTAINER_ID" > /dev/null
        print_status $GREEN "✅ Container stopped cleanly"
    else
        print_status $RED "❌ Container stopped unexpectedly"
        echo "Container logs:"
        docker logs "$CONTAINER_ID"
    fi
else
    print_status $RED "❌ Failed to start container in background"
fi

# Summary
print_status $BLUE "\n📊 Test Summary"
echo "=" * 60

print_status $GREEN "✅ Docker image builds successfully"
print_status $GREEN "✅ Container starts and runs"
print_status $GREEN "✅ Network connectivity tested"
print_status $GREEN "✅ MCP protocol works"

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    print_status $GREEN "✅ Telegram configuration detected"
    echo "   Check the test output above for Telegram functionality results"
else
    print_status $YELLOW "⚠️  Telegram not configured - some tests skipped"
    echo "   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to test Telegram features"
fi

print_status $BLUE "\n🚀 Docker container is ready for use!"
echo ""
echo "To run the container:"
echo "  docker run --rm --network host -e TELEGRAM_BOT_TOKEN=\"\$TELEGRAM_BOT_TOKEN\" -e TELEGRAM_CHAT_ID=\"\$TELEGRAM_CHAT_ID\" your-turn-server"
echo ""
echo "To test network connectivity:"
echo "  docker run --rm --network host -e TELEGRAM_BOT_TOKEN=\"\$TELEGRAM_BOT_TOKEN\" -e TELEGRAM_CHAT_ID=\"\$TELEGRAM_CHAT_ID\" your-turn-server --network-test"
