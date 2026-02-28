from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Dribbling"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./dribbling.db"

    # Telegram
    BOT_TOKEN: str
    WEBAPP_URL: str

    # Security
    SECRET_KEY: str = "your-secret-key-here"

    # Cities
    CITIES: List[str] = [
        "Пенджикент",

    ]

    # Default location for Panjakent
    DEFAULT_CITY: str = "Пенджикент"
    DEFAULT_LAT: float = 39.4952
    DEFAULT_LON: float = 67.6093

    class Config:
        env_file = ".env"


settings = Settings()