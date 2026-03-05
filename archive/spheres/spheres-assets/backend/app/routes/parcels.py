"""Parcel API routes."""

import json
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.models import Parcel

router = APIRouter(prefix="/api/parcels", tags=["parcels"])


@router.get("")
def list_parcels(
    owner: str | None = Query(None),
    score_min: int = Query(0),
    score_max: int = Query(100),
    size_min: float = Query(0),
    size_max: float | None = Query(None),
    category: str | None = Query(None),
    zoning: str | None = Query(None),
    ward: str | None = Query(None),
    vacancy: bool | None = Query(None),
    search: str | None = Query(None),
    bbox: str | None = Query(None, description="min_lng,min_lat,max_lng,max_lat"),
    limit: int = Query(200, le=5000),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    q = db.query(Parcel)

    if owner:
        q = q.filter(Parcel.owner_agency == owner)
    q = q.filter(Parcel.activation_score >= score_min, Parcel.activation_score <= score_max)
    q = q.filter(Parcel.total_area_sqft >= size_min)
    if size_max is not None:
        q = q.filter(Parcel.total_area_sqft <= size_max)
    if category:
        q = q.filter(Parcel.activation_categories.contains(f'"{category}"'))
    if zoning:
        q = q.filter(Parcel.zoning == zoning.upper())
    if ward:
        q = q.filter(Parcel.geographic_ward == ward)
    if vacancy is not None:
        q = q.filter(Parcel.vacancy_likely == vacancy)
    if search:
        pattern = f"%{search}%"
        q = q.filter(Parcel.address.ilike(pattern))
    if bbox:
        parts = bbox.split(",")
        if len(parts) == 4:
            min_lng, min_lat, max_lng, max_lat = map(float, parts)
            q = q.filter(and_(
                Parcel.lng >= min_lng, Parcel.lng <= max_lng,
                Parcel.lat >= min_lat, Parcel.lat <= max_lat,
            ))

    total = q.count()
    parcels = q.order_by(Parcel.activation_score.desc()).offset(offset).limit(limit).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "parcels": [_parcel_summary(p) for p in parcels],
    }


@router.get("/geojson")
def parcels_geojson(
    owner: str | None = Query(None),
    score_min: int = Query(0),
    category: str | None = Query(None),
    vacancy: bool | None = Query(None),
    db: Session = Depends(get_db),
):
    """Return all parcels as a GeoJSON FeatureCollection for map rendering."""
    q = db.query(Parcel).filter(Parcel.lat.isnot(None), Parcel.lng.isnot(None))

    if owner:
        q = q.filter(Parcel.owner_agency == owner)
    if score_min > 0:
        q = q.filter(Parcel.activation_score >= score_min)
    if category:
        q = q.filter(Parcel.activation_categories.contains(f'"{category}"'))
    if vacancy is not None:
        q = q.filter(Parcel.vacancy_likely == vacancy)

    features = []
    for p in q.all():
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [p.lng, p.lat]},
            "properties": {
                "id": p.parcel_number,
                "address": p.address,
                "owner_agency": p.owner_agency,
                "score": p.activation_score,
                "area": p.total_area_sqft,
                "value": p.market_value,
                "vacancy": p.vacancy_likely,
                "zoning": p.zoning,
                "categories": json.loads(p.activation_categories or "[]"),
            },
        })

    return {"type": "FeatureCollection", "features": features}


@router.get("/nearby")
def nearby_parcels(
    lat: float = Query(...),
    lng: float = Query(...),
    radius_ft: float = Query(1000),
    limit: int = Query(20),
    db: Session = Depends(get_db),
):
    """Find parcels within radius_ft feet of a point."""
    # Approximate: 1 degree lat ~= 364,000 ft, 1 degree lng ~= 288,000 ft at 40N
    lat_delta = radius_ft / 364000
    lng_delta = radius_ft / 288000

    parcels = (
        db.query(Parcel)
        .filter(
            Parcel.lat.between(lat - lat_delta, lat + lat_delta),
            Parcel.lng.between(lng - lng_delta, lng + lng_delta),
        )
        .all()
    )

    # Calculate actual distances and sort
    results = []
    for p in parcels:
        if p.lat is None or p.lng is None:
            continue
        dist_ft = _haversine_ft(lat, lng, p.lat, p.lng)
        if dist_ft <= radius_ft:
            results.append({**_parcel_summary(p), "distance_ft": round(dist_ft)})

    results.sort(key=lambda x: x["distance_ft"])
    return results[:limit]


@router.get("/{parcel_number}")
def get_parcel(parcel_number: str, db: Session = Depends(get_db)):
    p = db.query(Parcel).filter(Parcel.parcel_number == parcel_number).first()
    if not p:
        return {"error": "Not found"}, 404
    return _parcel_full(p)


def _parcel_summary(p: Parcel) -> dict:
    return {
        "parcel_number": p.parcel_number,
        "address": p.address,
        "lat": p.lat,
        "lng": p.lng,
        "owner_agency": p.owner_agency,
        "total_area_sqft": p.total_area_sqft,
        "market_value": p.market_value,
        "activation_score": p.activation_score,
        "activation_categories": json.loads(p.activation_categories or "[]"),
        "vacancy_likely": p.vacancy_likely,
        "zoning": p.zoning,
    }


def _parcel_full(p: Parcel) -> dict:
    return {
        **_parcel_summary(p),
        "owner": p.owner,
        "category_code": p.category_code,
        "category_description": p.category_description,
        "frontage": p.frontage,
        "depth": p.depth,
        "exterior_condition": p.exterior_condition,
        "year_built": p.year_built,
        "geographic_ward": p.geographic_ward,
        "zip_code": p.zip_code,
        "taxable_land": p.taxable_land,
        "taxable_building": p.taxable_building,
        "exempt_land": p.exempt_land,
        "exempt_building": p.exempt_building,
    }


def _haversine_ft(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 20902231  # Earth radius in feet
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
