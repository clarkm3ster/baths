"""
DOMES v2 — Alembic Environment Configuration

This module is loaded by Alembic CLI when running migrations.
It configures the migration environment for both offline (SQL script)
and online (live database) migration modes.

Async SQLAlchemy note:
    Alembic does not natively support async engines. We use a synchronous
    psycopg2 URL for migrations while keeping asyncpg for the application.
    The settings.sync_database_url property handles the URL conversion.

Usage:
    alembic upgrade head          # Apply all pending migrations
    alembic downgrade -1          # Roll back one migration
    alembic revision --autogenerate -m "add index"  # Generate new migration
    alembic history               # Show migration history
    alembic current               # Show current revision

Important:
    When autogenerating migrations, Alembic compares the current DB schema
    to the SQLAlchemy models. Import ALL models in this file to ensure they
    are included in the comparison — models not imported will be invisible
    to autogenerate.
"""
from __future__ import annotations

import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ---------------------------------------------------------------------------
# Import all models so Alembic can see them for autogenerate
# ---------------------------------------------------------------------------
from domes.models.base import DOMESBase  # noqa: F401 — must be first
from domes.models.person import Person  # noqa: F401
from domes.models.consent import Consent, ConsentAuditEntry  # noqa: F401
from domes.models.fragment import Fragment  # noqa: F401
from domes.models.system import GovernmentSystem  # noqa: F401
from domes.models.gap import DataGap, Provision  # noqa: F401
from domes.models.observation import Observation  # noqa: F401
from domes.models.encounter import Encounter  # noqa: F401
from domes.models.condition import Condition  # noqa: F401
from domes.models.medication import Medication  # noqa: F401
from domes.models.assessment import Assessment  # noqa: F401
from domes.models.enrollment import Enrollment  # noqa: F401
from domes.models.biometric import BiometricReading  # noqa: F401
from domes.models.environment import EnvironmentReading  # noqa: F401
from domes.models.dome import Dome  # noqa: F401
from domes.models.flourishing import FlourishingScore  # noqa: F401

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
from domes.config import settings

# ---------------------------------------------------------------------------
# Alembic config object
# ---------------------------------------------------------------------------
config = context.config

# Set up Python logging from alembic.ini [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

# Override the sqlalchemy.url from settings (supports environment variables)
# Use synchronous psycopg2 URL — Alembic does not support asyncpg
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

# Target metadata from our models — drives autogenerate
target_metadata = DOMESBase.metadata


# ---------------------------------------------------------------------------
# Offline migration (generates SQL script without connecting to DB)
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This generates a SQL script instead of running against a live database.
    Useful for environments where direct DB access is not available.

    Usage: alembic upgrade head --sql > migration.sql
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Include custom compare functions for PostgreSQL-specific types
        compare_type=True,
        compare_server_default=True,
        # Include schemas if using multiple PostgreSQL schemas
        include_schemas=False,
        # Render SQL for enum types
        render_as_batch=False,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online migration (runs against live database)
# ---------------------------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode against a live database connection.

    Uses psycopg2 (synchronous) via the sync_database_url.
    """
    # Build engine from alembic.ini [alembic:main] section, overridden by settings
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # No pooling for migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            # PostgreSQL-specific: handle enums
            include_object=_include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


def _include_object(
    object: object,
    name: str | None,
    type_: str,
    reflected: bool,
    compare_to: object,
) -> bool:
    """
    Filter which database objects are included in autogenerate comparisons.

    Excludes:
    - TimescaleDB internal tables (_timescaledb_*)
    - PostGIS spatial_ref_sys
    - Any table starting with 'pg_' (system tables)
    """
    if type_ == "table" and name:
        if name.startswith("_timescaledb_") or name.startswith("pg_") or name == "spatial_ref_sys":
            return False
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if context.is_offline_mode():
    logger.info("Running migrations in offline mode")
    run_migrations_offline()
else:
    logger.info("Running migrations in online mode")
    run_migrations_online()
