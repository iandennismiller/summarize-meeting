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

### Step by step

```bash
# switch to whisper.cpp dir
export GIT_DIR=$PWD
cd $HOME/Work/whisper.cpp

# transcribe audio
$GIT_DIR/bin/transcribe-diarize.sh \
  /tmp/meeting.wav \
  /tmp/transcript

# switch back
cd $GIT_DIR

# virtualenv
workon summarize-meeting

# summarize transcript with LLM
./bin/summarize.py \
  --endpoint "http://llama-api.mgmt/v1" \
  --model "qwen/qwen3.6-27b" \
  --input-file /tmp/transcript.txt \
  --output-file /tmp/summary.txt

# generate chronology of meeting
./bin/chronology.py \
  --endpoint "http://llama-api.mgmt/v1" \
  --model "qwen/qwen3.6-27b" \
  --input-file /tmp/transcript.txt \
  --output-file /tmp/chronology.txt
```

### One-line example

Here's the one-liner I use:

```bash
workon summarize-meeting && WHISPER_CPP_DIR=$HOME/Work/whisper.cpp LLM_ENDPOINT=http://llama-api.mgmt/v1 LLM_MODEL=qwen/qwen3.6-27b OUTPUT_DIR=$PWD/var ./bin/pipeline.sh "audio.wav"
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
