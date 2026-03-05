"""Data ingestion pipelines for public land sources.

Each function fetches data from an external API, transforms it into
ParcelRecord objects, and upserts them into the database.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

import httpx

from src.land.models import ParcelRecord
from src.land.scoring import calculate_viability_from_dict

logger = logging.getLogger(__name__)

PHILLY_VACANT_API = (
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/"
    "Vacant_Indicators_Land/FeatureServer/0/query"
)
PHILLY_LANDBANK_URL = "https://data.phila.gov/api/views/land-bank/rows.csv?accessType=DOWNLOAD"
OVERPASS_API = "https://overpass-api.de/api/interpreter"


async def ingest_philly_vacant(limit: int = 1000) -> list[ParcelRecord]:
    """Ingest Philadelphia Vacant Property Indicators from OpenDataPhilly ArcGIS.

    Args:
        limit: Max records per API call. ArcGIS limits to ~2000 per request.

    Returns:
        List of ParcelRecord objects ready for DB insert.
    """
    params: dict[str, Any] = {
        "where": "1=1",
        "outFields": "OPA_ID,VACANT_BLDG_COUNT,VACANT_LAND_COUNT,ADDRESS",
        "outSR": 4326,
        "f": "geojson",
        "resultRecordCount": limit,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(PHILLY_VACANT_API, params=params)
        resp.raise_for_status()
        data = resp.json()

    features = data.get("features", [])
    logger.info("Fetched %d features from Philly Vacant API", len(features))

    parcels = []
    for feature in features:
        props = feature.get("properties", {})
        geom = feature.get("geometry")
        parcel = _feature_to_parcel(props, geom, source="philly_vacant")
        if parcel:
            parcels.append(parcel)

    return parcels


async def ingest_overpass_brownfields(city: str = "Philadelphia") -> list[ParcelRecord]:
    """Ingest brownfield land-use polygons from OpenStreetMap via Overpass API."""
    query = f"""
    [out:json][timeout:25];
    area["name"="{city}"]->.a;
    (way["landuse"="brownfield"](area.a););
    out geom;
    """

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OVERPASS_API, data={"data": query})
        resp.raise_for_status()
        data = resp.json()

    elements = data.get("elements", [])
    logger.info("Fetched %d brownfield elements from Overpass", len(elements))

    parcels = []
    for elem in elements:
        parcel = _osm_element_to_parcel(elem)
        if parcel:
            parcels.append(parcel)

    return parcels


def _feature_to_parcel(
    props: dict[str, Any],
    geom: dict[str, Any] | None,
    source: str,
) -> ParcelRecord | None:
    """Convert a GeoJSON feature to a ParcelRecord."""
    external_id = props.get("OPA_ID") or props.get("opa_id")
    if not external_id:
        return None

    vacant_bldg = int(props.get("VACANT_BLDG_COUNT", 0) or 0)
    vacant_land = int(props.get("VACANT_LAND_COUNT", 0) or 0)

    parcel = ParcelRecord(
        id=uuid.uuid4(),
        source=source,
        external_id=str(external_id),
        ownership_type="city",
        vacant_building_count=vacant_bldg,
        vacant_land_indicator=vacant_land > 0,
        status="discovered",
    )

    # Calculate viability with available data
    breakdown = calculate_viability_from_dict(
        area_sqft=parcel.area_sqft,
        zoning=parcel.zoning,
        environmental_flags=list(parcel.environmental_flags) if parcel.environmental_flags else None,
    )
    parcel.sphere_viability_score = breakdown.overall_score
    parcel.sphere_viability_updated_at = datetime.now(timezone.utc)

    return parcel


def _osm_element_to_parcel(element: dict[str, Any]) -> ParcelRecord | None:
    """Convert an OSM Overpass element to a ParcelRecord."""
    osm_id = element.get("id")
    if not osm_id:
        return None

    tags = element.get("tags", {})

    parcel = ParcelRecord(
        id=uuid.uuid4(),
        source="osm_overpass",
        external_id=f"way/{osm_id}",
        ownership_type=tags.get("ownership", "unknown"),
        owner_name=tags.get("operator"),
        environmental_flags=["brownfield"],
        status="discovered",
    )

    return parcel
