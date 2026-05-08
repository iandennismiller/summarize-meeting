# AGENTS.md

## Dependencies
- **whisper.cpp**: External dependency. Must be cloned and built (`cmake --build build`) before running transcription scripts.
- **LLM API**: Requires OpenAI-compatible endpoint (e.g., `http://127.0.0.1:8000/v1`).

## Commands
- **Transcribe**: `bin/transcribe-diarize.sh <audio_file> <output_prefix>` (Note: usually run from within `whisper.cpp` dir).
- **Summarize**: `bin/summarize.py --endpoint <url> --model <model> --input-file <in.txt> --output-file <out.txt>`
- **Chronology**: `bin/chronology.py --endpoint <url> --model <model> --input-file <in.txt> --output-file <out.txt>`

## Workflow
`transcribe-diarize.sh` -> `summarize.py` -> `chronology.py`
