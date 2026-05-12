#!/bin/bash
set -e

# --- Defaults & Configuration ---
# These can be overridden by environment variables
AUDIO_FILE="${AUDIO_FILE:-}"
WHISPER_CPP_DIR="${WHISPER_CPP_DIR:-}"
LLM_ENDPOINT="${LLM_ENDPOINT:-http://localhost:8000/v1}"
LLM_MODEL="${LLM_MODEL:-qwen/qwen3.6-27b}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp}"

# Usage help
usage() {
    echo "Usage: $0 [options] <audio_file>"
    echo ""
    echo "Required arguments:"
    echo "  audio_file            Path to the input .wav file"
    echo ""
    echo "Optional environment variables or flags:"
    echo "  WHISPER_CPP_DIR       Path to the whisper.cpp repository (Required if not set)"
    echo "  LLM_ENDPOINT          OpenAI-compatible API URL (Default: $LLM_ENDPOINT)"
    echo "  LLM_MODEL             Model name for the LLM (Default: $LLM_MODEL)"
    echo "  OUTPUT_DIR            Directory to save outputs (Default: $OUTPUT_DIR)"
    echo ""
    echo "Example:"
    echo "  WHISPER_CPP_DIR=~/whisper.cpp ./bin/pipeline.sh meeting.wav"
    exit 1
}

# If no audio file is provided as the first argument, check if AUDIO_FILE env var is set
if [ $# -eq 0 ] && [ -z "$AUDIO_FILE" ]; then
    usage
fi

# Set audio file from argument if provided, otherwise keep the env var
if [ $# -gt 0 ]; then
    AUDIO_FILE="$1"
fi

# Validate required inputs
if [ -z "$WHISPER_CPP_DIR" ]; then
    echo "Error: WHISPER_CPP_DIR environment variable is not set."
    usage
fi

if [ -z "$AUDIO_FILE" ]; then
    echo "Error: Audio file must be specified."
    usage
fi

if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file not found: $AUDIO_FILE"
    exit 1
fi

# Set absolute paths for binaries and outputs
PROJECT_ROOT=$(pwd)
PIPELINE_BIN_DIR="$PROJECT_ROOT/bin"
TRANSCRIPT_FILE="$OUTPUT_DIR/transcript"
SUMMARY_FILE="$OUTPUT_DIR/summary.txt"
CHRONOLOGY_FILE="$OUTPUT_DIR/chronology.txt"

echo "--- Starting Meeting Summary Pipeline ---"
echo "Audio File: $AUDIO_FILE"
echo "Whisper Dir: $WHISPER_CPP_DIR"
echo "LLM Endpoint: $LLM_ENDPOINT"
echo "LLM Model: $LLM_MODEL"
echo "Output Dir: $OUTPUT_DIR"
echo "-----------------------------------------"

# Step 1: Transcription
echo "[1/3] Transcribing audio..."
# Must run from within whisper.cpp root
(
    cd "$WHISPER_CPP_DIR"
    "$PIPELINE_BIN_DIR/transcribe-diarize.sh" "$AUDIO_FILE" "$TRANSCRIPT_FILE"
)

if [ ! -f "${TRANSCRIPT_FILE}.txt" ]; then
    echo "Error: Transcription failed. ${TRANSCRIPT_FILE}.txt was not created."
    exit 1
fi
echo "✓ Transcription complete: ${TRANSCRIPT_FILE}.txt"

# Step 2: Summarization
echo "[2/3] Generating summary..."
"$PIPELINE_BIN_DIR/summarize.py" \
    --endpoint "$LLM_ENDPOINT" \
    --model "$LLM_MODEL" \
    --input-file "${TRANSCRIPT_FILE}.txt" \
    --output-file "$SUMMARY_FILE"

if [ ! -f "$SUMMARY_FILE" ]; then
    echo "Error: Summarization failed."
    exit 1
fi
echo "✓ Summary complete: $SUMMARY_FILE"

# Step 3: Chronology
echo "[3/3] Generating chronology..."
"$PIPELINE_BIN_DIR/chronology.py" \
    --endpoint "$LLM_ENDPOINT" \
    --model "$LLM_MODEL" \
    --input-file "${TRANSCRIPT_FILE}.txt" \
    --output-file "$CHRONOLOGY_FILE"

if [ ! -f "$CHRONOLOGY_FILE" ]; then
    echo "Error: Chronology generation failed."
    exit 1
fi
echo "✓ Chronology complete: $CHRONOLOGY_FILE"

echo "-----------------------------------------"
echo "Pipeline finished successfully!"
echo "Results saved in $OUTPUT_DIR:"
echo "  - Transcript: ${TRANSCRIPT_FILE}.txt"
echo "  - Summary: $SUMMARY_FILE"
echo "  - Chronology: $CHRONOLOGY_FILE"
