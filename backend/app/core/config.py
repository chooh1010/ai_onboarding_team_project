from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "광주·전라권 관광정보 서비스"
    app_env: str = "local"
    database_url: str = "sqlite:///./regional_tour.db"
    backend_cors_origins: str = "http://localhost:5173"
    openai_api_key: str = ""
    openai_model: str = "gpt-5-mini"
    openweather_api_key: str = ""
    data_directory: Path = Field(default=Path("app/data/raw"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
