"""SPHERE/OS global settings via pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://sphere:dev_password@localhost:5432/sphere_os"
    database_echo: bool = False

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Anthropic
    anthropic_api_key: str = ""

    # Mapbox
    mapbox_token: str = ""

    # Server
    host: str = "0.0.0.0"
    port: int = 8100
    debug: bool = True

    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}


settings = Settings()
