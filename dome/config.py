"""DOME configuration — loads from environment variables with sensible defaults."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application-wide settings sourced from env vars / .env file."""

    # --- Database ---
    database_url: str = "postgresql+asyncpg://dome:dome@localhost:5432/dome"
    database_echo: bool = False

    # --- API ---
    api_title: str = "THE DOME API"
    api_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # --- Simulation ---
    monte_carlo_iterations: int = 1000
    discount_rate: float = 0.03  # 3 % real discount rate for NPV
    default_projection_years: int = 50

    # --- Settlement ---
    settlement_risk_share_pct: float = 0.50  # beneficiaries share 50 % of savings
    settlement_cap_multiple: float = 3.0  # max transfer = 3× upfront investment

    model_config = {"env_prefix": "DOME_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
