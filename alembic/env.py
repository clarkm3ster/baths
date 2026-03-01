"""Alembic environment configuration for THE DOME.

This module configures Alembic to work with SQLAlchemy's async engine so that
migrations run against the same database connection that the application uses.

Key points:
    - Imports ``Base.metadata`` from :pymod:`dome.db.tables` so Alembic can
      auto-detect schema changes.
    - Reads the database URL from :pymod:`dome.config` (which honours the
      ``DOME_DATABASE_URL`` env var), falling back to ``alembic.ini`` only if
      the application settings are unavailable.
    - Supports both **offline** (SQL script generation) and **online** (live
      connection) migration modes.
    - Uses ``run_async`` with ``create_async_engine`` for online migrations so
      asyncpg is handled correctly.
"""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# ---------------------------------------------------------------------------
# Import DOME metadata so Alembic knows about every table
# ---------------------------------------------------------------------------
from dome.db.tables import Base  # noqa: E402

target_metadata = Base.metadata

# ---------------------------------------------------------------------------
# Alembic Config object — gives access to values in alembic.ini
# ---------------------------------------------------------------------------

config = context.config

# Interpret the config file for Python logging if present.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---------------------------------------------------------------------------
# Resolve the database URL
# ---------------------------------------------------------------------------
# Prefer the application settings (``DOME_DATABASE_URL``) so that the URL
# stays in one canonical place.  Fall back to whatever ``sqlalchemy.url``
# is set to in alembic.ini (useful for CI scripts that override it).
# ---------------------------------------------------------------------------


def _get_url() -> str:
    """Return the async database URL for migrations."""
    try:
        from dome.config import settings

        return settings.database_url
    except Exception:  # noqa: BLE001
        # Fall back to alembic.ini value
        return config.get_main_option("sqlalchemy.url", "")


# ---------------------------------------------------------------------------
# Offline migrations — emit SQL without a live connection
# ---------------------------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This generates the SQL statements that *would* be executed, without
    actually connecting to the database.  Useful for producing migration
    scripts that can be reviewed or applied manually.

    Calls ``context.configure`` with just a URL rather than an engine.
    """
    url = _get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online migrations — connect to the database and apply changes
# ---------------------------------------------------------------------------


def do_run_migrations(connection: Connection) -> None:
    """Execute migrations against the provided synchronous *connection*.

    This helper is called from within ``run_async`` after the async engine
    has been converted to a sync connection context.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations inside an async context.

    Uses ``NullPool`` because Alembic runs a single short-lived connection
    and we do not want to leave idle connections in a pool.
    """
    connectable = create_async_engine(
        _get_url(),
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an async engine, opens a connection, and delegates to
    :func:`do_run_migrations` for the actual schema changes.
    """
    asyncio.run(run_async_migrations())


# ---------------------------------------------------------------------------
# Entrypoint — Alembic calls whichever mode is active
# ---------------------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
