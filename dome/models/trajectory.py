"""Fiscal trajectory models for THE DOME.

A ``FiscalTrajectoryTag`` classifies a person's lifetime net fiscal
relationship with the public sector into one of five tiers, from
net contributor through catastrophic net cost.  This tag drives
triage logic in the cascade and intervention engines.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class FiscalTrajectoryTag(BaseModel):
    """Lifetime fiscal trajectory classification for a person.

    The tag summarises whether, over the person's remaining lifetime, they
    are projected to be a net contributor to public revenues or a net cost
    -- and if a net cost, how extreme the projected shortfall is.  The
    ``net_fiscal_impact_npv`` provides the point-estimate in net-present-
    value dollars (positive = net contributor, negative = net cost).
    """

    person_uid: str = Field(
        ..., description="Unique person identifier."
    )
    horizon: Literal["lifetime"] = Field(
        ..., description="Time horizon for the trajectory (currently always 'lifetime')."
    )
    trajectory: Literal[
        "net_contributor",
        "break_even",
        "moderate_net_cost",
        "high_net_cost",
        "catastrophic_net_cost",
    ] = Field(
        ...,
        description=(
            "Qualitative tier: net_contributor (positive NPV), break_even, "
            "moderate_net_cost, high_net_cost, or catastrophic_net_cost."
        ),
    )
    net_fiscal_impact_npv: float = Field(
        ...,
        description=(
            "Net-present-value estimate of lifetime fiscal impact (USD).  "
            "Positive means the person is projected to contribute more in "
            "taxes than they consume in public services."
        ),
    )
