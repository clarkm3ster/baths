"""
SPHERES — World Labs Marble API Client
=======================================
Generates 3D Gaussian splat worlds via the Marble API, one per episode.
Caches world IDs and splat URLs in marble_cache.json so we only generate once.

World Labs Marble API:
  Base URL: https://api.worldlabs.ai/marble/v1
  Auth:     WLT-Api-Key header
  Generate: POST /worlds:generate
  Poll:     GET /operations/{operationId}
  Get:      GET /worlds/{worldId}
"""

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Optional

import httpx

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MARBLE_BASE = "https://api.worldlabs.ai/marble/v1"
MARBLE_MODEL = "Marble 0.1-mini"
CACHE_PATH = Path(__file__).parent / "marble_cache.json"
POLL_INTERVAL = 5  # seconds between operation polls
POLL_TIMEOUT = 300  # max seconds to wait for a world to generate

# ---------------------------------------------------------------------------
# Episode prompts — one per episode, mapped by episode number (1-10)
# ---------------------------------------------------------------------------

EPISODE_PROMPTS: dict[int, dict] = {
    1: {
        "slug": "waterfront",
        "title": "Waterfront Theater",
        "prompt": (
            "An open-air amphitheater built on a Philadelphia river pier. "
            "Wooden stage over water, string lights, audience seats made from "
            "reclaimed lumber. Sunset light on the Delaware River."
        ),
    },
    2: {
        "slug": "cinema-garden",
        "title": "Cinema Garden",
        "prompt": (
            "An outdoor cinema in a transformed vacant lot in Philadelphia. "
            "Large inflatable screen, wildflower garden surrounding scattered "
            "blankets and lawn chairs. Evening twilight, fireflies."
        ),
    },
    3: {
        "slug": "rooftop",
        "title": "Rooftop Skate Park",
        "prompt": (
            "A rooftop skatepark on top of a converted Philadelphia warehouse. "
            "Concrete bowls and ramps, graffiti murals, city skyline in the "
            "background. Golden hour light."
        ),
    },
    4: {
        "slug": "alley",
        "title": "Art Alley",
        "prompt": (
            "A narrow Philadelphia alley transformed into an immersive art "
            "gallery. Murals on every surface, hanging sculptures, neon "
            "installations, mosaic ground. Night with dramatic uplighting."
        ),
    },
    5: {
        "slug": "sound-garden",
        "title": "Sound Garden",
        "prompt": (
            "A garden of musical instruments built from salvaged materials in "
            "a Philadelphia vacant lot. Wind chimes, aeolian harps, percussion "
            "walls, metal sound sculptures. Morning mist."
        ),
    },
    6: {
        "slug": "underpass",
        "title": "Climbing Gym Underpass",
        "prompt": (
            "A rock climbing gym built under a Philadelphia highway overpass. "
            "Colorful climbing holds on concrete pillars, crash pads, chalk "
            "dust in the air. Industrial urban setting."
        ),
    },
    7: {
        "slug": "night-market",
        "title": "Night Market",
        "prompt": (
            "A vibrant night market in a Philadelphia vacant lot. Food stalls "
            "with string lights, steam rising from grills, crowds browsing "
            "vendor tables. Lanterns and neon signs."
        ),
    },
    8: {
        "slug": "winter-village",
        "title": "Winter Village",
        "prompt": (
            "A winter village pop-up in a Philadelphia park. Small wooden "
            "chalets, ice skating rink, twinkling holiday lights, snow on the "
            "ground. Warm glow from cabin windows."
        ),
    },
    9: {
        "slug": "glow-corridor",
        "title": "Skating Corridor",
        "prompt": (
            "A long narrow ice skating path through a Philadelphia alley "
            "between buildings. Fairy lights overhead, brick walls on both "
            "sides, skaters gliding. Twilight blue hour."
        ),
    },
    10: {
        "slug": "quiet-garden",
        "title": "Recovery Garden",
        "prompt": (
            "A peaceful therapeutic garden in a Philadelphia vacant lot. "
            "Meditation circles, native plantings, water feature, wooden "
            "benches, winding gravel paths. Soft morning light."
        ),
    },
}


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

def load_cache() -> dict:
    """Load the marble_cache.json file. Returns empty dict if missing."""
    if CACHE_PATH.exists():
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache: dict) -> None:
    """Write the cache dict to marble_cache.json."""
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


# ---------------------------------------------------------------------------
# Marble API helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    """Build request headers with the Marble API key."""
    api_key = os.environ.get("MARBLE_API_KEY", "")
    return {
        "Content-Type": "application/json",
        "WLT-Api-Key": api_key,
    }


async def generate_world(client: httpx.AsyncClient, prompt: str) -> str:
    """
    POST /worlds:generate — kicks off world generation.
    Returns the operationId to poll.
    """
    body = {
        "world_prompt": {
            "type": "text",
            "text_prompt": prompt,
        },
        "model": MARBLE_MODEL,
    }
    resp = await client.post(
        f"{MARBLE_BASE}/worlds:generate",
        json=body,
        headers=_headers(),
        timeout=30.0,
    )
    resp.raise_for_status()
    data = resp.json()
    # The response contains an operation object with an id
    return data.get("operationId") or data.get("operation_id") or data["name"]


async def poll_operation(
    client: httpx.AsyncClient, operation_id: str
) -> dict:
    """
    GET /operations/{operationId} — poll until done=true.
    Returns the completed operation payload (which contains worldId).
    """
    start = time.time()
    while True:
        if time.time() - start > POLL_TIMEOUT:
            raise TimeoutError(
                f"Operation {operation_id} did not complete within "
                f"{POLL_TIMEOUT}s"
            )
        resp = await client.get(
            f"{MARBLE_BASE}/operations/{operation_id}",
            headers=_headers(),
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()

        if data.get("done"):
            return data

        await asyncio.sleep(POLL_INTERVAL)


async def get_world(client: httpx.AsyncClient, world_id: str) -> dict:
    """
    GET /worlds/{worldId} — fetch world details including splat asset URLs.
    """
    resp = await client.get(
        f"{MARBLE_BASE}/worlds/{world_id}",
        headers=_headers(),
        timeout=30.0,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# High-level: generate one episode world
# ---------------------------------------------------------------------------

async def generate_episode_world(
    client: httpx.AsyncClient, episode_num: int
) -> dict:
    """
    Generate a single episode world end-to-end:
      1. POST generate
      2. Poll until complete
      3. GET world details
      4. Return world data with splat URLs
    """
    ep = EPISODE_PROMPTS[episode_num]
    operation_id = await generate_world(client, ep["prompt"])
    operation = await poll_operation(client, operation_id)

    # Extract world ID from the operation result
    world_id = (
        operation.get("worldId")
        or operation.get("world_id")
        or operation.get("result", {}).get("worldId")
        or operation.get("result", {}).get("world_id")
        or operation.get("metadata", {}).get("worldId")
    )
    if not world_id:
        raise ValueError(
            f"Could not extract worldId from operation: {operation}"
        )

    world = await get_world(client, world_id)
    return world


# ---------------------------------------------------------------------------
# High-level: generate all 10 worlds (with caching)
# ---------------------------------------------------------------------------

async def generate_all_worlds(force: bool = False) -> dict:
    """
    Generate all 10 episode worlds. Skips episodes that already have a
    cached entry in marble_cache.json (unless force=True).

    Returns the full cache dict.
    """
    cache = load_cache()

    async with httpx.AsyncClient() as client:
        for ep_num in range(1, 11):
            key = str(ep_num)
            if not force and key in cache and cache[key].get("world_id"):
                continue  # already generated

            ep = EPISODE_PROMPTS[ep_num]
            try:
                world = await generate_episode_world(client, ep_num)

                # Extract splat URL(s) from world data
                splat_url = _extract_splat_url(world)

                cache[key] = {
                    "episode_num": ep_num,
                    "slug": ep["slug"],
                    "title": ep["title"],
                    "world_id": world.get("worldId") or world.get("id") or world.get("world_id"),
                    "splat_url": splat_url,
                    "world_data": world,
                    "generated_at": time.time(),
                    "status": "ready",
                }
            except Exception as exc:
                cache[key] = {
                    "episode_num": ep_num,
                    "slug": ep["slug"],
                    "title": ep["title"],
                    "world_id": None,
                    "splat_url": None,
                    "error": str(exc),
                    "generated_at": time.time(),
                    "status": "error",
                }

            # Save after each world so partial progress is preserved
            save_cache(cache)

    return cache


def _extract_splat_url(world: dict) -> Optional[str]:
    """
    Extract the Gaussian splat asset URL from a world response.
    The exact structure depends on the API response; we try common paths.
    """
    # Try direct field
    if "splat_url" in world:
        return world["splat_url"]
    if "splatUrl" in world:
        return world["splatUrl"]

    # Try assets array
    assets = world.get("assets") or world.get("outputs") or []
    if isinstance(assets, list):
        for asset in assets:
            url = asset.get("url") or asset.get("splatUrl") or asset.get("splat_url")
            if url:
                return url

    # Try nested result
    result = world.get("result", {})
    if isinstance(result, dict):
        if "splat_url" in result:
            return result["splat_url"]
        if "splatUrl" in result:
            return result["splatUrl"]

    return None


# ---------------------------------------------------------------------------
# Retrieval helpers (used by routes)
# ---------------------------------------------------------------------------

def get_cached_worlds() -> list[dict]:
    """Return all cached worlds as a list, sorted by episode number."""
    cache = load_cache()
    worlds = []
    for ep_num in range(1, 11):
        key = str(ep_num)
        if key in cache:
            worlds.append(cache[key])
        else:
            # Return placeholder for uncached episodes
            ep = EPISODE_PROMPTS[ep_num]
            worlds.append({
                "episode_num": ep_num,
                "slug": ep["slug"],
                "title": ep["title"],
                "world_id": None,
                "splat_url": None,
                "status": "pending",
            })
    return worlds


def get_cached_world(episode_num: int) -> Optional[dict]:
    """Return a single cached world by episode number."""
    cache = load_cache()
    key = str(episode_num)
    if key in cache:
        return cache[key]
    if episode_num in EPISODE_PROMPTS:
        ep = EPISODE_PROMPTS[episode_num]
        return {
            "episode_num": episode_num,
            "slug": ep["slug"],
            "title": ep["title"],
            "world_id": None,
            "splat_url": None,
            "status": "pending",
        }
    return None
