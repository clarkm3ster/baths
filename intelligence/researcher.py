"""
BATHS Intelligence — Frontier AI Researcher Agent

The ongoing researcher. This agent:
1. Scans the frontier map for capabilities approaching maturity transitions
2. Identifies when new research should be added to the tracker
3. Recommends which capabilities to integrate next based on BATHS priorities
4. Produces research briefs for principals and practitioners
5. Flags convergence zone activity — when multiple threads are approaching
   a BATHS-relevant breakthrough simultaneously

The researcher doesn't just track — it PRIORITIZES. Given limited engineering
resources, which capabilities should BATHS integrate first for maximum impact
on human-centered (domes) and place-centered (spheres) outcomes?
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime

from intelligence.models import (
    FrontierCapability, ResearchMaturity, IntelligenceMetrics,
)
from intelligence.frontier import FrontierTracker
from intelligence.memory import ProjectMemoryStore


class FrontierResearcher:
    """
    The ongoing frontier AI researcher agent.

    This agent operates as an intelligence analyst for BATHS.
    It synthesizes three inputs:
    1. The frontier map (what's being built in AI research)
    2. The memory system (what BATHS has learned from its own projects)
    3. BATHS priorities (what capabilities would have the most impact)

    And produces actionable recommendations.
    """

    def __init__(
        self,
        frontier: FrontierTracker,
        memory: ProjectMemoryStore,
    ):
        self.frontier = frontier
        self.memory = memory

    # ── Priority Assessment ─────────────────────────────────────

    def assess_integration_priorities(self) -> List[Dict]:
        """
        Rank frontier capabilities by integration priority.

        Priority is determined by:
        1. Maturity (closer to production = higher priority)
        2. Impact breadth (how many layers/capabilities it affects)
        3. Gap severity (how much the current system needs it)
        4. Dependencies satisfied (can we actually build it?)
        """
        priorities = []

        for cap in self.frontier.frontier.capabilities:
            score = self._compute_priority_score(cap)
            priorities.append({
                "capability": cap.name,
                "category": cap.category,
                "maturity": cap.maturity.value,
                "priority_score": round(score, 1),
                "impact_summary": self._summarize_impact(cap),
                "integration_path": cap.integration_path,
                "blockers": cap.dependencies,
                "estimated_timeline": cap.estimated_timeline,
            })

        priorities.sort(key=lambda x: x["priority_score"], reverse=True)
        return priorities

    def _compute_priority_score(self, cap: FrontierCapability) -> float:
        """Score a capability's integration priority."""
        score = 0.0

        # Maturity scoring (production-ready = highest)
        maturity_scores = {
            ResearchMaturity.PRODUCTION: 40,
            ResearchMaturity.PILOT: 30,
            ResearchMaturity.LAB: 15,
            ResearchMaturity.THEORETICAL: 5,
            ResearchMaturity.FRONTIER: 2,
        }
        score += maturity_scores.get(cap.maturity, 0)

        # Impact breadth (how many layers it affects)
        total_layers = len(cap.applicable_layers_dome) + len(cap.applicable_layers_sphere)
        score += min(total_layers * 2, 20)

        # Capability coverage (how many production capabilities it serves)
        score += min(len(cap.applicable_capabilities) * 3, 15)

        # Gap severity — how badly does the current system need this?
        # Based on what the memory system reveals about production weaknesses
        gap_score = self._assess_gap_severity(cap)
        score += gap_score

        # Dependency penalty — how many prerequisites are unmet?
        dep_penalty = len(cap.dependencies) * 2
        score -= min(dep_penalty, 15)

        return max(0, score)

    def _assess_gap_severity(self, cap: FrontierCapability) -> float:
        """
        Assess how severely the current system needs this capability.
        Based on learnings from the memory system.
        """
        severity = 0.0

        # Check if the memory system has learnings about failures
        # in the areas this capability would address
        for learning_cap in cap.applicable_capabilities:
            failure_learnings = self.memory.query_relevant_learnings(
                game_type="domes",
                keywords=[learning_cap, "failure", "limitation", "gap"],
                limit=5,
                min_reliability=0.2,
            )
            severity += len(failure_learnings) * 3.0

        # Check if this capability addresses a production bottleneck
        bottleneck_keywords = {
            "legal_navigation": ["manual", "hours", "paperwork", "navigation"],
            "data_systems": ["fragmentation", "duplicate", "incompatible"],
            "activation_design": ["measurement", "validation", "impact"],
            "economics": ["projection", "estimate", "model accuracy"],
        }
        for prod_cap in cap.applicable_capabilities:
            if prod_cap in bottleneck_keywords:
                bottleneck_learnings = self.memory.query_relevant_learnings(
                    game_type="domes",
                    keywords=bottleneck_keywords[prod_cap],
                    limit=5,
                    min_reliability=0.2,
                )
                severity += len(bottleneck_learnings) * 2.0

        return min(severity, 25)

    def _summarize_impact(self, cap: FrontierCapability) -> str:
        """Produce a one-sentence impact summary for a capability."""
        dome_layers = len(cap.applicable_layers_dome)
        sphere_layers = len(cap.applicable_layers_sphere)
        caps = len(cap.applicable_capabilities)

        parts = []
        if dome_layers > 0:
            parts.append(f"{dome_layers} dome layers")
        if sphere_layers > 0:
            parts.append(f"{sphere_layers} sphere layers")
        if caps > 0:
            parts.append(f"{caps} production capabilities")

        return f"Affects {', '.join(parts)}. {cap.maturity.value.title()} maturity."

    # ── Research Briefs ─────────────────────────────────────────

    def produce_research_brief(
        self,
        focus: Optional[str] = None,
    ) -> Dict:
        """
        Produce a comprehensive research brief.

        Args:
            focus: Optional category to focus on (e.g., "robotics", "agent_networks")
        """
        priorities = self.assess_integration_priorities()
        metrics = self.memory.compute_metrics()

        # Top 5 priorities
        top_priorities = priorities[:5]

        # Immediate opportunities (production-ready)
        immediate = [
            p for p in priorities
            if p["maturity"] in ("production", "pilot")
        ]

        # Convergence alerts
        convergences = self.frontier.get_convergence_zones()

        # Category focus
        if focus:
            category_caps = self.frontier.get_by_category(focus)
            category_brief = [
                {
                    "name": c.name,
                    "maturity": c.maturity.value,
                    "description": c.description,
                    "integration_path": c.integration_path,
                }
                for c in category_caps
            ]
        else:
            category_brief = None

        brief = {
            "generated_at": datetime.utcnow().isoformat(),
            "system_intelligence": {
                "projects_completed": metrics.total_projects_completed,
                "learnings_accumulated": metrics.total_learnings_stored,
                "cross_project_transfers": metrics.total_cross_project_transfers,
                "avg_learning_reliability": metrics.avg_learning_reliability,
            },
            "frontier_summary": self.frontier.intelligence_brief(),
            "top_integration_priorities": top_priorities,
            "immediate_opportunities": immediate[:5],
            "convergence_zones": convergences,
            "paradigm_shifts": self.frontier.frontier.paradigm_shifts,
        }

        if category_brief:
            brief["category_focus"] = {
                "category": focus,
                "capabilities": category_brief,
            }

        # Recommendations
        brief["recommendations"] = self._generate_recommendations(
            priorities, metrics, convergences,
        )

        return brief

    def _generate_recommendations(
        self,
        priorities: List[Dict],
        metrics: IntelligenceMetrics,
        convergences: List[Dict],
    ) -> List[str]:
        """Generate actionable recommendations based on current state."""
        recs = []

        # Recommendation 1: What to integrate now
        production_ready = [p for p in priorities if p["maturity"] == "production"]
        if production_ready:
            top = production_ready[0]
            recs.append(
                f"INTEGRATE NOW: {top['capability']} is production-ready and "
                f"affects {top['impact_summary']}. Path: {top['integration_path'][:150]}"
            )

        # Recommendation 2: What to pilot
        pilot_ready = [p for p in priorities if p["maturity"] == "pilot"]
        if pilot_ready:
            top = pilot_ready[0]
            recs.append(
                f"PILOT NEXT: {top['capability']} is in pilot stage. "
                f"{top['impact_summary']} Begin with supervised deployment."
            )

        # Recommendation 3: Data accumulation priority
        if metrics.total_projects_completed < 10:
            recs.append(
                f"DATA PRIORITY: Only {metrics.total_projects_completed} projects completed. "
                f"Run more games to build the learning corpus. Many frontier capabilities "
                f"(flourishing prediction, swarm team assembly) need accumulated data."
            )
        elif metrics.corroboration_rate < 0.3:
            recs.append(
                f"RELIABILITY: Corroboration rate is {metrics.corroboration_rate:.0%}. "
                f"Run more projects with overlapping characteristics to build "
                f"learning reliability through cross-project validation."
            )

        # Recommendation 4: Convergence zone alert
        if convergences:
            nearest = min(
                convergences,
                key=lambda c: c.get("estimated_convergence", "9999"),
            )
            recs.append(
                f"CONVERGENCE ALERT: '{nearest['name']}' — "
                f"{nearest['description'][:150]}. "
                f"Estimated convergence: {nearest.get('estimated_convergence', 'unknown')}."
            )

        # Recommendation 5: Gap analysis
        if metrics.total_learnings_stored > 0 and metrics.insight_reuse_rate < 0.2:
            recs.append(
                f"INTELLIGENCE UNDERUSE: {metrics.total_learnings_stored} learnings stored "
                f"but only {metrics.insight_reuse_rate:.0%} reuse rate. Ensure the production "
                f"engine is querying the memory system for each new project."
            )

        return recs

    # ── Capability Gap Analysis ─────────────────────────────────

    def analyze_capability_gaps(
        self,
        game_type: str,
    ) -> Dict:
        """
        Analyze what capability gaps exist for a specific game type
        and what frontier research could fill them.
        """
        if game_type == "domes":
            production_caps = [
                "legal_navigation", "data_systems",
                "narrative", "flourishing_design",
            ]
        else:
            production_caps = [
                "spatial_legal", "activation_design",
                "economics", "narrative",
            ]

        gaps = {}
        for cap in production_caps:
            frontier_options = self.frontier.get_capabilities_for_production(cap)
            gaps[cap] = {
                "current_status": "template_simulation",
                "frontier_options": [
                    {
                        "name": f.name,
                        "maturity": f.maturity.value,
                        "category": f.category,
                        "integration_path": f.integration_path[:200],
                    }
                    for f in frontier_options
                ],
                "nearest_to_production": (
                    min(
                        frontier_options,
                        key=lambda f: list(ResearchMaturity).index(f.maturity),
                    ).name
                    if frontier_options else None
                ),
            }

        return {
            "game_type": game_type,
            "production_capabilities": production_caps,
            "gap_analysis": gaps,
        }

    # ── Evolution Tracking ──────────────────────────────────────

    def track_maturity_changes(self) -> List[Dict]:
        """
        Report on capabilities whose maturity has changed recently.
        """
        changes = []
        for cap in self.frontier.frontier.capabilities:
            if cap.maturity_history:
                latest = cap.maturity_history[-1]
                changes.append({
                    "capability": cap.name,
                    "from": latest["from"],
                    "to": latest["to"],
                    "date": latest["date"],
                    "note": latest.get("note", ""),
                })
        return changes
