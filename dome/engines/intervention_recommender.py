"""
Intervention Recommender Engine (Step 6)
==========================================

Selects the optimal set of interventions for a person given their active
cascade alerts, available budget, and the intervention catalogue.

The algorithm:

1. For each active ``CascadeAlert``, identify all interventions that target
   the current or next cascade link.
2. Score each intervention by its return-on-investment:
   ``score = expected_savings * break_probability / midpoint_cost``.
3. Apply a **greedy knapsack** strategy: sort all candidate interventions
   by ROI, then greedily add them to the plan until the budget is exhausted
   or no more candidates remain.
4. Compute aggregate plan metrics: total cost, expected savings, and
   expected ROI.

Usage::

    from dome.engines.intervention_recommender import InterventionRecommender
    recommender = InterventionRecommender()
    plan = recommender.recommend(cascade_alerts, budget_key)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dome.data.cascades import CASCADE_DEFINITIONS
from dome.data.interventions import INTERVENTION_DEFINITIONS, INTERVENTION_INDEX
from dome.models.budget_key import PersonBudgetKey
from dome.models.cascade import CascadeAlert, CascadeDefinition
from dome.models.intervention import InterventionDefinition, InterventionPlan


@dataclass
class _ScoredIntervention:
    """Internal struct for ranking candidate interventions."""

    intervention: InterventionDefinition
    alert: CascadeAlert
    midpoint_cost: float
    expected_savings: float
    break_probability: float
    roi_score: float
    link_label: str


class InterventionRecommender:
    """Optimal intervention selection engine.

    Given a set of cascade alerts and an optional budget constraint,
    selects the highest-ROI combination of interventions using a greedy
    knapsack approach.

    Parameters
    ----------
    intervention_defs : list[InterventionDefinition] | None
        Custom intervention catalogue.  Defaults to the built-in
        ``INTERVENTION_DEFINITIONS`` from :mod:`dome.data.interventions`.
    cascade_defs : list[CascadeDefinition] | None
        Custom cascade definitions for link lookup.  Defaults to the
        built-in ``CASCADE_DEFINITIONS``.
    default_max_budget : float
        Default maximum budget when ``max_budget`` is not specified in
        the ``recommend`` call (default: $100,000).
    """

    def __init__(
        self,
        intervention_defs: list[InterventionDefinition] | None = None,
        cascade_defs: list[CascadeDefinition] | None = None,
        default_max_budget: float = 100_000.0,
    ) -> None:
        self.intervention_defs = intervention_defs or INTERVENTION_DEFINITIONS
        self.cascade_defs = cascade_defs or CASCADE_DEFINITIONS
        self.default_max_budget = default_max_budget

        # Build a quick-lookup map: cascade_id -> CascadeDefinition
        self._cascade_map: dict[str, CascadeDefinition] = {
            c.cascade_id: c for c in self.cascade_defs
        }

        # Build intervention index if not using the global one
        self._intv_index: dict[str, list[InterventionDefinition]] = {}
        for intv in self.intervention_defs:
            self._intv_index.setdefault(
                intv.targets_cascade_link, []
            ).append(intv)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def recommend(
        self,
        cascade_alerts: list[CascadeAlert],
        budget_key: PersonBudgetKey,
        max_budget: float | None = None,
    ) -> InterventionPlan:
        """Generate an optimal intervention plan for the given alerts.

        Parameters
        ----------
        cascade_alerts : list[CascadeAlert]
            Active cascade alerts from the cascade detector.  Each alert
            identifies a cascade the person is in and the link they have
            reached.
        budget_key : PersonBudgetKey
            The person's budget key (used for person_uid and context).
        max_budget : float | None
            Maximum total intervention budget (USD).  If ``None``, uses
            ``self.default_max_budget``.

        Returns
        -------
        InterventionPlan
            A plan containing the selected interventions in priority order,
            with aggregate cost, expected savings, and ROI.
        """
        effective_budget = max_budget if max_budget is not None else self.default_max_budget

        # Step 1: Collect all candidate interventions across all alerts
        candidates = self._collect_candidates(cascade_alerts)

        # Step 2: Deduplicate — same intervention may appear for multiple
        # alerts; keep the one with the highest expected savings.
        candidates = self._deduplicate(candidates)

        # Step 3: Sort by ROI score descending (greedy knapsack)
        candidates.sort(key=lambda c: c.roi_score, reverse=True)

        # Step 4: Greedy selection under budget constraint
        selected: list[_ScoredIntervention] = []
        remaining_budget = effective_budget
        used_intervention_ids: set[str] = set()

        for candidate in candidates:
            if candidate.midpoint_cost <= remaining_budget:
                if candidate.intervention.intervention_id not in used_intervention_ids:
                    selected.append(candidate)
                    remaining_budget -= candidate.midpoint_cost
                    used_intervention_ids.add(candidate.intervention.intervention_id)

        # Step 5: Compute aggregate metrics
        total_cost = sum(s.midpoint_cost for s in selected)
        expected_savings = sum(s.expected_savings for s in selected)
        expected_roi = expected_savings / total_cost if total_cost > 0 else 0.0

        # Build the plan
        # Use the first alert's ID as the primary cascade alert reference
        primary_alert_id = (
            cascade_alerts[0].alert_id if cascade_alerts else "no_alert"
        )

        return InterventionPlan(
            person_uid=budget_key.person_uid,
            cascade_alert_id=primary_alert_id,
            interventions=[s.intervention for s in selected],
            total_cost=round(total_cost, 2),
            expected_savings=round(expected_savings, 2),
            expected_roi=round(expected_roi, 4),
        )

    # ------------------------------------------------------------------ #
    # Internal methods
    # ------------------------------------------------------------------ #

    def _collect_candidates(
        self,
        cascade_alerts: list[CascadeAlert],
    ) -> list[_ScoredIntervention]:
        """Collect and score all candidate interventions for the alerts."""
        candidates: list[_ScoredIntervention] = []

        for alert in cascade_alerts:
            cascade_def = self._cascade_map.get(alert.cascade_id)
            if cascade_def is None:
                continue

            links = cascade_def.links
            potential_savings = alert.path_a_projected_cost - alert.path_b_projected_cost

            # Look for interventions targeting the current link and next link
            target_indices = [alert.current_link_index]
            if alert.current_link_index + 1 < len(links):
                target_indices.append(alert.current_link_index + 1)
            # Also include current link - 1 if applicable (upstream intervention)
            if alert.current_link_index > 0:
                target_indices.append(alert.current_link_index - 1)

            seen_ids: set[str] = set()
            for idx in target_indices:
                if idx < 0 or idx >= len(links):
                    continue
                link = links[idx]
                link_label = f"{link.cause}->{link.effect}"

                interventions = self._intv_index.get(link_label, [])
                for intv in interventions:
                    if intv.intervention_id in seen_ids:
                        continue
                    seen_ids.add(intv.intervention_id)

                    midpoint_cost = (intv.cost_min + intv.cost_max) / 2.0

                    # Expected savings for this intervention =
                    # cascade potential savings * break_probability
                    # (weighted by link position — earlier breaks save more)
                    position_weight = 1.0 - (idx / max(len(links), 1)) * 0.3
                    intv_expected_savings = (
                        potential_savings
                        * intv.break_probability
                        * position_weight
                    )

                    # ROI score: savings × break_prob / cost
                    roi_score = (
                        intv_expected_savings * intv.break_probability
                        / midpoint_cost
                    ) if midpoint_cost > 0 else 0.0

                    candidates.append(
                        _ScoredIntervention(
                            intervention=intv,
                            alert=alert,
                            midpoint_cost=midpoint_cost,
                            expected_savings=intv_expected_savings,
                            break_probability=intv.break_probability,
                            roi_score=roi_score,
                            link_label=link_label,
                        )
                    )

        return candidates

    def _deduplicate(
        self,
        candidates: list[_ScoredIntervention],
    ) -> list[_ScoredIntervention]:
        """Remove duplicate interventions, keeping the highest-savings version.

        The same intervention definition may appear for multiple cascade
        alerts.  We keep the instance with the highest ``expected_savings``
        so the plan does not double-count.
        """
        best: dict[str, _ScoredIntervention] = {}
        for c in candidates:
            key = c.intervention.intervention_id
            if key not in best or c.expected_savings > best[key].expected_savings:
                best[key] = c
        return list(best.values())

    # ------------------------------------------------------------------ #
    # Utility: plan summary
    # ------------------------------------------------------------------ #

    @staticmethod
    def summarize_plan(plan: InterventionPlan) -> dict[str, Any]:
        """Return a JSON-serializable summary of an intervention plan.

        Useful for API responses and logging.
        """
        return {
            "plan_id": plan.plan_id,
            "person_uid": plan.person_uid,
            "cascade_alert_id": plan.cascade_alert_id,
            "num_interventions": len(plan.interventions),
            "interventions": [
                {
                    "intervention_id": i.intervention_id,
                    "name": i.name,
                    "midpoint_cost": round((i.cost_min + i.cost_max) / 2, 2),
                    "break_probability": i.break_probability,
                    "time_to_effect_months": i.time_to_effect_months,
                    "targets": i.targets_cascade_link,
                }
                for i in plan.interventions
            ],
            "total_cost": plan.total_cost,
            "expected_savings": plan.expected_savings,
            "expected_roi": plan.expected_roi,
        }
