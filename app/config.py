from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    CLIENT_ID: str
    REGION: str
    JWT_SECRET: str
    CLIENT_SECRET: str
    TABLE_NAME: str
    AWS_ACCOUNT_ID: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
