"""Fiscal event models for THE DOME.

A ``FiscalEvent`` represents a single financial transaction between a payer
(federal, state, local, nonprofit, or health-system) and a person.  It
captures the who-paid-what-for-whom detail that feeds the Whole-Person Budget
engine and enables cross-payer settlement analysis.
"""

from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class FiscalEvent(BaseModel):
    """A single fiscal transaction associated with a person.

    Every dollar that flows to or on behalf of a person -- whether a Medicaid
    claim, a SNAP benefit, a housing voucher payment, or a tax credit -- is
    represented as one ``FiscalEvent``.  The combination of ``domain``,
    ``mechanism``, and ``service_category`` allows the budget engine to
    aggregate spending along multiple axes.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Globally unique event identifier (UUID4 by default).",
    )
    person_uid: str = Field(
        ..., description="Unique person identifier linking to the IdentitySpine."
    )
    event_date: date = Field(
        ..., description="Date the fiscal event occurred or was recorded."
    )
    payer_level: Literal[
        "federal", "state", "local", "nonprofit", "health_system"
    ] = Field(
        ..., description="Government level or sector of the paying entity."
    )
    payer_entity: str = Field(
        ...,
        description=(
            "Name of the specific payer, e.g. 'CMS', "
            "'State of Ohio ODJFS', 'County General Fund'."
        ),
    )
    program_or_fund: str = Field(
        ...,
        description=(
            "Program or funding stream, e.g. 'Medicaid', 'SNAP', "
            "'Section 8 HCV', 'EITC'."
        ),
    )
    domain: Literal[
        "healthcare",
        "income_support",
        "housing",
        "food",
        "education",
        "justice",
        "child_family",
        "transport",
        "other",
    ] = Field(
        ..., description="High-level policy domain of the spending."
    )
    mechanism: Literal[
        "cash_transfer",
        "in_kind_benefit",
        "service_utilization",
        "tax_expenditure",
    ] = Field(
        ..., description="How the value was delivered to the person."
    )
    service_category: str = Field(
        ...,
        description=(
            "Finer-grained category within the domain, e.g. "
            "'inpatient', 'outpatient', 'pharmacy', 'rental_assistance'."
        ),
    )
    utilization_unit: str = Field(
        ...,
        description=(
            "Unit of service or benefit, e.g. 'claim', 'month', "
            "'visit', 'bed_day'."
        ),
    )
    quantity: float | None = Field(
        default=None,
        ge=0,
        description="Number of utilization units consumed.",
    )
    amount_paid: float = Field(
        ..., description="Dollar amount paid for this event (USD)."
    )
    amount_type: Literal["actual_claim", "estimated_unit_cost"] = Field(
        ...,
        description=(
            "Whether amount_paid is from an actual adjudicated claim or "
            "an estimated unit cost applied to quantity."
        ),
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description=(
            "Confidence score (0-1) reflecting data quality and attribution "
            "certainty for this event."
        ),
    )
    data_source_system: str = Field(
        ...,
        description=(
            "Originating data system, e.g. 'state_mmis', 'irs_soi', "
            "'hmis', 'court_records'."
        ),
    )
    attribution_tags: list[str] = Field(
        default_factory=list,
        description=(
            "Tags for downstream attribution logic, e.g. "
            "['preventable_ed', 'cascade:housing_loss']."
        ),
    )

    @field_validator("confidence")
    @classmethod
    def _confidence_range(cls, v: float) -> float:
        """Ensure confidence is between 0 and 1 inclusive."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        return v
