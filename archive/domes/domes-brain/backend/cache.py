"""TTL-based in-memory cache for DOMES Brain.

Thread-safe (asyncio lock) dictionary cache with per-key time-to-live.
Used to avoid hammering downstream services for identical queries within
a short window.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float


@dataclass
class TTLCache:
    """Async-safe in-memory cache with per-key TTL.

    Usage::

        cache = TTLCache()
        await cache.set("key", {"data": 1}, ttl=60)
        hit = await cache.get("key")  # -> {"data": 1} or None
    """

    default_ttl: float = 300.0  # seconds
    _store: dict[str, _CacheEntry] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def get(self, key: str) -> Any | None:
        """Return cached value if present and not expired, else ``None``."""
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if time.monotonic() > entry.expires_at:
                del self._store[key]
                return None
            return entry.value

    async def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Store *value* under *key* with an optional per-key *ttl* (seconds)."""
        ttl = ttl if ttl is not None else self.default_ttl
        async with self._lock:
            self._store[key] = _CacheEntry(
                value=value,
                expires_at=time.monotonic() + ttl,
            )

    async def invalidate(self, key: str) -> bool:
        """Remove a single key. Returns ``True`` if it existed."""
        async with self._lock:
            return self._store.pop(key, None) is not None

    async def clear(self) -> int:
        """Drop every entry. Returns count of entries removed."""
        async with self._lock:
            count = len(self._store)
            self._store.clear()
            return count

    async def prune(self) -> int:
        """Remove all expired entries. Returns count pruned."""
        now = time.monotonic()
        async with self._lock:
            expired = [k for k, v in self._store.items() if now > v.expires_at]
            for k in expired:
                del self._store[k]
            return len(expired)

    @property
    def size(self) -> int:
        return len(self._store)


# Module-level singleton used across the application.
query_cache = TTLCache(default_ttl=120.0)
