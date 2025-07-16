# Developer Documentation

This document provides detailed information for developers who want to understand, modify, or contribute to the Enhanced MCP Your Turn Server.

## 🏗️ Architecture Overview

The project is built with a modular architecture that separates concerns and provides robust functionality:

```
Enhanced MCP Your Turn Server
├── mcp_your_turn_server.py     # Main MCP server and tool handlers
├── sound_manager.py            # Cross-platform sound notification system
├── telegram_notifier.py        # Telegram integration with interactive support
├── interactive_session.py      # Session management for interactive mode
└── config.py                   # Configuration management
```

## 📋 Core Components

### 1. MCPServer (`mcp_your_turn_server.py`)

The main server class that implements the Model Context Protocol:

- **Protocol Handling**: Implements MCP 2024-11-05 specification
- **Tool Management**: Handles three tools: `your_turn`, `your_turn_notify`, `your_turn_interactive`
- **Request Routing**: Routes tool calls to appropriate handlers
- **Error Handling**: Comprehensive error handling with proper JSON-RPC responses

**Key Methods**:
- `handle_request()`: Main request dispatcher
- `_handle_notification_tool()`: Handles simple notification tools
- `_handle_interactive_tool()`: Handles interactive sessions
- `play_notification_sound()`: Triggers sound notifications

### 2. SoundManager (`sound_manager.py`)

Robust sound notification system with multiple fallback strategies:

**Fallback Strategy**:
1. Platform-specific system sounds (primary)
2. External sound file (`alert.wav`)
3. Embedded minimal beep sound
4. ASCII bell character (final fallback)

**Key Features**:
- Cross-platform compatibility (Windows, macOS, Linux)
- Embedded sound data to eliminate external dependencies
- Graceful degradation when audio systems are unavailable
- Automatic cleanup of temporary files

### 3. TelegramNotifier (`telegram_notifier.py`)

Enhanced Telegram integration supporting both simple notifications and interactive sessions:

**Features**:
- Simple notification sending
- Interactive question sending
- Message handling for user responses
- Session-aware response processing
- Rich message formatting with Markdown

**Key Methods**:
- `send_notification()`: Send simple notifications
- `send_interactive_question()`: Send interactive questions
- `enable_interactive_mode()`: Enable response handling
- `_handle_message()`: Process incoming user messages

### 4. InteractiveSessionManager (`interactive_session.py`)

Manages interactive sessions where the server waits for user responses:

**Features**:
- Session creation and management
- Timeout handling
- Response processing
- Automatic cleanup of expired sessions
- Thread-safe operations

**Key Classes**:
- `InteractiveSession`: Represents a single interactive session
- `InteractiveSessionManager`: Manages multiple sessions
- `SessionStatus`: Enum for session states

### 5. Configuration (`config.py`)

Handles configuration from multiple sources with proper priority:

1. Environment variables (highest priority)
2. Command-line arguments
3. Configuration files (lowest priority)

## 🔧 Development Setup

### Prerequisites

- Python 3.7+
- Git
- Optional: Docker for containerized development

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd your-turn-mcp
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Install development dependencies**:
   ```bash
   pip install python-telegram-bot python-dotenv pytest pytest-asyncio
   ```

3. **Run tests**:
   ```bash
   python3 -m pytest tests/
   ```

4. **Test individual components**:
   ```bash
   # Test sound manager
   python3 sound_manager.py
   
   # Test interactive session manager
   python3 interactive_session.py
   
   # Test Telegram (requires configuration)
   python3 test_telegram.py
   ```

## 🧪 Testing

### Unit Tests

Create tests in the `tests/` directory:

```python
# tests/test_sound_manager.py
import pytest
from sound_manager import SoundManager

def test_sound_manager_initialization():
    manager = SoundManager()
    assert manager is not None

@pytest.mark.asyncio
async def test_interactive_session():
    from interactive_session import InteractiveSessionManager
    manager = InteractiveSessionManager()
    await manager.start()
    
    session = manager.create_session("Test question")
    assert session.message == "Test question"
    
    await manager.stop()
```

### Integration Tests

Test the full MCP protocol:

```python
# tests/test_mcp_protocol.py
import json
import asyncio
from mcp_your_turn_server import MCPServer

@pytest.mark.asyncio
async def test_mcp_initialize():
    server = MCPServer()
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    }
    
    response = await server.handle_request(request)
    assert response["result"]["protocolVersion"] == "2024-11-05"
```

## 🔌 Adding New Features

### Adding a New Tool

1. **Define the tool schema** in `MCPServer.__init__()`:
   ```python
   "my_new_tool": {
       "name": "my_new_tool",
       "description": "Description of what the tool does",
       "inputSchema": {
           "type": "object",
           "properties": {
               "param1": {
                   "type": "string",
                   "description": "Parameter description"
               }
           },
           "required": ["param1"]
       }
   }
   ```

2. **Add tool handler** in `handle_request()`:
   ```python
   elif tool_name == "my_new_tool":
       return await self._handle_my_new_tool(request, arguments)
   ```

3. **Implement the handler method**:
   ```python
   async def _handle_my_new_tool(self, request: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
       # Tool implementation
       return {
           "jsonrpc": "2.0",
           "id": request.get("id"),
           "result": {
               "content": [{"type": "text", "text": "Tool response"}]
           }
       }
   ```

### Extending Sound Support

Add new sound sources in `SoundManager`:

```python
def _play_custom_sound_source(self) -> bool:
    """Add a new sound source."""
    try:
        # Implementation for new sound source
        return True
    except Exception as e:
        logger.debug(f"Custom sound source failed: {e}")
        return False
```

Update the fallback chain in `play_notification_sound()`.

### Adding New Notification Channels

1. **Create a new notifier class**:
   ```python
   # slack_notifier.py
   class SlackNotifier:
       def __init__(self, webhook_url: str):
           self.webhook_url = webhook_url
       
       async def send_notification(self, message: str) -> bool:
           # Implementation
           pass
   ```

2. **Integrate in the main server**:
   ```python
   # In MCPServer.__init__()
   self.slack_notifier = SlackNotifier(slack_webhook_url)
   
   # In notification handlers
   if self.slack_notifier:
       await self.slack_notifier.send_notification(message)
   ```

## 🐛 Debugging

### Logging

The server uses Python's logging module. Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Import Errors**: Check that all dependencies are installed
2. **Sound Issues**: Test the sound manager independently
3. **Telegram Issues**: Verify bot token and chat ID
4. **MCP Protocol Issues**: Validate JSON-RPC format

### Debug Tools

```bash
# Test MCP protocol manually
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | python3 mcp_your_turn_server.py

# Test with verbose output
python3 -v mcp_your_turn_server.py

# Test individual components
python3 -c "from sound_manager import play_notification_sound; play_notification_sound()"
```

## 📦 Building and Distribution

### Docker Build

```bash
# Build development image
docker build -t your-turn-server:dev .

# Build production image
docker build -t your-turn-server:latest --target production .
```

### Python Package

Create a proper Python package:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="mcp-your-turn-server",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "mcp-your-turn=mcp_your_turn_server:main"
        ]
    }
)
```

## 🔒 Security Considerations

### Telegram Bot Security

- Store bot tokens securely (environment variables, not in code)
- Validate chat IDs to prevent unauthorized access
- Implement rate limiting for interactive sessions
- Sanitize user input in interactive responses

### Input Validation

- Validate all MCP request parameters
- Sanitize file paths and external inputs
- Implement timeout limits for all operations
- Handle malformed JSON gracefully

## 🚀 Performance Optimization

### Async Operations

- Use `asyncio` for all I/O operations
- Implement proper timeout handling
- Use connection pooling for external services
- Cache frequently accessed data

### Memory Management

- Clean up temporary files automatically
- Implement session cleanup for interactive mode
- Use weak references where appropriate
- Monitor memory usage in long-running sessions

## 📚 API Reference

### MCP Protocol Implementation

The server implements MCP protocol version 2024-11-05:

- `initialize`: Server initialization
- `tools/list`: List available tools
- `tools/call`: Execute tool calls

### Tool Schemas

Detailed schemas for all tools are defined in the main server class. Each tool follows the JSON Schema specification for parameter validation.

## 🤝 Contributing Guidelines

1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Documentation**: Update docstrings and documentation
3. **Testing**: Add tests for new features
4. **Backward Compatibility**: Maintain compatibility when possible
5. **Error Handling**: Implement comprehensive error handling

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with detailed description

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.
