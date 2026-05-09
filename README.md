# summarize-meeting

Local pipeline for converting meeting audio into a summary.

## Full Pipeline

Run the entire process (transcription -> summarization -> chronology) using the pipeline script:

```bash
export WHISPER_CPP_DIR=/tmp/whisper.cpp
export LLM_ENDPOINT=http://localhost:8000/v1
export LLM_MODEL=qwen/qwen3.6-27b
export OUTPUT_DIR=/tmp

./bin/pipeline.sh path/to/meeting.wav
```

## Jupyter notebook

1. Open `meeting_summary_pipeline.ipynb` in JupyterLab (Python 3 kernel).
2. Ensure a local OpenAI-compatible API endpoint is running (for example `http://127.0.0.1:8000/v1`).
3. Run all notebook cells.
4. Set `AUDIO_FILE_PATH` to your audio file path and run the pipeline cell.

The notebook will:
- install missing Python packages (`faster-whisper`, `openai`)
- download/load a local Whisper model for speech-to-text
- call a user-configurable local OpenAI endpoint (with configurable model, default `qwen/qwen3.6-27b`)
- produce transcript + meeting summary output

## Quick guide: build whisper.cpp

```bash
cd /tmp
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp

cmake --build build -j --config Release
cmake -B build
```
