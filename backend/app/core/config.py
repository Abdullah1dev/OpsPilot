from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate the OpsPilot project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "OpsPilot"
    environment: str = "development"

    database_user: str = "postgres"
    database_password: str
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "opspilot"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
