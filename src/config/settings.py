"""
Application settings management.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # App
    APP_NAME: str = "Multi-Agent Ecommerce Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Sarvam AI
    SARVAM_API_KEY: str
    SARVAM_MODEL: str

    # Logging
    LOG_LEVEL: str = "INFO"

    # API
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()