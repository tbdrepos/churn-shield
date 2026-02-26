from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    jwt_key: str = ""
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.production"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
        validate_assignment=True,
    )
