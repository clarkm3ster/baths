"""DOMES Brain — Central API Gateway and Routing Engine.

The brain connects all DOMES micro-services into a single unified
system.  It provides:

- Service registry with automatic health monitoring
- Unified query routing that fans out to relevant services
- Webhook subscriptions for event-driven workflows
- Activity logging and aggregate statistics
- In-memory TTL cache for frequent queries

Run with:
    uvicorn main:app --host 0.0.0.0 --port 8006 --reload
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, SessionLocal
from services import seed_service_registry, monitor_all_services
from orchestrator import router as orchestrator_router
from discovery import router as discovery_router
from discovery_db import create_tables as create_discovery_tables
from scheduler import start_scheduler, stop_scheduler

logger = logging.getLogger("domes.brain")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-28s  %(levelname)-7s  %(message)s",
)

# ---------------------------------------------------------------------------
# Background health monitor task
# ---------------------------------------------------------------------------

_monitor_task: asyncio.Task | None = None  # type: ignore[type-arg]


async def _health_monitor_loop() -> None:
    """Periodically check every registered service.

    Runs every 30 seconds.  Uses ``asyncio.sleep`` so it cooperates
    with the event loop (no extra thread required).
    """
    while True:
        try:
            results = await monitor_all_services()
            online = sum(1 for r in results if r["status"] == "online")
            logger.info(
                "Health check complete: %d/%d services online", online, len(results),
            )
        except Exception:
            logger.exception("Health monitor iteration failed")
        await asyncio.sleep(30)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hook.

    1. Initialize the database (create tables).
    2. Seed the service registry with the canonical DOMES services.
    3. Run an initial health check.
    4. Start the background health-monitor loop.
    """
    global _monitor_task

    # --- Startup ---------------------------------------------------------
    init_db()
    db = SessionLocal()
    try:
        inserted = seed_service_registry(db)
        if inserted:
            logger.info("Seeded %d services into registry", inserted)
        else:
            logger.info("Service registry already populated")
    finally:
        db.close()

    # Initialize discovery tables
    create_discovery_tables()
    logger.info("Discovery tables initialized")

    # Initial health check
    logger.info("Running initial health check...")
    await monitor_all_services()

    # Start background monitor
    _monitor_task = asyncio.create_task(_health_monitor_loop())
    logger.info("Background health monitor started (30s interval)")

    # Start discovery scheduler
    start_scheduler()
    logger.info("Discovery scheduler started")

    yield  # application is running

    # --- Shutdown --------------------------------------------------------
    stop_scheduler()
    if _monitor_task is not None:
        _monitor_task.cancel()
        try:
            await _monitor_task
        except asyncio.CancelledError:
            pass
    logger.info("DOMES Brain shutting down")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="DOMES Brain",
    description="Central API gateway and routing engine for the DOMES ecosystem",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orchestrator_router)
app.include_router(discovery_router)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "service": "domes-brain",
        "version": "1.0.0",
        "description": "Central API gateway for the DOMES ecosystem",
        "docs": "/docs",
        "health": "/api/health",
    }
