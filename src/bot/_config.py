from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Config(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET_TOKEN: Optional[str] = None

    HOST: str = '0.0.0.0'
    PORT: int = 80

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
