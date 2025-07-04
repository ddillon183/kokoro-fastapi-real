FROM python:3.10

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ffmpeg \
    espeak-ng \
    libsndfile1 \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libswscale-dev \
    libavfilter-dev \
    python3-dev \
    pkg-config \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Link espeak-ng data directory
RUN mkdir -p /usr/share/espeak-ng-data && \
    ln -s /usr/lib/*/espeak-ng-data/* /usr/share/espeak-ng-data/ || true

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/ && \
    mv /root/.local/bin/uvx /usr/local/bin/

# Create app user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

USER appuser
WORKDIR /app

# Copy requirement files and install dependencies
COPY --chown=appuser:appuser requirements.txt requirements.prod.txt ./

# Create virtual environment and install dependencies
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install --no-cache-dir -r requirements.prod.txt

# Copy project components individually to ensure presence
COPY --chown=appuser:appuser api ./api
COPY --chown=appuser:appuser web ./web
COPY --chown=appuser:appuser docker/scripts/entrypoint.sh ./docker/scripts/entrypoint.sh
COPY --chown=appuser:appuser docker/scripts/download_model.py ./docker/scripts/download_model.py
COPY --chown=appuser:appuser docker/scripts/update_requirements.sh ./docker/scripts/update_requirements.sh
COPY --chown=appuser:appuser download_voices.py ./download_voices.py
COPY --chown=appuser:appuser main.py ./main.py
COPY --chown=appuser:appuser models ./models

# Corrected: copy contents inside voices/v1_0 to /app/voices/v1_0
COPY --chown=appuser:appuser voices /app/voices

# Make sure entrypoint and directories are executable
RUN chmod +x ./docker/scripts/entrypoint.sh
RUN chmod -R 755 /app/voices /app/models

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    USE_GPU=false \
    PHONEMIZER_ESPEAK_PATH=/usr/bin \
    PHONEMIZER_ESPEAK_DATA=/usr/share/espeak-ng-data \
    ESPEAK_DATA_PATH=/usr/share/espeak-ng-data \
    PYTHONPATH=/app/api:/app \
    PATH="/app/.venv/bin:$PATH"

# Clean up .pyc etc
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf || true

# Optional: Download model in production if env var is set
RUN if [ "$DOWNLOAD_MODEL" = "true" ]; then \
        python docker/scripts/download_model.py --output models/v1_0; \
    fi

ENTRYPOINT ["bash", "docker/scripts/entrypoint.sh"]



