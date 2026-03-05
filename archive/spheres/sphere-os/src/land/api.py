"""FastAPI routes for the Land Intelligence Engine.

Provides parcel search, viability scoring, clustering, and ingestion endpoints.
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.land.models import ParcelCluster, ParcelRecord
from src.land.scoring import calculate_viability_breakdown
from src.shared.database import get_db

router = APIRouter()


@router.get("/parcels")
async def list_parcels(
    city: str = Query("philadelphia"),
    min_score: float = Query(0.0, ge=0, le=1),
    min_area: float = Query(0.0, ge=0),
    bbox: str | None = Query(None, description="lon_min,lat_min,lon_max,lat_max"),
    limit: int = Query(100, ge=1, le=5000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Return parcels as a GeoJSON FeatureCollection with scoring metadata."""
    stmt = select(ParcelRecord)

    if min_score > 0:
        stmt = stmt.where(ParcelRecord.sphere_viability_score >= min_score)
    if min_area > 0:
        stmt = stmt.where(ParcelRecord.area_sqft >= min_area)

    stmt = stmt.order_by(ParcelRecord.sphere_viability_score.desc().nullslast())
    stmt = stmt.offset(offset).limit(limit)

    result = await db.execute(stmt)
    parcels = result.scalars().all()

    features = [_parcel_to_feature(p) for p in parcels]
    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "count": len(features),
            "city": city,
            "filters": {"min_score": min_score, "min_area": min_area, "bbox": bbox},
        },
    }


@router.get("/parcels/{parcel_id}")
async def get_parcel(
    parcel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get a single parcel by ID."""
    result = await db.execute(select(ParcelRecord).where(ParcelRecord.id == parcel_id))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return _parcel_to_feature(parcel)


@router.get("/parcels/{parcel_id}/viability")
async def get_viability(
    parcel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Return detailed viability breakdown for a parcel."""
    result = await db.execute(select(ParcelRecord).where(ParcelRecord.id == parcel_id))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    breakdown = calculate_viability_breakdown(parcel)
    return breakdown.to_dict()


@router.get("/clusters")
async def list_clusters(
    city: str = Query("philadelphia"),
    max_radius_ft: float = Query(500, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    """Return parcel clusters."""
    stmt = (
        select(ParcelCluster)
        .order_by(ParcelCluster.avg_viability_score.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    clusters = result.scalars().all()

    return [
        {
            "id": str(c.id),
            "total_area_sqft": c.total_area_sqft,
            "parcel_count": c.parcel_count,
            "avg_viability_score": c.avg_viability_score,
        }
        for c in clusters
    ]


@router.post("/parcels/{parcel_id}/activate")
async def activate_parcel(
    parcel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Mark a parcel as a Sphere candidate."""
    result = await db.execute(select(ParcelRecord).where(ParcelRecord.id == parcel_id))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    parcel.status = "sphere_candidate"
    await db.flush()
    return {"status": "activated", "parcel_id": str(parcel_id)}


@router.post("/ingest/philly-vacant")
async def trigger_philly_ingest(
    limit: int = Query(1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Trigger ingestion of Philadelphia Vacant Property Indicators."""
    from src.land.ingestion import ingest_philly_vacant

    try:
        parcels = await ingest_philly_vacant(limit=limit)
        for p in parcels:
            db.add(p)
        await db.flush()
        return {"status": "success", "ingested": len(parcels)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")


def _parcel_to_feature(parcel: ParcelRecord) -> dict[str, Any]:
    """Convert a ParcelRecord to a GeoJSON Feature."""
    return {
        "type": "Feature",
        "id": str(parcel.id),
        "geometry": None,  # Would be populated from PostGIS geometry column
        "properties": {
            "id": str(parcel.id),
            "source": parcel.source,
            "external_id": parcel.external_id,
            "ownership_type": parcel.ownership_type,
            "area_sqft": parcel.area_sqft,
            "street_frontage_ft": parcel.street_frontage_ft,
            "zoning": parcel.zoning,
            "vacancy_score": parcel.vacancy_score,
            "vacant_building_count": parcel.vacant_building_count,
            "vacant_land_indicator": parcel.vacant_land_indicator,
            "sphere_viability_score": parcel.sphere_viability_score,
            "environmental_flags": list(parcel.environmental_flags) if parcel.environmental_flags else [],
            "status": parcel.status,
            "census_block_group": parcel.census_block_group,
            "transit_proximity_ft": parcel.transit_proximity_ft,
        },
    }
