"""
DOMES v2 — Async Database Engine + Session Factory

Provides the SQLAlchemy 2.0 async engine, session factory, and
FastAPI dependency injection for database sessions.

Usage in FastAPI routes:
    from domes.database import get_db

    @router.get("/persons/{id}")
    async def get_person(id: UUID, db: AsyncSession = Depends(get_db)):
        result = await db.get(Person, id)
        return result

Usage in standalone scripts / seeds:
    from domes.database import AsyncSessionLocal

    async def main():
        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add(person)

TimescaleDB setup:
    After running alembic upgrade head, run setup_timescaledb() to
    convert biometric_reading and environment_reading to hypertables.
"""
from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from domes.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Engine factory
# ---------------------------------------------------------------------------

def _build_engine(url: str | None = None, **overrides: Any) -> AsyncEngine:
    """
    Build the SQLAlchemy async engine from settings.

    Args:
        url: Override the database URL (used in tests).
        **overrides: Override any engine kwargs.

    Returns:
        Configured AsyncEngine instance.
    """
    engine_kwargs = settings.get_sqlalchemy_engine_kwargs()
    engine_kwargs.update(overrides)

    return create_async_engine(
        url or settings.database_url,
        **engine_kwargs,
    )


# ---------------------------------------------------------------------------
# Module-level singletons
# ---------------------------------------------------------------------------

engine: AsyncEngine = _build_engine()

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy-load errors after commit
    autocommit=False,
    autoflush=False,
)


# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session.

    The session is automatically committed on success and rolled back
    on exception. The session is always closed when the request finishes.

    Usage:
        @router.post("/persons/")
        async def create_person(
            body: PersonCreate,
            db: AsyncSession = Depends(get_db),
        ) -> PersonRead:
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ---------------------------------------------------------------------------
# Context manager for non-FastAPI usage
# ---------------------------------------------------------------------------

class DatabaseSession:
    """
    Async context manager for database sessions outside of FastAPI.

    Usage:
        async with DatabaseSession() as db:
            result = await db.execute(select(Person))
    """

    def __init__(self) -> None:
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self._session = AsyncSessionLocal()
        return self._session

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._session is None:
            return
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            self._session = None


# ---------------------------------------------------------------------------
# TimescaleDB setup helpers
# ---------------------------------------------------------------------------

async def setup_timescaledb() -> None:
    """
    Convert biometric_reading and environment_reading to TimescaleDB hypertables.

    Run this ONCE after running 'alembic upgrade head' if TimescaleDB is enabled.
    Safe to re-run — uses IF NOT EXISTS.

    Requires TimescaleDB extension installed:
        CREATE EXTENSION IF NOT EXISTS timescaledb;
    """
    if not settings.timescaledb_enabled:
        logger.info("TimescaleDB disabled — skipping hypertable setup")
        return

    async with engine.begin() as conn:
        # Enable extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE"))
        logger.info("TimescaleDB extension enabled")

        # Convert biometric_reading to hypertable
        await conn.execute(
            text("""
                SELECT create_hypertable(
                    'biometric_reading',
                    'timestamp',
                    partitioning_column => 'person_id',
                    number_partitions => :partitions,
                    chunk_time_interval => :chunk_interval::INTERVAL,
                    if_not_exists => TRUE,
                    migrate_data => TRUE
                )
            """),
            {
                "partitions": settings.timescaledb_partitions,
                "chunk_interval": settings.timescaledb_chunk_interval,
            },
        )
        logger.info("biometric_reading converted to TimescaleDB hypertable")

        # Convert environment_reading to hypertable
        await conn.execute(
            text("""
                SELECT create_hypertable(
                    'environment_reading',
                    'timestamp',
                    partitioning_column => 'person_id',
                    number_partitions => :partitions,
                    chunk_time_interval => :chunk_interval::INTERVAL,
                    if_not_exists => TRUE,
                    migrate_data => TRUE
                )
            """),
            {
                "partitions": settings.timescaledb_partitions,
                "chunk_interval": settings.timescaledb_chunk_interval,
            },
        )
        logger.info("environment_reading converted to TimescaleDB hypertable")

        # Enable compression on biometric_reading (TimescaleDB 2.0+)
        # Compress chunks older than 7 days
        try:
            await conn.execute(
                text("""
                    ALTER TABLE biometric_reading
                    SET (
                        timescaledb.compress,
                        timescaledb.compress_segmentby = 'person_id,metric',
                        timescaledb.compress_orderby = 'timestamp DESC'
                    )
                """)
            )
            await conn.execute(
                text("""
                    SELECT add_compression_policy(
                        'biometric_reading',
                        INTERVAL '7 days',
                        if_not_exists => TRUE
                    )
                """)
            )
            logger.info("Compression policy added to biometric_reading")
        except Exception as e:
            logger.warning(f"Compression setup failed (non-fatal): {e}")


async def check_db_connection() -> bool:
    """
    Check if the database is reachable.

    Returns:
        True if connection succeeds, False otherwise.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False


async def dispose_engine() -> None:
    """
    Dispose the engine — releases all connections.

    Call on application shutdown to cleanly close the connection pool.
    """
    await engine.dispose()
    logger.info("Database engine disposed")
