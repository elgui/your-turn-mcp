#!/bin/bash

# Build script for MCP Your Turn Server Docker image

set -e

echo "🐳 Building MCP Your Turn Server Docker Image"
echo "=============================================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

echo "✅ Docker found"

# Build the image
echo "📦 Building Docker image..."
docker build -t your-turn-server .

echo "✅ Docker image built successfully!"

# Test the image
echo "🧪 Testing Docker image..."

# Test basic functionality
echo "Testing basic startup..."
if echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | docker run -i --rm your-turn-server > /dev/null 2>&1; then
    echo "✅ Basic startup test passed"
else
    echo "❌ Basic startup test failed"
    exit 1
fi

# Test help functionality
echo "Testing help command..."
if docker run --rm your-turn-server --help > /dev/null 2>&1; then
    echo "✅ Help command test passed"
else
    echo "❌ Help command test failed"
    exit 1
fi

# Test with arguments
echo "Testing with Telegram arguments..."
if echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | docker run -i --rm your-turn-server --telegram-token "test" --telegram-chat-id "123" > /dev/null 2>&1; then
    echo "✅ Telegram arguments test passed"
else
    echo "❌ Telegram arguments test failed"
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
echo ""
echo "Usage examples:"
echo "  # Basic usage"
echo "  docker run -i --rm your-turn-server"
echo ""
echo "  # With Telegram"
echo "  docker run -i --rm your-turn-server --telegram-token \"YOUR_TOKEN\" --telegram-chat-id \"YOUR_CHAT_ID\""
echo ""
echo "  # In MCP configuration:"
echo "  {"
echo "    \"mcpServers\": {"
echo "      \"your-turn\": {"
echo "        \"command\": \"docker\","
echo "        \"args\": [\"run\", \"-i\", \"--rm\", \"your-turn-server\", \"--telegram-token\", \"YOUR_TOKEN\", \"--telegram-chat-id\", \"YOUR_CHAT_ID\"]"
echo "      }"
echo "    }"
echo "  }"
