# MCP Your Turn Server - Knowledge Base

## Project Overview
The MCP Your Turn Server is a Model Context Protocol (MCP) server that provides notification tools for LLM interactions. It allows LLMs to notify users when they need attention or input.

## Current Architecture

### Core Components
1. **MCPServer** (`mcp_your_turn_server.py`): Main server class handling MCP protocol
2. **TelegramNotifier** (`telegram_notifier.py`): Handles Telegram bot notifications
3. **Config** (`config.py`): Configuration management with environment variables

### Current Tool
- **`your_turn`**: Single tool that triggers sound + optional Telegram notification

### Key Features
- Cross-platform sound notifications (Windows, macOS, Linux)
- Optional Telegram bot integration
- Docker support with multi-stage builds
- Environment variable configuration
- Graceful fallback when Telegram unavailable

## Technical Details

### MCP Protocol Implementation
- Supports MCP protocol version "2024-11-05"
- Implements required methods: `initialize`, `tools/list`, `tools/call`
- Uses JSON-RPC 2.0 over stdin/stdout

### Sound System
- Platform-specific implementations:
  - Windows: `winsound.Beep()`
  - macOS: `afplay` with system sounds
  - Linux: `paplay`/`aplay` with ALSA sounds
  - Fallback: ASCII bell character (`\a`)

### Telegram Integration
- Uses `python-telegram-bot` library
- Supports bot token and chat ID configuration
- Formatted messages with Markdown, emojis, timestamps
- Timeout handling (10 seconds)
- Comprehensive error handling

### Configuration Priority
1. Environment variables
2. Command-line arguments  
3. Config file (.env support)

## Dependencies
- `python-telegram-bot>=20.0` (optional)
- `python-dotenv>=1.0.0` (optional)
- Python 3.7+ required

## Docker Architecture
- Multi-stage build for minimal image size
- Supports both environment variables and command-line args
- No client-side Python dependencies required

## Enhanced Architecture (v2.0.0)

### New Components Added
1. **SoundManager** (`sound_manager.py`): Multi-fallback sound system
2. **InteractiveSessionManager** (`interactive_session.py`): Session management for user responses
3. **Enhanced TelegramNotifier**: Interactive capabilities with response handling

### Three Tools Available
1. **`your_turn_notify`**: Simple notification (sound + optional Telegram)
2. **`your_turn_interactive`**: Ask questions and wait for responses via Telegram
3. **`your_turn`**: Legacy tool (backward compatibility)

### Sound System Improvements
- **Multi-fallback strategy**: System sounds → external file → embedded beep → ASCII bell
- **Embedded sound data**: No external file dependencies
- **Cross-platform robustness**: Enhanced platform-specific implementations
- **Graceful degradation**: Always provides some form of notification

### Interactive Features
- **Session Management**: UUID-based session tracking
- **Timeout Handling**: Configurable response timeouts
- **Response Processing**: Automatic response routing to sessions
- **Cleanup**: Automatic cleanup of expired sessions
- **Rich Messaging**: Formatted Telegram messages with session info

### Robustness Improvements
- **Comprehensive Error Handling**: Graceful failure modes
- **Structured Logging**: Proper logging throughout the system
- **Input Validation**: Parameter validation for all tools
- **Async Operations**: Non-blocking I/O operations
- **Resource Management**: Proper cleanup of temporary resources

## Enhanced File Structure (v2.0.0)
```
your-turn-mcp/
├── mcp_your_turn_server.py    # Main server with 3 tools
├── sound_manager.py           # Multi-fallback sound system
├── telegram_notifier.py       # Enhanced Telegram with interactive support
├── interactive_session.py     # Session management for interactive mode
├── config.py                  # Configuration management
├── alert.wav                  # External sound file (optional)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build
├── docker-compose.yml         # Docker Compose setup
├── README.md                  # Enhanced user documentation
├── DEVELOPER.md               # Developer documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT license
├── TELEGRAM_INTEGRATION.md    # Telegram setup guide
├── test_telegram.py           # Telegram testing script
├── TASK.md                    # Project progress tracking
└── KNOWLEDGE.md               # Project knowledge base
```

## Best Practices Learned
- Always provide graceful fallbacks for optional features
- Use stderr for logging to avoid interfering with MCP protocol
- Implement comprehensive error handling for network operations
- Support multiple configuration methods for flexibility
- Maintain backward compatibility when possible
- Use type hints for better code maintainability
