"""Kokoro V1 model management."""

from typing import Optional
import os
import time
from loguru import logger

from api.src.core import paths
from api.src.core.config import settings
from api.src.core.model_config import ModelConfig, model_config
from api.src.inference.base import BaseModelBackend
from api.src.inference.kokoro_v1 import KokoroV1


class ModelManager:
    """Manages Kokoro V1 model loading and inference."""

    # Singleton instance
    _instance = None

    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize manager.

        Args:
            config: Optional model configuration override
        """
        self._config = config or model_config
        self._backend: Optional[KokoroV1] = None
        self._device: Optional[str] = None

    def _determine_device(self) -> str:
        """Determine device based on settings."""
        return "cuda" if settings.use_gpu else "cpu"

    async def initialize(self) -> None:
        """Initialize Kokoro V1 backend."""
        try:
            self._device = self._determine_device()
            logger.info(f"Initializing Kokoro V1 on {self._device}")
            self._backend = KokoroV1()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Kokoro V1: {e}")

    async def initialize_with_warmup(self, voice_manager) -> tuple[str, str, int]:
        """Initialize and warm up model.

        Args:
            voice_manager: Voice manager instance for warmup

        Returns:
            Tuple of (device, backend type, voice count)

        Raises:
            RuntimeError: If initialization fails
        """
        start = time.perf_counter()

        try:
            # Initialize backend
            await self.initialize()

            # Load model with wait logic
            model_path = self._config.pytorch_kokoro_v1_file

            wait_time = 10
            while not os.path.exists(model_path) and wait_time > 0:
                logger.warning(f"Waiting for model file to exist at {model_path}... ({wait_time}s remaining)")
                time.sleep(1)
                wait_time -= 1

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file still not found after wait: {model_path}")

            await self.load_model(model_path)

            # Load voices
            try:
                voices = await paths.list_voices()
                voice_path = await paths.get_voice_path(settings.default_voice)

                warmup_text = "Warmup text for initialization."
                voice_name = settings.default_voice
                logger.debug(f"Using default voice '{voice_name}' for warmup")

                async for _ in self.generate(warmup_text, (voice_name, voice_path)):
                    pass
            except Exception as e:
                raise RuntimeError(f"Failed to get default voice: {e}")

            ms = int((time.perf_counter() - start) * 1000)
            logger.info(f"Warmup completed in {ms}ms")

            return self._device, "kokoro_v1", len(voices)

        except FileNotFoundError as e:
            logger.error("""
Model files not found! You need to download the Kokoro V1 model:

1. Download model using the script:
   python docker/scripts/download_model.py --output models/v1_0

2. Or set environment variable in docker-compose:
   DOWNLOAD_MODEL=true
""")
            exit(0)

        except Exception as e:
            raise RuntimeError(f"Warmup failed: {e}")

    def get_backend(self) -> BaseModelBackend:
        """Get initialized backend.

        Returns:
            Initialized backend instance

        Raises:
            RuntimeError: If backend not initialized
        """
        if not self._backend:
            raise RuntimeError("Backend not initialized")
        return self._backend

    async def load_model(self, path: str) -> None:
        """Load model using initialized backend.

        Args:
            path: Path to model file

        Raises:
            RuntimeError: If loading fails
        """
        if not self._backend:
            raise RuntimeError("Backend not initialized")

        wait_time = 10
        while not os.path.exists(path) and wait_time > 0:
            logger.warning(f"Waiting for model file to exist at {path}... ({wait_time}s remaining)")
            time.sleep(1)
            wait_time -= 1

        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file still not found after wait: {path}")

        try:
            await self._backend.load_model(path)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    async def generate(self, *args, **kwargs):
        """Generate audio using initialized backend.

        Raises:
            RuntimeError: If generation fails
        """
        if not self._backend:
            raise RuntimeError("Backend not initialized")

        try:
            async for chunk in self._backend.generate(*args, **kwargs):
                yield chunk
        except Exception as e:
            raise RuntimeError(f"Generation failed: {e}")

    def unload_all(self) -> None:
        """Unload model and free resources."""
        if self._backend:
            self._backend.unload()
            self._backend = None

    @property
    def current_backend(self) -> str:
        """Get current backend type."""
        return "kokoro_v1"


async def get_manager(config: Optional[ModelConfig] = None) -> ModelManager:
    """Get model manager instance.

    Args:
        config: Optional configuration override

    Returns:
        ModelManager instance
    """
    if ModelManager._instance is None:
        ModelManager._instance = ModelManager(config)
    return ModelManager._instance
