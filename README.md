# summarize-meeting

Jupyter-based local pipeline for converting meeting audio into a summary.

## Quick start

1. Open `meeting_summary_pipeline.ipynb` in JupyterLab (Python 3 kernel).
2. Ensure Ollama is installed and running locally.
3. Run all notebook cells.
4. Set `AUDIO_FILE_PATH` to your audio file path and run the pipeline cell.

The notebook will:
- install missing Python packages (`faster-whisper`, `requests`)
- download/load a local Whisper model for speech-to-text
- pull and use `qwen3.5:4b` through Ollama
- produce transcript + meeting summary output
