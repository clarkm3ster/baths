"""
DOMES v2 — Application Configuration

Pydantic-Settings based configuration for all DOMES v2 environment variables.
Settings are read from environment variables with an optional .env file.

Usage:
    from domes.config import settings

    print(settings.database_url)
    print(settings.timescaledb_enabled)

Environment variable prefix: DOMES_
(e.g., DOMES_DATABASE_URL, DOMES_TIMESCALEDB_ENABLED)

Production deployment notes:
- DOMES_SECRET_KEY must be set to a cryptographically random 64-char hex string
- DOMES_DATABASE_URL must use asyncpg driver: postgresql+asyncpg://...
- DOMES_SSN_SALT must be a random salt (never reuse across environments)
- DOMES_ENCRYPTION_KEY is used for field-level encryption of sensitive JSONB
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    DOMES v2 application settings.

    All settings can be overridden via environment variables with the
    DOMES_ prefix, or via a .env file in the working directory.
    """

    model_config = SettingsConfigDict(
        env_prefix="DOMES_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = Field(
        default="DOMES v2",
        description="Application display name",
    )

    app_version: str = Field(
        default="2.0.0",
        description="Application version string",
    )

    debug: bool = Field(
        default=False,
        description="Enable debug mode (never True in production)",
    )

    environment: str = Field(
        default="development",
        description="Deployment environment: development, staging, production",
    )

    log_level: str = Field(
        default="INFO",
        description="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    database_url: str = Field(
        default="postgresql+asyncpg://domes:domes@localhost:5432/domes",
        description=(
            "Async PostgreSQL connection URL. "
            "Must use asyncpg driver: postgresql+asyncpg://user:pass@host:port/db"
        ),
    )

    database_pool_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="SQLAlchemy async connection pool size",
    )

    database_max_overflow: int = Field(
        default=10,
        ge=0,
        le=50,
        description="Max overflow connections beyond pool_size",
    )

    database_pool_timeout: int = Field(
        default=30,
        description="Seconds to wait for a connection from the pool",
    )

    database_pool_recycle: int = Field(
        default=1800,
        description="Recycle connections older than this many seconds (30 min default)",
    )

    database_echo: bool = Field(
        default=False,
        description="Echo all SQL statements to stdout (debug only; never True in production)",
    )

    # ------------------------------------------------------------------
    # TimescaleDB
    # ------------------------------------------------------------------

    timescaledb_enabled: bool = Field(
        default=True,
        description="True if TimescaleDB extension is installed on PostgreSQL",
    )

    timescaledb_chunk_interval: str = Field(
        default="1 week",
        description="Chunk time interval for biometric_reading hypertable",
    )

    timescaledb_partitions: int = Field(
        default=4,
        ge=1,
        le=32,
        description="Number of space partitions for biometric_reading by person_id",
    )

    # ------------------------------------------------------------------
    # Security
    # ------------------------------------------------------------------

    secret_key: SecretStr = Field(
        default=SecretStr("CHANGE_ME_IN_PRODUCTION_USE_SECRETS_MANAGER"),
        description="Application secret key — use secrets manager in production",
    )

    ssn_salt: SecretStr = Field(
        default=SecretStr("CHANGE_ME_SSN_SALT"),
        description="Salt for SSN SHA-256 hashing — must be unique per environment",
    )

    encryption_key: SecretStr | None = Field(
        default=None,
        description="AES-256 key for field-level encryption of sensitive JSONB (optional)",
    )

    # ------------------------------------------------------------------
    # CORS / API
    # ------------------------------------------------------------------

    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    api_prefix: str = Field(
        default="/api/v2",
        description="API route prefix",
    )

    # ------------------------------------------------------------------
    # Consent / Privacy
    # ------------------------------------------------------------------

    default_consent_expiry_days: int = Field(
        default=365,
        ge=30,
        le=3650,
        description="Default consent expiry in days from signing (1 year default)",
    )

    require_42cfr_consent_for_sud: bool = Field(
        default=True,
        description=(
            "Enforce 42 CFR Part 2 consent check before returning SUD-related records. "
            "Should always be True in production."
        ),
    )

    # ------------------------------------------------------------------
    # Biometric / Wearable
    # ------------------------------------------------------------------

    biometric_retention_days: int = Field(
        default=730,
        description="How many days of biometric readings to retain (2 years default)",
    )

    cgm_alert_low_mg_dl: float = Field(
        default=70.0,
        description="Blood glucose low alert threshold (mg/dL) — ADA Level 1 hypo",
    )

    cgm_alert_critical_low_mg_dl: float = Field(
        default=54.0,
        description="Blood glucose critical low alert (mg/dL) — ADA Level 2 hypo",
    )

    cgm_alert_high_mg_dl: float = Field(
        default=250.0,
        description="Blood glucose high alert threshold (mg/dL)",
    )

    # ------------------------------------------------------------------
    # Dome assembly
    # ------------------------------------------------------------------

    dome_assembly_timeout_seconds: int = Field(
        default=30,
        description="Max seconds for a dome assembly before timeout",
    )

    dome_scheduled_interval_hours: int = Field(
        default=24,
        description="How often to run scheduled dome assemblies (24h default)",
    )

    dome_crisis_threshold_cosm: float = Field(
        default=25.0,
        description="COSM score below which a crisis alert is fired",
    )

    # ------------------------------------------------------------------
    # External APIs
    # ------------------------------------------------------------------

    openweathermap_api_key: SecretStr | None = Field(
        default=None,
        description="OpenWeatherMap API key for environmental data",
    )

    purpleair_api_key: SecretStr | None = Field(
        default=None,
        description="PurpleAir API key for hyperlocal PM2.5 data",
    )

    fhir_base_url: str | None = Field(
        default=None,
        description="Base URL of connected FHIR server (e.g., Epic / Cerner FHIR endpoint)",
    )

    fhir_client_id: str | None = Field(
        default=None,
        description="SMART on FHIR client ID",
    )

    fhir_client_secret: SecretStr | None = Field(
        default=None,
        description="SMART on FHIR client secret",
    )

    hmis_api_url: str | None = Field(
        default=None,
        description="HMIS Clarity API base URL",
    )

    hmis_api_key: SecretStr | None = Field(
        default=None,
        description="HMIS API key",
    )

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "staging", "production", "test"}
        if v not in allowed:
            raise ValueError(f"environment must be one of: {allowed}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of: {allowed}")
        return v.upper()

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://") and not v.startswith("postgresql://"):
            raise ValueError(
                "database_url must start with postgresql+asyncpg:// or postgresql://"
            )
        return v

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    @property
    def is_production(self) -> bool:
        """Return True if running in production environment."""
        return self.environment == "production"

    @property
    def sync_database_url(self) -> str:
        """Return a synchronous psycopg2 URL for Alembic migrations."""
        return self.database_url.replace(
            "postgresql+asyncpg://", "postgresql+psycopg2://"
        ).replace("postgresql://", "postgresql+psycopg2://")

    def get_sqlalchemy_engine_kwargs(self) -> dict[str, Any]:
        """Return SQLAlchemy engine kwargs from settings."""
        return {
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow,
            "pool_timeout": self.database_pool_timeout,
            "pool_recycle": self.database_pool_recycle,
            "echo": self.database_echo,
            "pool_pre_ping": True,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the cached Settings instance.

    Uses lru_cache so the .env file is read only once per process.
    Call get_settings.cache_clear() in tests to reset between test cases.
    """
    return Settings()


# Convenience singleton
settings: Settings = get_settings()
