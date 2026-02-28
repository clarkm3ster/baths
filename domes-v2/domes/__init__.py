"""
DOMES v2 — Application Package

Digital twin system for unified person-centric government data.

Core components:
    domes.models     — SQLAlchemy 2.0 async models (PostgreSQL + TimescaleDB)
    domes.schemas    — Pydantic v2 request/response schemas
    domes.enums      — System-wide enumerations
    domes.config     — Pydantic-settings environment configuration
    domes.database   — Async SQLAlchemy engine + session factory
    domes.seed       — Seed data: 5 archetypal characters + government systems

Version: 2.0.0
"""
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("domes-v2")
except PackageNotFoundError:
    __version__ = "2.0.0"

__all__ = ["__version__"]
