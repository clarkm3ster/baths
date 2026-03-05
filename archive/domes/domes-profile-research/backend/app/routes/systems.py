from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import SystemProfile

router = APIRouter(prefix="/api/systems", tags=["systems"])


@router.get("")
def list_systems(db: Session = Depends(get_db)):
    return [s.to_dict() for s in db.query(SystemProfile).all()]


@router.get("/{system_id}")
def get_system(system_id: str, db: Session = Depends(get_db)):
    s = db.query(SystemProfile).filter(SystemProfile.id == system_id).first()
    if not s:
        return {"error": "System not found"}
    return s.to_dict()
