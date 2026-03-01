"""Static profile models for THE DOME.

This module captures the essentially immutable or very-slowly-changing
characteristics of a person: birth geography, parental socioeconomic
status, early-childhood adversity, and genetic risk flags.  These
attributes anchor the causal graph's initial conditions.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class StaticProfile(BaseModel):
    """Time-invariant (or near-invariant) personal attributes.

    Fields like parental income quintile or ACE score rarely change after
    they are first recorded.  ``birth_tract_fips`` never changes;
    ``current_tract_fips`` is refreshed from the identity spine on each
    snapshot but is included here for convenience.
    """

    birth_tract_fips: str = Field(
        ...,
        pattern=r"^\d{11}$",
        description="11-digit Census tract FIPS code of the birth location.",
    )
    current_tract_fips: str = Field(
        ...,
        pattern=r"^\d{11}$",
        description="11-digit Census tract FIPS code of the current residence.",
    )
    parental_income_quintile: int | None = Field(
        default=None,
        description="Household income quintile of parents at time of birth (1-5).",
    )
    parental_education_level: (
        Literal["<HS", "HS", "some_college", "BA", "Grad"] | None
    ) = Field(
        default=None,
        description="Highest education credential of most-educated parent.",
    )
    ace_score_estimate: float | None = Field(
        default=None,
        ge=0,
        le=10,
        description="Estimated Adverse Childhood Experiences score (0-10).",
    )
    birth_weight_grams: float | None = Field(
        default=None,
        gt=0,
        description="Birth weight in grams.",
    )
    genetics_risk_flags: list[str] = Field(
        default_factory=list,
        description=(
            "Known genetic risk markers, e.g. "
            "['BRCA1', 'sickle_cell_trait']."
        ),
    )

    @field_validator("parental_income_quintile")
    @classmethod
    def _quintile_range(cls, v: int | None) -> int | None:
        if v is not None and (v < 1 or v > 5):
            raise ValueError("parental_income_quintile must be between 1 and 5")
        return v
