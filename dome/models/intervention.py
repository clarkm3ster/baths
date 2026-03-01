"""Intervention models for THE DOME.

An ``InterventionDefinition`` describes a specific action that can break a
cascade link -- its cost range, target link, probability of success, and
expected time to effect.  An ``InterventionPlan`` bundles one or more
interventions into a concrete plan tied to a person and cascade alert,
with projected total cost, savings, and ROI.
"""

from __future__ import annotations

from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class InterventionDefinition(BaseModel):
    """Specification of a single intervention that can break a cascade link.

    Interventions are catalogued with their cost envelope, the specific
    cascade link they target, and their estimated effectiveness.
    """

    intervention_id: str = Field(
        ..., description="Unique identifier for this intervention."
    )
    name: str = Field(
        ..., description="Human-readable intervention name (e.g. 'Rapid Rehousing')."
    )
    cost_min: float = Field(
        ...,
        ge=0,
        description="Minimum expected cost to deliver this intervention (USD).",
    )
    cost_max: float = Field(
        ...,
        ge=0,
        description="Maximum expected cost to deliver this intervention (USD).",
    )
    targets_cascade_link: str = Field(
        ...,
        description=(
            "Identifier or label of the cascade link this intervention "
            "is designed to break (e.g. 'job_loss->housing_instability')."
        ),
    )
    break_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Estimated probability (0-1) that the intervention successfully "
            "prevents the downstream effect."
        ),
    )
    time_to_effect_months: float = Field(
        ...,
        ge=0,
        description="Expected months until the intervention takes full effect.",
    )

    @field_validator("break_probability")
    @classmethod
    def _break_prob_range(cls, v: float) -> float:
        """Ensure break_probability is between 0 and 1 inclusive."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("break_probability must be between 0.0 and 1.0")
        return v


class InterventionPlan(BaseModel):
    """A concrete plan of interventions tied to a person and cascade alert.

    The plan aggregates one or more ``InterventionDefinition`` instances,
    calculates total cost, and projects expected savings and return on
    investment (ROI) relative to the do-nothing path.
    """

    plan_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Globally unique plan identifier (UUID4 by default).",
    )
    person_uid: str = Field(
        ..., description="Unique person identifier."
    )
    cascade_alert_id: str = Field(
        ...,
        description="ID of the CascadeAlert this plan responds to.",
    )
    interventions: list[InterventionDefinition] = Field(
        ...,
        min_length=1,
        description="Ordered list of interventions in this plan.",
    )
    total_cost: float = Field(
        ...,
        ge=0,
        description="Estimated total cost of all interventions in the plan (USD).",
    )
    expected_savings: float = Field(
        ...,
        description=(
            "Expected savings relative to the do-nothing path (USD).  "
            "Positive means the plan saves money."
        ),
    )
    expected_roi: float = Field(
        ...,
        description=(
            "Expected return on investment: expected_savings / total_cost.  "
            "Values > 1.0 mean the plan more than pays for itself."
        ),
    )
