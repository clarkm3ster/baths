"""
Marble API Client — World Labs 3D World Generation

Wraps the World Labs Marble API for generating immersive 3D worlds
from text prompts.  Handles generation, polling, and caching.

API Reference:
  Base URL:  https://api.worldlabs.ai/marble/v1
  Auth:      WLT-Api-Key header from MARBLE_API_KEY env var
  Generate:  POST /worlds:generate
  Poll:      GET  /operations/{operationId}
  Get world: GET  /worlds/{worldId}
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any

import httpx

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MARBLE_BASE_URL = "https://api.worldlabs.ai/marble/v1"
MARBLE_API_KEY = os.environ.get("MARBLE_API_KEY", "")
MARBLE_MODEL = "Marble 0.1-mini"
POLL_INTERVAL = 5          # seconds between poll requests
POLL_TIMEOUT = 300         # max seconds to wait for generation
CACHE_FILE = Path(__file__).resolve().parent.parent / "data" / "marble_cache.json"


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _load_cache() -> dict[str, Any]:
    """Load the marble cache from disk."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"worlds": []}


def _save_cache(cache: dict[str, Any]) -> None:
    """Persist the marble cache to disk."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, default=str))


def _append_world(world_entry: dict[str, Any]) -> None:
    """Append a world record to the cache."""
    cache = _load_cache()
    # Deduplicate by world_id
    cache["worlds"] = [
        w for w in cache["worlds"] if w.get("world_id") != world_entry.get("world_id")
    ]
    cache["worlds"].insert(0, world_entry)
    _save_cache(cache)


def get_cached_worlds() -> list[dict[str, Any]]:
    """Return all cached worlds, newest first."""
    return _load_cache().get("worlds", [])


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    return {
        "WLT-Api-Key": MARBLE_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ---------------------------------------------------------------------------
# Core API methods
# ---------------------------------------------------------------------------

async def generate_world(prompt: str) -> dict[str, Any]:
    """
    Generate a 3D world from a text prompt.

    1. POST /worlds:generate  -- kick off generation
    2. Poll GET /operations/{id}  until done=true
    3. GET /worlds/{worldId}  -- retrieve splat URLs

    Returns a dict with world_id, prompt, splat_url, status, etc.
    """
    if not MARBLE_API_KEY:
        # Return a mock/fallback world so the UI still works without a key
        return _mock_world(prompt)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Kick off generation
        gen_resp = await client.post(
            f"{MARBLE_BASE_URL}/worlds:generate",
            headers=_headers(),
            json={
                "world_prompt": {
                    "type": "text",
                    "text_prompt": prompt,
                },
                "model": MARBLE_MODEL,
            },
        )
        gen_resp.raise_for_status()
        gen_data = gen_resp.json()

        operation_id = gen_data.get("operationId") or gen_data.get("operation_id", "")
        world_id = gen_data.get("worldId") or gen_data.get("world_id", "")

        # Step 2: Poll until done
        if operation_id:
            world_id = await _poll_operation(client, operation_id)

        # Step 3: Fetch world details
        if world_id:
            world_data = await _fetch_world(client, world_id)
        else:
            world_data = gen_data

    # Build normalised result
    result = _normalise_world(world_data, prompt)

    # Cache it
    _append_world(result)

    return result


async def _poll_operation(client: httpx.AsyncClient, operation_id: str) -> str:
    """Poll an operation until done, returning the world_id."""
    start = time.monotonic()
    while time.monotonic() - start < POLL_TIMEOUT:
        resp = await client.get(
            f"{MARBLE_BASE_URL}/operations/{operation_id}",
            headers=_headers(),
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("done"):
            # Extract world ID from the response
            result = data.get("result", data)
            return (
                result.get("worldId")
                or result.get("world_id")
                or data.get("worldId")
                or data.get("world_id")
                or ""
            )

        await asyncio.sleep(POLL_INTERVAL)

    raise TimeoutError(f"Marble operation {operation_id} timed out after {POLL_TIMEOUT}s")


async def _fetch_world(client: httpx.AsyncClient, world_id: str) -> dict[str, Any]:
    """Fetch full world details including splat asset URLs."""
    resp = await client.get(
        f"{MARBLE_BASE_URL}/worlds/{world_id}",
        headers=_headers(),
    )
    resp.raise_for_status()
    return resp.json()


def _normalise_world(data: dict[str, Any], prompt: str) -> dict[str, Any]:
    """Normalise Marble API response into a consistent shape."""
    # Try to extract splat URL from various response shapes
    splat_url = ""
    assets = data.get("assets", [])
    if isinstance(assets, list):
        for asset in assets:
            if isinstance(asset, dict):
                url = asset.get("url", "")
                if url and (".splat" in url or ".ply" in url or "splat" in asset.get("type", "")):
                    splat_url = url
                    break
                if url and not splat_url:
                    splat_url = url

    if not splat_url:
        splat_url = data.get("splat_url", "") or data.get("splatUrl", "")

    world_id = data.get("worldId") or data.get("world_id") or data.get("id", "")

    return {
        "world_id": world_id,
        "prompt": prompt,
        "splat_url": splat_url,
        "status": "completed",
        "created_at": time.time(),
        "raw": data,
    }


def _mock_world(prompt: str) -> dict[str, Any]:
    """
    Return a mock world result when no API key is available.
    The frontend will render a fallback geometric scene.
    """
    mock_id = f"mock-{int(time.time())}"
    result = {
        "world_id": mock_id,
        "prompt": prompt,
        "splat_url": "",
        "status": "completed",
        "created_at": time.time(),
        "is_mock": True,
        "raw": {},
    }
    _append_world(result)
    return result
