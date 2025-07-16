#!/bin/bash

# Docker entrypoint script for MCP Your Turn Server
# Handles command-line arguments and environment variables

set -e

# Function to show usage
show_usage() {
    echo "MCP Your Turn Server - Docker Container"
    echo ""
    echo "Usage:"
    echo "  docker run your-turn-server [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --telegram-token TOKEN     Telegram bot token"
    echo "  --telegram-chat-id ID      Telegram chat ID"
    echo "  --help                     Show help"
    echo "  --version                  Show version"
    echo ""
    echo "Environment Variables:"
    echo "  TELEGRAM_BOT_TOKEN         Telegram bot token"
    echo "  TELEGRAM_CHAT_ID           Telegram chat ID"
    echo ""
    echo "Examples:"
    echo "  # Sound notifications only"
    echo "  docker run your-turn-server"
    echo ""
    echo "  # With Telegram (via arguments)"
    echo "  docker run your-turn-server --telegram-token \"123:ABC\" --telegram-chat-id \"456789\""
    echo ""
    echo "  # With Telegram (via environment variables)"
    echo "  docker run -e TELEGRAM_BOT_TOKEN=\"123:ABC\" -e TELEGRAM_CHAT_ID=\"456789\" your-turn-server"
    echo ""
    echo "  # In MCP configuration:"
    echo "  {"
    echo "    \"mcpServers\": {"
    echo "      \"your-turn\": {"
    echo "        \"command\": \"docker\","
    echo "        \"args\": [\"run\", \"-i\", \"--rm\", \"your-turn-server\", \"--telegram-token\", \"123:ABC\", \"--telegram-chat-id\", \"456789\"]"
    echo "      }"
    echo "    }"
    echo "  }"
}

# Handle help and version flags
for arg in "$@"; do
    case $arg in
        --help|-h)
            show_usage
            exit 0
            ;;
        --version)
            python3 mcp_your_turn_server.py --version
            exit 0
            ;;
    esac
done

# Log startup information
echo "[DOCKER] Starting MCP Your Turn Server..." >&2
echo "[DOCKER] Container version: 1.1.0" >&2

# Check if we have Telegram configuration
if [ -n "$TELEGRAM_BOT_TOKEN" ] || [ -n "$TELEGRAM_CHAT_ID" ]; then
    echo "[DOCKER] Telegram environment variables detected" >&2
fi

# Check for command-line Telegram arguments
for arg in "$@"; do
    case $arg in
        --telegram-token*|--telegram-chat-id*)
            echo "[DOCKER] Telegram command-line arguments detected" >&2
            break
            ;;
    esac
done

# Start the MCP server with all provided arguments
echo "[DOCKER] Executing: python3 mcp_your_turn_server.py $*" >&2
exec python3 mcp_your_turn_server.py "$@"
