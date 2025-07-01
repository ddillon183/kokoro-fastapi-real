#!/bin/bash
set -e

echo "🔍 Checking ffmpeg version..."
ffmpeg -version || { echo "❌ ffmpeg not found"; exit 1; }

echo "🔍 Listing voices in /app/voices/v1_0:"
ls -l /app/voices/v1_0 || echo "❌ voices folder NOT found at /app/voices/v1_0"

echo "📦 Using Python from venv: $(realpath /app/.venv/bin/python)"
echo "📦 Using Uvicorn from venv: $(realpath /app/.venv/bin/uvicorn)"

# ✅ Set environment variable so the app uses the correct voice path
export VOICES_DIR=/app/voices/v1_0
echo "📁 Set VOICES_DIR to: $VOICES_DIR"

# Download model if enabled
if [ "$DOWNLOAD_MODEL" = "true" ]; then
    echo "⬇️ Downloading model..."
    /app/.venv/bin/python docker/scripts/download_model.py --output api/src/models/v1_0
fi

echo "🚀 Starting FastAPI server..."
/app/.venv/bin/uvicorn api.src.main:app --host 0.0.0.0 --port 8888 --loop uvloop --workers 4



