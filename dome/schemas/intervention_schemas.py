"""Request/response schemas for intervention endpoints."""

from __future__ import annotations

from pydantic import BaseModel, Field


class InterventionPlanRequest(BaseModel):
    """Request to generate an optimal intervention plan."""

    cascade_alert_id: str
    max_budget: float | None = None
    max_interventions: int = Field(5, ge=1, le=20)


class InterventionPlanSummary(BaseModel):
    """Summary of a generated intervention plan."""

    plan_id: str
    cascade_alert_id: str
    interventions: list[InterventionSummary]
    total_cost: float
    expected_savings: float
    expected_roi: float


class InterventionSummary(BaseModel):
    """Lightweight intervention description."""

    intervention_id: str
    name: str
    cost_estimate: float
    break_probability: float
    time_to_effect_months: float


class SimulationRequest(BaseModel):
    """Request to run a Path A vs Path B Monte Carlo simulation."""

    iterations: int = Field(1000, ge=100, le=10000)
    projection_years: int = Field(50, ge=1, le=80)
    intervention_ids: list[str] | None = None  # if None, use recommended


class SimulationSummary(BaseModel):
    """Summary of a simulation run."""

    path_a_median_cost: float
    path_a_p90_cost: float
    path_b_median_cost: float
    path_b_p90_cost: float
    dome_intervention_cost: float
    net_savings: float
    dome_roi: float
    iterations_run: int


class BenefitsCliffPoint(BaseModel):
    """A single point on the benefits cliff curve."""

    income_level: float
    total_benefits_value: float
    net_resources: float
    effective_marginal_tax_rate: float
    programs_lost: list[str]
    is_cliff: bool


class DashboardData(BaseModel):
    """Coordinator dashboard payload for a single person."""

    person_uid: str
    name_hash: str
    age: float
    trajectory: str | None = None
    active_cascade_alerts: int = 0
    total_lifetime_cost_path_a: float | None = None
    total_lifetime_cost_path_b: float | None = None
    potential_savings: float | None = None
    dome_roi: float | None = None
    top_interventions: list[str] = Field(default_factory=list)
    benefits_cliff_detected: bool = False
