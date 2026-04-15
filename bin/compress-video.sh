#!/bin/bash

IN_FILE="$1"
OUT_FILE="$2"

if [ -z "$IN_FILE" ] || [ -z "$OUT_FILE" ]; then
  echo "Usage: $0 <input-audio-file> <output-text-file>"
  exit 1
fi

ffmpeg \
	-i "$IN_FILE" \
	-ar 44100 \
	-b:a 64k \
	-c:v h264_videotoolbox \
	-b:v 200k \
	-vf "scale=-1:720,fps=10" \
	-pix_fmt yuv420p \
	-movflags +faststart \
	"$OUT_FILE"
