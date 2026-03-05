"""
Background job scheduler for the DOMES Discovery Engine.

Uses APScheduler to run scanners on independent schedules:
  - Federal Register:     every 24 hours
  - eCFR:                 every 12 hours
  - State Legislation:    every  6 hours
  - Academic:             every 48 hours
  - News:                 every  4 hours
  - Gap Analysis:         every 24 hours

Provides start_scheduler() / stop_scheduler() lifecycle helpers that
should be called from the FastAPI app's startup/shutdown events.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from discovery_db import (
    create_discovery,
    discovery_url_exists,
    get_session_factory,
    update_source_last_scanned,
)
from scanners import run_scanner_and_collect

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Singleton scheduler instance
# ---------------------------------------------------------------------------

_scheduler: AsyncIOScheduler | None = None


def get_scheduler() -> AsyncIOScheduler:
    """Return the global scheduler, creating it lazily."""
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler(
            job_defaults={"coalesce": True, "max_instances": 1},
        )
    return _scheduler


# ---------------------------------------------------------------------------
# Scan job — generic runner for any source type
# ---------------------------------------------------------------------------

async def _run_scan_job(source_type: str) -> None:
    """
    Execute a single scanner, persist new discoveries, and update the
    source's last_scanned timestamp.  This is the function APScheduler calls.
    """
    logger.info("Scheduled scan starting: %s", source_type)
    session_factory = get_session_factory()
    db = session_factory()

    try:
        discoveries, scan_results = await run_scanner_and_collect(source_type)

        new_count = 0
        for disc in discoveries:
            if not discovery_url_exists(db, disc.url):
                create_discovery(db, disc)
                new_count += 1

        for sr in scan_results:
            update_source_last_scanned(db, sr.source_name)

        logger.info(
            "Scheduled scan complete: %s — found %d, persisted %d new",
            source_type,
            sum(sr.items_found for sr in scan_results),
            new_count,
        )
    except Exception:
        logger.exception("Scheduled scan failed: %s", source_type)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Schedule definitions
# ---------------------------------------------------------------------------

SCAN_SCHEDULES: list[dict] = [
    {
        "id": "scan_federal_register",
        "source_type": "federal_register",
        "hours": 24,
        "description": "Federal Register — every 24 h",
    },
    {
        "id": "scan_ecfr",
        "source_type": "ecfr",
        "hours": 12,
        "description": "eCFR — every 12 h",
    },
    {
        "id": "scan_state_legislation",
        "source_type": "state_legislation",
        "hours": 6,
        "description": "State Legislation — every 6 h",
    },
    {
        "id": "scan_academic",
        "source_type": "academic",
        "hours": 48,
        "description": "Academic / Semantic Scholar — every 48 h",
    },
    {
        "id": "scan_news",
        "source_type": "news",
        "hours": 4,
        "description": "News Monitor — every 4 h",
    },
    {
        "id": "scan_gap_analysis",
        "source_type": "gap_analysis",
        "hours": 24,
        "description": "DOMES Gap Analyzer — every 24 h",
    },
]


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

def start_scheduler() -> None:
    """
    Register all scan jobs and start the scheduler.
    Call this from FastAPI's ``on_startup`` or ``lifespan`` hook.
    """
    scheduler = get_scheduler()

    for sched in SCAN_SCHEDULES:
        scheduler.add_job(
            _run_scan_job,
            trigger=IntervalTrigger(hours=sched["hours"]),
            id=sched["id"],
            name=sched["description"],
            args=[sched["source_type"]],
            replace_existing=True,
        )
        logger.info("Registered scheduled job: %s (%s)", sched["id"], sched["description"])

    if not scheduler.running:
        scheduler.start()
        logger.info("Discovery scheduler started with %d jobs.", len(SCAN_SCHEDULES))


def stop_scheduler() -> None:
    """
    Gracefully shut down the scheduler.
    Call this from FastAPI's ``on_shutdown`` or ``lifespan`` hook.
    """
    scheduler = get_scheduler()
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Discovery scheduler stopped.")


def get_scheduled_jobs() -> list[dict]:
    """Return a list of currently registered jobs and their next run times."""
    scheduler = get_scheduler()
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time) if job.next_run_time else None,
            "trigger": str(job.trigger),
        })
    return jobs
