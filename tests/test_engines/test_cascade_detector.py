"""Tests for cascade detection engine."""

import pytest

from dome.models.budget_key import PersonBudgetKey
from dome.models.dome_metrics import DomeMetrics
from dome.models.dynamic_state import EligibilitySnapshot, EnrollmentSnapshot
from dome.engines.cascade_detector import CascadeDetector


def _make_key(**overrides) -> PersonBudgetKey:
    """Helper to build a PersonBudgetKey with sensible defaults + overrides."""
    defaults = dict(
        person_uid="test",
        age=35,
        sex_at_birth="female",
        current_tract_fips="42101002500",
        household_size=1,
        dependents_ages=[],
        current_annual_income=50000.0,
        income_volatility_score=0.2,
        employment_status="FT",
        educational_attainment="HS",
        disability_flag=False,
        chronic_condition_flags=[],
        high_need_flag=False,
        housing_status="stable",
        homelessness_history_flag=False,
        area_deprivation_index=30.0,
        justice_involvement_flag=False,
        past_12m_jail_days=0,
        past_12m_prison_days=0,
        past_12m_police_contacts=0,
        eligibility_snapshot=EligibilitySnapshot(),
        enrollment_snapshot=EnrollmentSnapshot(),
        budget_horizons=[],
    )
    defaults.update(overrides)
    return PersonBudgetKey(**defaults)


def _make_metrics(**layer_overrides) -> DomeMetrics:
    return DomeMetrics(**layer_overrides)


class TestCascadeDetector:
    def test_no_cascades_for_healthy_person(self):
        """A stable, healthy person should trigger no cascades."""
        detector = CascadeDetector()
        key = _make_key(employment_status="FT", current_annual_income=60000)
        alerts = detector.detect(key, _make_metrics(), [])
        assert len(alerts) == 0

    def test_econ_psych_cascade_detected(self):
        """Job loss + depression should trigger cascade type 1."""
        detector = CascadeDetector()
        key = _make_key(employment_status="unemployed", current_annual_income=0.0)
        metrics = _make_metrics(
            behavioral_layer={"depression_severity": 0.7},
            clinical_layer={"depression_diagnosis": True},
        )
        alerts = detector.detect(key, metrics, [])
        cascade_ids = [a.cascade_id for a in alerts]
        assert "econ_psych_bio_fiscal" in cascade_ids

    def test_legal_cascade_detected(self):
        """Recent incarceration should trigger cascade type 3."""
        detector = CascadeDetector()
        key = _make_key(
            justice_involvement_flag=True,
            past_12m_jail_days=30,
            past_12m_police_contacts=3,
            employment_status="unemployed",
            current_annual_income=0.0,
        )
        alerts = detector.detect(key, _make_metrics(), [])
        cascade_ids = [a.cascade_id for a in alerts]
        assert "legal_econ_social_geo_bio_fiscal" in cascade_ids

    def test_social_psych_cascade(self):
        """Social isolation + depression + SUD should trigger cascade type 4."""
        detector = CascadeDetector()
        key = _make_key(employment_status="unemployed", current_annual_income=8000.0)
        metrics = _make_metrics(
            social_layer={"social_isolation_score": 0.8, "social_network_size": 1},
            behavioral_layer={"depression_severity": 0.6, "sud_severity": 0.5, "substance_use_active": True},
        )
        alerts = detector.detect(key, metrics, [])
        cascade_ids = [a.cascade_id for a in alerts]
        assert "social_psych_bio_fiscal" in cascade_ids

    def test_alerts_have_cost_projections(self):
        """All alerts should have positive path_a and path_b costs."""
        detector = CascadeDetector()
        key = _make_key(
            employment_status="unemployed",
            current_annual_income=0.0,
            housing_status="shelter",
            homelessness_history_flag=True,
            justice_involvement_flag=True,
            past_12m_jail_days=14,
        )
        alerts = detector.detect(key, _make_metrics(), [])
        for alert in alerts:
            assert alert.path_a_projected_cost > 0
            assert alert.path_b_projected_cost >= 0
            assert alert.path_a_projected_cost > alert.path_b_projected_cost
