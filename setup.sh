#!/bin/bash

# MCP Your Turn Server - Setup Script
# This script helps you set up the server with Telegram integration

set -e

echo "🚀 MCP Your Turn Server Setup"
echo "=============================="

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "❌ Python 3 is required but not found"
    exit 1
}

echo "✅ Python 3 found"

# Ask user if they want Telegram integration
echo ""
read -p "Do you want to set up Telegram notifications? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📱 Setting up Telegram integration..."
    
    # Install dependencies
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt || {
        echo "❌ Failed to install dependencies"
        echo "Try: pip3 install --user -r requirements.txt"
        exit 1
    }
    
    echo "✅ Dependencies installed"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        echo "✅ Created .env file from template"
        echo ""
        echo "📝 Please edit .env file with your Telegram bot token and chat ID:"
        echo "   1. Get bot token from @BotFather on Telegram"
        echo "   2. Get chat ID by messaging your bot, then visiting:"
        echo "      https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates"
        echo ""
        read -p "Press Enter when you've configured .env file..."
        
        # Test configuration
        echo "Testing Telegram configuration..."
        python3 test_telegram.py || {
            echo "❌ Telegram test failed. Please check your configuration."
            exit 1
        }
    else
        echo "⚠️  .env file already exists"
        echo "Testing existing configuration..."
        python3 test_telegram.py || {
            echo "❌ Telegram test failed. Please check your .env configuration."
            exit 1
        }
    fi
    
    echo "✅ Telegram integration configured successfully!"
else
    echo "📢 Skipping Telegram setup - sound notifications only"
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x mcp_your_turn_server.py
chmod +x test_telegram.py
echo "✅ Scripts are now executable"

# Test server startup
echo ""
echo "Testing server startup..."
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | python3 mcp_your_turn_server.py > /dev/null 2>&1 || {
    echo "❌ Server startup test failed"
    exit 1
}

echo "✅ Server startup test passed"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add the server to your MCP client configuration"
echo "2. Use the path: $(pwd)/mcp_your_turn_server.py"
echo ""
echo "Example MCP configuration:"
echo '{'
echo '  "mcpServers": {'
echo '    "your-turn": {'
echo '      "command": "python3",'
echo '      "args": ["'$(pwd)'/mcp_your_turn_server.py"]'
if [[ $REPLY =~ ^[Yy]$ ]]; then
echo '      "env": {'
echo '        "TELEGRAM_BOT_TOKEN": "your_bot_token_here",'
echo '        "TELEGRAM_CHAT_ID": "your_chat_id_here"'
echo '      }'
fi
echo '    }'
echo '  }'
echo '}'
echo ""
echo "For more configuration examples, see README.md"
