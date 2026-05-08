# summarize-meeting

Jupyter-based local pipeline for converting meeting audio into a summary.

## Quick start

1. Open `meeting_summary_pipeline.ipynb` in JupyterLab (Python 3 kernel).
2. Ensure a local OpenAI-compatible API endpoint is running (for example `http://127.0.0.1:8000/v1`).
3. Run all notebook cells.
4. Set `AUDIO_FILE_PATH` to your audio file path and run the pipeline cell.

The notebook will:
- install missing Python packages (`faster-whisper`, `openai`)
- download/load a local Whisper model for speech-to-text
- call a user-configurable local OpenAI endpoint (with configurable model, default `qwen3.5:4b`)
- produce transcript + meeting summary output

## Script method

```bash
# configure locations and model

export GIT_REPO=$HOME/Work/summarize-meeting
export LLAMA_API=http://llama-api.mgmt/v1
export LLAMA_MODEL=qwen/qwen3.6-27b

# switch to whisper.cpp path, then transcribe audio with whisper.cpp
# the .txt extension is automatically added to to yield `transcript.txt`

cd ~/Work/whisper.cpp

"$GIT_REPO"/bin/transcribe-diarize.sh \
    /tmp/meeting.wav \
    /tmp/transcript

# summarize transcript with LLM

"$GIT_REPO"/bin/summarize.py \
    --endpoint "$LLAMA_API" \
    --model "$LLAMA_MODEL" \
    --input-file /tmp/transcript.txt \
    --output-file /tmp/summary.txt

# generate chronology of meeting

"$GIT_REPO"/bin/chronology.py \
    --endpoint "$LLAMA_API" \
    --model "$LLAMA_MODEL" \
    --input-file /tmp/transcript.txt \
    --output-file /tmp/chronology.txt
```

## quick guide: build whisper.cpp

```bash
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp

cmake --build build -j --config Release
cmake -B build
```
