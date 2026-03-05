"""
SPHERES Studio — Design API Router

Endpoints for creating, reading, updating, deleting, listing,
and duplicating activation designs.  Uses an in-memory store (dict)
as the persistence layer; swap for a real database in production.
"""

from __future__ import annotations

import math
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models.design import (
    Design,
    DesignCreate,
    DesignSummary,
    DesignUpdate,
    PaginatedDesigns,
)
from models.elements import ELEMENT_LIBRARY, ElementCategory

router = APIRouter(prefix="/api/designs", tags=["designs"])

# ---------------------------------------------------------------------------
# In-memory design store (replace with DB in production)
# ---------------------------------------------------------------------------

_designs: dict[str, Design] = {}


def _to_summary(d: Design) -> DesignSummary:
    return DesignSummary(
        id=d.id,
        name=d.name,
        description=d.description,
        parcel_id=d.parcel_id,
        element_count=len(d.elements),
        created_at=d.created_at,
        updated_at=d.updated_at,
        author_id=d.author_id,
        is_public=d.is_public,
        tags=d.tags,
        thumbnail_url=d.thumbnail_url,
    )


# ---------------------------------------------------------------------------
# Element library catalog
# ---------------------------------------------------------------------------

@router.get("/elements")
def list_elements(category: Optional[ElementCategory] = Query(default=None)):
    """Return the full element library, optionally filtered by category."""
    elements = ELEMENT_LIBRARY
    if category is not None:
        elements = [e for e in elements if e.category == category]
    return [e.model_dump() for e in elements]


# ---------------------------------------------------------------------------
# Design CRUD
# ---------------------------------------------------------------------------

@router.post("/save", status_code=201)
def save_design(payload: DesignCreate) -> Design:
    """Create and persist a new design."""
    now = datetime.now(timezone.utc)
    design = Design(
        id=uuid.uuid4().hex,
        name=payload.name,
        description=payload.description,
        parcel_id=payload.parcel_id,
        parcel_footprint=payload.parcel_footprint,
        elements=payload.elements,
        created_at=now,
        updated_at=now,
        author_id=payload.author_id,
        is_public=payload.is_public,
        tags=payload.tags,
    )
    _designs[design.id] = design
    return design


@router.get("/{design_id}")
def get_design(design_id: str) -> Design:
    """Load a single design by its ID."""
    design = _designs.get(design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.get("")
def list_designs(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    author_id: Optional[str] = Query(default=None),
    tag: Optional[str] = Query(default=None),
    is_public: Optional[bool] = Query(default=None),
) -> PaginatedDesigns:
    """List all designs with optional filters and pagination."""
    results = list(_designs.values())

    # Filters
    if author_id is not None:
        results = [d for d in results if d.author_id == author_id]
    if tag is not None:
        results = [d for d in results if tag in d.tags]
    if is_public is not None:
        results = [d for d in results if d.is_public == is_public]

    # Sort newest first
    results.sort(key=lambda d: d.updated_at, reverse=True)

    total = len(results)
    total_pages = max(1, math.ceil(total / page_size))
    start = (page - 1) * page_size
    page_items = results[start : start + page_size]

    return PaginatedDesigns(
        items=[_to_summary(d) for d in page_items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put("/{design_id}")
def update_design(design_id: str, payload: DesignUpdate) -> Design:
    """Update an existing design.  Only supplied fields are changed."""
    design = _designs.get(design_id)
    if design is None:
        raise HTTPException(status_code=404, detail="Design not found")

    update_data = payload.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(design, field, value)

    design.updated_at = datetime.now(timezone.utc)
    _designs[design_id] = design
    return design


@router.delete("/{design_id}", status_code=204)
def delete_design(design_id: str) -> None:
    """Delete a design by ID."""
    if design_id not in _designs:
        raise HTTPException(status_code=404, detail="Design not found")
    del _designs[design_id]


@router.post("/{design_id}/duplicate", status_code=201)
def duplicate_design(design_id: str) -> Design:
    """Create a deep copy of an existing design with a new ID and timestamp."""
    original = _designs.get(design_id)
    if original is None:
        raise HTTPException(status_code=404, detail="Design not found")

    now = datetime.now(timezone.utc)
    duplicate = deepcopy(original)
    duplicate.id = uuid.uuid4().hex
    duplicate.name = f"{original.name} (Copy)"
    duplicate.created_at = now
    duplicate.updated_at = now

    # Give each element instance a fresh ID
    for el in duplicate.elements:
        el.instance_id = uuid.uuid4().hex[:12]

    _designs[duplicate.id] = duplicate
    return duplicate
