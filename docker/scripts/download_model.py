#!/usr/bin/env python3
"""Download and prepare Kokoro v1.0 model."""

import os
import argparse
from urllib.request import urlretrieve
from loguru import logger


def verify_files(model_path: str, config_path: str) -> bool:
    """Check if model and config files exist and are non-empty."""
    return all(os.path.exists(path) and os.path.getsize(path) > 0 for path in [model_path, config_path])


def download_model(output_dir: str) -> None:
    """Download Kokoro model files into given directory."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        model_file = "kokoro-v1_0.pth"
        config_file = "config.json"
        model_path = os.path.join(output_dir, model_file)
        config_path = os.path.join(output_dir, config_file)

        if verify_files(model_path, config_path):
            logger.info("✓ Model files already exist and are valid.")
            return

        logger.info(f"⬇️ Downloading Kokoro model files to: {output_dir}")

        base_url = "https://github.com/remsky/Kokoro-FastAPI/releases/download/v0.1.4"
        urlretrieve(f"{base_url}/{model_file}", model_path)
        logger.info("✓ Downloaded model file")

        urlretrieve(f"{base_url}/{config_file}", config_path)
        logger.info("✓ Downloaded config file")

        if not verify_files(model_path, config_path):
            raise RuntimeError("Model verification failed after download.")

        logger.info(f"✅ Model files ready in: {output_dir}")

    except Exception as e:
        logger.error(f"❌ Model download failed: {e}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    default_dir = os.environ.get("MODEL_DIR", "models/v1_0")
    parser.add_argument("--output", default=default_dir, help="Target directory for model files")

    args = parser.parse_args()

    download_model(args.output)

