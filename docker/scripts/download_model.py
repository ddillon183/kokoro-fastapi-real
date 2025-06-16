#!/usr/bin/env python3
"""Download and prepare Kokoro v1.0 model."""

import os
from urllib.request import urlretrieve
from loguru import logger


def verify_files(model_path: str, config_path: str) -> bool:
    """Check if model and config files exist and are non-empty."""
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in [model_path, config_path])


def download_model() -> None:
    """Download Kokoro model files into models/v1_0 directory."""
    try:
        output_dir = "models/v1_0"
        os.makedirs(output_dir, exist_ok=True)

        # Define filenames and paths
        model_file = "kokoro-v1_0.pth"
        config_file = "config.json"
        model_path = os.path.join(output_dir, model_file)
        config_path = os.path.join(output_dir, config_file)

        if verify_files(model_path, config_path):
            logger.info("✓ Model files already exist and are valid.")
            return

        logger.info("⬇️ Downloading Kokoro v1.0 model files...")

        # GitHub release URLs
        base_url = "https://github.com/remsky/Kokoro-FastAPI/releases/download/v0.1.4"
        urlretrieve(f"{base_url}/{model_file}", model_path)
        logger.info("✓ Downloaded model file")

        urlretrieve(f"{base_url}/{config_file}", config_path)
        logger.info("✓ Downloaded config file")

        # Final validation
        if not verify_files(model_path, config_path):
            raise RuntimeError("Model verification failed after download.")

        logger.info(f"✅ Model files ready in: {output_dir}")

    except Exception as e:
        logger.error(f"❌ Model download failed: {e}")
        raise


if __name__ == "__main__":
    download_model()
