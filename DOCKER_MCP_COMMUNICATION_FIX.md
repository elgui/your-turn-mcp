# Docker MCP Communication Fix - Critical Issue Resolved! 🔧

## 🎯 **Root Cause Identified**

The MCP client is waiting indefinitely because the **Docker container is not running in interactive mode**. MCP protocol requires **stdin/stdout communication**, which needs the `-i` flag in Docker.

## ❌ **What's Wrong**

If you're running Docker like this:
```bash
# WRONG - Missing -i flag
docker run --rm --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server
```

The MCP client **cannot communicate** with the container because stdin is not connected.

## ✅ **Correct Solution**

### **Method 1: Direct Docker Run (RECOMMENDED)**
```bash
# CORRECT - With -i flag for stdin communication
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk" \
  -e TELEGRAM_CHAT_ID="969881075" \
  your-turn-server
```

**Key flags**:
- `-i`: **CRITICAL** - Keeps stdin open for MCP communication
- `--rm`: Removes container when done
- `--network host`: Required for Telegram API access
- **NO `-t` flag**: TTY interferes with JSON-RPC communication

### **Method 2: Docker Compose (UPDATED)**
```bash
# Set environment variables
export TELEGRAM_BOT_TOKEN="7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk"
export TELEGRAM_CHAT_ID="969881075"

# Run with updated Docker Compose
docker-compose --profile telegram up your-turn-telegram
```

The `docker-compose.yml` has been updated with:
```yaml
stdin_open: true    # CRITICAL: Keep stdin open for MCP communication
tty: false          # Don't allocate TTY for MCP (JSON-RPC over stdin/stdout)
```

## 🧪 **Test the Fix**

### **Test 1: Basic MCP Communication**
```bash
# Test that MCP communication works
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | \
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server
```

**Expected output**: JSON response with tools list

### **Test 2: Notification Tool**
```bash
# Test notification tool
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "your_turn_notify", "arguments": {"reason": "Docker test"}}}' | \
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server
```

**Expected output**: JSON response with notification result

### **Test 3: Interactive Tool**
```bash
# Test interactive tool
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "your_turn_interactive", "arguments": {"message": "Test question", "interactive": true, "timeout_seconds": 30}}}' | \
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server
```

**Expected behavior**: 
1. Question sent to Telegram
2. Bot waits for your response
3. JSON response returned with your answer or timeout

## 🔧 **MCP Client Configuration**

Make sure your MCP client configuration uses the correct Docker command:

```json
{
  "mcpServers": {
    "your-turn": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--network", "host",
        "-e", "TELEGRAM_BOT_TOKEN=your_token_here",
        "-e", "TELEGRAM_CHAT_ID=your_chat_id_here",
        "your-turn-server"
      ]
    }
  }
}
```

**Critical points**:
- ✅ Include `-i` flag
- ✅ Include `--network host`
- ✅ Set environment variables
- ❌ **Don't** include `-t` flag
- ❌ **Don't** include `-d` flag (detached mode)

## 🎯 **Why This Fixes the Issue**

### **Before (Broken)**:
1. Docker container starts without `-i` flag
2. stdin is not connected to MCP client
3. Container runs but cannot receive MCP requests
4. MCP client sends request → **gets no response** → waits forever
5. User has to kill container manually

### **After (Fixed)**:
1. Docker container starts with `-i` flag
2. stdin is connected to MCP client
3. Container receives MCP requests via stdin
4. Container processes request and sends response via stdout
5. MCP client receives response immediately ✅

## 📋 **Troubleshooting**

### **If MCP Client Still Hangs**:

1. **Check Docker command has `-i` flag**:
   ```bash
   # Verify your command includes -i
   docker run --rm -i --network host ...
   ```

2. **Test basic communication**:
   ```bash
   # This should return immediately
   echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | \
   docker run --rm -i your-turn-server
   ```

3. **Check for TTY interference**:
   ```bash
   # Make sure you're NOT using -t flag
   # WRONG: docker run -it ...
   # RIGHT: docker run -i ...
   ```

4. **Verify environment variables**:
   ```bash
   # Test with explicit env vars
   docker run --rm -i \
     -e TELEGRAM_BOT_TOKEN="your_token" \
     -e TELEGRAM_CHAT_ID="your_chat_id" \
     your-turn-server
   ```

### **If Telegram Still Doesn't Work**:

1. **Verify network connectivity**:
   ```bash
   docker run --rm --network host your-turn-server --network-test
   ```

2. **Check credentials**:
   - Bot token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
   - Chat ID format: `123456789` or `-123456789`

3. **Test with interactive tool**:
   - Use `your_turn_interactive` instead of `your_turn_notify`
   - Set `"interactive": true` in arguments
   - Check Telegram for the question message

## 🎉 **Expected Results**

After applying this fix:

### **Notification Tool** (`your_turn_notify`):
- ✅ Sends Telegram notification immediately
- ✅ Returns MCP response immediately
- ✅ MCP client receives response and continues

### **Interactive Tool** (`your_turn_interactive`):
- ✅ Sends Telegram question with inline keyboard
- ✅ Bot actively listens for your response
- ✅ When you respond → returns your answer to MCP client
- ✅ MCP client receives response and continues

### **No More Hanging**:
- ✅ MCP client gets responses immediately
- ✅ No need to kill Docker container
- ✅ Proper request/response cycle

## 🚀 **Ready Commands**

```bash
# Build the image
docker build -t your-turn-server .

# Run with notification support (CORRECT WAY)
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server

# Test communication
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | \
docker run --rm -i --network host \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e TELEGRAM_CHAT_ID="your_chat_id" \
  your-turn-server
```

**The `-i` flag is the critical missing piece that fixes the MCP communication issue!** 🎯
