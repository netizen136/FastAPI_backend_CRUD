
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    access_token_secret_key: str
    access_token_expire_minutes: int

    # Database settings
    app_name: str = "xxxx dummy Learning API xxxxx"
    database_url: str = "dummyurl+psycopg://postgres:8630@localhost:5432/x_product_learning_db_3"
    frontend_origin: str = "http://dunmmyhost:5174"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
    )

settings = Settings()
