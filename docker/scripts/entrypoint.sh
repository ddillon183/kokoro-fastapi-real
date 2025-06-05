#!/bin/bash
set -e

# Check if ffmpeg is installed (for verification during deployment)
echo "Checking ffmpeg version..."
ffmpeg -version || { echo "❌ ffmpeg not found"; exit 1; }

# Download model if enabled
if [ "$DOWNLOAD_MODEL" = "true" ]; then
    python download_model.py --output api/src/models/v1_0
fi

# Start FastAPI server on the correct port (8888) and bind to IPv6
exec uvicorn main:app --host 0.0.0.0 --port 8888 --log-level debug


