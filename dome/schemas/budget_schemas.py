"""Request/response schemas for budget endpoints."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class BudgetComputeRequest(BaseModel):
    """Request to compute a WholePersonBudget for a person."""

    horizons: list[HorizonRequest] = Field(
        default_factory=lambda: [
            HorizonRequest(label="1y"),
            HorizonRequest(label="5y"),
            HorizonRequest(label="lifetime"),
        ],
    )
    monte_carlo_iterations: int = Field(1000, ge=100, le=10000)
    include_scenarios: bool = True


class HorizonRequest(BaseModel):
    """Which time horizons to compute."""

    label: Literal["1y", "5y", "20y", "lifetime"]
    time_step: Literal["month", "quarter", "year"] = "year"
    start_date: date | None = None  # defaults to today
    end_date: date | None = None  # computed from label if omitted


class WrongPocketRequest(BaseModel):
    """Request for wrong-pocket analysis."""

    horizon_label: Literal["1y", "5y", "20y", "lifetime"] = "lifetime"
    interventions: list[str] | None = None  # specific interventions or all


class SettlementComputeRequest(BaseModel):
    """Request to compute a settlement matrix for a person + scenario."""

    scenario_id: str
    horizon_label: Literal["1y", "5y", "20y", "lifetime"] = "lifetime"
    risk_share_pct: float = Field(0.50, ge=0.0, le=1.0)
    cap_multiple: float = Field(3.0, ge=1.0)
