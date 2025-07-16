# Enhanced MCP Your Turn Server

A powerful Model Context Protocol (MCP) server that provides notification and interactive communication tools for LLM interactions. Features both simple notifications and interactive user input capabilities via Telegram.

## 🚀 Features

- **🔔 Smart Notifications**: Cross-platform sound notifications with multiple fallback options
- **💬 Interactive Mode**: Ask users questions and wait for responses via Telegram
- **📱 Telegram Integration**: Rich Telegram bot notifications with interactive capabilities
- **🎵 Embedded Sound**: No external sound file dependencies
- **🐳 Docker Support**: Easy deployment with Docker
- **⚙️ Flexible Configuration**: Environment variables, command-line args, or config files
- **🛡️ Robust Fallbacks**: Graceful degradation when services are unavailable
- **🔄 Backward Compatible**: Maintains compatibility with existing implementations

## 🛠️ Tools Available

### 1. `your_turn_notify` - Simple Notifications
Send a notification to the user with sound and optional Telegram message.

**Parameters**:
- `reason` (optional, string): Reason for the notification

### 2. `your_turn_interactive` - Interactive Questions
Ask the user a question and wait for their response via Telegram.

**Parameters**:
- `message` (required, string): The question to ask the user
- `interactive` (required, boolean): Must be `true` to enable interactive mode
- `timeout_seconds` (optional, integer): How long to wait for response (default: 300)

### 3. `your_turn` - Legacy Tool
Backward-compatible tool that works like `your_turn_notify`.

## 🚀 Quick Start

### Basic Usage (Sound Only)

```bash
python3 mcp_your_turn_server.py
```

### With Telegram Notifications

1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID (see [Telegram Setup Guide](TELEGRAM_INTEGRATION.md))
3. Run with your credentials:

```bash
python3 mcp_your_turn_server.py --telegram-token "YOUR_BOT_TOKEN" --telegram-chat-id "YOUR_CHAT_ID"
```

### Interactive Mode Example

```json
{
  "name": "your_turn_interactive",
  "arguments": {
    "message": "What color scheme would you prefer for the website?",
    "interactive": true,
    "timeout_seconds": 600
  }
}
```

## 📦 Installation

### Prerequisites

- Python 3.7+
- Optional: `python-telegram-bot` for Telegram features

### Install Dependencies

```bash
# Basic installation
pip install -r requirements.txt

# For full Telegram support (including interactive mode)
pip install python-telegram-bot python-dotenv
```

### Docker Installation

```bash
# Build the image
docker build -t your-turn-server .

# Run with Telegram support
docker run -e TELEGRAM_BOT_TOKEN="your_token" -e TELEGRAM_CHAT_ID="your_chat_id" your-turn-server
```

## ⚙️ Configuration

The server supports multiple configuration methods (in order of priority):

1. **Environment Variables** (highest priority)
2. **Command-line Arguments**
3. **Config File** (lowest priority)

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### Command-line Arguments

- `--telegram-token`: Telegram bot token
- `--telegram-chat-id`: Telegram chat ID
- `--version`: Show version information

## 🎵 Sound System

The enhanced sound system provides multiple fallback options:

1. **Platform-specific system sounds** (primary)
   - Windows: System notification sounds
   - macOS: Built-in system sounds
   - Linux: ALSA system sounds

2. **External sound file** (secondary)
   - Uses `alert.wav` if present

3. **Embedded minimal beep** (tertiary)
   - Built-in sound data, no external files needed

4. **ASCII bell** (final fallback)
   - Always works as last resort

## 📱 Telegram Integration

### Simple Notifications
Rich formatted messages with emojis, timestamps, and status information.

### Interactive Mode
- Send questions to users
- Wait for responses with configurable timeouts
- Session management with unique IDs
- Automatic cleanup of expired sessions
- Confirmation messages for received responses

See [TELEGRAM_INTEGRATION.md](TELEGRAM_INTEGRATION.md) for detailed setup instructions.

## 🐳 Docker Usage

### Using Docker Compose

```yaml
version: '3.8'
services:
  your-turn-server:
    build: .
    environment:
      - TELEGRAM_BOT_TOKEN=your_bot_token_here
      - TELEGRAM_CHAT_ID=your_chat_id_here
    stdin_open: true
    tty: true
```

### Direct Docker Commands

```bash
# Build
docker build -t your-turn-server .

# Run with environment variables
docker run -e TELEGRAM_BOT_TOKEN="token" -e TELEGRAM_CHAT_ID="chat_id" your-turn-server

# Run with command-line args
docker run your-turn-server --telegram-token "token" --telegram-chat-id "chat_id"
```

## 🔧 Troubleshooting

### Common Issues

1. **No sound on any platform**: The embedded sound system provides fallbacks
   ```bash
   # Test the sound manager
   python3 -c "from sound_manager import play_notification_sound; play_notification_sound()"
   ```

2. **Interactive mode not working**: Ensure Telegram is properly configured
   ```bash
   python3 test_telegram.py
   ```

3. **Import errors**: Install missing dependencies
   ```bash
   pip install python-telegram-bot python-dotenv
   ```

### Debug Mode

Run with Python's verbose mode to see detailed error messages:
```bash
python3 -v mcp_your_turn_server.py
```

## 🏗️ Architecture

The enhanced server is built with a modular architecture:

- **`mcp_your_turn_server.py`**: Main server with tool handling
- **`sound_manager.py`**: Robust sound notification system
- **`telegram_notifier.py`**: Telegram integration with interactive support
- **`interactive_session.py`**: Session management for interactive mode
- **`config.py`**: Configuration management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See [DEVELOPER.md](DEVELOPER.md) for detailed development information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- 📖 **Documentation**: Check the docs/ directory
- 🐛 **Issues**: Report bugs on GitHub
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🔧 **Developer Guide**: See [DEVELOPER.md](DEVELOPER.md)

## 📈 Changelog

### v2.0.0 (Enhanced Release)
- ✨ Added interactive mode with Telegram response waiting
- 🔧 Split tools: `your_turn_notify` and `your_turn_interactive`
- 🎵 Embedded sound system with multiple fallbacks
- 🛡️ Improved robustness and error handling
- 📚 Comprehensive documentation
- 🏗️ Modular architecture
- 🔄 Maintained backward compatibility

### v1.1.0
- Added Telegram bot integration
- Improved cross-platform sound support
- Added Docker support
- Enhanced error handling

### v1.0.0
- Initial release
- Basic sound notifications
- MCP protocol support
