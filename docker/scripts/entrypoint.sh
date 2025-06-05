#!/bin/bash
set -e

# Check if ffmpeg is installed
echo "Checking ffmpeg version..."
ffmpeg -version || { echo "❌ ffmpeg not found"; exit 1; }

# Download model if enabled
if [ "$DOWNLOAD_MODEL" = "true" ]; then
    python docker/scripts/download_model.py --output api/src/models/v1_0
fi

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8888 --loop uvloop --workers 4
