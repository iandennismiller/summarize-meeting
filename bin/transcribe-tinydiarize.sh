#!/bin/bash

MODEL_FILE=models/ggml-small.en-tdrz.bin

IN_FILE="$1"
OUT_FILE="$2"

if [ -z "$IN_FILE" ] || [ -z "$OUT_FILE" ]; then
  echo "Usage: $0 <input-audio-file> <output-text-file>"
  exit 1
fi

if [ ! -d "models" ]; then
  echo "Models directory not found. Please run this script from the root of the whisper.cpp repository."
  exit 1
fi

if [ ! -f "$MODEL_FILE" ]; then
  echo "Model file not found: $MODEL_FILE"
  wget https://huggingface.co/akashmjn/tinydiarize-whisper.cpp/resolve/main/ggml-small.en-tdrz.bin
      echo "Model downloaded"
fi

./build/bin/whisper-cli \
    --tinydiarize \
    --model "$MODEL_FILE" \
    --file "$IN_FILE" \
    --output-txt \
    --no-prints \
    --print-colors \
    --output-file "$OUT_FILE"
