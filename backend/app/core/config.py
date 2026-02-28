from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    jwt_key: str = ""
    jwt_algorithm: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.production"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
        validate_assignment=True,
    )


@lru_cache
def get_settings():
    return Settings()
