"""
BATHS Scraper Framework — Fetches from real public APIs, accumulates in store.

All APIs used are free, public, and require no authentication:
  - eCFR API (ecfr.gov)           → federal regulations
  - Federal Register API          → proposed rules, final rules, notices
  - USASpending API               → federal spending by agency/program
  - data.cms.gov                  → Medicare/Medicaid cost data
  - HUD User datasets             → fair market rents, shelter costs
  - OpenDataPhilly / Carto        → Philadelphia parcel and property data
  - Census API                    → demographics (optional, key recommended)

The scheduler can run all engines or individual engines on demand.
Every run is logged. Data only grows.
"""

import asyncio
import logging
import time
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Any

import httpx

from .store import DataStore, get_store

logger = logging.getLogger("baths.scraper")

# Rate limiting: max requests per second per domain
RATE_LIMITS = {
    "ecfr.gov": 2,
    "federalregister.gov": 5,
    "api.usaspending.gov": 5,
    "data.cms.gov": 3,
    "huduser.gov": 2,
    "phl.carto.com": 3,
    "api.census.gov": 5,
}

# Backoff config
MAX_RETRIES = 4
BACKOFF_BASE = 2  # seconds


class BaseScraper(ABC):
    """Base class for all domain scrapers."""

    engine_name: str = "base"
    source_name: str = "unknown"

    def __init__(self, store: DataStore | None = None):
        self.store = store or get_store()
        self._last_request: dict[str, float] = {}

    async def _fetch(self, url: str, params: dict | None = None,
                     method: str = "GET", json_body: dict | None = None,
                     timeout: float = 30.0) -> dict | list | None:
        """Fetch URL with rate limiting and exponential backoff."""
        from urllib.parse import urlparse
        domain = urlparse(url).hostname or ""

        # Rate limit
        limit = RATE_LIMITS.get(domain, 10)
        min_interval = 1.0 / limit
        last = self._last_request.get(domain, 0)
        elapsed = time.time() - last
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)

        for attempt in range(MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
                    if method == "GET":
                        resp = await client.get(url, params=params)
                    elif method == "POST":
                        resp = await client.post(url, json=json_body, params=params)
                    else:
                        raise ValueError(f"Unsupported method: {method}")

                    self._last_request[domain] = time.time()
                    resp.raise_for_status()

                    content_type = resp.headers.get("content-type", "")
                    if "json" in content_type:
                        return resp.json()
                    elif "xml" in content_type or "html" in content_type:
                        return {"_raw": resp.text, "_content_type": content_type}
                    else:
                        return resp.json()

            except httpx.ProxyError as e:
                # Proxy blocks outbound — no point retrying
                logger.warning(f"[{self.engine_name}] Proxy blocked {url}: {e}")
                return None

            except (httpx.HTTPStatusError, httpx.ConnectError, httpx.ReadTimeout) as e:
                if attempt < MAX_RETRIES:
                    wait = BACKOFF_BASE ** (attempt + 1)
                    logger.warning(f"[{self.engine_name}] Retry {attempt+1}/{MAX_RETRIES} "
                                   f"for {url}: {e}. Waiting {wait}s")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"[{self.engine_name}] Failed after {MAX_RETRIES} retries: {url}")
                    return None

    @abstractmethod
    async def scrape(self) -> dict:
        """Run a full scrape cycle. Returns {added: int, updated: int}."""
        ...

    async def run(self) -> dict:
        """Execute scrape with logging to store."""
        run_id = self.store.start_scrape_run(self.engine_name, self.source_name)
        try:
            result = await self.scrape()
            self.store.complete_scrape_run(
                run_id,
                records_added=result.get("added", 0),
                records_updated=result.get("updated", 0),
            )
            logger.info(f"[{self.engine_name}/{self.source_name}] Completed: "
                        f"+{result.get('added', 0)} added, "
                        f"~{result.get('updated', 0)} updated")
            return result
        except Exception as e:
            self.store.complete_scrape_run(run_id, error=traceback.format_exc())
            logger.error(f"[{self.engine_name}/{self.source_name}] Failed: {e}")
            return {"added": 0, "updated": 0, "error": str(e)}


class ScrapeScheduler:
    """Runs scraper engines on configurable intervals."""

    def __init__(self):
        self._engines: list[tuple[BaseScraper, timedelta]] = []
        self._running = False
        self._task: asyncio.Task | None = None

    def register(self, scraper: BaseScraper, interval: timedelta):
        self._engines.append((scraper, interval))

    async def _loop(self):
        """Main scheduler loop."""
        last_run: dict[str, datetime] = {}
        while self._running:
            now = datetime.now(timezone.utc)
            for scraper, interval in self._engines:
                key = f"{scraper.engine_name}/{scraper.source_name}"
                last = last_run.get(key)
                if last is None or (now - last) >= interval:
                    logger.info(f"[scheduler] Starting {key}")
                    try:
                        await scraper.run()
                    except Exception as e:
                        logger.error(f"[scheduler] Error in {key}: {e}")
                    last_run[key] = datetime.now(timezone.utc)
            await asyncio.sleep(60)  # Check every minute

    def start(self):
        self._running = True
        self._task = asyncio.create_task(self._loop())
        logger.info(f"[scheduler] Started with {len(self._engines)} engines")

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
        logger.info("[scheduler] Stopped")

    async def run_all_once(self) -> dict:
        """Run all engines once immediately. Returns combined stats."""
        results = {}
        for scraper, _ in self._engines:
            key = f"{scraper.engine_name}/{scraper.source_name}"
            results[key] = await scraper.run()
        return results

    async def run_engine(self, engine_name: str) -> dict:
        """Run a specific engine by name."""
        results = {}
        for scraper, _ in self._engines:
            if scraper.engine_name == engine_name:
                key = f"{scraper.engine_name}/{scraper.source_name}"
                results[key] = await scraper.run()
        return results
