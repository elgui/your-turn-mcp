# AI Context: Your Turn MCP Server – Audio via Telegram + Deepgram

This document provides a clean, actionable reference for coding agents working on the MCP Your Turn server with Telegram audio transcription using Deepgram.

## Overview
- The server notifies users and optionally collects responses via Telegram.
- Now supports audio messages: Telegram audio/voice/doc (audio/*) are downloaded, transcribed with Deepgram STT, and submitted as text answers to the latest active interactive session.

## Key Components
- telegram_notifier.py
  - enable_interactive_mode(): registers handlers for TEXT and audio (AUDIO | VOICE | Document.ALL)
  - _handle_message(): handles text replies
  - NEW _handle_audio_message():
    - downloads file to temp path
    - validates size (AUDIO_MAX_BYTES, default 25 MB)
    - transcribes with Deepgram (model nova-3, smart_format=True)
    - submits transcript via InteractiveSessionManager
- interactive_session.py
  - Session manager used to submit responses
- mcp_your_turn_server.py
  - Boots TelegramNotifier; drives interactive questions and waits for replies

## Dependencies
- python-telegram-bot>=20 (currently 22.x)
- python-dotenv>=1.0.0
- PyYAML>=6.0
- deepgram-sdk (installed for runtime; consider pinning)

Note: We installed deepgram-sdk in a local virtualenv for testing. To ensure reproducibility, consider adding `deepgram-sdk` to requirements.txt.

## Environment Variables
- TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED
- DEEPGRAM_API_KEY – required for STT
- AUDIO_MAX_BYTES – optional size limit in bytes (default 26214400 = 25 MB)

These are loaded by config.py via python-dotenv (see .env).

## Audio Handling
- Accepted Telegram update types:
  - Voice (OGG/Opus)
  - Audio (MP3/M4A/WAV)
  - Document when `mime_type` starts with `audio/`
- File download: `message.voice|audio|document.get_file().download_to_drive(path)`
- Temp file naming preserves extension when available
- Size guard: rejects files larger than AUDIO_MAX_BYTES

## Deepgram STT
- Client: DeepgramClient(api_key)
- Prerecorded transcription (REST): `listen.rest.v("1").transcribe_file(source=..., options=PrerecordedOptions(model="nova-3", smart_format=True))`
- Supported formats include mp3, wav, m4a/aac, ogg/opus – so no conversion is required for common Telegram audio types
- Timeout and threading:
  - The SDK call is executed in a background thread and wrapped with `asyncio.wait_for(..., timeout=45s)` to avoid blocking the event loop

## Error Handling
- Unauthorized chat guarded
- Missing/misconfigured Deepgram -> user sees a helpful error and can type a reply instead
- Empty transcript -> user notified; no submission
- Over-size file -> user notified
- Generic network/Telegram errors logged & messaged

## File Paths to Review
- telegram_notifier.py: _handle_audio_message, _download_telegram_file, _transcribe_with_deepgram
- .env: ensure DEEPGRAM_API_KEY is present
- tests/ok-cool.mp3: sample audio for local tests

## References (Docs)
- python-telegram-bot
  - MessageHandler + filters (text/audio/voice/document)
  - Working with Files: get_file(), download_to_drive()
  - Example: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Working-with-Files-and-Media
- Deepgram Python SDK
  - Synchronous prerecorded: transcribe_file open(file, 'rb') with PrerecordedOptions(model='nova-3')
  - README: https://github.com/deepgram/deepgram-python-sdk#readme

## Testing Notes
- Local scripted test may require internet access; ensure environment allows outbound HTTPS to Deepgram.
- Manual flow:
  1. Start the MCP server with TELEGRAM_* & DEEPGRAM_API_KEY set.
  2. Trigger an interactive question.
  3. Send a voice note/audio in Telegram; confirm transcript is echoed and submitted.

## Future Improvements (Suggestions)
- Optional ffmpeg fallback conversion to 16k mono WAV for rare/unsupported formats
- Add unit/integration tests with mocked Deepgram responses
- Configurable language and model selection
- Rate limiting and backoff for large/slow files
- Persist transcripts/logs behind a debug flag for audits

