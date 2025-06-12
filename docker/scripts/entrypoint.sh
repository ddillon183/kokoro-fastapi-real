#!/bin/bash
set -e

# Check if ffmpeg is installed (for verification during deployment)
echo "Checking ffmpeg version..."
ffmpeg -version || { echo "❌ ffmpeg not found"; exit 1; }

# Activate virtual environment
echo "Activating virtual environment..."
source /app/.venv/bin/activate

# Download model if enabled
if [ "$DOWNLOAD_MODEL" = "true" ]; then
    echo "Downloading model..."
    python docker/scripts/download_model.py --output api/src/models/v1_0
fi

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn api.src.main:app --host 0.0.0.0 --port 8888 --loop uvloop --workers 4

