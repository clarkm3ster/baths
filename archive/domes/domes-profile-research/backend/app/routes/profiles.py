from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CompositeProfile
from ..profile_builder import build_profile

router = APIRouter(prefix="/api/profiles", tags=["profiles"])


@router.post("/generate")
def generate_profile(body: dict, db: Session = Depends(get_db)):
    circumstances = body.get("circumstances", {})
    return build_profile(db, circumstances)


@router.get("/{profile_id}")
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(CompositeProfile).filter(CompositeProfile.id == profile_id).first()
    if not profile:
        return {"error": "Profile not found"}
    return profile.to_dict()
