"""
world.py — FastAPI router for the SPHERES Studio 3D World Preview system.

Endpoints:
  POST /api/world/generate    — Generate 3D scene config from a design
  GET  /api/world/share/{id}  — Retrieve a shareable 3D preview payload
  POST /api/world/screenshot  — Accept a base64 screenshot and persist it
"""

from __future__ import annotations

import base64
import hashlib
import math
import os
import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/world", tags=["world"])

# ---------------------------------------------------------------------------
# Storage paths (configurable via env)
# ---------------------------------------------------------------------------

SCREENSHOT_DIR = Path(
    os.environ.get("SPHERES_SCREENSHOT_DIR", "/tmp/spheres-screenshots")
)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# In-memory store for shared previews (replace with DB in production)
_shared_previews: dict[str, dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class Point2D(BaseModel):
    x: float
    y: float


class Polygon2D(BaseModel):
    points: list[Point2D]


class DesignElement(BaseModel):
    id: str
    type: str
    x: float
    y: float
    width: float
    height: float
    rotation: float = 0.0
    color: str = "#888888"
    name: str = ""
    is_permanent: bool = False
    category: str = ""


class GenerateRequest(BaseModel):
    design_id: str
    elements: list[DesignElement] = Field(default_factory=list)
    parcel_polygon: Polygon2D | None = None
    parcel_width: float = 100.0
    parcel_depth: float = 80.0


class Element3DConfig(BaseModel):
    id: str
    mesh_type: str
    position: list[float]  # [x, y, z]
    rotation: list[float]  # [x, y, z] radians
    scale: list[float]  # [x, y, z]
    color: str
    name: str
    is_permanent: bool
    category: str


class CameraConfig(BaseModel):
    position: list[float]
    target: list[float]


class EnvironmentConfig(BaseModel):
    parcel_width: float
    parcel_depth: float
    parcel_center: list[float]
    parcel_polygon: list[list[float]] | None = None


class GenerateResponse(BaseModel):
    design_id: str
    elements: list[Element3DConfig]
    camera: CameraConfig
    environment: EnvironmentConfig
    share_id: str


class ScreenshotRequest(BaseModel):
    image_data: str  # base64-encoded PNG
    design_id: str = ""
    view_mode: str = "after"


class ScreenshotResponse(BaseModel):
    url: str
    filename: str


class ShareResponse(BaseModel):
    design_id: str
    elements: list[Element3DConfig]
    camera: CameraConfig
    environment: EnvironmentConfig


# ---------------------------------------------------------------------------
# Height table — same as the frontend (keep in sync)
# ---------------------------------------------------------------------------

BASE_HEIGHTS: dict[str, float] = {
    "stage_small": 3,
    "stage_medium": 4,
    "stage_large": 5,
    "sound_equipment": 5,
    "screening_wall": 12,
    "bench": 3,
    "picnic_table": 3,
    "chair_cluster": 3,
    "bleachers": 8,
    "amphitheater_seating": 6,
    "food_cart": 7,
    "food_truck_space": 9,
    "market_stall": 8,
    "vendor_tent": 9,
    "raised_bed": 2,
    "tree_planting": 15,
    "flower_garden": 1,
    "native_meadow": 2,
    "water_feature": 0.5,
    "mural_wall": 14,
    "sculpture_pad": 8,
    "interactive_art": 6,
    "art_installation": 10,
    "play_structure": 10,
    "basketball_half": 10,
    "fitness_station": 8,
    "sports_field": 0.1,
    "pathway": 0.05,
    "fencing": 6,
    "lighting_pole": 16,
    "power_hookup": 2,
    "water_hookup": 2,
    "shade_structure": 10,
    "signage": 8,
}

# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------


def _compute_parcel_center(
    polygon: Polygon2D | None, width: float, depth: float
) -> tuple[float, float]:
    """Return the center of the parcel in canvas feet."""
    if polygon and polygon.points:
        xs = [p.x for p in polygon.points]
        ys = [p.y for p in polygon.points]
        return (
            (min(xs) + max(xs)) / 2,
            (min(ys) + max(ys)) / 2,
        )
    return width / 2, depth / 2


def _element_to_3d(
    el: DesignElement, center_x: float, center_y: float
) -> Element3DConfig:
    """Convert a single 2D design element to 3D config."""
    mesh_type = el.type
    base_height = BASE_HEIGHTS.get(mesh_type, 4.0)

    cx = el.x + el.width / 2
    cy = el.y + el.height / 2

    px = cx - center_x
    py = base_height / 2
    pz = cy - center_y

    rot_y = -(el.rotation * math.pi) / 180

    return Element3DConfig(
        id=el.id,
        mesh_type=mesh_type,
        position=[round(px, 3), round(py, 3), round(pz, 3)],
        rotation=[0, round(rot_y, 5), 0],
        scale=[1.0, 1.0, 1.0],
        color=el.color,
        name=el.name or mesh_type.replace("_", " "),
        is_permanent=el.is_permanent,
        category=el.category or "other",
    )


def _camera_for_parcel(width: float, depth: float) -> CameraConfig:
    """Return a sensible default camera for the given parcel size."""
    max_dim = max(width, depth)
    altitude = max(max_dim * 0.8, 30)
    pullback = max(max_dim * 0.5, 20)
    return CameraConfig(
        position=[round(-pullback, 2), round(altitude, 2), round(-pullback, 2)],
        target=[0, 0, 0],
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/generate", response_model=GenerateResponse)
async def generate_world(req: GenerateRequest) -> GenerateResponse:
    """
    Generate a full 3D scene configuration from a design.

    Takes the flat 2D element list and parcel geometry and returns
    positioned, rotated, scaled 3D element configs plus camera and
    environment settings.
    """
    center_x, center_y = _compute_parcel_center(
        req.parcel_polygon, req.parcel_width, req.parcel_depth
    )

    elements_3d = [_element_to_3d(el, center_x, center_y) for el in req.elements]

    camera = _camera_for_parcel(req.parcel_width, req.parcel_depth)

    polygon_raw: list[list[float]] | None = None
    if req.parcel_polygon:
        polygon_raw = [[p.x, p.y] for p in req.parcel_polygon.points]

    env = EnvironmentConfig(
        parcel_width=req.parcel_width,
        parcel_depth=req.parcel_depth,
        parcel_center=[center_x, center_y],
        parcel_polygon=polygon_raw,
    )

    share_id = hashlib.sha256(
        f"{req.design_id}-{time.time()}".encode()
    ).hexdigest()[:12]

    response = GenerateResponse(
        design_id=req.design_id,
        elements=elements_3d,
        camera=camera,
        environment=env,
        share_id=share_id,
    )

    # Cache for sharing
    _shared_previews[share_id] = response.model_dump()

    return response


@router.get("/share/{share_id}", response_model=ShareResponse)
async def get_shared_preview(share_id: str) -> ShareResponse:
    """Retrieve a previously generated shareable 3D preview."""
    data = _shared_previews.get(share_id)
    if not data:
        raise HTTPException(status_code=404, detail="Preview not found or expired")

    return ShareResponse(
        design_id=data["design_id"],
        elements=[Element3DConfig(**el) for el in data["elements"]],
        camera=CameraConfig(**data["camera"]),
        environment=EnvironmentConfig(**data["environment"]),
    )


@router.post("/screenshot", response_model=ScreenshotResponse)
async def save_screenshot(req: ScreenshotRequest) -> ScreenshotResponse:
    """
    Accept a base64-encoded PNG screenshot from the 3D view and persist
    it to disk. Returns the URL path to the saved image.
    """
    # Strip data URL prefix if present
    raw = req.image_data
    if "," in raw:
        raw = raw.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(raw)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid base64 data: {exc}")

    filename = f"spheres-{req.view_mode}-{uuid.uuid4().hex[:8]}.png"
    filepath = SCREENSHOT_DIR / filename

    filepath.write_bytes(image_bytes)

    url = f"/api/world/screenshots/{filename}"

    return ScreenshotResponse(url=url, filename=filename)
