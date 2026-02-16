"""
SPHERES — Marble World Routes
===============================
API endpoints for World Labs Marble 3D worlds.

GET  /api/marble/worlds             — list all 10 cached worlds
GET  /api/marble/worlds/{episode_num} — get a single world by episode number
POST /api/marble/generate           — trigger generation of all worlds (admin)
POST /api/marble/generate/{episode_num} — trigger generation of one world
"""

import os
from fastapi import APIRouter, HTTPException, BackgroundTasks

from marble import (
    get_cached_worlds,
    get_cached_world,
    generate_all_worlds,
    generate_episode_world,
    load_cache,
    save_cache,
    EPISODE_PROMPTS,
    _extract_splat_url,
)

router = APIRouter(prefix="/api/marble", tags=["marble"])


@router.get("/worlds")
def list_worlds():
    """
    Return all 10 episode worlds from cache.
    Each entry includes: episode_num, slug, title, world_id, splat_url, status.
    """
    return get_cached_worlds()


@router.get("/worlds/{episode_num}")
def get_world(episode_num: int):
    """
    Return a single cached world by episode number (1-10).
    """
    if episode_num < 1 or episode_num > 10:
        raise HTTPException(
            status_code=400,
            detail="Episode number must be between 1 and 10.",
        )
    world = get_cached_world(episode_num)
    if world is None:
        raise HTTPException(
            status_code=404,
            detail=f"No world found for episode {episode_num}.",
        )
    return world


@router.post("/generate")
async def trigger_generate_all(background_tasks: BackgroundTasks):
    """
    Trigger generation of all 10 worlds in the background.
    Returns immediately with a status message.
    Requires MARBLE_API_KEY environment variable.
    """
    api_key = os.environ.get("MARBLE_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="MARBLE_API_KEY not configured. Set the environment variable to enable world generation.",
        )

    background_tasks.add_task(generate_all_worlds)
    return {
        "status": "generating",
        "message": "World generation started for all 10 episodes. Poll GET /api/marble/worlds to check progress.",
    }


@router.post("/generate/{episode_num}")
async def trigger_generate_one(
    episode_num: int, background_tasks: BackgroundTasks
):
    """
    Trigger generation of a single episode world in the background.
    """
    if episode_num < 1 or episode_num > 10:
        raise HTTPException(
            status_code=400,
            detail="Episode number must be between 1 and 10.",
        )

    api_key = os.environ.get("MARBLE_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="MARBLE_API_KEY not configured.",
        )

    async def _generate_single():
        import httpx
        import time

        cache = load_cache()
        ep = EPISODE_PROMPTS[episode_num]
        async with httpx.AsyncClient() as client:
            try:
                world = await generate_episode_world(client, episode_num)
                splat_url = _extract_splat_url(world)
                cache[str(episode_num)] = {
                    "episode_num": episode_num,
                    "slug": ep["slug"],
                    "title": ep["title"],
                    "world_id": world.get("worldId") or world.get("id") or world.get("world_id"),
                    "splat_url": splat_url,
                    "world_data": world,
                    "generated_at": time.time(),
                    "status": "ready",
                }
            except Exception as exc:
                cache[str(episode_num)] = {
                    "episode_num": episode_num,
                    "slug": ep["slug"],
                    "title": ep["title"],
                    "world_id": None,
                    "splat_url": None,
                    "error": str(exc),
                    "generated_at": time.time(),
                    "status": "error",
                }
            save_cache(cache)

    background_tasks.add_task(_generate_single)
    return {
        "status": "generating",
        "message": f"World generation started for episode {episode_num}.",
    }
