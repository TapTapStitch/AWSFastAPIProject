from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    CLIENT_ID: str
    REGION: str
    JWT_SECRET: str
    CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
