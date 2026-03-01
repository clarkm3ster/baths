"""Settlement matrix models for THE DOME.

The settlement matrix determines how costs and savings are redistributed
among payers when an intervention changes a person's fiscal trajectory.
``PayerSettlementRow`` tracks each payer's position; ``PayerTransfer``
records the inter-payer transfers needed to settle; and ``SettlementMatrix``
ties everything together for a given person, scenario, and horizon.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class PayerSettlementRow(BaseModel):
    """One payer's position in the settlement matrix.

    Captures the payer's upfront investment in interventions, the gross
    savings they are projected to realise, and their net position after
    inter-payer transfers are applied.
    """

    payer_id: str = Field(
        ..., description="Unique identifier for this payer."
    )
    payer_level: Literal[
        "federal", "state", "local", "nonprofit", "health_system"
    ] = Field(
        ..., description="Government level or sector of the payer."
    )
    payer_name: str = Field(
        ..., description="Human-readable payer name."
    )
    upfront_investment: float = Field(
        ...,
        description="Amount the payer invests upfront in interventions (USD).",
    )
    expected_gross_savings: float = Field(
        ...,
        description="Gross savings the payer is projected to realise (USD).",
    )
    net_position_after_settlement: float = Field(
        ...,
        description=(
            "Payer's net financial position after transfers (USD).  "
            "Positive means net gain; negative means net cost."
        ),
    )


class PayerTransfer(BaseModel):
    """A single inter-payer transfer in the settlement.

    When one payer realises savings from another payer's investment, a
    transfer may be warranted to ensure equitable distribution of costs
    and benefits.
    """

    from_payer_id: str = Field(
        ..., description="Payer ID of the entity sending the transfer."
    )
    to_payer_id: str = Field(
        ..., description="Payer ID of the entity receiving the transfer."
    )
    amount: float = Field(
        ..., description="Transfer amount (USD)."
    )
    transfer_schedule: str | None = Field(
        default=None,
        description=(
            "Description of the payment schedule, e.g. "
            "'quarterly over 5 years', 'lump sum at year end'."
        ),
    )


class SettlementMatrix(BaseModel):
    """Complete settlement matrix for a person-scenario-horizon combination.

    Brings together all payer positions, the transfers needed to settle
    them, and the assumptions underlying the calculation.
    """

    person_uid: str = Field(
        ..., description="Unique person identifier."
    )
    scenario_id: str = Field(
        ..., description="Scenario ID this settlement corresponds to."
    )
    horizon_label: Literal["1y", "5y", "20y", "lifetime"] = Field(
        ..., description="Time horizon label for the settlement."
    )
    currency: str = Field(
        default="USD", description="Currency code for all monetary values."
    )
    payers: list[PayerSettlementRow] = Field(
        default_factory=list,
        description="Settlement position for each involved payer.",
    )
    transfers: list[PayerTransfer] = Field(
        default_factory=list,
        description="Inter-payer transfers required to settle.",
    )
    assumptions: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Key assumptions underlying the settlement "
            "(e.g. discount rate, cost-growth rate, attribution method)."
        ),
    )
    generated_at: datetime = Field(
        ..., description="UTC timestamp when this settlement was generated."
    )
    model_version: str = Field(
        ..., description="Version identifier of the settlement engine model."
    )
