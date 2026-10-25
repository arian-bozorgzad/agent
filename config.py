from functools import lru_cache
from pathlib import Path

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./data/jarvis.db"
    app_token: str = ""
    app_env: str = "development"
    allowed_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000,http://127.0.0.1:8000"
    )
    openai_api_key: str = ""
    openai_model: str = ""
    transcription_provider: str = "openai"
    transcription_model: str = "whisper-1"
    local_whisper_model: str = "base.en"
    web_search_enabled: bool = False
    max_audio_bytes: int = 20 * 1024 * 1024
    static_dir: str = "../frontend/dist"
    run_timeout_seconds: int = Field(default=180, ge=1, le=600)

    @model_validator(mode="after")
    def validate_settings(self):
        if self.app_env == "production" and len(self.app_token) < 32:
            raise ValueError("Production requires APP_TOKEN with at least 32 characters")
        if self.transcription_provider not in {"openai", "local"}:
            raise ValueError("TRANSCRIPTION_PROVIDER must be openai or local")
        if self.database_url.startswith("sqlite:///"):
            path = self.database_url.removeprefix("sqlite:///")
            if path != ":memory:":
                Path(path).parent.mkdir(parents=True, exist_ok=True)
        return self

    @property
    def origins(self) -> list[str]:
        return [value.strip() for value in self.allowed_origins.split(",") if value.strip()]

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openai_api_key and self.openai_model)


@lru_cache
def get_settings() -> Settings:
    return Settings()
