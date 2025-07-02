from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from contextlib import asynccontextmanager
import os
import sys
import subprocess

from api.src.core.config import settings
from api.src.routers.debug import router as debug_router
from api.src.routers.openai_compatible import router as openai_router
from api.src.routers.web_player import router as web_router


def setup_logger():
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "<fg #2E8B57>{time:hh:mm:ss A}</fg #2E8B57> | "
                          "{level: <8} | "
                          "<fg #4169E1>{module}:{line}</fg #4169E1> | "
                          "{message}",
                "colorize": True,
                "level": "DEBUG",
            },
        ],
    }
    logger.remove()
    logger.configure(**config)
    logger.level("ERROR", color="<red>")


setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from api.src.inference.model_manager import get_manager
    from api.src.inference.voice_manager import get_manager as get_voice_manager
    from api.src.services.temp_manager import cleanup_temp_files
    import torch

    if os.environ.get("DOWNLOAD_MODEL", "false").lower() == "true":
        logger.info("Downloading model files...")
        result = subprocess.run(["python", "docker/scripts/download_model.py", "--output", "app/models/v1_0"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Model download failed:\n{result.stderr}")
            raise RuntimeError("Model download failed.")
        logger.debug(result.stdout)

    if os.environ.get("DOWNLOAD_VOICES", "false").lower() == "true":
        logger.info("Downloading voice files...")
        result = subprocess.run(["python", "download_voices.py"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Voice download failed:\n{result.stderr}")
            raise RuntimeError("Voice download failed.")
        logger.debug(result.stdout)

    voices_path = settings.voices_dir
    if not os.path.exists(voices_path):
        logger.warning(f"Voices directory missing at {voices_path}. Voice loading may fail.")
    else:
        logger.info(f"Voices directory verified at: {voices_path}")

    await cleanup_temp_files()
    logger.info("Initializing TTS model and voices...")

    try:
        model_manager = await get_manager()
        voice_manager = await get_voice_manager()
        device, model, voicepack_count = await model_manager.initialize_with_warmup(voice_manager)

        banner = (
            "Model Initialized\n"
            f"Model: {model}\n"
            f"Device: {device}\n"
            f"Voice Packs Loaded: {voicepack_count}\n"
        )

        if settings.enable_web_player:
            banner += f"Web Player: http://{settings.host}:{settings.port}/web/"

        logger.info(banner)

    except Exception as e:
        logger.error(f"Failed to initialize model or voices: {e}")
        raise

    yield


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    openapi_url="/openapi.json",
)

if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(openai_router, prefix="/v1")
app.include_router(debug_router)
if settings.enable_web_player:
    app.include_router(web_router, prefix="/web")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/v1/test")
async def test_check():
    return {"status": "ok"}
