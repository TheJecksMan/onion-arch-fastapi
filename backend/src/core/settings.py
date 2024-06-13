from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Define the path to the .env file
BASE_URL = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Settings class to handle environment variables and application settings."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
        env_file=(BASE_URL, ".env"),
    )

    DEBUG_MODE: bool = False
    URL_DATABASE: str


settings = Settings()  # type: ignore
