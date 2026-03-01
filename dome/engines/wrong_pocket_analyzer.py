"""Wrong-Pocket Analyzer for THE DOME.

The "wrong pocket" problem is one of the core barriers to effective
intervention in complex human-services cases: the entity that *pays* for an
intervention is rarely the same entity that *saves* from the intervention's
downstream effects.  A county that funds housing-first saves money for
CMS-Medicaid (fewer ER visits), State Corrections (fewer incarcerations),
and hospitals (less uncompensated care) -- but sees little direct return.

This engine computes an **intervention-payer savings matrix** that makes the
cross-payer fiscal flows explicit, then builds a ``SettlementMatrix`` that
proposes the inter-payer transfers needed to align incentives.

Algorithm
---------
1. For each candidate intervention, look up which policy domains it affects
   and by what percentage (reduction in domain spend).

2. Map domain-level savings to specific payer entities using empirically
   derived allocation shares (e.g., healthcare savings flow 40% to
   CMS-Medicaid, 30% to CMS-Medicare, 20% to hospitals, 10% to State).

3. Construct a matrix:  rows = interventions, columns = payer entities,
   cells = expected annual savings to that payer.

4. Build a ``SettlementMatrix`` that identifies who pays for the intervention,
   who benefits, and what transfers are needed to make everyone whole.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from dome.models.budget_key import PersonBudgetKey
from dome.models.budget_output import (
    PayerBreakdown,
    WholePersonBudget,
)
from dome.models.intervention import InterventionDefinition
from dome.models.settlement_matrix import (
    PayerSettlementRow,
    PayerTransfer,
    SettlementMatrix,
)


# ---------------------------------------------------------------------------
# Constants: intervention domain-reduction effects
# ---------------------------------------------------------------------------

# Each intervention maps to the domains it affects and the fractional
# reduction in annual domain spend.  Negative values indicate cost reduction.
_INTERVENTION_DOMAIN_EFFECTS: dict[str, dict[str, float]] = {
    "housing_first": {
        "housing": -0.60,
        "healthcare": -0.40,
        "justice": -0.30,
    },
    "CBT": {
        "healthcare": -0.20,
        "income_support": -0.15,
    },
    "income_bridge": {
        "income_support": -0.40,
        "housing": -0.20,
        "food": -0.30,
    },
    "MAT": {
        "healthcare": -0.50,
        "justice": -0.40,
    },
    "supported_employment": {
        "income_support": -0.60,
        "housing": -0.20,
    },
    "care_coordination": {
        "healthcare": -0.30,
    },
    "reentry_services": {
        "justice": -0.50,
        "housing": -0.20,
        "income_support": -0.20,
    },
}


# ---------------------------------------------------------------------------
# Constants: domain-to-payer savings allocation
# ---------------------------------------------------------------------------

# The canonical set of payer entities used in the matrix columns.
_PAYER_ENTITIES: list[dict[str, str]] = [
    {"id": "cms_medicaid", "level": "federal", "name": "CMS-Medicaid"},
    {"id": "cms_medicare", "level": "federal", "name": "CMS-Medicare"},
    {"id": "hud", "level": "federal", "name": "HUD"},
    {"id": "state_dhs", "level": "state", "name": "State DHS"},
    {"id": "state_corrections", "level": "state", "name": "State Corrections"},
    {"id": "county", "level": "local", "name": "County"},
    {"id": "city", "level": "local", "name": "City"},
    {"id": "hospitals", "level": "health_system", "name": "Hospitals"},
    {"id": "nonprofits", "level": "nonprofit", "name": "Nonprofits"},
]

_PAYER_IDS: list[str] = [p["id"] for p in _PAYER_ENTITIES]
_PAYER_LOOKUP: dict[str, dict[str, str]] = {p["id"]: p for p in _PAYER_ENTITIES}

# When a domain sees savings, this table specifies what fraction goes to
# each payer entity.  Shares within each domain should sum to 1.0.
_DOMAIN_TO_PAYER_ALLOCATION: dict[str, dict[str, float]] = {
    "healthcare": {
        "cms_medicaid": 0.40,
        "cms_medicare": 0.30,
        "hospitals": 0.20,
        "state_dhs": 0.10,
    },
    "housing": {
        "hud": 0.50,
        "state_dhs": 0.20,
        "county": 0.20,
        "city": 0.10,
    },
    "justice": {
        "state_corrections": 0.50,
        "county": 0.30,
        "city": 0.20,
    },
    "income_support": {
        "cms_medicaid": 0.20,   # Medicaid savings from income stability
        "state_dhs": 0.40,
        "county": 0.15,
        "nonprofits": 0.10,
        "hud": 0.15,
    },
    "food": {
        "cms_medicaid": 0.15,   # Federal SNAP
        "state_dhs": 0.25,
        "county": 0.20,
        "nonprofits": 0.40,     # Food banks etc.
    },
    "education": {
        "state_dhs": 0.45,
        "county": 0.40,
        "nonprofits": 0.15,
    },
    "child_family": {
        "state_dhs": 0.40,
        "county": 0.30,
        "nonprofits": 0.20,
        "cms_medicaid": 0.10,
    },
    "transport": {
        "city": 0.50,
        "county": 0.30,
        "state_dhs": 0.20,
    },
    "other": {
        "state_dhs": 0.40,
        "county": 0.30,
        "city": 0.20,
        "nonprofits": 0.10,
    },
}


# ---------------------------------------------------------------------------
# Constants: intervention cost and typical payer of the intervention
# ---------------------------------------------------------------------------

# Annual cost of each intervention and which payer entity typically funds it.
_INTERVENTION_COSTS: dict[str, dict[str, Any]] = {
    "housing_first": {
        "annual_cost": 22_000.0,
        "typical_duration_years": 3.0,
        "funders": {
            "hud": 0.40,
            "county": 0.25,
            "state_dhs": 0.20,
            "nonprofits": 0.15,
        },
    },
    "CBT": {
        "annual_cost": 6_000.0,
        "typical_duration_years": 1.0,
        "funders": {
            "cms_medicaid": 0.50,
            "state_dhs": 0.25,
            "nonprofits": 0.25,
        },
    },
    "income_bridge": {
        "annual_cost": 12_000.0,
        "typical_duration_years": 2.0,
        "funders": {
            "state_dhs": 0.40,
            "county": 0.30,
            "nonprofits": 0.30,
        },
    },
    "MAT": {
        "annual_cost": 8_500.0,
        "typical_duration_years": 2.0,
        "funders": {
            "cms_medicaid": 0.50,
            "state_dhs": 0.20,
            "hospitals": 0.15,
            "nonprofits": 0.15,
        },
    },
    "supported_employment": {
        "annual_cost": 15_000.0,
        "typical_duration_years": 2.0,
        "funders": {
            "state_dhs": 0.40,
            "county": 0.25,
            "nonprofits": 0.25,
            "hud": 0.10,
        },
    },
    "care_coordination": {
        "annual_cost": 5_000.0,
        "typical_duration_years": 3.0,
        "funders": {
            "cms_medicaid": 0.40,
            "hospitals": 0.25,
            "state_dhs": 0.20,
            "nonprofits": 0.15,
        },
    },
    "reentry_services": {
        "annual_cost": 10_000.0,
        "typical_duration_years": 2.0,
        "funders": {
            "state_corrections": 0.35,
            "county": 0.25,
            "state_dhs": 0.20,
            "nonprofits": 0.20,
        },
    },
}

# Default horizon for wrong-pocket analysis (5-year window).
_DEFAULT_ANALYSIS_HORIZON_YEARS: float = 5.0

# Model version string.
_MODEL_VERSION: str = "dome-wrong-pocket-v1.0"


# ---------------------------------------------------------------------------
# Helper: extract annual domain spend from budget
# ---------------------------------------------------------------------------

def _extract_domain_annual_spend(budget: WholePersonBudget) -> dict[str, float]:
    """Extract annualised domain-level spend from the budget.

    Prefers the ``"5y"`` horizon for a balanced estimate; falls back to
    ``"1y"`` or the first available horizon.
    """
    preferred_labels = ["5y", "1y", "20y", "lifetime"]
    chosen_hz = None

    for label in preferred_labels:
        for hz in budget.horizons:
            if hz.label == label:
                chosen_hz = hz
                break
        if chosen_hz is not None:
            break

    if chosen_hz is None and budget.horizons:
        chosen_hz = budget.horizons[0]

    if chosen_hz is None:
        return {}

    span_years = max((chosen_hz.end_date - chosen_hz.start_date).days / 365.25, 1.0)

    domain_annual: dict[str, float] = {}
    for db in chosen_hz.domain_view:
        domain_annual[db.domain] = db.expected_spend / span_years

    return domain_annual


# ---------------------------------------------------------------------------
# Helper: resolve intervention name
# ---------------------------------------------------------------------------

def _resolve_intervention_name(intervention: InterventionDefinition | str) -> str:
    """Extract the canonical intervention name string."""
    if isinstance(intervention, str):
        return intervention
    # Try to match the InterventionDefinition name to our catalog.
    name = intervention.name.lower().replace(" ", "_").replace("-", "_")
    # Fuzzy matching for common variants.
    _ALIASES: dict[str, str] = {
        "housing_first": "housing_first",
        "rapid_rehousing": "housing_first",
        "permanent_supportive_housing": "housing_first",
        "cbt": "CBT",
        "cognitive_behavioral_therapy": "CBT",
        "income_bridge": "income_bridge",
        "emergency_cash": "income_bridge",
        "mat": "MAT",
        "medication_assisted_treatment": "MAT",
        "buprenorphine": "MAT",
        "methadone": "MAT",
        "supported_employment": "supported_employment",
        "ips": "supported_employment",
        "individual_placement_and_support": "supported_employment",
        "care_coordination": "care_coordination",
        "case_management": "care_coordination",
        "reentry_services": "reentry_services",
        "reentry": "reentry_services",
        "transitional_services": "reentry_services",
    }
    return _ALIASES.get(name, name)


# ===========================================================================
# WrongPocketAnalyzer -- the public API
# ===========================================================================

class WrongPocketAnalyzer:
    """Analyze wrong-pocket dynamics for cross-payer interventions.

    Computes a savings matrix showing, for each candidate intervention, how
    much each payer entity is projected to save.  Then constructs a
    ``SettlementMatrix`` that proposes transfers to align incentives between
    the entity paying for the intervention and the entities receiving the
    downstream savings.

    Examples
    --------
    >>> analyzer = WrongPocketAnalyzer()
    >>> result = analyzer.analyze(budget_key, budget, ["housing_first", "MAT"])
    >>> result["savings_matrix"]["housing_first"]["cms_medicaid"]
    18432.0
    >>> result["settlement"].transfers[0].amount
    12500.0
    """

    def __init__(
        self,
        analysis_horizon_years: float = _DEFAULT_ANALYSIS_HORIZON_YEARS,
    ) -> None:
        """Initialize the analyzer.

        Parameters
        ----------
        analysis_horizon_years : float
            Number of years over which to project savings (default 5).
        """
        self._horizon_years = analysis_horizon_years

    def analyze(
        self,
        budget_key: PersonBudgetKey,
        budget: WholePersonBudget,
        interventions: list[InterventionDefinition | str],
    ) -> dict[str, Any]:
        """Run the wrong-pocket analysis.

        Parameters
        ----------
        budget_key : PersonBudgetKey
            Person-level attributes.
        budget : WholePersonBudget
            Computed whole-person budget.
        interventions : list[InterventionDefinition | str]
            Candidate interventions to evaluate.  May be
            ``InterventionDefinition`` objects or plain intervention name
            strings (e.g. ``"housing_first"``, ``"MAT"``).

        Returns
        -------
        dict
            Keys:

            - ``savings_matrix``:  ``dict[str, dict[str, float]]``
              Rows = intervention names, columns = payer entity IDs,
              cells = expected savings over the analysis horizon.

            - ``cost_matrix``:  ``dict[str, dict[str, float]]``
              Rows = intervention names, columns = payer entity IDs,
              cells = expected cost borne by each payer to fund the
              intervention.

            - ``net_position_matrix``:  ``dict[str, dict[str, float]]``
              Savings minus cost for each intervention-payer pair.

            - ``settlement``: ``SettlementMatrix``
              Proposed inter-payer transfers for the combined intervention
              package.

            - ``payer_entities``: list of payer entity metadata dicts.

            - ``summary``: High-level narrative summary dict.
        """
        domain_annual = _extract_domain_annual_spend(budget)

        savings_matrix: dict[str, dict[str, float]] = {}
        cost_matrix: dict[str, dict[str, float]] = {}
        net_position_matrix: dict[str, dict[str, float]] = {}

        for intervention in interventions:
            name = _resolve_intervention_name(intervention)
            savings_row = self._compute_savings_row(name, domain_annual)
            cost_row = self._compute_cost_row(name)
            net_row = {
                payer_id: round(savings_row.get(payer_id, 0.0) - cost_row.get(payer_id, 0.0), 2)
                for payer_id in _PAYER_IDS
            }

            savings_matrix[name] = savings_row
            cost_matrix[name] = cost_row
            net_position_matrix[name] = net_row

        # Build aggregate settlement across all interventions.
        settlement = self._build_settlement(
            budget_key, savings_matrix, cost_matrix, net_position_matrix,
        )

        # Build summary.
        summary = self._build_summary(
            savings_matrix, cost_matrix, net_position_matrix,
        )

        return {
            "savings_matrix": savings_matrix,
            "cost_matrix": cost_matrix,
            "net_position_matrix": net_position_matrix,
            "settlement": settlement,
            "payer_entities": _PAYER_ENTITIES,
            "summary": summary,
        }

    # ----- private: savings computation ------------------------------------

    def _compute_savings_row(
        self,
        intervention_name: str,
        domain_annual: dict[str, float],
    ) -> dict[str, float]:
        """Compute expected savings by payer entity for one intervention.

        Parameters
        ----------
        intervention_name : str
            Canonical intervention name.
        domain_annual : dict[str, float]
            Annual domain-level spend for the person.

        Returns
        -------
        dict[str, float]
            Payer entity ID -> expected savings over the analysis horizon.
        """
        effects = _INTERVENTION_DOMAIN_EFFECTS.get(intervention_name, {})
        payer_savings: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}

        for domain, reduction_fraction in effects.items():
            # reduction_fraction is negative (e.g. -0.40).
            annual_domain_spend = domain_annual.get(domain, 0.0)
            annual_saving = annual_domain_spend * abs(reduction_fraction)
            horizon_saving = annual_saving * self._horizon_years

            # Allocate across payer entities.
            allocation = _DOMAIN_TO_PAYER_ALLOCATION.get(domain, {})
            for payer_id, share in allocation.items():
                payer_savings[payer_id] += horizon_saving * share

        # Round all values.
        return {k: round(v, 2) for k, v in payer_savings.items()}

    def _compute_cost_row(
        self,
        intervention_name: str,
    ) -> dict[str, float]:
        """Compute intervention cost borne by each payer entity.

        Parameters
        ----------
        intervention_name : str
            Canonical intervention name.

        Returns
        -------
        dict[str, float]
            Payer entity ID -> cost allocated to that payer.
        """
        info = _INTERVENTION_COSTS.get(intervention_name)
        payer_costs: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}

        if info is None:
            # Unknown intervention: assume generic $10K/year split across
            # state + county + nonprofits.
            total_cost = 10_000.0 * min(self._horizon_years, 3.0)
            payer_costs["state_dhs"] = round(total_cost * 0.40, 2)
            payer_costs["county"] = round(total_cost * 0.30, 2)
            payer_costs["nonprofits"] = round(total_cost * 0.30, 2)
            return payer_costs

        annual_cost = info["annual_cost"]
        duration = min(info["typical_duration_years"], self._horizon_years)
        total_cost = annual_cost * duration

        for payer_id, share in info["funders"].items():
            payer_costs[payer_id] = round(total_cost * share, 2)

        return payer_costs

    # ----- private: settlement matrix construction -------------------------

    def _build_settlement(
        self,
        budget_key: PersonBudgetKey,
        savings_matrix: dict[str, dict[str, float]],
        cost_matrix: dict[str, dict[str, float]],
        net_position_matrix: dict[str, dict[str, float]],
    ) -> SettlementMatrix:
        """Build a ``SettlementMatrix`` from the analysis results.

        Aggregates positions across all interventions and proposes transfers
        from net beneficiaries (those who save more than they pay) to net
        investors (those who pay more than they save).
        """
        # Aggregate across all interventions.
        agg_savings: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}
        agg_costs: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}
        agg_net: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}

        for intervention_name in savings_matrix:
            for pid in _PAYER_IDS:
                agg_savings[pid] += savings_matrix[intervention_name].get(pid, 0.0)
                agg_costs[pid] += cost_matrix[intervention_name].get(pid, 0.0)

        for pid in _PAYER_IDS:
            agg_net[pid] = agg_savings[pid] - agg_costs[pid]

        # Build payer rows.
        payer_rows: list[PayerSettlementRow] = []
        for pid in _PAYER_IDS:
            meta = _PAYER_LOOKUP[pid]
            payer_rows.append(PayerSettlementRow(
                payer_id=pid,
                payer_level=meta["level"],
                payer_name=meta["name"],
                upfront_investment=round(agg_costs[pid], 2),
                expected_gross_savings=round(agg_savings[pid], 2),
                net_position_after_settlement=round(agg_net[pid], 2),
            ))

        # Compute transfers: from net beneficiaries to net investors.
        transfers = self._compute_transfers(agg_net, agg_costs)

        # Update net positions after transfers.
        transfer_adjustments: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}
        for t in transfers:
            transfer_adjustments[t.from_payer_id] -= t.amount
            transfer_adjustments[t.to_payer_id] += t.amount

        for row in payer_rows:
            row.net_position_after_settlement = round(
                agg_net[row.payer_id] + transfer_adjustments.get(row.payer_id, 0.0), 2
            )

        # Build combined scenario ID.
        intervention_names = sorted(savings_matrix.keys())
        scenario_id = "wrong_pocket_" + "_".join(intervention_names)

        return SettlementMatrix(
            person_uid=budget_key.person_uid,
            scenario_id=scenario_id,
            horizon_label="5y",
            currency="USD",
            payers=payer_rows,
            transfers=transfers,
            assumptions={
                "analysis_horizon_years": self._horizon_years,
                "real_discount_rate": 0.03,
                "domain_savings_model": "proportional_reduction",
                "payer_allocation_model": "empirical_shares_v1",
                "interventions_analyzed": intervention_names,
            },
            generated_at=datetime.now(timezone.utc),
            model_version=_MODEL_VERSION,
        )

    def _compute_transfers(
        self,
        agg_net: dict[str, float],
        agg_costs: dict[str, float],
    ) -> list[PayerTransfer]:
        """Propose inter-payer transfers to settle wrong-pocket imbalances.

        Logic:
        - Identify **net beneficiaries**: payers with positive net position
          (they save more than they invest).  They owe transfers.
        - Identify **net investors**: payers with negative net position
          (they invest more than they save).  They receive transfers.
        - Transfers flow from the largest beneficiary to the largest
          investor, proportional to the size of the imbalance, until
          all positions are zeroed out (or as close as rounding permits).

        The transfer schedule is set to "quarterly over {horizon} years"
        to spread out the fiscal impact.
        """
        # Separate net beneficiaries (positive net) from net investors (negative net).
        beneficiaries: list[tuple[str, float]] = []
        investors: list[tuple[str, float]] = []

        for pid in _PAYER_IDS:
            net_val = agg_net[pid]
            if net_val > 100.0:  # meaningful positive balance
                beneficiaries.append((pid, net_val))
            elif net_val < -100.0:  # meaningful negative balance
                investors.append((pid, abs(net_val)))

        if not beneficiaries or not investors:
            return []

        # Sort both lists by magnitude (descending).
        beneficiaries.sort(key=lambda x: x[1], reverse=True)
        investors.sort(key=lambda x: x[1], reverse=True)

        # Total transferable pool: min of total surplus and total deficit.
        total_surplus = sum(b[1] for b in beneficiaries)
        total_deficit = sum(i[1] for i in investors)
        pool = min(total_surplus, total_deficit)

        transfers: list[PayerTransfer] = []
        schedule = f"quarterly over {self._horizon_years:.0f} years"

        # Greedy matching: largest beneficiary pays largest investor first.
        b_remaining = {pid: amt for pid, amt in beneficiaries}
        i_remaining = {pid: amt for pid, amt in investors}

        for b_pid in [b[0] for b in beneficiaries]:
            if b_remaining[b_pid] <= 0.0:
                continue
            for i_pid in [i[0] for i in investors]:
                if i_remaining[i_pid] <= 0.0:
                    continue

                transfer_amt = min(b_remaining[b_pid], i_remaining[i_pid])
                if transfer_amt < 50.0:
                    continue  # skip trivial transfers

                transfers.append(PayerTransfer(
                    from_payer_id=b_pid,
                    to_payer_id=i_pid,
                    amount=round(transfer_amt, 2),
                    transfer_schedule=schedule,
                ))

                b_remaining[b_pid] -= transfer_amt
                i_remaining[i_pid] -= transfer_amt

        return transfers

    # ----- private: summary ------------------------------------------------

    @staticmethod
    def _build_summary(
        savings_matrix: dict[str, dict[str, float]],
        cost_matrix: dict[str, dict[str, float]],
        net_position_matrix: dict[str, dict[str, float]],
    ) -> dict[str, Any]:
        """Build a narrative summary of the wrong-pocket analysis.

        Returns a dict with aggregate statistics and key findings.
        """
        total_savings = 0.0
        total_cost = 0.0

        for intervention_name in savings_matrix:
            total_savings += sum(savings_matrix[intervention_name].values())
            total_cost += sum(cost_matrix[intervention_name].values())

        net_benefit = total_savings - total_cost
        roi = total_savings / total_cost if total_cost > 0 else 0.0

        # Find the biggest winner and biggest loser (wrong-pocket victims).
        payer_net_agg: dict[str, float] = {pid: 0.0 for pid in _PAYER_IDS}
        for intervention_name in net_position_matrix:
            for pid in _PAYER_IDS:
                payer_net_agg[pid] += net_position_matrix[intervention_name].get(pid, 0.0)

        biggest_winner = max(payer_net_agg.items(), key=lambda x: x[1])
        biggest_loser = min(payer_net_agg.items(), key=lambda x: x[1])

        # Identify wrong-pocket misalignments: payers whose cost > savings.
        misaligned_payers = [
            {
                "payer_id": pid,
                "payer_name": _PAYER_LOOKUP[pid]["name"],
                "cost_borne": round(sum(
                    cost_matrix[i].get(pid, 0.0) for i in cost_matrix
                ), 2),
                "savings_received": round(sum(
                    savings_matrix[i].get(pid, 0.0) for i in savings_matrix
                ), 2),
                "net_position": round(payer_net_agg[pid], 2),
            }
            for pid in _PAYER_IDS
            if payer_net_agg[pid] < -100.0  # meaningfully negative
        ]

        # Identify free-rider payers: those who receive savings without
        # investing (cost ~ 0 but savings > 0).
        free_riders = [
            {
                "payer_id": pid,
                "payer_name": _PAYER_LOOKUP[pid]["name"],
                "savings_received": round(sum(
                    savings_matrix[i].get(pid, 0.0) for i in savings_matrix
                ), 2),
            }
            for pid in _PAYER_IDS
            if (
                sum(cost_matrix[i].get(pid, 0.0) for i in cost_matrix) < 100.0
                and sum(savings_matrix[i].get(pid, 0.0) for i in savings_matrix) > 500.0
            )
        ]

        return {
            "total_savings": round(total_savings, 2),
            "total_intervention_cost": round(total_cost, 2),
            "net_benefit": round(net_benefit, 2),
            "aggregate_roi": round(roi, 2),
            "biggest_beneficiary": {
                "payer_id": biggest_winner[0],
                "payer_name": _PAYER_LOOKUP[biggest_winner[0]]["name"],
                "net_gain": round(biggest_winner[1], 2),
            },
            "biggest_investor": {
                "payer_id": biggest_loser[0],
                "payer_name": _PAYER_LOOKUP[biggest_loser[0]]["name"],
                "net_cost": round(biggest_loser[1], 2),
            },
            "wrong_pocket_victims": misaligned_payers,
            "free_riders": free_riders,
            "interventions_analyzed": sorted(savings_matrix.keys()),
        }
