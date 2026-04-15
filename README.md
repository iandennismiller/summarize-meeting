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
# convert audio file as needed
ffmpeg -i in.mp4 /tmp/in.wav

# switch to whisper.cpp path
cd ~/Work/whisper.cpp

# transcribe audio with whisper.cpp
~/Work/summarize-meeting/bin/transcribe.sh \
    /tmp/in.wav \
    /tmp/meeting-transcript

# summarize transcript with LLM
~/Work/summarize-meeting/bin/summarize.py \
    --endpoint http://llama-api.mgmt/v1 \
    --model google/gemma4-26b-a4b \
    --input-file /tmp/meeting.txt \
    --output-file /tmp/summary.txt
```
