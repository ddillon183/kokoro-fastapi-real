from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_title: str = "Kokoro TTS API"
    api_description: str = "A FastAPI implementation for text-to-speech"
    api_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8888

    # Optional settings
    cors_enabled: bool = True
    cors_origins: list[str] = ["*"]

    # Toggle beta web player
    enable_web_player: bool = True

    # ✅ Add the correct model and voices directories
    model_dir: str = "models/v1_0"
    voices_dir: str = "/app/voices/v1_0"

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()

