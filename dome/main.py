"""THE DOME — FastAPI application entrypoint.

Creates the ASGI app, wires up routers, middleware, and a dev-friendly
lifespan handler that auto-creates tables on startup.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dome.config import settings
from dome.db.database import engine
from dome.db.tables import Base

logger = logging.getLogger("dome")

# ---------------------------------------------------------------------------
# Lifespan — create tables on startup (dev convenience; use Alembic in prod)
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    On startup the handler creates all ORM tables if they do not already exist.
    This is a convenience for local development and testing — production
    deployments should rely on Alembic migrations instead.
    """
    logger.info("DOME starting up — ensuring database tables exist")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("DOME shutting down")
    await engine.dispose()


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan,
    debug=settings.debug,
)

# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Health-check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """Lightweight health-check endpoint.

    Returns a simple JSON payload confirming the service is alive.
    """
    return {"status": "ok", "service": "dome", "version": settings.api_version}


# ---------------------------------------------------------------------------
# Router registration
# ---------------------------------------------------------------------------
# Each router module is imported inside a try/except so the app still boots
# even if individual route files have not been created yet.
# ---------------------------------------------------------------------------

_ROUTER_MODULES: list[str] = [
    "dome.api.persons",
    "dome.api.budgets",
    "dome.api.cascades",
    "dome.api.interventions",
    "dome.api.simulations",
    "dome.api.dashboards",
    "dome.api.validation",
    "dome.api.settlements",
]


def _register_routers() -> None:
    """Dynamically import and register API routers.

    Each module is expected to expose a ``router`` attribute (an
    ``APIRouter`` instance).  Modules that cannot be imported or that lack
    the attribute are silently skipped so the core app remains functional
    while features are still under development.
    """
    import importlib

    for module_path in _ROUTER_MODULES:
        try:
            mod = importlib.import_module(module_path)
            router = getattr(mod, "router", None)
            if router is not None:
                app.include_router(router, prefix=settings.api_prefix)
                logger.info("Registered router: %s", module_path)
            else:
                logger.debug(
                    "Module %s has no 'router' attribute — skipped", module_path
                )
        except ImportError as exc:
            logger.debug("Could not import %s — skipped (%s)", module_path, exc)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Unexpected error importing %s: %s", module_path, exc
            )


_register_routers()
