from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: str = "INFO"
    database_url: str = "sqlite:///./db.sqlite3"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Settings.model_validate({})
