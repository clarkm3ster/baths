"""
BATHS Intelligence — World Models

Two world models that accumulate understanding over time:

1. PersonWorldModel (domes) — understands human situations.
   Not "a model of a person" but a model of what it means to be a person
   navigating these systems, in these circumstances, toward these dimensions
   of flourishing. Gets smarter with every dome project.

2. PlaceWorldModel (spheres) — understands physical sites.
   Not "a model of a parcel" but a model of what makes spaces come alive,
   what regulatory pathways work, what triggers produce awe, and how
   activation catalyzes adjacent change. Gets smarter with every sphere.

These are WORKING MODELS that produce actionable outputs.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime

from intelligence.models import (
    PersonKnowledge, PlaceKnowledge, WorldModelDomain,
    LearningType, Learning,
)
from intelligence.memory import ProjectMemoryStore


class PersonWorldModel:
    """
    The system's accumulated understanding of human situations.

    As domes are simulated, this model learns:
    - Which systems interact in which ways
    - What coordination patterns reduce fragmentation
    - What flourishing actually looks like for people in specific circumstances
    - What produces awe in dome contexts
    - What the real costs of fragmentation are

    Used to make each new dome project smarter than the last.
    """

    def __init__(self, memory_store: ProjectMemoryStore):
        self._store = memory_store

    def assess_situation(
        self,
        key_systems: List[str],
        flourishing_dimensions: List[str],
        situation_description: str,
    ) -> Dict:
        """
        Given a new person's situation, produce an intelligence briefing
        based on everything the system has learned from prior domes.

        This is the primary interface: a new dome project calls this
        to get the accumulated wisdom of all prior dome projects.
        """
        # Query for relevant person knowledge
        person_knowledge = self._store.query_person_knowledge(
            system_tags=key_systems,
            dimension_tags=flourishing_dimensions,
        )

        # Query for relevant learnings
        keywords = []
        for sys in key_systems:
            keywords.extend(sys.lower().split())
        keywords.extend(d.lower() for d in flourishing_dimensions)
        # Add significant words from situation
        for word in situation_description.lower().split():
            if len(word) > 4:
                keywords.append(word)

        relevant_learnings = self._store.query_relevant_learnings(
            game_type="domes",
            keywords=keywords,
            domains=[WorldModelDomain.LEGAL, WorldModelDomain.COMMUNITY],
            limit=15,
        )

        # Build the intelligence briefing
        briefing = {
            "prior_dome_count": len(self._store.memories),
            "relevant_knowledge_entries": len(person_knowledge),
            "relevant_learnings": len(relevant_learnings),
            "system_interaction_warnings": [],
            "coordination_recommendations": [],
            "cost_intelligence": {},
            "flourishing_insights": [],
            "awe_design_guidance": [],
            "prior_project_references": [],
        }

        # Extract system interaction warnings
        for pk in person_knowledge:
            for pattern_key, pattern_desc in pk.system_interaction_patterns.items():
                systems_in_pattern = pattern_key.split(" + ")
                # Check if any of these systems are in the new project
                if any(sys.lower() in [s.lower() for s in key_systems]
                       for sys in systems_in_pattern):
                    briefing["system_interaction_warnings"].append({
                        "systems": systems_in_pattern,
                        "warning": pattern_desc,
                        "observation_count": pk.observation_count,
                    })

            # Coordination insights from prior projects
            for insight in pk.coordination_insights[-5:]:
                briefing["coordination_recommendations"].append(insight)

            # Awe design guidance
            for awe_insight in pk.awe_design_insights[-3:]:
                briefing["awe_design_guidance"].append(awe_insight)

        # Extract specific learning types
        for learning in relevant_learnings:
            ref = {
                "source_project": learning.source_project_title,
                "insight_type": learning.learning_type.value,
                "insight": learning.insight,
                "reliability": round(learning.reliability, 2),
                "times_corroborated": learning.times_corroborated,
            }
            briefing["prior_project_references"].append(ref)

            if learning.learning_type == LearningType.COST_INSIGHT:
                briefing["cost_intelligence"][learning.source_capability] = {
                    "insight": learning.insight,
                    "confidence": learning.confidence,
                }
            elif learning.learning_type == LearningType.METHOD:
                briefing["coordination_recommendations"].append(learning.insight)
            elif learning.learning_type == LearningType.FAILURE:
                briefing["system_interaction_warnings"].append({
                    "systems": learning.keywords[:3],
                    "warning": learning.insight,
                    "observation_count": learning.times_corroborated + 1,
                })

        # Flourishing pathway intelligence
        for pk in person_knowledge:
            for pathway in pk.flourishing_pathways[-3:]:
                briefing["flourishing_insights"].append(pathway)

        return briefing

    def predict_fragmentation_cost(
        self,
        key_systems: List[str],
    ) -> Dict:
        """
        Based on prior dome projects, estimate the fragmentation cost
        for a person navigating these specific systems.
        """
        # Find cost learnings related to these systems
        keywords = []
        for sys in key_systems:
            keywords.extend(sys.lower().split())
        keywords.extend(["cost", "fragmentation", "savings", "coordination"])

        cost_learnings = self._store.query_relevant_learnings(
            game_type="domes",
            keywords=keywords,
            domains=[WorldModelDomain.FISCAL],
            limit=10,
            min_reliability=0.4,
        )

        return {
            "system_count": len(key_systems),
            "prior_cost_observations": len(cost_learnings),
            "cost_insights": [
                {
                    "source": l.source_project_title,
                    "insight": l.insight,
                    "confidence": l.confidence,
                    "reliability": round(l.reliability, 2),
                }
                for l in cost_learnings
            ],
            "estimated_coordination_savings_confidence": (
                sum(l.confidence for l in cost_learnings) / max(len(cost_learnings), 1)
            ),
        }

    def get_system_interaction_map(self) -> Dict[str, List[str]]:
        """
        Return the accumulated map of how government systems interact.
        Built from all dome projects' findings.
        """
        interaction_map = {}
        for pk in self._store.person_knowledge.values():
            for pattern_key, pattern_desc in pk.system_interaction_patterns.items():
                if pattern_key not in interaction_map:
                    interaction_map[pattern_key] = []
                interaction_map[pattern_key].append(pattern_desc)
        return interaction_map


class PlaceWorldModel:
    """
    The system's accumulated understanding of physical places.

    As spheres are simulated, this model learns:
    - Which regulatory pathways work for which zoning types
    - What activation patterns produce the strongest community response
    - Which awe triggers work best for different site types
    - What the real economics of space activation look like
    - How activation catalyzes adjacent change

    Used to make each new sphere project smarter than the last.
    """

    def __init__(self, memory_store: ProjectMemoryStore):
        self._store = memory_store

    def assess_site(
        self,
        address: str,
        neighborhood: str,
        zoning: str,
        lot_size_sqft: float,
        constraints: List[str],
        community_context: str,
    ) -> Dict:
        """
        Given a new parcel, produce an intelligence briefing based on
        everything the system has learned from prior spheres.
        """
        # Query for similar places
        place_knowledge = self._store.query_place_knowledge(
            zoning_tags=[zoning] if zoning else None,
            neighborhood_tags=[neighborhood] if neighborhood else None,
            site_tags=["vacant lot"],
            lot_size_sqft=lot_size_sqft,
        )

        # Build keyword set for learning retrieval
        keywords = [zoning.lower()] if zoning else []
        keywords.append(neighborhood.lower())
        for c in constraints:
            keywords.extend(c.lower().split())
        for word in community_context.lower().split():
            if len(word) > 4:
                keywords.append(word)
        keywords.extend(["activation", "sphere", "parcel"])

        relevant_learnings = self._store.query_relevant_learnings(
            game_type="spheres",
            keywords=keywords,
            domains=[WorldModelDomain.ZONING, WorldModelDomain.ECONOMICS,
                     WorldModelDomain.AWE],
            limit=15,
        )

        briefing = {
            "prior_sphere_count": sum(
                1 for m in self._store.memories.values()
                if m.game_type == "spheres"
            ),
            "similar_sites_studied": len(place_knowledge),
            "relevant_learnings": len(relevant_learnings),
            "regulatory_intelligence": [],
            "activation_recommendations": [],
            "awe_trigger_guidance": {},
            "economics_intelligence": {},
            "catalyst_predictions": [],
            "prior_project_references": [],
        }

        # Extract regulatory intelligence from similar places
        for plk in place_knowledge:
            for cap, pattern in plk.regulatory_patterns.items():
                briefing["regulatory_intelligence"].append({
                    "capability": cap,
                    "pattern": pattern,
                    "observation_count": plk.observation_count,
                })

            # Awe trigger effectiveness from similar sites
            for trigger, score in plk.awe_trigger_effectiveness.items():
                if trigger not in briefing["awe_trigger_guidance"]:
                    briefing["awe_trigger_guidance"][trigger] = {
                        "scores": [],
                        "avg_effectiveness": 0.0,
                    }
                briefing["awe_trigger_guidance"][trigger]["scores"].append(score)

            # Activation patterns that worked
            for pattern in plk.activation_patterns[-5:]:
                briefing["activation_recommendations"].append(pattern)

            # Community impact patterns
            for impact in plk.community_impact_patterns[-3:]:
                briefing["catalyst_predictions"].append(impact)

        # Compute average awe trigger effectiveness
        for trigger, data in briefing["awe_trigger_guidance"].items():
            if data["scores"]:
                data["avg_effectiveness"] = round(
                    sum(data["scores"]) / len(data["scores"]), 2
                )

        # Extract specific learnings
        for learning in relevant_learnings:
            ref = {
                "source_project": learning.source_project_title,
                "insight_type": learning.learning_type.value,
                "insight": learning.insight,
                "reliability": round(learning.reliability, 2),
            }
            briefing["prior_project_references"].append(ref)

            if learning.learning_type == LearningType.COST_INSIGHT:
                briefing["economics_intelligence"][learning.source_capability] = {
                    "insight": learning.insight,
                    "confidence": learning.confidence,
                }
            elif learning.learning_type == LearningType.POLICY_INSIGHT:
                briefing["regulatory_intelligence"].append({
                    "capability": learning.source_capability,
                    "pattern": learning.insight,
                    "observation_count": learning.times_corroborated + 1,
                })

        return briefing

    def predict_activation_economics(
        self,
        lot_size_sqft: float,
        zoning: str,
        neighborhood: str,
    ) -> Dict:
        """
        Predict activation economics based on prior sphere data.
        """
        keywords = ["activation", "cost", "investment", "returns",
                     "economic", "multiplier", zoning.lower(), neighborhood.lower()]

        econ_learnings = self._store.query_relevant_learnings(
            game_type="spheres",
            keywords=keywords,
            domains=[WorldModelDomain.ECONOMICS],
            limit=10,
            min_reliability=0.4,
        )

        return {
            "lot_size_sqft": lot_size_sqft,
            "prior_economic_observations": len(econ_learnings),
            "economic_insights": [
                {
                    "source": l.source_project_title,
                    "insight": l.insight,
                    "confidence": l.confidence,
                    "reliability": round(l.reliability, 2),
                }
                for l in econ_learnings
            ],
        }

    def recommend_awe_triggers(
        self,
        lot_size_sqft: float,
        neighborhood: str,
        community_context: str,
    ) -> Dict:
        """
        Based on prior spheres, recommend which awe triggers
        are most likely to work for this type of site.
        """
        awe_learnings = self._store.query_relevant_learnings(
            game_type="spheres",
            keywords=["awe", "vastness", "accommodation", "effervescence",
                       "moral beauty", "nature", "epiphany",
                       neighborhood.lower()],
            domains=[WorldModelDomain.AWE],
            limit=15,
        )

        # Aggregate awe trigger recommendations
        trigger_scores: Dict[str, List[float]] = {}
        for learning in awe_learnings:
            for kw in learning.keywords:
                if kw in ["vastness", "accommodation", "effervescence",
                          "moral-beauty", "nature", "epiphany",
                          "music", "visual-art"]:
                    if kw not in trigger_scores:
                        trigger_scores[kw] = []
                    trigger_scores[kw].append(learning.confidence)

        recommendations = {}
        for trigger, scores in trigger_scores.items():
            avg = sum(scores) / len(scores)
            recommendations[trigger] = {
                "avg_confidence": round(avg, 2),
                "observation_count": len(scores),
                "recommendation": (
                    "strongly recommended" if avg > 0.7 and len(scores) >= 3
                    else "recommended" if avg > 0.5
                    else "worth testing"
                ),
            }

        return {
            "total_awe_observations": len(awe_learnings),
            "trigger_recommendations": recommendations,
            "awe_insights": [
                l.insight for l in awe_learnings
                if l.learning_type == LearningType.AWE_INSIGHT
            ][:5],
        }

    def get_activation_pattern_library(self) -> Dict[str, List[str]]:
        """
        Return all accumulated activation patterns, organized by site type.
        """
        patterns = {}
        for plk in self._store.place_knowledge.values():
            key = "|".join(sorted(plk.zoning_tags[:3]))
            if not key:
                key = "general"
            if key not in patterns:
                patterns[key] = []
            patterns[key].extend(plk.activation_patterns)
        return patterns
