"""Cascade models for THE DOME.

A *cascade* is a directed chain of causally linked adverse events (e.g.
job loss -> housing instability -> ED visit -> chronic disease
exacerbation).  ``CascadeLink`` defines one edge; ``CascadeDefinition``
defines the full chain; ``CascadeAlert`` fires when the system detects a
person entering a known cascade and projects the cost divergence between
intervention and non-intervention paths.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class CascadeLink(BaseModel):
    """A single causal edge in a cascade chain.

    Each link captures the cause event, the effect event, the transition
    probability, the expected lag window, and a subjective strength score
    reflecting evidence quality.
    """

    cause: str = Field(
        ..., description="Label for the upstream event (e.g. 'job_loss')."
    )
    effect: str = Field(
        ..., description="Label for the downstream event (e.g. 'housing_instability')."
    )
    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability that cause triggers effect (0-1).",
    )
    lag_months_min: int = Field(
        ..., ge=0, description="Minimum expected lag in months before effect manifests."
    )
    lag_months_max: int = Field(
        ..., ge=0, description="Maximum expected lag in months before effect manifests."
    )
    strength: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Evidence strength score (0-1) reflecting confidence in "
            "the causal relationship."
        ),
    )

    @field_validator("probability")
    @classmethod
    def _probability_range(cls, v: float) -> float:
        """Ensure probability is between 0 and 1 inclusive."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("probability must be between 0.0 and 1.0")
        return v

    @field_validator("strength")
    @classmethod
    def _strength_range(cls, v: float) -> float:
        """Ensure strength is between 0 and 1 inclusive."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("strength must be between 0.0 and 1.0")
        return v


class CascadeDefinition(BaseModel):
    """A named, reusable cascade template.

    Cascade definitions are maintained in a library and matched against
    incoming person-state transitions to generate alerts.
    """

    cascade_id: str = Field(
        ..., description="Unique identifier for this cascade definition."
    )
    name: str = Field(
        ..., description="Human-readable name (e.g. 'Housing Loss Spiral')."
    )
    links: list[CascadeLink] = Field(
        ...,
        min_length=1,
        description="Ordered list of causal links forming the cascade chain.",
    )


class CascadeAlert(BaseModel):
    """An alert fired when a person is detected entering a cascade.

    The alert includes the person's current position in the cascade chain,
    confidence, projected costs under the two paths (intervene vs. do
    nothing), and recommended interventions.
    """

    alert_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Globally unique alert identifier (UUID4 by default).",
    )
    person_uid: str = Field(
        ..., description="Unique person identifier."
    )
    cascade_id: str = Field(
        ..., description="ID of the cascade definition that matched."
    )
    current_link_index: int = Field(
        ...,
        ge=0,
        description=(
            "Zero-based index of the link the person is currently at "
            "in the cascade chain."
        ),
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence that the person has entered this cascade (0-1).",
    )
    detected_at: datetime = Field(
        ..., description="UTC timestamp when the cascade entry was detected."
    )
    path_a_projected_cost: float = Field(
        ...,
        description=(
            "Projected total public cost if the cascade runs to completion "
            "without intervention (Path A = do nothing)."
        ),
    )
    path_b_projected_cost: float = Field(
        ...,
        description=(
            "Projected total public cost if recommended interventions are "
            "applied (Path B = intervene)."
        ),
    )
    recommended_interventions: list[str] = Field(
        default_factory=list,
        description="Intervention IDs or labels recommended to break the cascade.",
    )

    @field_validator("confidence")
    @classmethod
    def _confidence_range(cls, v: float) -> float:
        """Ensure confidence is between 0 and 1 inclusive."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return v
