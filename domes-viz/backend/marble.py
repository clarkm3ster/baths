"""
World Labs Marble API client for domes-viz.

Generates and manages 3D walkable worlds using the Marble API,
with local JSON caching so worlds load instantly on repeat visits.
"""

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger("marble")

# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────

MARBLE_BASE_URL = "https://api.worldlabs.ai/marble/v1"
MARBLE_API_KEY = os.environ.get("MARBLE_API_KEY", "")
MARBLE_MODEL = "Marble 0.1-mini"
CACHE_FILE = Path(__file__).parent / "marble_cache.json"
POLL_INTERVAL = 5  # seconds between operation polls
POLL_TIMEOUT = 300  # max seconds to wait for generation

# The three canonical domes
WORLD_PROMPTS: dict[str, str] = {
    "renaissance": (
        "A grand Renaissance dome interior with golden afternoon light streaming "
        "through an oculus. Frescoes on the curved ceiling depict the human figure "
        "at the center of the cosmos. Marble columns, warm stone, a single person "
        "standing in the center looking up."
    ),
    "broken-capitol": (
        "A decaying government Capitol rotunda interior, cracked plaster walls, "
        "harsh fluorescent lighting, a single plastic chair in the center, a "
        "'TAKE A NUMBER' paper ticket dispenser on a metal stand. Institutional "
        "decay, bureaucratic nightmare."
    ),
    "personal-dome": (
        "A futuristic personal dome structure made of curved glass and brushed "
        "steel, flooded with natural daylight. Holographic data panels float in "
        "the air glowing blue. Living plants grow along the interior walls. One "
        "person works at a minimal desk."
    ),
}

WORLD_TITLES: dict[str, str] = {
    "renaissance": "The Human Dome",
    "broken-capitol": "The Broken Dome",
    "personal-dome": "The Future Dome",
}


# ──────────────────────────────────────────────────────────────
# HTTP helpers
# ──────────────────────────────────────────────────────────────


def _headers() -> dict[str, str]:
    return {
        "WLT-Api-Key": MARBLE_API_KEY,
        "Content-Type": "application/json",
    }


async def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=MARBLE_BASE_URL,
        headers=_headers(),
        timeout=60.0,
    )


# ──────────────────────────────────────────────────────────────
# Core API functions
# ──────────────────────────────────────────────────────────────


async def generate_world(prompt: str) -> dict[str, Any]:
    """
    POST /worlds:generate — kicks off world generation.
    Returns the operation object with operationId.
    """
    async with await _client() as client:
        body = {
            "world_prompt": {
                "type": "text",
                "text_prompt": prompt,
            },
            "model": MARBLE_MODEL,
        }
        resp = await client.post("/worlds:generate", json=body)
        resp.raise_for_status()
        return resp.json()


async def poll_operation(operation_id: str) -> dict[str, Any]:
    """
    GET /operations/{operationId} — polls until done=true or timeout.
    Returns the completed operation object.
    """
    async with await _client() as client:
        start = time.time()
        while True:
            resp = await client.get(f"/operations/{operation_id}")
            resp.raise_for_status()
            data = resp.json()

            if data.get("done"):
                logger.info("Operation %s completed", operation_id)
                return data

            elapsed = time.time() - start
            if elapsed > POLL_TIMEOUT:
                raise TimeoutError(
                    f"Operation {operation_id} did not complete within {POLL_TIMEOUT}s"
                )

            logger.debug(
                "Operation %s not done (%.0fs elapsed), polling again in %ds...",
                operation_id,
                elapsed,
                POLL_INTERVAL,
            )
            await asyncio.sleep(POLL_INTERVAL)


async def get_world(world_id: str) -> dict[str, Any]:
    """
    GET /worlds/{worldId} — returns world details including splat asset URLs.
    """
    async with await _client() as client:
        resp = await client.get(f"/worlds/{world_id}")
        resp.raise_for_status()
        return resp.json()


# ──────────────────────────────────────────────────────────────
# Cache management
# ──────────────────────────────────────────────────────────────


def load_cache() -> dict[str, Any] | None:
    """Load cached world data from marble_cache.json, or return None."""
    if CACHE_FILE.exists():
        try:
            data = json.loads(CACHE_FILE.read_text())
            if isinstance(data, dict) and "worlds" in data:
                logger.info("Loaded %d cached worlds", len(data["worlds"]))
                return data
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("Cache file corrupt, ignoring: %s", exc)
    return None


def save_cache(worlds: list[dict[str, Any]]) -> None:
    """Persist world data to marble_cache.json."""
    payload = {"worlds": worlds, "generated_at": time.time()}
    CACHE_FILE.write_text(json.dumps(payload, indent=2))
    logger.info("Saved %d worlds to cache", len(worlds))


# ──────────────────────────────────────────────────────────────
# Seed: generate all 3 worlds
# ──────────────────────────────────────────────────────────────


async def _generate_single_world(key: str, prompt: str) -> dict[str, Any]:
    """Generate one world end-to-end: trigger, poll, fetch details."""
    logger.info("Generating world '%s'...", key)

    # Step 1: kick off generation
    op_response = generate_world_response = await generate_world(prompt)
    operation_id = (
        op_response.get("operationId")
        or op_response.get("operation_id")
        or op_response.get("name", "")
    )

    if not operation_id:
        raise ValueError(
            f"No operationId in generate response: {generate_world_response}"
        )

    # Step 2: poll until done
    completed_op = await poll_operation(operation_id)

    # Step 3: extract worldId and fetch full details
    world_id = (
        completed_op.get("worldId")
        or completed_op.get("world_id")
        or completed_op.get("metadata", {}).get("worldId", "")
        or completed_op.get("response", {}).get("worldId", "")
    )

    world_details: dict[str, Any] = {}
    if world_id:
        try:
            world_details = await get_world(world_id)
        except Exception as exc:
            logger.warning("Could not fetch world details for %s: %s", world_id, exc)

    return {
        "key": key,
        "title": WORLD_TITLES[key],
        "prompt": prompt,
        "worldId": world_id or "",
        "operationId": operation_id,
        "details": world_details,
        "splatUrl": _extract_splat_url(world_details),
    }


def _extract_splat_url(details: dict[str, Any]) -> str:
    """Try to pull the .splat asset URL from world details."""
    # The API may nest this in various places — try common patterns
    for key in ("splatUrl", "splat_url", "assets", "url"):
        val = details.get(key)
        if isinstance(val, str) and val:
            return val
        if isinstance(val, dict):
            for inner_key in ("splat", "splatUrl", "url"):
                inner = val.get(inner_key)
                if isinstance(inner, str) and inner:
                    return inner
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    u = item.get("url") or item.get("splatUrl") or ""
                    if u:
                        return u
                elif isinstance(item, str) and ".splat" in item:
                    return item
    return ""


async def seed_worlds() -> list[dict[str, Any]]:
    """
    Generate all 3 canonical worlds. Called on startup if no cache exists.
    Returns list of world data dicts.
    """
    if not MARBLE_API_KEY:
        logger.warning(
            "MARBLE_API_KEY not set — skipping world generation. "
            "Fallback geometric scenes will be used."
        )
        return _fallback_worlds()

    worlds: list[dict[str, Any]] = []
    for key, prompt in WORLD_PROMPTS.items():
        try:
            world = await _generate_single_world(key, prompt)
            worlds.append(world)
        except Exception as exc:
            logger.error("Failed to generate world '%s': %s", key, exc)
            worlds.append(_fallback_world(key))

    save_cache(worlds)
    return worlds


def _fallback_world(key: str) -> dict[str, Any]:
    """Return a placeholder entry when API generation fails."""
    return {
        "key": key,
        "title": WORLD_TITLES[key],
        "prompt": WORLD_PROMPTS[key],
        "worldId": "",
        "operationId": "",
        "details": {},
        "splatUrl": "",
        "fallback": True,
    }


def _fallback_worlds() -> list[dict[str, Any]]:
    """Return all 3 placeholder entries."""
    worlds = [_fallback_world(key) for key in WORLD_PROMPTS]
    save_cache(worlds)
    return worlds


# ──────────────────────────────────────────────────────────────
# Startup hook
# ──────────────────────────────────────────────────────────────


async def ensure_worlds_ready() -> list[dict[str, Any]]:
    """
    Called at app startup. Returns cached worlds or generates fresh ones.
    """
    cache = load_cache()
    if cache:
        return cache["worlds"]

    logger.info("No cache found — generating worlds from Marble API...")
    return await seed_worlds()
