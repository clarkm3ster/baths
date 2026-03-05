"""
SPHERES Studio — Marble API Router

Endpoints for generating 3D worlds via the World Labs Marble API
and listing previously generated worlds.

  POST /api/marble/generate  — Generate a new 3D world from a prompt
  GET  /api/marble/worlds    — List all cached generated worlds
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.marble import generate_world, get_cached_worlds

router = APIRouter(prefix="/api/marble", tags=["marble"])


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=2000, description="Text description of the 3D world to generate")


class WorldEntry(BaseModel):
    world_id: str
    prompt: str
    splat_url: str
    status: str
    created_at: float
    is_mock: bool = False


class GenerateResponse(BaseModel):
    world_id: str
    prompt: str
    splat_url: str
    status: str
    created_at: float
    is_mock: bool = False


class WorldsListResponse(BaseModel):
    worlds: list[WorldEntry]
    total: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/generate", response_model=GenerateResponse)
async def marble_generate(req: GenerateRequest) -> GenerateResponse:
    """
    Generate a 3D world from a text prompt using the World Labs Marble API.

    The endpoint kicks off generation, polls until completion, and returns
    the world metadata including the splat asset URL for 3D rendering.
    """
    try:
        result = await generate_world(req.prompt)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Marble API error: {exc}",
        )

    return GenerateResponse(
        world_id=result.get("world_id", ""),
        prompt=result.get("prompt", req.prompt),
        splat_url=result.get("splat_url", ""),
        status=result.get("status", "completed"),
        created_at=result.get("created_at", 0),
        is_mock=result.get("is_mock", False),
    )


@router.get("/worlds", response_model=WorldsListResponse)
async def marble_list_worlds() -> WorldsListResponse:
    """Return all previously generated worlds from the local cache."""
    worlds = get_cached_worlds()
    entries = [
        WorldEntry(
            world_id=w.get("world_id", ""),
            prompt=w.get("prompt", ""),
            splat_url=w.get("splat_url", ""),
            status=w.get("status", "unknown"),
            created_at=w.get("created_at", 0),
            is_mock=w.get("is_mock", False),
        )
        for w in worlds
    ]
    return WorldsListResponse(worlds=entries, total=len(entries))
