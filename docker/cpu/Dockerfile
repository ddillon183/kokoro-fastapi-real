FROM python:3.10-slim

# Install system dependencies and check espeak location
RUN apt-get update && apt-get install -y \
    espeak-ng \
    espeak-ng-data \
    git \
    libsndfile1 \
    curl \
    ffmpeg \
    g++ \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* \
&& mkdir -p /usr/share/espeak-ng-data \
&& ln -s /usr/lib/*/espeak-ng-data/* /usr/share/espeak-ng-data/

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/ && \
    mv /root/.local/bin/uvx /usr/local/bin/

# Create non-root user and set permissions
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/api/src/models/v1_0 && \
    chown -R appuser:appuser /app

USER appuser
WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=appuser:appuser docker/cpu/requirements.txt ./requirements.txt
RUN python -m venv .venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser api ./api
COPY --chown=appuser:appuser web ./web
COPY --chown=appuser:appuser docker/scripts/ ./

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Install Rust (required for certain dependencies like pyopenjtalk)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/home/appuser/.cargo/bin:$PATH"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/api/src \
    PATH="/app/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    USE_GPU=false \
    PHONEMIZER_ESPEAK_PATH=/usr/bin \
    PHONEMIZER_ESPEAK_DATA=/usr/share/espeak-ng-data \
    ESPEAK_DATA_PATH=/usr/share/espeak-ng-data \
    DEVICE=cpu \
    DOWNLOAD_MODEL=true

# Download model if enabled
RUN if [ "$DOWNLOAD_MODEL" = "true" ]; then \
    python docker/scripts/download_model.py --output api/src/models/v1_0 || echo "Model download failed"; \
fi

# Start server
CMD ["./entrypoint.sh"]


