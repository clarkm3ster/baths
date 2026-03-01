"""Budget output models for THE DOME.

These models represent the *output* of the Whole-Person Budget engine:
projected spending broken down by payer, policy domain, delivery mechanism,
risk quantile, and counterfactual scenario.  The top-level
``WholePersonBudget`` aggregates results across multiple time horizons.
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class PayerBreakdown(BaseModel):
    """Expected spend attributed to a single payer entity."""

    payer_level: str = Field(
        ..., description="Government level or sector (e.g. 'federal', 'state')."
    )
    payer_entity: str = Field(
        ..., description="Name of the specific payer entity."
    )
    expected_spend: float = Field(
        ..., description="Projected spending amount (USD)."
    )


class PayerView(BaseModel):
    """Aggregate spending projections broken down by payer tier.

    Provides both roll-up totals by payer level and a detailed per-entity
    breakdown list.
    """

    federal_expected_spend: float = Field(
        ..., description="Total projected federal spending (USD)."
    )
    state_expected_spend: float = Field(
        ..., description="Total projected state spending (USD)."
    )
    local_expected_spend: float = Field(
        ..., description="Total projected local/county spending (USD)."
    )
    healthcare_delivery_expected_spend: float = Field(
        ..., description="Total projected health-system spending (USD)."
    )
    nonprofit_expected_spend: float = Field(
        ..., description="Total projected nonprofit spending (USD)."
    )
    per_payer_breakdown: list[PayerBreakdown] = Field(
        default_factory=list,
        description="Itemised breakdown by individual payer entity.",
    )


class ProgramSpend(BaseModel):
    """Projected spending for a single program or funding stream."""

    program_or_fund: str = Field(
        ..., description="Program name (e.g. 'Medicaid', 'Section 8 HCV')."
    )
    expected_spend: float = Field(
        ..., description="Projected spending (USD)."
    )


class DomainBudget(BaseModel):
    """Projected spending within a single policy domain.

    Each domain (healthcare, housing, justice, etc.) aggregates spending
    across the programs that fund services in that domain.
    """

    domain: str = Field(
        ..., description="Policy domain (e.g. 'healthcare', 'housing')."
    )
    expected_spend: float = Field(
        ..., description="Total projected domain spending (USD)."
    )
    per_program: list[ProgramSpend] = Field(
        default_factory=list,
        description="Per-program breakdown within this domain.",
    )


class MechanismBudget(BaseModel):
    """Projected spending by delivery mechanism."""

    mechanism: str = Field(
        ...,
        description=(
            "Delivery mechanism (e.g. 'cash_transfer', 'in_kind_benefit', "
            "'service_utilization', 'tax_expenditure')."
        ),
    )
    expected_spend: float = Field(
        ..., description="Total projected spending via this mechanism (USD)."
    )


class CatastrophicEventRisk(BaseModel):
    """Risk profile for a single catastrophic cost event.

    Catastrophic events (e.g. incarceration, organ transplant, prolonged
    ICU stay) have low probability but extreme cost impact.  Each is modeled
    separately so that the settlement engine can price them.
    """

    event_type: str = Field(
        ...,
        description=(
            "Type of catastrophic event "
            "(e.g. 'incarceration', 'transplant', 'icu_30d')."
        ),
    )
    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated probability of occurrence within the horizon.",
    )
    expected_incremental_cost: float = Field(
        ...,
        description="Expected incremental cost if the event occurs (USD).",
    )
    payer_distribution: list[PayerBreakdown] = Field(
        default_factory=list,
        description="How incremental cost distributes across payers.",
    )


class RiskProfile(BaseModel):
    """Distributional cost summary across probability quantiles.

    Provides the 50th, 90th, and 99th percentile total-cost projections
    alongside an enumeration of identified catastrophic event risks.
    """

    p50_total_cost: float = Field(
        ..., description="Median (50th percentile) projected total cost (USD)."
    )
    p90_total_cost: float = Field(
        ..., description="90th percentile projected total cost (USD)."
    )
    p99_total_cost: float = Field(
        ..., description="99th percentile projected total cost (USD)."
    )
    catastrophic_events: list[CatastrophicEventRisk] = Field(
        default_factory=list,
        description="Identified catastrophic event risks.",
    )


class ScenarioBudget(BaseModel):
    """Counterfactual or intervention scenario cost projection.

    Each scenario describes what would happen to the person's projected
    budget if a specific intervention, policy change, or life event
    occurred.
    """

    scenario_id: str = Field(
        ..., description="Unique identifier for this scenario."
    )
    description: str = Field(
        ..., description="Human-readable description of the scenario."
    )
    incremental_cost_of_scenario: float = Field(
        ...,
        description="Cost of the intervention or change itself (USD).",
    )
    expected_total_cost_under_scenario: float = Field(
        ...,
        description="Projected total cost if the scenario is enacted (USD).",
    )
    expected_savings_vs_baseline: float = Field(
        ...,
        description=(
            "Expected savings relative to the baseline projection (USD).  "
            "Positive means the scenario saves money."
        ),
    )
    savings_by_payer: list[PayerBreakdown] = Field(
        default_factory=list,
        description="How savings distribute across payers.",
    )


class HorizonBudget(BaseModel):
    """Complete budget projection for a single time horizon.

    Combines payer, domain, mechanism, and risk views into a single coherent
    projection for one horizon window (e.g. 1-year, 5-year, lifetime).
    """

    label: str = Field(
        ..., description="Horizon label (e.g. '1y', '5y', 'lifetime')."
    )
    start_date: date = Field(
        ..., description="Inclusive start date of the projection window."
    )
    end_date: date = Field(
        ..., description="Inclusive end date of the projection window."
    )
    payer_view: PayerView = Field(
        ..., description="Spending breakdown by payer."
    )
    domain_view: list[DomainBudget] = Field(
        default_factory=list,
        description="Spending breakdown by policy domain.",
    )
    mechanism_view: list[MechanismBudget] = Field(
        default_factory=list,
        description="Spending breakdown by delivery mechanism.",
    )
    risk_profile: RiskProfile = Field(
        ..., description="Distributional cost risk profile."
    )
    scenarios: list[ScenarioBudget] | None = Field(
        default=None,
        description="Optional counterfactual scenario projections.",
    )


class WholePersonBudget(BaseModel):
    """Top-level budget output for a single person.

    Aggregates ``HorizonBudget`` projections across all requested time
    windows (1-year, 5-year, 20-year, lifetime) into one serialisable
    document.
    """

    person_uid: str = Field(
        ..., description="Unique person identifier."
    )
    generated_at: datetime = Field(
        ..., description="UTC timestamp when this budget was generated."
    )
    horizons: list[HorizonBudget] = Field(
        default_factory=list,
        description="Budget projections for each requested time horizon.",
    )
