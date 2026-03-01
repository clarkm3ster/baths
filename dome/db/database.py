"""DOME database layer — async SQLAlchemy engine, session factory, and FastAPI dependency.

Uses ``asyncpg`` for PostgreSQL in production and ``aiosqlite`` for
lightweight SQLite-backed tests.  All configuration is pulled from
:pymod:`dome.config`.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dome.config import settings

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------
#  * ``echo`` mirrors SQL to stdout when ``DOME_DATABASE_ECHO=true``.
#  * ``pool_pre_ping`` keeps connections healthy across idle periods.
#  * For SQLite (testing) we disable ``pool_pre_ping`` because aiosqlite
#    does not support it reliably.
# ---------------------------------------------------------------------------

_is_sqlite = settings.database_url.startswith("sqlite")

engine = create_async_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=not _is_sqlite,
    future=True,
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an ``AsyncSession`` and guarantee cleanup.

    Usage inside a FastAPI route::

        @router.get("/items")
        async def list_items(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
