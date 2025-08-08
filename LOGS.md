2025-07-23 21:42:05.036 | [DOCKER] Starting MCP Your Turn Server...
2025-07-23 21:42:05.037 | [DOCKER] Container version: 1.1.0
2025-07-23 21:42:05.037 | [DOCKER] Telegram environment variables detected
2025-07-23 21:42:05.037 | [DOCKER] Executing: python3 mcp_your_turn_server.py 
2025-07-23 21:42:07.746 | DEBUG: TELEGRAM_BOT_TOKEN from os.getenv: 7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk
2025-07-23 21:42:07.747 | DEBUG: TELEGRAM_CHAT_ID from os.getenv: 969881075
2025-07-23 21:42:08.812 | 2025-07-23 18:42:08,812 - telegram_notifier - INFO - 🤖 Initializing Telegram notifier...
2025-07-23 21:42:09.039 | 2025-07-23 18:42:09,039 - telegram_notifier - INFO - ✅ Telegram notifier initialized successfully
2025-07-23 21:42:09.039 | [TELEGRAM] Initialized with chat ID: 969881075
2025-07-23 21:42:09.077 | {"jsonrpc": "2.0", "id": 0, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "your-turn-server", "version": "1.0.0"}}}
2025-07-23 21:42:09.133 | {"jsonrpc": "2.0", "id": null, "error": {"code": -32601, "message": "Unknown method: notifications/initialized"}}
2025-07-23 21:42:09.133 | {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "your_turn", "description": "Send notification and wait for user response via Telegram. Plays sound and waits 300 seconds for user response.", "inputSchema": {"type": "object", "properties": {"reason": {"type": "string", "description": "Optional reason for the notification (e.g., 'mission completed', 'need user input')"}}, "additionalProperties": false}}]}}
2025-07-23 23:11:14.872 | 2025-07-23 20:11:14,860 - __main__ - INFO - 🔔 Your Turn tool called with reason: Need to test the real strategy agent tool but want to check if Django setup is needed first
2025-07-23 23:11:14.873 | 2025-07-23 20:11:14,873 - sound_manager - INFO - 🔊 Starting sound notification on platform: linux
2025-07-23 23:11:15.101 | 🔔 NOTIFICATION: Your turn!
2025-07-23 23:11:15.101 | 2025-07-23 20:11:15,101 - sound_manager - INFO - ✅ ASCII bell fallback used successfully
2025-07-23 23:11:15.101 | 2025-07-23 20:11:15,101 - __main__ - INFO - 🤖 Attempting to get user response via Telegram...
2025-07-23 23:11:15.101 | 2025-07-23 20:11:15,101 - __main__ - INFO - 🔍 Testing Telegram connection...
2025-07-23 23:11:15.546 | 2025-07-23 20:11:15,546 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getMe "HTTP/1.1 200 OK"
2025-07-23 23:11:15.551 | 2025-07-23 20:11:15,551 - telegram_notifier - INFO - ✅ Connected to Telegram bot: @MCP_guibot (MCP-bot)
2025-07-23 23:11:15.551 | 2025-07-23 20:11:15,551 - __main__ - INFO - 🚀 Starting Telegram interactive mode...
2025-07-23 23:11:15.551 | 2025-07-23 20:11:15,551 - __main__ - INFO - 📱 Enabling interactive mode...
2025-07-23 23:11:15.607 | [TELEGRAM] Interactive mode enabled
2025-07-23 23:11:15.607 | 2025-07-23 20:11:15,607 - __main__ - INFO - ✅ Interactive mode enabled
2025-07-23 23:11:15.608 | 2025-07-23 20:11:15,607 - __main__ - INFO - 🔄 Starting interactive polling...
2025-07-23 23:11:15.608 | 2025-07-23 20:11:15,607 - telegram_notifier - INFO - 🔄 Initializing Telegram application...
2025-07-23 23:11:15.776 | 2025-07-23 20:11:15,776 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getMe "HTTP/1.1 200 OK"
2025-07-23 23:11:15.778 | 2025-07-23 20:11:15,778 - telegram_notifier - INFO - ✅ Application initialized
2025-07-23 23:11:15.779 | 2025-07-23 20:11:15,779 - telegram.ext.Application - INFO - Application started
2025-07-23 23:11:15.779 | 2025-07-23 20:11:15,779 - telegram_notifier - INFO - ✅ Application started
2025-07-23 23:11:15.779 | 2025-07-23 20:11:15,779 - telegram_notifier - INFO - 🔄 Starting polling for updates...
2025-07-23 23:11:15.837 | 2025-07-23 20:11:15,837 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/deleteWebhook "HTTP/1.1 200 OK"
2025-07-23 23:11:15.839 | 2025-07-23 20:11:15,838 - telegram_notifier - INFO - ✅ Interactive mode started successfully - now listening for messages!
2025-07-23 23:11:15.839 | [TELEGRAM] 🤖 Telegram bot is now actively listening for your responses
2025-07-23 23:11:15.839 | 2025-07-23 20:11:15,839 - telegram_notifier - INFO - 🔍 Starting connection monitoring...
2025-07-23 23:11:17.846 | 2025-07-23 20:11:17,846 - __main__ - INFO - ✅ Interactive polling started successfully
2025-07-23 23:11:17.848 | 2025-07-23 20:11:17,847 - interactive_session - INFO - Interactive session manager started
2025-07-23 23:11:17.849 | 2025-07-23 20:11:17,849 - interactive_session - INFO - Created interactive session f1e05dcb-4b69-4d4d-b752-6944c9de214c
2025-07-23 23:11:17.969 | 2025-07-23 20:11:17,969 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/sendMessage "HTTP/1.1 200 OK"
2025-07-23 23:11:17.973 | [TELEGRAM] Interactive question sent for session f1e05dcb-4b69-4d4d-b752-6944c9de214c
2025-07-23 23:11:17.973 | 2025-07-23 20:11:17,973 - __main__ - INFO - ⏳ Waiting for user response (300 seconds max)...
2025-07-23 23:11:17.973 | 2025-07-23 20:11:17,973 - interactive_session - INFO - ⏳ Starting wait for response to session f1e05dcb-4b69-4d4d-b752-6944c9de214c
2025-07-23 23:11:26.236 | 2025-07-23 20:11:26,233 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:11:36.884 | 2025-07-23 20:11:36,884 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:11:37.114 | 2025-07-23 20:11:37,114 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/answerCallbackQuery "HTTP/1.1 200 OK"
2025-07-23 23:11:37.115 | 2025-07-23 20:11:37,115 - telegram_notifier - INFO - 🔘 Received button click from user Unknown (969881075) in chat 969881075: 'response:f1e05dcb-4b69-4d4d-b752-6944c9de214c:default'
2025-07-23 23:11:37.115 | 2025-07-23 20:11:37,115 - telegram_notifier - INFO - 🎯 Processing quick response: default for session f1e05dcb-4b69-4d4d-b752-6944c9de214c
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,115 - telegram_notifier - INFO - 📝 Quick response mapped: default -> '📝 Send default message (no user input)'
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,115 - telegram_notifier - INFO - 🔍 Submitting quick response to session f1e05dcb-4b69-4d4d-b752-6944c9de214c: '📝 Send default message (no user input)'
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,115 - interactive_session - INFO - 📥 Attempting to submit response for session f1e05dcb-4b69-4d4d-b752-6944c9de214c: '📝 Send default message (no user input)'
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,116 - interactive_session - INFO - ✅ Response submitted for session f1e05dcb-4b69-4d4d-b752-6944c9de214c (status changed from waiting to completed)
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,116 - telegram_notifier - INFO - ✅ Quick response successfully submitted for session f1e05dcb-4b69-4d4d-b752-6944c9de214c: 📝 Send default message (no user input)
2025-07-23 23:11:37.116 | 2025-07-23 20:11:37,116 - telegram_notifier - INFO - 🔄 Updating message to show response...
2025-07-23 23:11:37.192 | 2025-07-23 20:11:37,191 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/editMessageText "HTTP/1.1 200 OK"
2025-07-23 23:11:37.193 | 2025-07-23 20:11:37,193 - telegram_notifier - INFO - ✅ Message updated successfully
2025-07-23 23:11:38.041 | 2025-07-23 20:11:38,040 - interactive_session - INFO - ✅ Session f1e05dcb-4b69-4d4d-b752-6944c9de214c completed with response: '📝 Send default message (no user input)' (after 21 polls)
2025-07-23 23:11:38.041 | 2025-07-23 20:11:38,040 - __main__ - INFO - ✅ User response received: '📝 Send default message (no user input)'
2025-07-23 23:11:38.042 | 2025-07-23 20:11:38,040 - __main__ - INFO - 📤 Returning response (user_response: True)
2025-07-23 23:11:38.043 | {"jsonrpc": "2.0", "id": 2, "result": {"content": [{"type": "text", "text": "\ud83d\udd14 Notification sent! The user has been alerted.\n\n\ud83d\udcdd Reason: Need to test the real strategy agent tool but want to check if Django setup is needed first\n\n\u2705 User Response: \"\ud83d\udcdd Send default message (no user input)\"\n\n It appears that you haven't entirely completed your mission, have you ?\n\nOnce you have, please update : \n\n- the right 'AI-CONTEXT.md' with tools and documentation data and references, and keep it clean!\n\nAnd create a well designed, comprehensive prompt for a relevant new session, referencing files and passing sharp instructions for high quality job\n\nThe new session might be about valuable improvements, but because we aim at developing robust solutions, it might be a better idea to do an honest critic of what has been accompilshed in this session, and plan for a healthy checkup and quality improvements"}]}}
2025-07-23 23:11:48.237 | 2025-07-23 20:11:48,235 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:11:59.456 | 2025-07-23 20:11:59,455 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:12:10.662 | 2025-07-23 20:12:10,662 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:12:15.861 | 2025-07-23 20:12:15,860 - telegram_notifier - INFO - 🤖 Bot status: Running for 39s, waiting for messages...
2025-07-23 23:12:21.930 | 2025-07-23 20:12:21,929 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:12:33.088 | 2025-07-23 20:12:33,088 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:12:44.256 | 2025-07-23 20:12:44,255 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:12:45.863 | 2025-07-23 20:12:45,862 - telegram_notifier - INFO - 🤖 Bot status: Running for 30s, waiting for messages...
2025-07-23 23:12:55.426 | 2025-07-23 20:12:55,426 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:13:06.512 | 2025-07-23 20:13:06,512 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"
2025-07-23 23:13:15.875 | 2025-07-23 20:13:15,873 - telegram_notifier - INFO - 🤖 Bot status: Running for 30s, waiting for messages...
2025-07-23 23:13:17.738 | 2025-07-23 20:13:17,738 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot7574559697:AAHoYyVRp1KbF-yoc19X4m9r7Qa4GrCSYFk/getUpdates "HTTP/1.1 200 OK"