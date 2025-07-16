# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Enhanced MCP Your Turn Server, particularly with sound notifications and Telegram functionality.

## 🔍 Quick Diagnostic

Run the diagnostic tool to automatically check your setup:

```bash
python3 diagnostic_tool.py
```

This will test all components and provide specific recommendations.

## 🔊 Sound Issues

### Sound Not Playing

**Symptoms**: No sound when notifications are triggered

**Diagnosis Steps**:

1. **Test sound manager directly**:
   ```bash
   python3 -c "from sound_manager import play_notification_sound; play_notification_sound()"
   ```

2. **Check platform-specific requirements**:

   **Windows**:
   - Ensure `winsound` module is available (built-in with Python)
   - Check system volume settings
   - Test: `python3 -c "import winsound; winsound.Beep(800, 500)"`

   **macOS**:
   - Ensure `afplay` command is available: `which afplay`
   - Check system sound files exist: `ls /System/Library/Sounds/`
   - Test: `afplay /System/Library/Sounds/Ping.aiff`

   **Linux**:
   - Install audio utilities: `sudo apt-get install alsa-utils pulseaudio-utils`
   - Test PulseAudio: `paplay /usr/share/sounds/alsa/Front_Left.wav`
   - Test ALSA: `aplay /usr/share/sounds/alsa/Front_Left.wav`

3. **Enable debug logging**:
   ```bash
   PYTHONPATH=. python3 -c "
   import logging
   logging.basicConfig(level=logging.DEBUG)
   from sound_manager import play_notification_sound
   play_notification_sound()
   "
   ```

**Common Solutions**:

- **No audio system**: The ASCII bell fallback should still work
- **Missing sound files**: The embedded sound fallback should work
- **Permission issues**: Run with appropriate user permissions
- **Audio server not running**: Start PulseAudio/ALSA on Linux

### Sound Fallback Chain

The system tries these methods in order:

1. **Platform-specific system sounds** (primary)
2. **External sound file** (`alert.wav`)
3. **Embedded minimal beep** (base64 encoded)
4. **ASCII bell character** (final fallback)

Each failure is logged with specific error messages.

## 🤖 Telegram Issues

### Telegram Not Working

**Symptoms**: No Telegram notifications sent, error messages in logs

**Diagnosis Steps**:

1. **Check environment variables**:
   ```bash
   echo "Bot Token: $TELEGRAM_BOT_TOKEN"
   echo "Chat ID: $TELEGRAM_CHAT_ID"
   ```

2. **Validate credentials format**:
   - Bot token should look like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - Chat ID should be a number: `123456789` or `-123456789`

3. **Test Telegram connection**:
   ```bash
   python3 -c "
   import asyncio
   import os
   from telegram import Bot
   
   async def test():
       bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
       me = await bot.get_me()
       print(f'Connected to: @{me.username}')
   
   asyncio.run(test())
   "
   ```

4. **Test notification sending**:
   ```bash
   python3 test_telegram.py
   ```

**Common Issues and Solutions**:

### "Unauthorized" Error
- **Cause**: Invalid or expired bot token
- **Solution**: 
  1. Get a new token from [@BotFather](https://t.me/botfather)
  2. Update `TELEGRAM_BOT_TOKEN` environment variable

### "Chat not found" Error
- **Cause**: Invalid chat ID or bot hasn't been messaged
- **Solution**:
  1. Send a message to your bot first
  2. Use the correct chat ID (check bot logs or use [@userinfobot](https://t.me/userinfobot))

### Network/Timeout Errors
- **Cause**: Internet connectivity issues
- **Solutions**:
  - Check internet connection
  - Try again later
  - Check if Telegram is blocked in your region

### "python-telegram-bot not installed"
- **Solution**: `pip install python-telegram-bot`

## 🔧 Environment Variable Issues

### Variables Not Being Read

**Check loading order** (highest to lowest priority):
1. Environment variables
2. Command-line arguments
3. Config file

**Debug environment loading**:
```bash
python3 -c "
import os
from config import config
print('Environment variables:')
print(f'  TELEGRAM_BOT_TOKEN: {os.getenv(\"TELEGRAM_BOT_TOKEN\")}')
print(f'  TELEGRAM_CHAT_ID: {os.getenv(\"TELEGRAM_CHAT_ID\")}')
print('Config object:')
print(f'  telegram_bot_token: {config.telegram_bot_token}')
print(f'  telegram_chat_id: {config.telegram_chat_id}')
print(f'  telegram_configured: {config.telegram_configured}')
"
```

### Setting Environment Variables

**Linux/macOS**:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
python3 mcp_your_turn_server.py
```

**Windows Command Prompt**:
```cmd
set TELEGRAM_BOT_TOKEN=your_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
python mcp_your_turn_server.py
```

**Windows PowerShell**:
```powershell
$env:TELEGRAM_BOT_TOKEN="your_token_here"
$env:TELEGRAM_CHAT_ID="your_chat_id_here"
python mcp_your_turn_server.py
```

**Using .env file**:
Create a `.env` file in the project directory:
```
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 🖥️ MCP Server Issues

### Server Not Starting

**Check Python version**: Requires Python 3.7+
```bash
python3 --version
```

**Check imports**:
```bash
python3 -c "
try:
    from mcp_your_turn_server import MCPServer
    print('✅ Server imports successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
"
```

### Tools Not Working

**Test tool availability**:
```bash
python3 test_enhanced_server.py
```

**Check tool schemas**:
```bash
python3 -c "
from mcp_your_turn_server import MCPServer
server = MCPServer()
for name, tool in server.tools.items():
    print(f'{name}: {tool[\"description\"]}')
"
```

## 📊 Logging and Debugging

### Enable Debug Logging

**Method 1**: Environment variable
```bash
export PYTHONPATH=.
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Your test code here
"
```

**Method 2**: In code
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Log Locations

- **Server logs**: stderr (visible in terminal)
- **Sound manager logs**: Uses Python logging
- **Telegram logs**: Uses Python logging
- **MCP protocol**: stdout/stdin (don't interfere)

### Common Log Messages

**Sound System**:
- `🔊 Starting sound notification on platform: darwin`
- `✅ Played system sound successfully`
- `❌ System sound failed, trying next strategy...`

**Telegram**:
- `🤖 Initializing Telegram notifier...`
- `✅ Connected to Telegram bot: @your_bot_name`
- `📤 Sending Telegram notification...`
- `🔐 Telegram authorization error`

## 🚀 Performance Issues

### Slow Notifications

**Causes**:
- Network timeouts (Telegram)
- Audio system delays
- Resource constraints

**Solutions**:
- Reduce timeout values
- Use faster audio methods
- Check system resources

### Memory Issues

**Monitor memory usage**:
```bash
python3 -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

**Clean up resources**:
- Temporary sound files are auto-cleaned
- Telegram connections are properly closed
- Interactive sessions have timeouts

## 🔄 Recovery Procedures

### Reset Configuration

1. **Clear environment variables**:
   ```bash
   unset TELEGRAM_BOT_TOKEN
   unset TELEGRAM_CHAT_ID
   ```

2. **Remove temporary files**:
   ```bash
   rm -f /tmp/tmp*.wav  # Temporary sound files
   ```

3. **Restart with clean state**:
   ```bash
   python3 mcp_your_turn_server.py
   ```

### Factory Reset

1. **Backup current configuration**
2. **Remove all custom settings**
3. **Reinstall dependencies**:
   ```bash
   pip uninstall python-telegram-bot python-dotenv
   pip install python-telegram-bot python-dotenv
   ```
4. **Reconfigure from scratch**

## 📞 Getting Help

### Before Asking for Help

1. **Run the diagnostic tool**: `python3 diagnostic_tool.py`
2. **Check this troubleshooting guide**
3. **Enable debug logging**
4. **Collect error messages**

### Information to Include

- Operating system and version
- Python version
- Error messages (full traceback)
- Environment variable status
- Diagnostic tool output

### Support Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and help
- **Documentation**: Check README.md and DEVELOPER.md

## 🔧 Advanced Debugging

### Custom Sound Testing

```python
from sound_manager import SoundManager
import logging

logging.basicConfig(level=logging.DEBUG)
manager = SoundManager()

# Test each strategy individually
print("Testing system sound:", manager._play_system_sound())
print("Testing external sound:", manager._play_external_sound())
print("Testing embedded sound:", manager._play_embedded_sound())
print("Testing ASCII bell:", manager._play_ascii_bell())
```

### Custom Telegram Testing

```python
import asyncio
import os
from telegram_notifier import TelegramNotifier

async def test_telegram():
    notifier = TelegramNotifier(
        os.getenv('TELEGRAM_BOT_TOKEN'),
        os.getenv('TELEGRAM_CHAT_ID')
    )
    
    if notifier.is_enabled():
        success = await notifier.send_notification("Test message")
        print(f"Notification sent: {success}")
    else:
        print("Telegram not enabled")

asyncio.run(test_telegram())
```

This troubleshooting guide should help you resolve most common issues. If you're still having problems, please run the diagnostic tool and include its output when seeking help.
