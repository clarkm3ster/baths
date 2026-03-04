"""Tests for the land viability scoring engine."""

import pytest
from src.land.scoring import (
    score_lot_size,
    score_street_visibility,
    score_pedestrian_traffic,
    score_environmental_risk,
    score_zoning_compatibility,
    score_neighborhood_density,
    score_cluster_potential,
    calculate_viability_from_dict,
)


class TestScoreLotSize:
    def test_zero_area(self):
        assert score_lot_size(0) == 0.0

    def test_none_area(self):
        assert score_lot_size(None) == 0.0

    def test_tiny_lot(self):
        s = score_lot_size(500)
        assert 0 < s < 0.2

    def test_micro_sphere_threshold(self):
        s = score_lot_size(2000)
        assert s == pytest.approx(0.2, abs=0.01)

    def test_preferred_size(self):
        s = score_lot_size(5000)
        assert s == pytest.approx(0.6, abs=0.01)

    def test_full_sphere(self):
        s = score_lot_size(50000)
        assert s == pytest.approx(1.0, abs=0.05)

    def test_massive_lot(self):
        assert score_lot_size(200000) == 1.0


class TestScoreStreetVisibility:
    def test_none_values(self):
        assert score_street_visibility(None, None) == 0.3

    def test_deep_lot(self):
        # Low frontage relative to area = hard to see
        s = score_street_visibility(20, 10000)
        assert s < 0.5

    def test_wide_shallow_lot(self):
        # High frontage relative to area = very visible
        s = score_street_visibility(200, 5000)
        assert s > 0.6


class TestScorePedestrianTraffic:
    def test_near_transit(self):
        s = score_pedestrian_traffic(100)
        assert s > 0.9

    def test_walkable(self):
        s = score_pedestrian_traffic(500)
        assert 0.7 < s < 1.0

    def test_far_from_transit(self):
        s = score_pedestrian_traffic(5000)
        assert s < 0.3

    def test_none(self):
        assert score_pedestrian_traffic(None) == 0.4


class TestScoreEnvironmentalRisk:
    def test_clean_site(self):
        assert score_environmental_risk([]) == 1.0
        assert score_environmental_risk(None) == 1.0

    def test_brownfield(self):
        s = score_environmental_risk(["brownfield"])
        assert s == pytest.approx(0.3, abs=0.01)

    def test_flood_zone(self):
        s = score_environmental_risk(["flood_zone"])
        assert s == pytest.approx(0.6, abs=0.01)

    def test_brownfield_and_flood(self):
        s = score_environmental_risk(["brownfield", "flood_zone"])
        assert s == pytest.approx(0.18, abs=0.02)

    def test_superfund(self):
        s = score_environmental_risk(["superfund"])
        assert s < 0.15


class TestScoreZoningCompatibility:
    def test_commercial_mixed_use(self):
        assert score_zoning_compatibility("CMX-3") == 1.0
        assert score_zoning_compatibility("SP-ENT") == 1.0
        assert score_zoning_compatibility("ICMX") == 1.0

    def test_residential(self):
        s = score_zoning_compatibility("RSA-1")
        assert s == 0.15

    def test_neutral(self):
        s = score_zoning_compatibility("CMX-2")
        assert s == 0.65

    def test_unknown(self):
        assert score_zoning_compatibility(None) == 0.4
        assert score_zoning_compatibility("") == 0.4


class TestClusterPotential:
    def test_isolated(self):
        assert score_cluster_potential(0, 0) == 0.2

    def test_one_neighbor(self):
        assert score_cluster_potential(1, 5000) == 0.5

    def test_many_neighbors_large_area(self):
        s = score_cluster_potential(5, 60000)
        assert s == 1.0


class TestViabilityFromDict:
    def test_ideal_parcel(self):
        breakdown = calculate_viability_from_dict(
            area_sqft=25000,
            street_frontage_ft=150,
            transit_proximity_ft=200,
            environmental_flags=[],
            zoning="CMX-3",
            census_block_group="421010100001",
            neighbor_count=3,
            combined_area_sqft=40000,
        )
        assert breakdown.overall_score > 0.8

    def test_terrible_parcel(self):
        breakdown = calculate_viability_from_dict(
            area_sqft=500,
            street_frontage_ft=5,
            transit_proximity_ft=10000,
            environmental_flags=["brownfield", "flood_zone", "superfund"],
            zoning="RSA-1",
            census_block_group=None,
            neighbor_count=0,
        )
        assert breakdown.overall_score < 0.2

    def test_scores_bounded_0_1(self):
        breakdown = calculate_viability_from_dict()
        assert 0 <= breakdown.overall_score <= 1
