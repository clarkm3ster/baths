"""Tests for spatial clustering (DBSCAN on parcel centroids)."""

import pytest
from src.land.clustering import cluster_parcels_in_memory, get_neighbor_counts

# Philadelphia coordinates
PHI_LON = -75.1652
PHI_LAT = 39.9526

# Approximate 200ft in degrees at Philadelphia latitude
FT_200_DEG = 200 / 364000  # ~0.000549 degrees


def _make_parcel(lon: float, lat: float, idx: int, area: float = 5000) -> dict:
    return {
        "id": f"parcel-{idx}",
        "centroid_x": lon,
        "centroid_y": lat,
        "area_sqft": area,
        "sphere_viability_score": 0.7,
        "geometry_wkt": None,
    }


class TestClusterParcelsInMemory:
    def test_too_few_parcels(self):
        result = cluster_parcels_in_memory([_make_parcel(PHI_LON, PHI_LAT, 0)])
        assert result == []

    def test_two_adjacent_parcels_cluster(self):
        parcels = [
            _make_parcel(PHI_LON, PHI_LAT, 0),
            _make_parcel(PHI_LON + FT_200_DEG * 0.5, PHI_LAT, 1),
        ]
        result = cluster_parcels_in_memory(parcels)
        assert len(result) == 1
        assert result[0]["parcel_count"] == 2

    def test_distant_parcels_no_cluster(self):
        parcels = [
            _make_parcel(PHI_LON, PHI_LAT, 0),
            _make_parcel(PHI_LON + 0.01, PHI_LAT, 1),  # ~1000ft away
        ]
        result = cluster_parcels_in_memory(parcels)
        assert len(result) == 0

    def test_three_groups(self):
        # Group A: 3 parcels close together
        group_a = [_make_parcel(PHI_LON, PHI_LAT, i) for i in range(3)]
        for i, p in enumerate(group_a):
            p["centroid_x"] += i * FT_200_DEG * 0.3

        # Group B: 2 parcels close together, far from A
        group_b = [
            _make_parcel(PHI_LON + 0.02, PHI_LAT, 10),
            _make_parcel(PHI_LON + 0.02 + FT_200_DEG * 0.3, PHI_LAT, 11),
        ]

        # Isolated parcel (noise)
        isolated = [_make_parcel(PHI_LON + 0.05, PHI_LAT, 20)]

        parcels = group_a + group_b + isolated
        result = cluster_parcels_in_memory(parcels)
        assert len(result) == 2

    def test_cluster_stats(self):
        parcels = [
            _make_parcel(PHI_LON, PHI_LAT, 0, area=10000),
            _make_parcel(PHI_LON + FT_200_DEG * 0.3, PHI_LAT, 1, area=15000),
        ]
        parcels[0]["sphere_viability_score"] = 0.8
        parcels[1]["sphere_viability_score"] = 0.6

        result = cluster_parcels_in_memory(parcels)
        assert len(result) == 1
        assert result[0]["total_area_sqft"] == 25000
        assert result[0]["avg_viability_score"] == pytest.approx(0.7, abs=0.01)


class TestGetNeighborCounts:
    def test_no_neighbors(self):
        parcels = [
            _make_parcel(PHI_LON, PHI_LAT, 0),
            _make_parcel(PHI_LON + 0.01, PHI_LAT, 1),
        ]
        counts = get_neighbor_counts(parcels)
        assert counts["parcel-0"][0] == 0
        assert counts["parcel-1"][0] == 0

    def test_adjacent_neighbors(self):
        parcels = [
            _make_parcel(PHI_LON, PHI_LAT, 0),
            _make_parcel(PHI_LON + FT_200_DEG * 0.3, PHI_LAT, 1),
        ]
        counts = get_neighbor_counts(parcels)
        assert counts["parcel-0"][0] == 1
        assert counts["parcel-1"][0] == 1
