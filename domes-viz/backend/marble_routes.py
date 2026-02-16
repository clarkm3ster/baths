"""
FastAPI routes for World Labs Marble integration.

GET  /api/marble/worlds   — return cached (or generated) worlds
POST /api/marble/generate — generate a new world from a custom prompt
"""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from marble import (
    generate_world,
    get_world,
    load_cache,
    poll_operation,
    save_cache,
    seed_worlds,
    WORLD_TITLES,
    _extract_splat_url,
    _fallback_world,
)

logger = logging.getLogger("marble_routes")

router = APIRouter()


# ──────────────────────────────────────────────────────────────
# GET /api/marble/worlds
# ──────────────────────────────────────────────────────────────


@router.get("/marble/worlds")
async def get_worlds():
    """
    Return all cached Marble worlds.
    If no cache exists, trigger generation and return the results.
    """
    cache = load_cache()
    if cache:
        return {"worlds": cache["worlds"]}

    # No cache — generate on demand
    try:
        worlds = await seed_worlds()
        return {"worlds": worlds}
    except Exception as exc:
        logger.error("Failed to seed worlds: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Marble API error: {exc}",
        )


# ──────────────────────────────────────────────────────────────
# POST /api/marble/generate
# ──────────────────────────────────────────────────────────────


class GenerateRequest(BaseModel):
    prompt: str
    key: str | None = None
    title: str | None = None


@router.post("/marble/generate")
async def generate_new_world(req: GenerateRequest):
    """
    Generate a brand-new Marble world from an arbitrary prompt.
    Optionally provide a key and title; otherwise they are auto-assigned.
    """
    try:
        op_response = await generate_world(req.prompt)
        operation_id = (
            op_response.get("operationId")
            or op_response.get("operation_id")
            or op_response.get("name", "")
        )

        if not operation_id:
            raise HTTPException(
                status_code=502,
                detail="Marble API did not return an operationId",
            )

        completed = await poll_operation(operation_id)

        world_id = (
            completed.get("worldId")
            or completed.get("world_id")
            or completed.get("metadata", {}).get("worldId", "")
            or completed.get("response", {}).get("worldId", "")
        )

        details = {}
        if world_id:
            try:
                details = await get_world(world_id)
            except Exception as exc:
                logger.warning("Could not fetch world details: %s", exc)

        key = req.key or f"custom-{operation_id[:8]}"
        title = req.title or "Custom World"

        world_entry = {
            "key": key,
            "title": title,
            "prompt": req.prompt,
            "worldId": world_id or "",
            "operationId": operation_id,
            "details": details,
            "splatUrl": _extract_splat_url(details),
        }

        # Append to cache
        cache = load_cache()
        worlds = cache["worlds"] if cache else []
        worlds.append(world_entry)
        save_cache(worlds)

        return {"world": world_entry}

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Generate failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"Marble API error: {exc}",
        )
