"""
BATHS Data Engines — Elite data infrastructure that gets smarter over time.

Usage:
    from data import initialize, scrape_all, get_stats, get_store

    # On startup: seed + enrich
    initialize()

    # On schedule or on demand: scrape + re-enrich
    await scrape_all()

    # Check how much data has accumulated
    stats = get_stats()
"""

import asyncio
import logging
from datetime import timedelta

from .store import DataStore, get_store
from .legal import seed_provisions, ECFRScraper, FederalRegisterScraper
from .costs import seed_costs, CMSScraper, HUDScraper, USASpendingScraper
from .systems import seed_systems, SystemsScraper
from .parcels import seed_parcels, PhillyParcelScraper
from .enrichment import EnrichmentEngine
from .scraper import ScrapeScheduler
from .coordination import COORDINATION_MODELS, recommend_models
from .flourishing import FRAMEWORKS, FLOURISHING_INDICATORS, get_flourishing_score

logger = logging.getLogger("baths.data")

_initialized = False
_scheduler: ScrapeScheduler | None = None


def initialize(store: DataStore | None = None):
    """Seed all engines with base data and run initial enrichment."""
    global _initialized
    if _initialized:
        return

    store = store or get_store()

    logger.info("Seeding data engines...")
    seed_provisions(store)
    seed_costs(store)
    seed_systems(store)
    seed_parcels(store)

    logger.info("Running initial enrichment...")
    enricher = EnrichmentEngine(store)
    enricher.run_all()

    _initialized = True
    stats = store.stats()
    logger.info(f"Data engines initialized: {stats}")
    return stats


def get_scheduler() -> ScrapeScheduler:
    """Get or create the scrape scheduler with all engines registered."""
    global _scheduler
    if _scheduler is None:
        store = get_store()
        _scheduler = ScrapeScheduler()

        # Register all scrapers with intervals
        _scheduler.register(ECFRScraper(store), timedelta(hours=24))
        _scheduler.register(FederalRegisterScraper(store), timedelta(hours=12))
        _scheduler.register(CMSScraper(store), timedelta(hours=24))
        _scheduler.register(HUDScraper(store), timedelta(days=7))
        _scheduler.register(USASpendingScraper(store), timedelta(days=7))
        _scheduler.register(SystemsScraper(store), timedelta(days=7))
        _scheduler.register(PhillyParcelScraper(store), timedelta(hours=6))

    return _scheduler


async def scrape_all() -> dict:
    """Run all scrapers once, then re-enrich. Returns combined results."""
    scheduler = get_scheduler()
    results = await scheduler.run_all_once()

    # Re-enrich after new data
    store = get_store()
    enricher = EnrichmentEngine(store)
    enrichment_results = enricher.run_all()
    results["enrichment"] = enrichment_results

    return results


async def scrape_engine(engine_name: str) -> dict:
    """Run a specific engine's scrapers."""
    scheduler = get_scheduler()
    return await scheduler.run_engine(engine_name)


def get_stats() -> dict:
    """Get current data stats across all engines."""
    store = get_store()
    stats = store.stats()
    stats["initialized"] = _initialized
    return stats


def start_scheduler():
    """Start the background scrape scheduler."""
    scheduler = get_scheduler()
    scheduler.start()
    logger.info("Scrape scheduler started")


def stop_scheduler():
    """Stop the background scrape scheduler."""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
        logger.info("Scrape scheduler stopped")
