# Next Session Prompt: Harden Audio Transcription & Quality Checks

## Context
We have implemented Telegram audio handling in `telegram_notifier.py`:
- Audio/voice/document (audio/*) messages are downloaded to a temp file
- Transcribed via Deepgram STT (model nova-3, smart_format)
- The resulting transcript is submitted as a normal text response to the latest interactive session
- `.env` includes `DEEPGRAM_API_KEY`
- Sample audio exists at `tests/ok-cool.mp3`

Reference docs captured in AI-CONTEXT.md.

## Goals for this session
1) Reliability & Coverage
- Add optional ffmpeg-based fallback conversion to 16kHz mono WAV when Deepgram fails or when MIME type is unknown/non-audio
- Add explicit handling for captions on media (if user adds a caption to audio, include it when posting transcript)
- Add configurable STT options (language, model, diarization toggle, punctuate)

2) Observability & Errors
- Improve logs around download sizes, mime types, and transcription options
- Emit structured error codes and user-friendly messages for common cases (no API, timeout, unsupported format, empty transcript)

3) Tests
- Add unit tests for `_download_telegram_file` (mock PTB File, verify temp path & extension)
- Add tests for size limits and over-limit handling
- Add integration-style test with a mocked Deepgram HTTP layer to return a known transcript

4) Documentation
- Update README sections to include audio support and environment settings
- Document optional ffmpeg requirement & installation guidance

## Constraints
- Keep changes small and focused; no breaking changes to existing message flow
- Maintain async responsiveness (run blocking transcribe in a background executor)
- Preserve safety defaults (size limit, timeouts)

## Concrete tasks
- [ ] Add `ffmpeg` fallback conversion behind a feature flag (AUDIO_CONVERT_FALLBACK=true)
- [ ] Make language/model configurable via env: `DG_MODEL`, `DG_LANGUAGE`, `DG_PUNCTUATE`, `DG_DIARIZE`
- [ ] Add telemetry logs for audio metadata
- [ ] Write unit tests for download / size limit / happy-path transcript submission (mock Deepgram)
- [ ] Update README + AI-CONTEXT with new knobs and fallback behavior

## Pointers
- Core code: `telegram_notifier.py` (search for `_handle_audio_message`, `_transcribe_with_deepgram`)
- Session flow: `interactive_session.py`
- Sample media: `tests/ok-cool.mp3`
- Env: `.env` + `config.py`

## Acceptance
- Audio messages continue to work; if Deepgram fails but ffmpeg fallback succeeds, transcript is submitted
- Tests added and passing locally
- Docs updated to reflect audio support and options
