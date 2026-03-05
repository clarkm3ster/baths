"""
API routes for DOMES Profiles.

Profile CRUD, generation, comparison, dome visualization, and version history.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile, ProfileVersion
from .. import profile_engine

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


# ===========================================================================
# Request / Response schemas
# ===========================================================================

class GenerateRequest(BaseModel):
    circumstances: dict = Field(..., description="Dict of circumstance flags, e.g. {'is_homeless': true}")
    name: Optional[str] = Field(None, description="Human-readable name or label for the profile")


class CompareRequest(BaseModel):
    profile_ids: list[str] = Field(..., min_length=2, max_length=2, description="Two profile IDs to compare")


class UpdateRequest(BaseModel):
    circumstances: dict = Field(..., description="New or updated circumstance flags")


# ===========================================================================
# Routes
# ===========================================================================

@router.post("/generate")
async def generate_profile(body: GenerateRequest, db: Session = Depends(get_db)):
    """Generate a new profile from circumstances."""
    if not body.circumstances:
        raise HTTPException(status_code=400, detail="At least one circumstance must be provided")

    # Check that at least one circumstance is True
    active = {k: v for k, v in body.circumstances.items() if v}
    if not active:
        raise HTTPException(status_code=400, detail="At least one circumstance must be set to true")

    try:
        profile = await profile_engine.generate_profile(
            circumstances=body.circumstances,
            db=db,
            name=body.name,
        )
        return profile.to_full()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Profile generation failed: {str(exc)}")


@router.get("")
def list_profiles(
    is_sample: Optional[bool] = Query(None, description="Filter by sample status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """List profiles (summaries only, no domains)."""
    query = db.query(Profile)
    if is_sample is not None:
        query = query.filter(Profile.is_sample == is_sample)
    query = query.order_by(Profile.created_at.desc())
    total = query.count()
    profiles = query.offset(offset).limit(limit).all()
    return {
        "items": [p.to_summary() for p in profiles],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/circumstances")
def get_circumstances():
    """Return all available circumstances with labels and categories."""
    return {
        "circumstances": profile_engine.AVAILABLE_CIRCUMSTANCES,
        "categories": [
            {"key": "health", "label": "Health", "color": "#1A6B3C"},
            {"key": "justice", "label": "Justice", "color": "#8B1A1A"},
            {"key": "housing", "label": "Housing", "color": "#1A3D8B"},
            {"key": "income", "label": "Income", "color": "#6B5A1A"},
            {"key": "education", "label": "Education", "color": "#5A1A6B"},
            {"key": "child_welfare", "label": "Child Welfare", "color": "#1A6B6B"},
        ],
    }


@router.get("/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    """Get a full profile with all domains."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")
    return profile.to_full()


@router.get("/{profile_id}/dome")
def get_dome(profile_id: str, db: Session = Depends(get_db)):
    """Get the full Dome visualization structure for a profile."""
    try:
        return profile_engine.get_dome(profile_id, db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("/compare")
def compare_profiles(body: CompareRequest, db: Session = Depends(get_db)):
    """Compare two profiles side-by-side."""
    try:
        return profile_engine.compare_profiles(body.profile_ids[0], body.profile_ids[1], db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{profile_id}")
async def update_profile(
    profile_id: str,
    body: UpdateRequest,
    db: Session = Depends(get_db),
):
    """Update a profile with new circumstances."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")
    if profile.is_sample:
        raise HTTPException(status_code=400, detail="Cannot update a sample profile. Generate a new one instead.")

    try:
        updated = await profile_engine.update_profile(profile_id, body.circumstances, db)
        return updated.to_full()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(exc)}")


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    """Delete a profile (only non-sample profiles)."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")
    if profile.is_sample:
        raise HTTPException(status_code=400, detail="Cannot delete a sample profile")

    db.delete(profile)
    db.commit()
    return {"status": "deleted", "id": profile_id}


@router.get("/{profile_id}/versions")
def get_versions(profile_id: str, db: Session = Depends(get_db)):
    """Get version history for a profile."""
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile {profile_id} not found")

    versions = (
        db.query(ProfileVersion)
        .filter(ProfileVersion.profile_id == profile_id)
        .order_by(ProfileVersion.version.desc())
        .all()
    )
    return {
        "profile_id": profile_id,
        "current_version": profile.version,
        "versions": [v.to_dict() for v in versions],
    }
