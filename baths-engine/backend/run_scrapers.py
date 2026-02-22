#!/usr/bin/env python3
"""
CLI runner for BATHS data scrapers — used by GitHub Actions.

Usage:
    python run_scrapers.py              # seed + scrape all engines + enrich
    python run_scrapers.py legal        # seed + scrape legal engine only
    python run_scrapers.py costs        # seed + scrape costs engine only
    python run_scrapers.py systems      # seed + scrape systems engine only
    python run_scrapers.py parcels      # seed + scrape parcels engine only

After scraping, exports all data to JSON in data/exports/ so it can be
committed to git (the SQLite database itself is gitignored).
"""

import asyncio
import json
import logging
import sys
import os
from pathlib import Path

# Ensure the backend package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data import initialize, scrape_all, scrape_engine, get_stats
from data.store import get_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("baths.runner")

# Export directory — tracked by git (unlike the SQLite db)
EXPORT_DIR = Path(__file__).parent / "data" / "exports"


def export_data():
    """Export all store tables to JSON files for git persistence."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    store = get_store()

    tables = {
        "provisions": store.get_provisions(limit=10000),
        "cost_points": store.get_costs(limit=10000),
        "gov_systems": store.get_systems(limit=10000),
        "system_links": store.get_system_links(limit=10000),
        "parcels": store.get_parcels(limit=10000),
        "enrichments": store.get_enrichments(limit=10000),
        "scrape_history": store.get_scrape_history(limit=500),
    }

    for name, rows in tables.items():
        path = EXPORT_DIR / f"{name}.json"
        with open(path, "w") as f:
            json.dump(rows, f, indent=2, default=str)
        logger.info(f"Exported {len(rows)} {name} → {path}")

    # Write summary stats
    stats = store.stats()
    with open(EXPORT_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2, default=str)

    logger.info(f"Export complete: {EXPORT_DIR}")


async def main():
    engine_name = sys.argv[1] if len(sys.argv) > 1 else None

    # Always seed first so the store has base data
    logger.info("Initializing data engines (seed + enrich)...")
    initialize()

    if engine_name:
        logger.info(f"Scraping engine: {engine_name}")
        results = await scrape_engine(engine_name)
    else:
        logger.info("Scraping all engines...")
        results = await scrape_all()

    logger.info(f"Results: {json.dumps(results, indent=2, default=str)}")

    stats = get_stats()
    logger.info(f"Store stats: {json.dumps(stats, indent=2, default=str)}")

    # Export data to JSON for git
    export_data()


if __name__ == "__main__":
    asyncio.run(main())
