from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..cost_calculator import calculate_costs, get_benchmarks

router = APIRouter(prefix="/api/cost", tags=["cost"])


@router.post("/calculate")
def calc_costs(body: dict, db: Session = Depends(get_db)):
    system_ids = body.get("system_ids", [])
    return calculate_costs(db, system_ids)


@router.get("/benchmarks")
def benchmarks(db: Session = Depends(get_db)):
    return get_benchmarks(db)
