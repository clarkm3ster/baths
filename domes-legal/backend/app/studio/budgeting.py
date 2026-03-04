"""Production finance model — Monte Carlo budgeting for Dome Studio.

Provides:
- Cost-to-complete by stage
- Monte Carlo overrun risk (p50/p75/p90/p95)
- Return stack analysis (IP revenue, civic value, OS value)
"""
from __future__ import annotations

import random
import statistics
from datetime import date
from typing import Any
from pydantic import BaseModel, Field


# ── Result Models ──────────────────────────────────────────────────

class StageBreakdown(BaseModel):
    stage: str
    cost_cap: float
    status: str  # "completed", "in_progress", "upcoming"
    spent: float = 0.0


class CostToComplete(BaseModel):
    budget_total: float
    spent_to_date: float
    remaining: float
    percent_complete: float
    stages: list[StageBreakdown]


class OverrunRisk(BaseModel):
    p50: float
    p75: float
    p90: float
    p95: float
    probability_over_budget: float
    n_simulations: int


class ReturnStack(BaseModel):
    ip_revenue_low: float
    ip_revenue_high: float
    civic_value_score: float  # 0-1
    os_value_score: float  # 0-1
    roi_low: float
    roi_high: float


class FinancialSummary(BaseModel):
    cost_to_complete: CostToComplete
    overrun_risk: OverrunRisk
    return_stack: ReturnStack


# ── Stage ordering ─────────────────────────────────────────────────

STAGE_ORDER = ["development", "pre_production", "production", "post", "distribution"]

# Revenue ranges by medium (low, high) in USD
MEDIUM_REVENUE: dict[str, tuple[float, float]] = {
    "film": (50_000, 500_000),
    "short": (10_000, 100_000),
    "doc": (25_000, 250_000),
    "series": (100_000, 1_000_000),
    "installation": (20_000, 200_000),
    "live_event": (15_000, 150_000),
    "product": (30_000, 300_000),
    "game": (50_000, 500_000),
    "interactive": (25_000, 250_000),
}


def _stage_status(stage_data: dict, current_stage: str) -> str:
    """Determine if a stage is completed, in_progress, or upcoming."""
    stage_name = stage_data.get("stage", "")
    if stage_name not in STAGE_ORDER:
        return "upcoming"
    current_idx = STAGE_ORDER.index(current_stage) if current_stage in STAGE_ORDER else 0
    stage_idx = STAGE_ORDER.index(stage_name)
    if stage_idx < current_idx:
        return "completed"
    elif stage_idx == current_idx:
        return "in_progress"
    return "upcoming"


# ── Cost-to-Complete ───────────────────────────────────────────────

def calculate_cost_to_complete(production: dict[str, Any]) -> CostToComplete:
    """Calculate cost breakdown by stage."""
    budget_total = float(production.get("budget_total", 0))
    current_stage = production.get("stage", "greenlit")
    stages_data = production.get("stages", [])

    breakdowns = []
    spent = 0.0

    for s in stages_data:
        status = _stage_status(s, current_stage)
        cost_cap = float(s.get("cost_cap", 0))
        stage_spent = cost_cap if status == "completed" else 0.0
        if status == "in_progress":
            stage_spent = cost_cap * 0.5  # estimate 50% spent

        spent += stage_spent
        breakdowns.append(StageBreakdown(
            stage=s.get("stage", "unknown"),
            cost_cap=cost_cap,
            status=status,
            spent=stage_spent,
        ))

    remaining = max(budget_total - spent, 0)
    total_caps = sum(float(s.get("cost_cap", 0)) for s in stages_data)
    pct = (spent / total_caps * 100) if total_caps > 0 else 0

    return CostToComplete(
        budget_total=budget_total,
        spent_to_date=spent,
        remaining=remaining,
        percent_complete=round(pct, 1),
        stages=breakdowns,
    )


# ── Monte Carlo Overrun Risk ──────────────────────────────────────

def simulate_overrun_risk(
    production: dict[str, Any],
    n_simulations: int = 10_000,
) -> OverrunRisk:
    """Run Monte Carlo simulation on remaining stage costs.

    For each remaining stage, cost = cost_cap * (1 + overrun_factor)
    where overrun_factor ~ Triangular(min, mode, max).
    Risk register length drives the distribution shape.
    """
    budget_total = float(production.get("budget_total", 0))
    current_stage = production.get("stage", "greenlit")
    stages_data = production.get("stages", [])

    # Find remaining stages
    remaining_stages = []
    for s in stages_data:
        if _stage_status(s, current_stage) in ("in_progress", "upcoming"):
            remaining_stages.append(s)

    if not remaining_stages:
        return OverrunRisk(
            p50=0, p75=0, p90=0, p95=0,
            probability_over_budget=0, n_simulations=n_simulations,
        )

    # Already spent
    ctc = calculate_cost_to_complete(production)
    spent = ctc.spent_to_date

    totals = []
    for _ in range(n_simulations):
        sim_total = spent
        for s in remaining_stages:
            cost_cap = float(s.get("cost_cap", 0))
            risk_count = len(s.get("risk_register", []))

            # Higher risk = wider overrun distribution
            if risk_count <= 1:
                overrun = random.triangular(0, 0.05, 0.3)
            elif risk_count <= 3:
                overrun = random.triangular(0, 0.15, 0.6)
            else:
                overrun = random.triangular(0, 0.25, 1.0)

            sim_total += cost_cap * (1 + overrun)
        totals.append(sim_total)

    totals.sort()
    n = len(totals)

    return OverrunRisk(
        p50=round(totals[int(n * 0.50)], 2),
        p75=round(totals[int(n * 0.75)], 2),
        p90=round(totals[int(n * 0.90)], 2),
        p95=round(totals[int(n * 0.95)], 2),
        probability_over_budget=round(
            sum(1 for t in totals if t > budget_total) / n, 4
        ) if budget_total > 0 else 0,
        n_simulations=n_simulations,
    )


# ── Return Stack ───────────────────────────────────────────────────

def estimate_return_stack(
    production: dict[str, Any],
    gap_count: int = 0,
    learning_count: int = 0,
) -> ReturnStack:
    """Estimate IP, civic, and OS returns for a production."""
    budget_total = float(production.get("budget_total", 0))
    medium = production.get("medium", "short")

    # IP revenue estimate
    rev_low, rev_high = MEDIUM_REVENUE.get(medium, (10_000, 100_000))

    # Civic value: probability-weighted impact (0-1)
    # More gaps resolved = more civic value (discovery is valuable)
    civic = min(gap_count * 0.05 + learning_count * 0.15, 1.0)

    # OS value: features shipped, connector coverage
    os_val = min(gap_count * 0.03 + learning_count * 0.1, 1.0)

    # ROI
    roi_low = (rev_low - budget_total) / budget_total if budget_total > 0 else 0
    roi_high = (rev_high - budget_total) / budget_total if budget_total > 0 else 0

    return ReturnStack(
        ip_revenue_low=rev_low,
        ip_revenue_high=rev_high,
        civic_value_score=round(civic, 3),
        os_value_score=round(os_val, 3),
        roi_low=round(roi_low, 3),
        roi_high=round(roi_high, 3),
    )


# ── Full Summary ───────────────────────────────────────────────────

def full_financial_summary(
    production: dict[str, Any],
    gap_count: int = 0,
    learning_count: int = 0,
    n_simulations: int = 10_000,
) -> FinancialSummary:
    """Generate complete financial summary for a production."""
    return FinancialSummary(
        cost_to_complete=calculate_cost_to_complete(production),
        overrun_risk=simulate_overrun_risk(production, n_simulations),
        return_stack=estimate_return_stack(production, gap_count, learning_count),
    )
