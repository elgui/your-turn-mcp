2025-08-09 13:58:40.820 | [DOCKER] Starting MCP Your Turn Server...
2025-08-09 13:58:40.820 | [DOCKER] Container version: 1.1.0
2025-08-09 13:58:40.820 | [DOCKER] Telegram environment variables detected
2025-08-09 13:58:40.820 | [DOCKER] Executing: python3 mcp_your_turn_server.py 
2025-08-09 13:58:41.296 | DEBUG: TELEGRAM_BOT_TOKEN from os.getenv: 8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA
2025-08-09 13:58:41.296 | DEBUG: TELEGRAM_CHAT_ID from os.getenv: 969881075
2025-08-09 13:58:41.868 | 2025-08-09 11:58:41,867 - telegram_notifier - INFO - 🤖 Initializing Telegram notifier...
2025-08-09 13:58:41.953 | 2025-08-09 11:58:41,952 - telegram_notifier - INFO - ✅ Telegram notifier initialized successfully
2025-08-09 13:58:41.953 | [TELEGRAM] Initialized with chat ID: 969881075
2025-08-09 13:58:41.959 | 2025-08-09 11:58:41,959 - __main__ - INFO - 🧾 Raw stdin line: '{"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"augment-mcp-client","version":"1.0.0"}},"jsonrpc":"2.0","id":0}'
2025-08-09 13:58:41.959 | 2025-08-09 11:58:41,959 - __main__ - INFO - 📥 Received request: initialize (ID: 0)
2025-08-09 13:58:41.959 | 2025-08-09 11:58:41,959 - __main__ - INFO - 🔄 Sending response for request ID 0: ...
2025-08-09 13:58:41.959 | 2025-08-09 11:58:41,959 - __main__ - INFO - ✅ Response sent successfully (length: 167 chars)
2025-08-09 13:58:41.959 | 2025-08-09 11:58:41,959 - __main__ - INFO - 🔍 Response ID: 0, Method: initialize
2025-08-09 13:58:41.959 | {"jsonrpc": "2.0", "id": 0, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "your-turn-server", "version": "1.0.0"}}}
2025-08-09 13:58:42.161 | 2025-08-09 11:58:42,160 - __main__ - INFO - 🔄 Ready for next request...
2025-08-09 13:58:42.662 | 2025-08-09 11:58:42,662 - __main__ - INFO - 🧾 Raw stdin line: '{"method":"notifications/initialized","jsonrpc":"2.0"}'
2025-08-09 13:58:42.662 | 2025-08-09 11:58:42,662 - __main__ - INFO - 📥 Received request: notifications/initialized (ID: None)
2025-08-09 13:58:42.662 | 2025-08-09 11:58:42,662 - __main__ - INFO - 🔄 Sending response for request ID None: ...
2025-08-09 13:58:42.662 | 2025-08-09 11:58:42,662 - __main__ - INFO - ✅ Response sent successfully (length: 113 chars)
2025-08-09 13:58:42.662 | 2025-08-09 11:58:42,662 - __main__ - INFO - 🔍 Response ID: None, Method: notifications/initialized
2025-08-09 13:58:42.662 | {"jsonrpc": "2.0", "id": null, "error": {"code": -32601, "message": "Unknown method: notifications/initialized"}}
2025-08-09 13:58:42.864 | 2025-08-09 11:58:42,863 - __main__ - INFO - 🔄 Ready for next request...
2025-08-09 13:58:43.365 | 2025-08-09 11:58:43,365 - __main__ - INFO - 🧾 Raw stdin line: '{"method":"tools/list","jsonrpc":"2.0","id":1}'
2025-08-09 13:58:43.365 | 2025-08-09 11:58:43,365 - __main__ - INFO - 📥 Received request: tools/list (ID: 1)
2025-08-09 13:58:43.365 | 2025-08-09 11:58:43,365 - __main__ - INFO - 🔄 Sending response for request ID 1: ...
2025-08-09 13:58:43.365 | 2025-08-09 11:58:43,365 - __main__ - INFO - ✅ Response sent successfully (length: 559 chars)
2025-08-09 13:58:43.365 | 2025-08-09 11:58:43,365 - __main__ - INFO - 🔍 Response ID: 1, Method: tools/list
2025-08-09 13:58:43.365 | {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "your_turn", "description": "Send notification and wait for user response via Telegram. Plays sound and waits up to timeout_seconds (default 300).", "inputSchema": {"type": "object", "properties": {"reason": {"type": "string", "description": "Optional reason for the notification (e.g., 'mission completed', 'need user input')"}, "timeout_seconds": {"type": "number", "description": "Optional override for wait timeout in seconds (min 10, max 7200). Default 300."}}, "additionalProperties": false}}]}}
2025-08-09 13:58:43.566 | 2025-08-09 11:58:43,566 - __main__ - INFO - 🔄 Ready for next request...
2025-08-09 14:00:16.350 | 2025-08-09 12:00:16,348 - __main__ - INFO - 🧾 Raw stdin line: '{"method":"tools/call","params":{"name":"your_turn","arguments":{"reason":"Testing audio transcription: Please send a voice note or audio file saying \'hello world\' so I can verify the Deepgram integration works correctly","timeout_seconds":180}},"jsonrpc":"2.0","id":2}'
2025-08-09 14:00:16.350 | 2025-08-09 12:00:16,348 - __main__ - INFO - 📥 Received request: tools/call (ID: 2)
2025-08-09 14:00:16.350 | 2025-08-09 12:00:16,348 - __main__ - INFO - 🔔 Your Turn tool called with reason: Testing audio transcription: Please send a voice note or audio file saying 'hello world' so I can verify the Deepgram integration works correctly (timeout_seconds=180)
2025-08-09 14:00:16.350 | 2025-08-09 12:00:16,348 - sound_manager - INFO - 🔊 Starting sound notification on platform: linux
2025-08-09 14:00:16.395 | 🔔 NOTIFICATION: Your turn!
2025-08-09 14:00:16.395 | 2025-08-09 12:00:16,395 - sound_manager - INFO - ✅ ASCII bell fallback used successfully
2025-08-09 14:00:16.395 | 2025-08-09 12:00:16,395 - __main__ - INFO - 🤖 Attempting to get user response via Telegram...
2025-08-09 14:00:16.395 | 2025-08-09 12:00:16,395 - __main__ - INFO - 🔍 Testing Telegram connection...
2025-08-09 14:00:16.653 | 2025-08-09 12:00:16,653 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getMe "HTTP/1.1 200 OK"
2025-08-09 14:00:16.654 | 2025-08-09 12:00:16,654 - telegram_notifier - INFO - ✅ Connected to Telegram bot: @yt_mcp_bot (your-turn)
2025-08-09 14:00:16.654 | 2025-08-09 12:00:16,654 - __main__ - INFO - 🚀 Starting Telegram interactive mode...
2025-08-09 14:00:16.654 | 2025-08-09 12:00:16,654 - __main__ - INFO - 📱 Enabling interactive mode...
2025-08-09 14:00:16.695 | [TELEGRAM] Interactive mode enabled
2025-08-09 14:00:16.695 | 2025-08-09 12:00:16,695 - __main__ - INFO - ✅ Interactive mode enabled
2025-08-09 14:00:16.695 | 2025-08-09 12:00:16,695 - __main__ - INFO - 🔄 Starting interactive polling...
2025-08-09 14:00:16.695 | 2025-08-09 12:00:16,695 - telegram_notifier - INFO - 🔄 Initializing Telegram application...
2025-08-09 14:00:16.871 | 2025-08-09 12:00:16,871 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getMe "HTTP/1.1 200 OK"
2025-08-09 14:00:16.872 | 2025-08-09 12:00:16,872 - telegram_notifier - INFO - ✅ Application initialized
2025-08-09 14:00:16.872 | 2025-08-09 12:00:16,872 - telegram.ext.Application - INFO - Application started
2025-08-09 14:00:16.872 | 2025-08-09 12:00:16,872 - telegram_notifier - INFO - ✅ Application started
2025-08-09 14:00:16.872 | 2025-08-09 12:00:16,872 - telegram_notifier - INFO - 🔄 Starting polling for updates...
2025-08-09 14:00:16.955 | 2025-08-09 12:00:16,955 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/deleteWebhook "HTTP/1.1 200 OK"
2025-08-09 14:00:16.956 | 2025-08-09 12:00:16,956 - telegram_notifier - INFO - ✅ Interactive mode started successfully - now listening for messages!
2025-08-09 14:00:16.956 | [TELEGRAM] 🤖 Telegram bot is now actively listening for your responses
2025-08-09 14:00:16.956 | 2025-08-09 12:00:16,956 - telegram_notifier - INFO - 🔍 Starting connection monitoring...
2025-08-09 14:00:18.959 | 2025-08-09 12:00:18,959 - __main__ - INFO - ✅ Interactive polling started successfully
2025-08-09 14:00:18.959 | 2025-08-09 12:00:18,959 - interactive_session - INFO - Interactive session manager started
2025-08-09 14:00:18.959 | 2025-08-09 12:00:18,959 - interactive_session - INFO - Created interactive session b07d17cf-973e-4c8f-b844-020058557a96
2025-08-09 14:00:19.062 | 2025-08-09 12:00:19,061 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/sendMessage "HTTP/1.1 200 OK"
2025-08-09 14:00:19.063 | [TELEGRAM] Interactive question sent for session b07d17cf-973e-4c8f-b844-020058557a96
2025-08-09 14:00:19.063 | 2025-08-09 12:00:19,063 - __main__ - INFO - ⏳ Waiting for user response (180 seconds max)...
2025-08-09 14:00:19.063 | 2025-08-09 12:00:19,063 - interactive_session - INFO - ⏳ Starting wait for response to session b07d17cf-973e-4c8f-b844-020058557a96
2025-08-09 14:00:21.798 | 2025-08-09 12:00:21,797 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:00:21.804 | 2025-08-09 12:00:21,798 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:00:21.804 | Traceback (most recent call last):
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:00:21.804 |     if not await do_action():
2025-08-09 14:00:21.804 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:00:21.804 |     return action_cb_task.result()
2025-08-09 14:00:21.804 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:00:21.804 |     updates = await self.bot.get_updates(
2025-08-09 14:00:21.804 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:00:21.804 |     updates = await super().get_updates(
2025-08-09 14:00:21.804 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:00:21.804 |     await self._post(
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:00:21.804 |     return await self._do_post(
2025-08-09 14:00:21.804 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:00:21.804 |     return await super()._do_post(
2025-08-09 14:00:21.804 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:00:21.804 |     result = await request.post(
2025-08-09 14:00:21.804 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:00:21.804 |     result = await self._request_wrapper(
2025-08-09 14:00:21.804 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:21.804 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:00:21.804 |     raise exception
2025-08-09 14:00:21.804 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:00:28.761 | 2025-08-09 12:00:28,761 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:00:28.763 | 2025-08-09 12:00:28,762 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:00:28.763 | Traceback (most recent call last):
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:00:28.763 |     if not await do_action():
2025-08-09 14:00:28.763 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:00:28.763 |     return action_cb_task.result()
2025-08-09 14:00:28.763 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:00:28.763 |     updates = await self.bot.get_updates(
2025-08-09 14:00:28.763 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:00:28.763 |     updates = await super().get_updates(
2025-08-09 14:00:28.763 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:00:28.763 |     await self._post(
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:00:28.763 |     return await self._do_post(
2025-08-09 14:00:28.763 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:00:28.763 |     return await super()._do_post(
2025-08-09 14:00:28.763 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:00:28.763 |     result = await request.post(
2025-08-09 14:00:28.763 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:00:28.763 |     result = await self._request_wrapper(
2025-08-09 14:00:28.763 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:28.763 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:00:28.763 |     raise exception
2025-08-09 14:00:28.763 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:00:34.506 | 2025-08-09 12:00:34,506 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:00:34.507 | 2025-08-09 12:00:34,506 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:00:34.507 | Traceback (most recent call last):
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:00:34.507 |     if not await do_action():
2025-08-09 14:00:34.507 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:00:34.507 |     return action_cb_task.result()
2025-08-09 14:00:34.507 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:00:34.507 |     updates = await self.bot.get_updates(
2025-08-09 14:00:34.507 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:00:34.507 |     updates = await super().get_updates(
2025-08-09 14:00:34.507 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:00:34.507 |     await self._post(
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:00:34.507 |     return await self._do_post(
2025-08-09 14:00:34.507 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:00:34.507 |     return await super()._do_post(
2025-08-09 14:00:34.507 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:00:34.507 |     result = await request.post(
2025-08-09 14:00:34.507 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:00:34.507 |     result = await self._request_wrapper(
2025-08-09 14:00:34.507 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:34.507 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:00:34.507 |     raise exception
2025-08-09 14:00:34.507 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:00:43.185 | 2025-08-09 12:00:43,184 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:00:43.185 | 2025-08-09 12:00:43,184 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:00:43.185 | Traceback (most recent call last):
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:00:43.185 |     if not await do_action():
2025-08-09 14:00:43.185 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:00:43.185 |     return action_cb_task.result()
2025-08-09 14:00:43.185 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:00:43.185 |     updates = await self.bot.get_updates(
2025-08-09 14:00:43.185 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:00:43.185 |     updates = await super().get_updates(
2025-08-09 14:00:43.185 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:00:43.185 |     await self._post(
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:00:43.185 |     return await self._do_post(
2025-08-09 14:00:43.185 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:00:43.185 |     return await super()._do_post(
2025-08-09 14:00:43.185 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:00:43.185 |     result = await request.post(
2025-08-09 14:00:43.185 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:00:43.185 |     result = await self._request_wrapper(
2025-08-09 14:00:43.185 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:43.185 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:00:43.185 |     raise exception
2025-08-09 14:00:43.185 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:00:46.959 | 2025-08-09 12:00:46,959 - telegram_notifier - INFO - 🤖 Bot status: Running for 30s, waiting for messages...
2025-08-09 14:00:48.119 | 2025-08-09 12:00:48,119 - interactive_session - INFO - 🔄 Still waiting for session b07d17cf-973e-4c8f-b844-020058557a96 (poll #30, status: waiting)
2025-08-09 14:00:56.446 | 2025-08-09 12:00:56,446 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:00:56.448 | 2025-08-09 12:00:56,447 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:00:56.448 | Traceback (most recent call last):
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:00:56.448 |     if not await do_action():
2025-08-09 14:00:56.448 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:00:56.448 |     return action_cb_task.result()
2025-08-09 14:00:56.448 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:00:56.448 |     updates = await self.bot.get_updates(
2025-08-09 14:00:56.448 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:00:56.448 |     updates = await super().get_updates(
2025-08-09 14:00:56.448 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:00:56.448 |     await self._post(
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:00:56.448 |     return await self._do_post(
2025-08-09 14:00:56.448 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:00:56.448 |     return await super()._do_post(
2025-08-09 14:00:56.448 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:00:56.448 |     result = await request.post(
2025-08-09 14:00:56.448 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:00:56.448 |     result = await self._request_wrapper(
2025-08-09 14:00:56.448 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:00:56.448 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:00:56.448 |     raise exception
2025-08-09 14:00:56.448 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:01:14.241 | 2025-08-09 12:01:14,240 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 200 OK"
2025-08-09 14:01:15.799 | 2025-08-09 12:01:15,799 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:01:15.801 | 2025-08-09 12:01:15,800 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:01:15.801 | Traceback (most recent call last):
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:01:15.801 |     if not await do_action():
2025-08-09 14:01:15.801 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:01:15.801 |     return action_cb_task.result()
2025-08-09 14:01:15.801 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:01:15.801 |     updates = await self.bot.get_updates(
2025-08-09 14:01:15.801 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:01:15.801 |     updates = await super().get_updates(
2025-08-09 14:01:15.801 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:01:15.801 |     await self._post(
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:01:15.801 |     return await self._do_post(
2025-08-09 14:01:15.801 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:01:15.801 |     return await super()._do_post(
2025-08-09 14:01:15.801 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:01:15.801 |     result = await request.post(
2025-08-09 14:01:15.801 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:01:15.801 |     result = await self._request_wrapper(
2025-08-09 14:01:15.801 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:15.801 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:01:15.801 |     raise exception
2025-08-09 14:01:15.801 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:01:16.962 | 2025-08-09 12:01:16,961 - telegram_notifier - INFO - 🤖 Bot status: Running for 30s, waiting for messages...
2025-08-09 14:01:18.177 | 2025-08-09 12:01:18,176 - interactive_session - INFO - 🔄 Still waiting for session b07d17cf-973e-4c8f-b844-020058557a96 (poll #60, status: waiting)
2025-08-09 14:01:22.053 | 2025-08-09 12:01:22,053 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:01:22.055 | 2025-08-09 12:01:22,054 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:01:22.055 | Traceback (most recent call last):
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:01:22.055 |     if not await do_action():
2025-08-09 14:01:22.055 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:01:22.055 |     return action_cb_task.result()
2025-08-09 14:01:22.055 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:01:22.055 |     updates = await self.bot.get_updates(
2025-08-09 14:01:22.055 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:01:22.055 |     updates = await super().get_updates(
2025-08-09 14:01:22.055 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:01:22.055 |     await self._post(
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:01:22.055 |     return await self._do_post(
2025-08-09 14:01:22.055 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:01:22.055 |     return await super()._do_post(
2025-08-09 14:01:22.055 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:01:22.055 |     result = await request.post(
2025-08-09 14:01:22.055 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:01:22.055 |     result = await self._request_wrapper(
2025-08-09 14:01:22.055 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:22.055 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:01:22.055 |     raise exception
2025-08-09 14:01:22.055 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:01:29.741 | 2025-08-09 12:01:29,740 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:01:29.741 | 2025-08-09 12:01:29,741 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:01:29.741 | Traceback (most recent call last):
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:01:29.741 |     if not await do_action():
2025-08-09 14:01:29.741 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:01:29.741 |     return action_cb_task.result()
2025-08-09 14:01:29.741 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:01:29.741 |     updates = await self.bot.get_updates(
2025-08-09 14:01:29.741 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:01:29.741 |     updates = await super().get_updates(
2025-08-09 14:01:29.741 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:01:29.741 |     await self._post(
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:01:29.741 |     return await self._do_post(
2025-08-09 14:01:29.741 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:01:29.741 |     return await super()._do_post(
2025-08-09 14:01:29.741 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:01:29.741 |     result = await request.post(
2025-08-09 14:01:29.741 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:01:29.741 |     result = await self._request_wrapper(
2025-08-09 14:01:29.741 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:29.741 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:01:29.741 |     raise exception
2025-08-09 14:01:29.741 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:01:37.731 | 2025-08-09 12:01:37,731 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:01:37.733 | 2025-08-09 12:01:37,732 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:01:37.733 | Traceback (most recent call last):
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:01:37.733 |     if not await do_action():
2025-08-09 14:01:37.733 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:01:37.733 |     return action_cb_task.result()
2025-08-09 14:01:37.733 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:01:37.733 |     updates = await self.bot.get_updates(
2025-08-09 14:01:37.733 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:01:37.733 |     updates = await super().get_updates(
2025-08-09 14:01:37.733 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:01:37.733 |     await self._post(
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:01:37.733 |     return await self._do_post(
2025-08-09 14:01:37.733 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:01:37.733 |     return await super()._do_post(
2025-08-09 14:01:37.733 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:01:37.733 |     result = await request.post(
2025-08-09 14:01:37.733 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:01:37.733 |     result = await self._request_wrapper(
2025-08-09 14:01:37.733 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:37.733 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:01:37.733 |     raise exception
2025-08-09 14:01:37.733 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
2025-08-09 14:01:46.515 | 2025-08-09 12:01:46,515 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8353655097:AAE3bLkNDaCrzotXNqt-wWYXDWcuIKQehUA/getUpdates "HTTP/1.1 409 Conflict"
2025-08-09 14:01:46.516 | 2025-08-09 12:01:46,515 - telegram.ext.Updater - ERROR - Exception happened while polling for updates.
2025-08-09 14:01:46.516 | Traceback (most recent call last):
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 115, in network_retry_loop
2025-08-09 14:01:46.516 |     if not await do_action():
2025-08-09 14:01:46.516 |            ^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_utils/networkloop.py", line 108, in do_action
2025-08-09 14:01:46.516 |     return action_cb_task.result()
2025-08-09 14:01:46.516 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_updater.py", line 340, in polling_action_cb
2025-08-09 14:01:46.516 |     updates = await self.bot.get_updates(
2025-08-09 14:01:46.516 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 670, in get_updates
2025-08-09 14:01:46.516 |     updates = await super().get_updates(
2025-08-09 14:01:46.516 |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 4611, in get_updates
2025-08-09 14:01:46.516 |     await self._post(
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 698, in _post
2025-08-09 14:01:46.516 |     return await self._do_post(
2025-08-09 14:01:46.516 |            ^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 370, in _do_post
2025-08-09 14:01:46.516 |     return await super()._do_post(
2025-08-09 14:01:46.516 |            ^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/_bot.py", line 727, in _do_post
2025-08-09 14:01:46.516 |     result = await request.post(
2025-08-09 14:01:46.516 |              ^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 197, in post
2025-08-09 14:01:46.516 |     result = await self._request_wrapper(
2025-08-09 14:01:46.516 |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-08-09 14:01:46.516 |   File "/opt/venv/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 374, in _request_wrapper
2025-08-09 14:01:46.516 |     raise exception
2025-08-09 14:01:46.516 | telegram.error.Conflict: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running