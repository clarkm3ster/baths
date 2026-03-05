"""Spatial clustering of vacant parcels using DBSCAN.

Groups adjacent vacant parcels within epsilon distance into ParcelCluster
records, enabling identification of combined sites for larger Sphere installations.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPolygon, Point
from shapely.ops import unary_union
import structlog

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# 200 feet in degrees latitude (approximate at Philadelphia's latitude ~40N)
# 1 degree latitude ~= 364,000 ft
EPSILON_FT: float = 200.0
FT_PER_DEGREE_LAT: float = 364_000.0
FT_PER_DEGREE_LON_40N: float = 288_000.0  # approximate at 40N

# DBSCAN requires at least 2 parcels to form a cluster
MIN_SAMPLES: int = 2


# ---------------------------------------------------------------------------
# Core clustering logic (operates on in-memory data, no DB dependency)
# ---------------------------------------------------------------------------

def cluster_parcels_in_memory(
    parcel_data: list[dict],
    epsilon_ft: float = EPSILON_FT,
    min_samples: int = MIN_SAMPLES,
) -> list[dict]:
    """Run DBSCAN clustering on a list of parcel dicts.

    Args:
        parcel_data: List of dicts, each with keys:
            - id (str/UUID)
            - centroid_x (float, longitude)
            - centroid_y (float, latitude)
            - area_sqft (float)
            - sphere_viability_score (float | None)
            - geometry_wkt (str | None, WKT of parcel polygon)
        epsilon_ft: Maximum distance in feet between parcels in a cluster.
        min_samples: Minimum parcels to form a cluster.

    Returns:
        List of cluster dicts with keys:
            - cluster_label (int)
            - parcel_ids (list of IDs)
            - centroid_x, centroid_y (cluster centroid)
            - total_area_sqft (float)
            - parcel_count (int)
            - avg_viability_score (float)
            - geometry_wkt (MultiPolygon WKT from merging parcel geometries)
    """
    if len(parcel_data) < min_samples:
        logger.info("clustering.skip", reason="too_few_parcels", count=len(parcel_data))
        return []

    # Extract centroids as numpy array [lon, lat]
    coords = np.array([
        [p["centroid_x"], p["centroid_y"]] for p in parcel_data
    ])

    # Convert coordinates to feet-equivalent for uniform distance metric
    avg_lat = np.mean(coords[:, 1])
    ft_per_deg_lon = FT_PER_DEGREE_LON_40N * np.cos(np.radians(avg_lat)) / np.cos(np.radians(40.0))

    coords_scaled = np.column_stack([
        coords[:, 0] * ft_per_deg_lon,    # longitude -> feet
        coords[:, 1] * FT_PER_DEGREE_LAT,  # latitude -> feet
    ])

    dbscan = DBSCAN(
        eps=epsilon_ft,
        min_samples=min_samples,
        metric="euclidean",
        n_jobs=-1,
    )
    labels = dbscan.fit_predict(coords_scaled)

    # Group parcels by cluster label (skip noise label -1)
    clusters_map: dict[int, list[int]] = {}
    for idx, label in enumerate(labels):
        if label == -1:
            continue
        clusters_map.setdefault(label, []).append(idx)

    results = []
    for label, indices in clusters_map.items():
        cluster_parcels = [parcel_data[i] for i in indices]
        parcel_ids = [p["id"] for p in cluster_parcels]

        # Compute aggregate stats
        total_area = sum(p.get("area_sqft", 0) or 0 for p in cluster_parcels)
        scores = [
            p["sphere_viability_score"]
            for p in cluster_parcels
            if p.get("sphere_viability_score") is not None
        ]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        # Compute cluster centroid
        cx = float(np.mean([p["centroid_x"] for p in cluster_parcels]))
        cy = float(np.mean([p["centroid_y"] for p in cluster_parcels]))

        # Build merged MultiPolygon geometry from individual parcel geometries
        geometry_wkt = _merge_geometries(cluster_parcels, label)

        results.append({
            "cluster_label": label,
            "parcel_ids": parcel_ids,
            "centroid_x": cx,
            "centroid_y": cy,
            "total_area_sqft": total_area,
            "parcel_count": len(parcel_ids),
            "avg_viability_score": avg_score,
            "geometry_wkt": geometry_wkt,
        })

    logger.info(
        "clustering.complete",
        total_parcels=len(parcel_data),
        clusters_found=len(results),
        noise_parcels=int(np.sum(labels == -1)),
    )
    return results


def _merge_geometries(cluster_parcels: list[dict], label: int) -> str | None:
    """Merge individual parcel geometries into a MultiPolygon WKT."""
    try:
        from shapely import wkt as shapely_wkt

        polygons = []
        for p in cluster_parcels:
            if p.get("geometry_wkt"):
                geom = shapely_wkt.loads(p["geometry_wkt"])
                polygons.append(geom)
        if not polygons:
            return None
        merged = unary_union(polygons)
        if merged.geom_type == "Polygon":
            merged = MultiPolygon([merged])
        elif merged.geom_type != "MultiPolygon":
            valid_polys = [g for g in merged.geoms if g.geom_type == "Polygon"]
            merged = MultiPolygon(valid_polys) if valid_polys else None
        return merged.wkt if merged is not None else None
    except Exception:
        logger.warning("clustering.geometry_merge_failed", label=label)
        return None


def get_neighbor_counts(
    parcel_data: list[dict],
    radius_ft: float = EPSILON_FT,
) -> dict[str, tuple[int, float]]:
    """For each parcel, count neighbors within radius and their combined area.

    Args:
        parcel_data: List of dicts with centroid_x, centroid_y, area_sqft, id keys.
        radius_ft: Search radius in feet.

    Returns:
        Dict mapping parcel_id (str) -> (neighbor_count, combined_neighbor_area_sqft)
    """
    if len(parcel_data) < 2:
        return {str(p["id"]): (0, p.get("area_sqft", 0) or 0) for p in parcel_data}

    coords = np.array([
        [p["centroid_x"], p["centroid_y"]] for p in parcel_data
    ])

    avg_lat = np.mean(coords[:, 1])
    ft_per_deg_lon = FT_PER_DEGREE_LON_40N * np.cos(np.radians(avg_lat)) / np.cos(np.radians(40.0))

    coords_scaled = np.column_stack([
        coords[:, 0] * ft_per_deg_lon,
        coords[:, 1] * FT_PER_DEGREE_LAT,
    ])

    tree = cKDTree(coords_scaled)
    result = {}

    for i, p in enumerate(parcel_data):
        neighbors = tree.query_ball_point(coords_scaled[i], radius_ft)
        neighbors = [n for n in neighbors if n != i]
        combined_area = sum(
            (parcel_data[n].get("area_sqft", 0) or 0) for n in neighbors
        )
        result[str(p["id"])] = (len(neighbors), combined_area)

    return result


# ---------------------------------------------------------------------------
# ORM-based clustering (for direct use with ParcelRecord objects)
# ---------------------------------------------------------------------------

def cluster_parcels(
    parcels: list,
    epsilon_ft: float = EPSILON_FT,
    min_samples: int = MIN_SAMPLES,
) -> list:
    """Run DBSCAN clustering on ParcelRecord objects (or parcel-like dicts).

    Accepts either ORM ParcelRecord objects or dicts with centroid/area fields.
    Returns list of ParcelCluster-like dicts.

    This is a convenience wrapper around cluster_parcels_in_memory for use
    with ORM objects that have centroid_x/centroid_y attributes or _centroid_coords.
    """
    from src.land.models import ParcelCluster, ParcelRecord

    if len(parcels) < min_samples:
        return []

    # Convert ORM objects to dict format
    parcel_data = []
    for p in parcels:
        coords = _extract_centroid(p)
        if coords is None:
            continue
        lat, lon = coords
        parcel_data.append({
            "id": str(p.id),
            "centroid_x": lon,
            "centroid_y": lat,
            "area_sqft": getattr(p, "area_sqft", 0) or 0,
            "sphere_viability_score": getattr(p, "sphere_viability_score", None),
            "geometry_wkt": None,  # Skip geometry merge for ORM path
        })

    if len(parcel_data) < min_samples:
        return []

    cluster_results = cluster_parcels_in_memory(parcel_data, epsilon_ft, min_samples)

    # Build ParcelCluster ORM objects
    orm_clusters = []
    parcel_by_id = {str(p.id): p for p in parcels}
    for info in cluster_results:
        cluster = ParcelCluster(
            id=uuid.uuid4(),
            total_area_sqft=info["total_area_sqft"],
            parcel_count=info["parcel_count"],
            avg_viability_score=info["avg_viability_score"],
        )
        # Assign parcels to cluster
        for pid in info["parcel_ids"]:
            if pid in parcel_by_id:
                parcel_by_id[pid].cluster_id = cluster.id
        orm_clusters.append(cluster)

    return orm_clusters


def _extract_centroid(parcel) -> tuple[float, float] | None:
    """Extract (lat, lon) from a parcel object.

    Handles WKBElements (from DB), coordinate tuples, and _centroid_coords attribute.
    """
    # Check for explicit coordinates set for testing
    if hasattr(parcel, "_centroid_coords"):
        return parcel._centroid_coords

    centroid = getattr(parcel, "centroid", None)
    if centroid is None:
        return None

    # GeoAlchemy2 WKBElement
    if hasattr(centroid, "desc"):
        try:
            from shapely import wkb
            point = wkb.loads(bytes(centroid.desc))
            return (point.y, point.x)
        except Exception:
            return None

    # Plain tuple/list [lon, lat]
    if isinstance(centroid, (list, tuple)) and len(centroid) >= 2:
        return (centroid[1], centroid[0])

    return None


# ---------------------------------------------------------------------------
# Database-integrated clustering (async)
# ---------------------------------------------------------------------------

async def run_clustering_for_city(
    db: AsyncSession,
    city: str = "philadelphia",
    epsilon_ft: float = EPSILON_FT,
    min_samples: int = MIN_SAMPLES,
) -> list[dict]:
    """Run DBSCAN clustering on all parcels for a city, persist ParcelCluster records.

    1. Loads parcel centroids from DB
    2. Runs in-memory DBSCAN
    3. Creates/updates ParcelCluster records
    4. Updates parcel cluster_id foreign keys

    Returns list of cluster summary dicts.
    """
    from geoalchemy2.shape import to_shape, from_shape
    from sqlalchemy import select, update, delete
    from shapely import wkt as shapely_wkt

    from src.land.models import ParcelCluster, ParcelRecord

    # Load parcels with centroids
    stmt = (
        select(
            ParcelRecord.id,
            ParcelRecord.centroid,
            ParcelRecord.area_sqft,
            ParcelRecord.sphere_viability_score,
            ParcelRecord.geometry,
        )
        .where(ParcelRecord.centroid.isnot(None))
    )

    # Filter by city source
    if city.lower() == "philadelphia":
        stmt = stmt.where(
            ParcelRecord.source.in_(["philly_vacant", "landbank", "regrid_philly"])
        )

    result = await db.execute(stmt)
    rows = result.all()

    if len(rows) < min_samples:
        logger.info("clustering.skip", city=city, reason="too_few_parcels", count=len(rows))
        return []

    # Convert to in-memory format
    parcel_data = []
    for row in rows:
        centroid_shape = to_shape(row.centroid)
        geom_wkt = None
        if row.geometry is not None:
            try:
                geom_wkt = to_shape(row.geometry).wkt
            except Exception:
                pass

        parcel_data.append({
            "id": str(row.id),
            "centroid_x": centroid_shape.x,
            "centroid_y": centroid_shape.y,
            "area_sqft": row.area_sqft,
            "sphere_viability_score": row.sphere_viability_score,
            "geometry_wkt": geom_wkt,
        })

    # Run clustering
    clusters = cluster_parcels_in_memory(parcel_data, epsilon_ft, min_samples)
    if not clusters:
        return []

    # Clear old cluster assignments for these parcels
    all_parcel_ids = [uuid.UUID(p["id"]) for p in parcel_data]
    await db.execute(
        update(ParcelRecord)
        .where(ParcelRecord.id.in_(all_parcel_ids))
        .values(cluster_id=None)
    )

    # Delete orphaned clusters
    await db.execute(
        delete(ParcelCluster).where(
            ~ParcelCluster.id.in_(
                select(ParcelRecord.cluster_id)
                .where(ParcelRecord.cluster_id.isnot(None))
                .distinct()
            )
        )
    )

    # Create new cluster records
    persisted_clusters = []
    for cluster_info in clusters:
        cluster_id = uuid.uuid4()

        # Build geometry
        geom = _build_cluster_geometry(cluster_info)

        cluster_record = ParcelCluster(
            id=cluster_id,
            geometry=geom,
            total_area_sqft=cluster_info["total_area_sqft"],
            parcel_count=cluster_info["parcel_count"],
            avg_viability_score=cluster_info["avg_viability_score"],
        )
        db.add(cluster_record)

        # Update parcel FK
        parcel_uuids = [uuid.UUID(pid) for pid in cluster_info["parcel_ids"]]
        await db.execute(
            update(ParcelRecord)
            .where(ParcelRecord.id.in_(parcel_uuids))
            .values(cluster_id=cluster_id)
        )

        persisted_clusters.append({
            "id": str(cluster_id),
            **cluster_info,
        })

    await db.flush()
    logger.info("clustering.persisted", city=city, cluster_count=len(persisted_clusters))
    return persisted_clusters


def _build_cluster_geometry(cluster_info: dict):
    """Build a GeoAlchemy2 geometry from cluster info."""
    from geoalchemy2.shape import from_shape
    from shapely import wkt as shapely_wkt

    if cluster_info.get("geometry_wkt"):
        try:
            shape = shapely_wkt.loads(cluster_info["geometry_wkt"])
            if shape.geom_type == "Polygon":
                shape = MultiPolygon([shape])
            return from_shape(shape, srid=4326)
        except Exception:
            pass

    # Fallback: buffer around cluster centroid
    point = Point(cluster_info["centroid_x"], cluster_info["centroid_y"])
    return from_shape(MultiPolygon([point.buffer(0.001)]), srid=4326)
