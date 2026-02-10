"""Value calculation routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.value import static_value, activation_value, leveraged_value

router = APIRouter(prefix="/api/value", tags=["value"])


@router.get("/static")
def get_static_value(db: Session = Depends(get_db)):
    return static_value(db)


@router.get("/activation")
def get_activation_value(db: Session = Depends(get_db)):
    return activation_value(db)


@router.get("/leveraged")
def get_leveraged_value(db: Session = Depends(get_db)):
    return leveraged_value(db)
