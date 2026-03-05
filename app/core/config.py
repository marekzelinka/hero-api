from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, UrlConstraints, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:  # noqa: ANN401
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v

    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database configuration
    database_url: Annotated[
        MultiHostUrl,
        UrlConstraints(allowed_schemes=["sqlite"]),
    ]

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> str:
        return str(self.database_url).replace("sqlite", "sqlite+aiosqlite")

    # Application settings
    api_v1_str: str = "/api/v1"
    frontend_host: str = "http://localhost:5173"
    environment: Literal["local", "staging", "production"] = "local"
    log_level: str = "info"
    backend_cors_origins: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.backend_cors_origins] + [
            self.frontend_host
        ]


settings = Settings.model_validate({})
