"""
SPHERES Studio — Timeline API Routes

FastAPI router providing endpoints for timeline generation, retrieval,
update, and Philadelphia city event conflict detection.

Endpoints
---------
POST   /api/timeline/generate     Generate a timeline from a design
GET    /api/timeline/conflicts    Check for city event conflicts
GET    /api/timeline/{id}         Retrieve a saved timeline
PUT    /api/timeline/{id}         Update a timeline
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models.timeline import (
    ConflictReport,
    Timeline,
    TimelineGenerateRequest,
    TimelineUpdateRequest,
)
from services.timeline_generator import TimelineGenerator

router = APIRouter(prefix="/api/timeline", tags=["timeline"])

# In-memory store (swap for a database in production)
_timelines: dict[str, Timeline] = {}

# Singleton generator
_generator = TimelineGenerator()


# ---------------------------------------------------------------------------
# POST /api/timeline/generate
# ---------------------------------------------------------------------------

@router.post("/generate", response_model=Timeline)
async def generate_timeline(req: TimelineGenerateRequest) -> Timeline:
    """
    Accept a design specification and target activation date, then return a
    fully-phased project timeline with tasks, dependencies, milestones, and
    season/weather intelligence.
    """
    timeline = _generator.generate_timeline(
        design=req.design,
        target_activation_date=req.target_activation_date,
        duration_days=req.duration_days,
    )
    # Persist
    _timelines[timeline.id] = timeline
    return timeline


# ---------------------------------------------------------------------------
# GET /api/timeline/conflicts
# ---------------------------------------------------------------------------

@router.get("/conflicts", response_model=ConflictReport)
async def check_conflicts(
    start_date: date = Query(..., description="Start of the date range to check"),
    end_date: date = Query(..., description="End of the date range to check"),
    location: str = Query("Philadelphia, PA", description="City / location"),
) -> ConflictReport:
    """
    Check a date range against the Philadelphia city event calendar and return
    any overlapping events with their conflict severity and impact notes.
    """
    if end_date < start_date:
        raise HTTPException(
            status_code=422,
            detail="end_date must be on or after start_date",
        )
    return _generator.check_conflicts(
        start_date=start_date,
        end_date=end_date,
        location=location,
    )


# ---------------------------------------------------------------------------
# GET /api/timeline/{id}
# ---------------------------------------------------------------------------

@router.get("/{timeline_id}", response_model=Timeline)
async def get_timeline(timeline_id: str) -> Timeline:
    """Retrieve a previously generated and saved timeline by its ID."""
    timeline = _timelines.get(timeline_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="Timeline not found")
    return timeline


# ---------------------------------------------------------------------------
# PUT /api/timeline/{id}
# ---------------------------------------------------------------------------

@router.put("/{timeline_id}", response_model=Timeline)
async def update_timeline(
    timeline_id: str,
    req: TimelineUpdateRequest,
) -> Timeline:
    """
    Update an existing timeline.  You can change the task list (to adjust
    dates, assignments, or statuses), the target activation date, or the
    timeline name.
    """
    timeline = _timelines.get(timeline_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="Timeline not found")

    if req.name is not None:
        timeline.name = req.name

    if req.target_activation_date is not None:
        timeline.target_activation_date = req.target_activation_date

    if req.tasks is not None:
        timeline.tasks = req.tasks
        # Recompute total duration
        all_dates = [t.start_date for t in timeline.tasks] + [
            t.end_date for t in timeline.tasks
        ]
        if all_dates:
            earliest = min(all_dates)
            latest = max(all_dates)
            timeline.total_duration_days = (latest - earliest).days + 1

    _timelines[timeline_id] = timeline
    return timeline
