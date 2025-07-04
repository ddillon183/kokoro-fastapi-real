#!/bin/bash
set -e

echo "🔍 Checking ffmpeg version..."
ffmpeg -version || { echo "❌ ffmpeg not found"; exit 1; }

echo "🔍 Listing voices in /app/voices/v1_0:"
ls -l /app/voices/v1_0 || echo "❌ voices folder NOT found at /app/voices/v1_0"

export VOICES_DIR=/app/voices/v1_0
echo "📁 Set VOICES_DIR to: $VOICES_DIR"

echo "📦 Using Python: $(which python)"
echo "📦 Using Uvicorn: $(which uvicorn)"

# ✅ Download voices if flag is set
if [ "$DOWNLOAD_VOICES" = "true" ]; then
    echo "⬇️ Downloading voices..."
    /app/.venv/bin/python download_voices.py
    echo "✅ Voices downloaded."
fi

# ✅ Download model if flag is set
if [ "$DOWNLOAD_MODEL" = "true" ]; then
    echo "⬇️ Downloading model..."
    /app/.venv/bin/python docker/scripts/download_model.py --output models/v1_0
    echo "✅ Model downloaded."
fi

echo "🚀 Starting FastAPI server with Gunicorn and 4 workers..."
exec /app/.venv/bin/gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
