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

# Copy requirement files and install dependencies (use compiled file)
COPY --chown=appuser:appuser docs/requirements.txt ./requirements.txt
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entire project
COPY --chown=appuser:appuser api ./api
COPY --chown=appuser:appuser web ./web
COPY --chown=appuser:appuser docker/scripts/ ./docker/scripts
RUN chmod +x ./docker/scripts/entrypoint.sh

# Set environment variables
# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/api:/app \
    PATH="/app/.venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    USE_GPU=false \
    PHONEMIZER_ESPEAK_PATH=/usr/bin \
    PHONEMIZER_ESPEAK_DATA=/usr/share/espeak-ng-data \
    ESPEAK_DATA_PATH=/usr/share/espeak-ng-data

# Run entrypoint script
ENV DEVICE="cpu"
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf || true
CMD ["./docker/scripts/entrypoint.sh"]
