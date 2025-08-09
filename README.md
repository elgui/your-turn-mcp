# Enhanced MCP Your Turn Server v2.0

A powerful Model Context Protocol (MCP) server that provides notification and interactive communication tools for LLM interactions. Designed specifically for coding agents to signal task completion and gather user feedback.

## 🎯 Purpose

This MCP server serves a unique purpose: **providing "post-instructions" to coding agents**. When an AI coding assistant believes it has completed its mission, it calls the `your_turn` tool to:

1. **Alert the user** that the task appears complete
2. **Gather optional feedback** from the user (with 5-minute timeout)
3. **Provide guidance** for next steps and quality improvements
4. **Encourage reflection** on what was accomplished

The tool acts as a checkpoint, ensuring coding agents don't just finish tasks but also consider documentation, testing, and continuous improvement.

## 🚀 Features

- **🔔 Smart Notifications**: Cross-platform sound notifications with multiple fallback options
- **💬 Interactive Feedback**: Collect user responses via Telegram with 300-second timeout
- **📱 Telegram Integration**: Rich bot notifications with inline keyboard buttons
- **🎵 Embedded Sound**: No external sound file dependencies
- **🐳 Docker Support**: Easy deployment with Docker
- **⚙️ Flexible Configuration**: Environment variables, command-line args, or config files
- **🛡️ Robust Architecture**: Race condition handling and graceful fallbacks
- **📝 Post-Instructions**: Built-in guidance for coding agents

## 🛠️ Tool Available

### `your_turn` - Interactive Notification with Post-Instructions

**The primary tool for coding agents to signal task completion and gather feedback.**

**Parameters**:
- `reason` (optional, string): Reason for the notification (e.g., "Task completed", "Need user input")
- `timeout_seconds` (optional, number): Override wait timeout in seconds (default 300; min 10, max 7200)

**Behavior**:
1. **🔊 Plays notification sound** (cross-platform)
2. **📱 Sends Telegram message** (if configured) with interactive buttons
3. **⏰ Waits up to `timeout_seconds`** for user response
4. **📝 Returns comprehensive message** including:
   - Notification confirmation
   - User response (if provided)
   - **Post-instructions for the coding agent**

**Post-Instructions Message**:
The tool automatically includes guidance for coding agents:
```
It appears that you haven't entirely completed your mission, have you?

Once you have, please update:
- the right 'AI-CONTEXT.md' with tools and documentation data and references, and keep it clean!

And create a well designed, comprehensive prompt for a relevant new session,
referencing files and passing sharp instructions for high quality job

The new session might be about valuable improvements, but because we aim at
developing robust solutions, it might be a better idea to do an honest critic
of what has been accomplished in this session, and plan for a healthy checkup
and quality improvements
```

**Example Usage**:
```json
{
  "name": "your_turn",
  "arguments": {
    "reason": "Completed implementing the new feature"
  }
}

### Suggested usage in MCP coding agents

Use your "your_turn" tool systematically in these situations:
- when you need to ask the user clarification about something, in order to improve the quality of your job
- when you are done with the mission that has been given to you, so that it sends a notification to the user

You should never end a session without calling this tool.

Additional tips:
- Provide a concise `reason` so the human has context
- Adjust `timeout_seconds` for faster feedback loops during development (e.g., 30–90s)
- Prefer composing answers via the Telegram buttons using the YAML templates when wrapping up a session
```
🔔 Notification sent! The user has been alerted.

📝 Reason: Completed implementing the new feature

✅ User Response: "Please add unit tests before finishing"

[Post-instructions message follows...]
```

## 🚀 Quick Start

### Basic Usage (Sound Only)

```bash
python3 mcp_your_turn_server.py
```

This provides sound notifications only. Perfect for local development.

### With Telegram Interactive Features

1. Create a Telegram bot via [@BotFather](https://t.me/botfather)
2. Get your chat ID (see [Telegram Setup Guide](TELEGRAM_INTEGRATION.md))
3. Run with your credentials:

```bash
python3 mcp_your_turn_server.py --telegram-token "YOUR_BOT_TOKEN" --telegram-chat-id "YOUR_CHAT_ID"
```

### Example Usage in Coding Agent

When your coding agent thinks it's done:

```json
{
  "name": "your_turn",
  "arguments": {
    "reason": "Implemented user authentication system with tests"
  }
}
```

**Response with user feedback** (user responds within 5 minutes):
```
🔔 Notification sent! The user has been alerted.

📝 Reason: Implemented user authentication system with tests

✅ User Response: "Great! Please also add rate limiting to the login endpoint"

 It appears that you haven't entirely completed your mission, have you ?

Once you have, please update :

- the right 'AI-CONTEXT.md' with tools and documentation data and references, and keep it clean!

And create a well designed, comprehensive prompt for a relevant new session, referencing files and passing sharp instructions for high quality job

The new session might be about valuable improvements, but because we aim at developing robust solutions, it might be a better idea to do an honest critic of what has been accompilshed in this session, and plan for a healthy checkup and quality improvements
```

**Response with "Send Default Message"** (user clicks the default button):
```
🔔 Notification sent! The user has been alerted.

📝 Reason: Implemented user authentication system with tests

✅ User Response: "📝 Send default message (no user input)"

[...post-instructions continue as above...]
```

**Response without user feedback** (timeout or no Telegram):
```
🔔 Notification sent! The user has been alerted.

📝 Reason: Implemented user authentication system with tests

⏰ No user response received (5 minute timeout)

[...post-instructions continue as above...]
```

## 🏗️ Architecture & Design Patterns

### Robust Response Collection

The server uses several design patterns to ensure reliable user response transmission:

**1. Response Collector Pattern**
- Encapsulates the complex process of collecting user responses
- Handles Telegram setup, session management, and error recovery
- Returns structured `ResponseResult` with metadata

**2. Template Method Pattern**
- Separates response collection from message building
- Allows for consistent message formatting
- Makes the code more maintainable and testable

**3. Race Condition Mitigation**
- Multiple verification points to ensure responses are captured
- Fallback mechanisms when timing issues occur
- Robust session state checking

**4. Observer Pattern (via Telegram)**
- Session manager observes Telegram updates
- Asynchronous response handling
- Clean separation of concerns

### Key Improvements in v2.0

- **🛡️ Race Condition Handling**: Robust mechanisms to prevent lost user responses
- **📊 Structured Results**: `ResponseResult` dataclass for better error handling
- **🔄 Fallback Mechanisms**: Multiple ways to capture user responses
- **📝 Better Logging**: Comprehensive logging for debugging and monitoring
- **🧪 Testable Architecture**: Clean separation allows for comprehensive testing

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

## 💡 Pre-written answers via YAML templates

Define reusable templates and compose them into powerful one-tap answers in `messages.yml`:

```yaml
messages:
  templates:
    finalize_session: |
      ... multi-line markdown ...
    generate_docs: |
      ... multi-line markdown ...
    commit_message: |
      ... conventional commits guidance ...
    next_session_plan: |
      ... detailed checklist for next session ...
    sync_instructions: |
      ... context and methodology to transfer ...

  prewritten:
    - label: "FIN/DOC"
      compose: [finalize_session, generate_docs]
    - label: "DOC/COMMIT/NEXT"
      compose: [generate_docs, commit_message, next_session_plan, sync_instructions]
```

- Labels are concise “codes” summarizing the composed content
- You can also use `use: templateName` or `text:` with raw content
- YAML supports multi-line and markdown safely

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
- ✨ **Interactive Telegram Integration**: Full two-way communication with inline keyboards
- 📱 **Inline Keyboard Buttons**: Quick response options (Complete, Progress, Help, Pause)
- 💬 **Custom Response Support**: Users can type custom answers or use quick buttons
- 🔄 **Real-time Message Updates**: Messages update to show user responses
- 📊 **Advanced Session Management**: Multiple concurrent sessions with timeout handling
- 🔧 **Split Tools**: `your_turn_notify` (simple) and `your_turn_interactive` (advanced)
- 🎵 **Robust Sound System**: 4-tier fallback system with embedded sounds
- 🛡️ **Enhanced Error Handling**: Comprehensive logging and graceful degradation
- 🧪 **Diagnostic Tools**: Built-in testing and troubleshooting utilities
- 📚 **Complete Documentation**: Setup guides, troubleshooting, and API reference
- 🐳 **Docker Support**: Updated container with all new features
- 🏗️ **Modular Architecture**: Clean separation of concerns
- 🔄 **Backward Compatibility**: All existing functionality preserved

### v1.1.0
- Added Telegram bot integration
- Improved cross-platform sound support
- Added Docker support
- Enhanced error handling

### v1.0.0
- Initial release
- Basic sound notifications
- MCP protocol support
