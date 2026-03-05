"""Aggregate statistics routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Parcel

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Parcel.parcel_number)).scalar() or 0
    total_area = db.query(func.sum(Parcel.total_area_sqft)).scalar() or 0
    total_value = db.query(func.sum(Parcel.market_value)).scalar() or 0
    avg_score = db.query(func.avg(Parcel.activation_score)).scalar() or 0
    vacant_count = db.query(func.count(Parcel.parcel_number)).filter(
        Parcel.vacancy_likely == True  # noqa: E712
    ).scalar() or 0

    by_agency = [
        {"agency": row[0], "count": row[1], "total_value": float(row[2] or 0)}
        for row in db.query(
            Parcel.owner_agency,
            func.count(Parcel.parcel_number),
            func.sum(Parcel.market_value),
        ).group_by(Parcel.owner_agency).all()
    ]

    by_zoning = [
        {"zoning": row[0] or "Unknown", "count": row[1]}
        for row in db.query(Parcel.zoning, func.count(Parcel.parcel_number))
        .group_by(Parcel.zoning)
        .order_by(func.count(Parcel.parcel_number).desc())
        .limit(20)
        .all()
    ]

    by_ward = [
        {"ward": row[0] or "Unknown", "count": row[1]}
        for row in db.query(Parcel.geographic_ward, func.count(Parcel.parcel_number))
        .group_by(Parcel.geographic_ward)
        .order_by(func.count(Parcel.parcel_number).desc())
        .all()
    ]

    return {
        "total_parcels": total,
        "total_area_sqft": float(total_area),
        "total_acres": float(total_area) / 43560,
        "total_value": float(total_value),
        "avg_activation_score": round(float(avg_score), 1),
        "vacant_count": vacant_count,
        "by_agency": sorted(by_agency, key=lambda x: -x["count"]),
        "by_zoning": by_zoning,
        "by_ward": by_ward,
    }
