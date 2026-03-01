"""DOME metrics model for THE DOME.

The nine-layer DOME (Dynamic Observation of Multi-dimensional Existence)
metric structure captures a whole-person view across biometric, clinical,
behavioral, economic, environmental, social, institutional, legal, and
subjective-wellbeing dimensions.  Each layer is a free-form dictionary
so that domain-specific engines can evolve their schemas independently.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DomeMetrics(BaseModel):
    """Nine-layer DOME metrics snapshot.

    Each layer is stored as an open ``dict[str, Any]`` so that upstream
    data pipelines can inject arbitrary domain metrics without requiring
    a schema migration.  Downstream consumers should validate the
    contents of each layer against their own expectations.
    """

    biometric_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Biometric indicators (e.g. vitals, lab results, wearable data).",
    )
    clinical_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Clinical data (diagnoses, procedures, medications).",
    )
    behavioral_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Behavioral signals (substance use, adherence, activity patterns).",
    )
    economic_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Economic indicators (income, employment, financial stress).",
    )
    environmental_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Environmental factors (housing quality, pollution, food access).",
    )
    social_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Social determinants (network size, isolation, community engagement).",
    )
    institutional_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Institutional interactions (program enrollment, benefit gaps).",
    )
    legal_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Legal factors (justice involvement, supervision status, legal needs).",
    )
    subjective_wellbeing_layer: dict[str, Any] = Field(
        default_factory=dict,
        description="Self-reported wellbeing (life satisfaction, purpose, autonomy).",
    )
