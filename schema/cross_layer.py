"""
BATHS Dome — Cross-Layer Query System

The BATHS Dome: A Whole-Person Digital Twin Architecture

Cross-layer queries are the reason the dome is a digital twin and not
a dashboard. A dashboard shows Layer 4 (Health) and Layer 5 (Housing)
side by side. A digital twin answers:

  "Given this person's Layer 1 (legal entitlements) and Layer 4
   (health conditions), what is the optimal coordination in
   Layer 3 (fiscal)?"

This module implements a working cross-layer query engine.
Every query produces a typed result with evidence and recommendations.
"""

from typing import Optional, Dict, List, Any, Tuple, Set
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid


# ── Cross-Layer Relationship Types ──────────────────────────────

class RelationshipType(str, Enum):
    """How two layers relate to each other."""
    CAUSAL = "causal"              # Layer X causes changes in Layer Y
    COORDINATION = "coordination"  # Layers X and Y need coordinated action
    RESOURCE = "resource"          # Layer X provides resources Layer Y needs
    BARRIER = "barrier"            # Layer X blocks Layer Y
    AMPLIFIER = "amplifier"        # Layer X amplifies effects in Layer Y
    MEASUREMENT = "measurement"    # Layer X measures outcomes for Layer Y


class CrossLayerRelationship(BaseModel):
    """A defined relationship between two dome layers."""
    relationship_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_layer: int
    target_layer: int
    relationship_type: RelationshipType
    description: str
    strength: float = 0.5              # 0-1, how strong the relationship
    evidence: str = ""
    bidirectional: bool = False
    # Specific field mappings
    source_fields: List[str] = Field(default_factory=list)
    target_fields: List[str] = Field(default_factory=list)


# ── The Dome Relationship Graph ─────────────────────────────────
# These are the known cross-layer relationships that make the dome
# a connected system rather than 12 independent layers.

DOME_RELATIONSHIPS: List[CrossLayerRelationship] = [
    # ── Housing (5) → Health (4) ────────────────────────────────
    CrossLayerRelationship(
        source_layer=5, target_layer=4,
        relationship_type=RelationshipType.CAUSAL,
        description=(
            "Housing instability directly causes health deterioration. "
            "Lead exposure, mold, temperature extremes, stress from "
            "eviction threat all produce measurable health outcomes."
        ),
        strength=0.9,
        evidence="Desmond (2016). Evicted. WHO Housing and Health Guidelines (2018).",
        bidirectional=True,  # Health problems also cause housing instability
        source_fields=["housing_stability_score", "current_housing.environmental_hazards"],
        target_fields=["conditions", "encounters"],
    ),
    # ── Legal (1) → Fiscal (3) ──────────────────────────────────
    CrossLayerRelationship(
        source_layer=1, target_layer=3,
        relationship_type=RelationshipType.RESOURCE,
        description=(
            "Legal entitlements directly determine fiscal resources. "
            "Every unclaimed entitlement is money left on the table. "
            "The access gap between entitled and accessed is the "
            "primary fiscal opportunity."
        ),
        strength=0.95,
        evidence="National Academy for State Health Policy. Benefits Access Analysis.",
        source_fields=["entitlements", "total_entitled_value", "access_gap"],
        target_fields=["income_streams", "total_monthly_income"],
    ),
    # ── Systems (2) → all other layers ──────────────────────────
    CrossLayerRelationship(
        source_layer=2, target_layer=0,  # 0 = all layers
        relationship_type=RelationshipType.COORDINATION,
        description=(
            "System fragmentation affects every layer. The fragmentation "
            "index in Layer 2 predicts coordination difficulty across "
            "all other layers. High fragmentation = high cost, poor outcomes."
        ),
        strength=0.85,
        evidence="GAO (2019). Fragmented government programs.",
        source_fields=["fragmentation_index", "cross_system_gaps"],
        target_fields=[],  # Affects all layers
    ),
    # ── Health (4) → Economic (6) ───────────────────────────────
    CrossLayerRelationship(
        source_layer=4, target_layer=6,
        relationship_type=RelationshipType.BARRIER,
        description=(
            "Untreated health conditions create employment barriers. "
            "Chronic pain, mental health conditions, substance use "
            "disorders all reduce workforce participation and earnings."
        ),
        strength=0.8,
        evidence="OECD (2015). Mental Health and Work. CDC Workplace Health Promotion.",
        bidirectional=True,
        source_fields=["conditions", "medication_requests"],
        target_fields=["current_employment", "skills_gaps", "barriers"],
    ),
    # ── Housing (5) → Education (7) ─────────────────────────────
    CrossLayerRelationship(
        source_layer=5, target_layer=7,
        relationship_type=RelationshipType.CAUSAL,
        description=(
            "Housing instability causes educational disruption. "
            "Children change schools with each move. Adults can't "
            "pursue education without stable housing."
        ),
        strength=0.75,
        evidence="National Center for Homeless Education (2022). Educational attainment data.",
        source_fields=["housing_stability_score", "eviction_history"],
        target_fields=["children_education", "current_enrollment"],
    ),
    # ── Community (8) → Health (4) ──────────────────────────────
    CrossLayerRelationship(
        source_layer=8, target_layer=4,
        relationship_type=RelationshipType.AMPLIFIER,
        description=(
            "Social connection amplifies health outcomes. "
            "Isolation is as lethal as smoking 15 cigarettes/day. "
            "Community support accelerates recovery."
        ),
        strength=0.7,
        evidence="Holt-Lunstad (2015). Loneliness and social isolation as risk factors.",
        source_fields=["isolation_risk_score", "support_network_strength"],
        target_fields=["conditions", "care_plans"],
    ),
    # ── Fiscal (3) → Housing (5) ────────────────────────────────
    CrossLayerRelationship(
        source_layer=3, target_layer=5,
        relationship_type=RelationshipType.RESOURCE,
        description=(
            "Financial resources determine housing options. "
            "Income-to-rent ratio, voucher access, and savings "
            "directly constrain housing quality and stability."
        ),
        strength=0.9,
        evidence="Harvard Joint Center for Housing Studies (2023). State of the Nation's Housing.",
        source_fields=["total_monthly_income", "coordination_savings"],
        target_fields=["current_housing", "housing_stability_score"],
    ),
    # ── Environment (9) → Health (4) ────────────────────────────
    CrossLayerRelationship(
        source_layer=9, target_layer=4,
        relationship_type=RelationshipType.CAUSAL,
        description=(
            "Environmental conditions directly cause health conditions. "
            "Air quality, water quality, food access, lead exposure — "
            "each produces specific, measurable health impacts."
        ),
        strength=0.85,
        evidence="EPA Environmental Justice Screening. Lancet Commission on Pollution and Health (2017).",
        source_fields=["air_quality_index", "water_quality_score", "food_access_score"],
        target_fields=["conditions", "observations"],
    ),
    # ── Legal (1) → Autonomy (10) ───────────────────────────────
    CrossLayerRelationship(
        source_layer=1, target_layer=10,
        relationship_type=RelationshipType.BARRIER,
        description=(
            "Legal barriers constrain autonomy. Criminal records, "
            "immigration status, custody arrangements, benefits "
            "cliffs — legal constraints define the boundaries "
            "of what's possible."
        ),
        strength=0.8,
        evidence="Collateral Consequences Resource Center. Legal barriers database.",
        source_fields=["legal_barriers", "active_cases"],
        target_fields=["friction_points", "total_friction_score"],
    ),
    # ── Flourishing (12) ← all layers ──────────────────────────
    CrossLayerRelationship(
        source_layer=0, target_layer=12,  # 0 = all layers
        relationship_type=RelationshipType.MEASUREMENT,
        description=(
            "Flourishing is measured across all layers. "
            "Each layer's completeness contributes to the "
            "flourishing assessment. The dome is whole when "
            "all layers are coordinated."
        ),
        strength=1.0,
        evidence="VanderWeele (2017). On the promotion of human flourishing.",
        source_fields=[],  # All layers contribute
        target_fields=["flourishing_dimensions", "life_trajectory"],
    ),
    # ── Economic (6) → Community (8) ────────────────────────────
    CrossLayerRelationship(
        source_layer=6, target_layer=8,
        relationship_type=RelationshipType.AMPLIFIER,
        description=(
            "Economic stability enables community participation. "
            "People with stable income have more time, energy, and "
            "resources for social connection."
        ),
        strength=0.6,
        evidence="Putnam (2000). Bowling Alone. Economic correlates of social capital.",
        source_fields=["current_employment", "income_trajectory"],
        target_fields=["connections", "social_capital_score"],
    ),
    # ── Education (7) → Economic (6) ────────────────────────────
    CrossLayerRelationship(
        source_layer=7, target_layer=6,
        relationship_type=RelationshipType.RESOURCE,
        description=(
            "Education and credentials directly affect employment "
            "options and earnings potential."
        ),
        strength=0.8,
        evidence="BLS (2023). Education pays. Earnings and unemployment by educational attainment.",
        source_fields=["highest_level", "certifications"],
        target_fields=["current_employment", "market_demand_match", "income_trajectory"],
    ),
]


# ── Cross-Layer Query Engine ────────────────────────────────────

class CrossLayerQueryResult(BaseModel):
    """Result of a cross-layer query."""
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query_description: str
    source_layers: List[int]
    target_layers: List[int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Findings
    relationships_found: List[CrossLayerRelationship] = Field(default_factory=list)
    data_points: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    coordination_opportunities: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_impact: Dict[str, float] = Field(default_factory=dict)
    confidence: float = 0.0


class CrossLayerQueryEngine:
    """
    Query engine for cross-layer analysis.

    This is the working engine that answers questions across dome layers.
    It uses the relationship graph to trace connections and produce
    actionable insights.
    """

    def __init__(self, relationships: Optional[List[CrossLayerRelationship]] = None):
        self.relationships = relationships or DOME_RELATIONSHIPS
        self._adjacency = self._build_adjacency()

    def _build_adjacency(self) -> Dict[int, List[CrossLayerRelationship]]:
        """Build adjacency list for traversal."""
        adj: Dict[int, List[CrossLayerRelationship]] = {}
        for rel in self.relationships:
            source = rel.source_layer
            target = rel.target_layer
            if source not in adj:
                adj[source] = []
            adj[source].append(rel)
            if rel.bidirectional:
                if target not in adj:
                    adj[target] = []
                # Create reverse relationship
                reverse = CrossLayerRelationship(
                    source_layer=target,
                    target_layer=source,
                    relationship_type=rel.relationship_type,
                    description=f"(Reverse) {rel.description}",
                    strength=rel.strength * 0.8,
                    evidence=rel.evidence,
                    source_fields=rel.target_fields,
                    target_fields=rel.source_fields,
                )
                adj[target].append(reverse)
        return adj

    def query(
        self,
        source_layers: List[int],
        target_layers: List[int],
        dome_data: Dict[int, Dict[str, Any]],
    ) -> CrossLayerQueryResult:
        """
        Execute a cross-layer query.

        Args:
            source_layers: Layers to query FROM (conditions, constraints)
            target_layers: Layers to query INTO (what to optimize)
            dome_data: Dict mapping layer number → layer data dict

        Example:
            query(
                source_layers=[1, 4],    # Legal + Health
                target_layers=[3],       # Fiscal
                dome_data={1: {...}, 3: {...}, 4: {...}},
            )
        """
        result = CrossLayerQueryResult(
            query_description=(
                f"Cross-layer analysis: Layers {source_layers} → Layers {target_layers}"
            ),
            source_layers=source_layers,
            target_layers=target_layers,
        )

        # Find all relevant relationships
        for rel in self.relationships:
            # Direct relationships
            if (rel.source_layer in source_layers and
                    rel.target_layer in target_layers):
                result.relationships_found.append(rel)
            # Wildcard relationships (source_layer=0 means "all")
            elif (rel.source_layer == 0 and
                  any(t in target_layers for t in [rel.target_layer])):
                result.relationships_found.append(rel)
            elif (rel.target_layer == 0 and
                  rel.source_layer in source_layers):
                result.relationships_found.append(rel)

        # Extract relevant data points from dome data
        for layer_num, layer_data in dome_data.items():
            if layer_num in source_layers:
                for rel in result.relationships_found:
                    for field in rel.source_fields:
                        value = _extract_field(layer_data, field)
                        if value is not None:
                            result.data_points.append({
                                "layer": layer_num,
                                "field": field,
                                "value": value,
                                "relationship": rel.description[:100],
                            })

        # Generate recommendations based on findings
        result.recommendations = self._generate_recommendations(
            result.relationships_found,
            dome_data,
            source_layers,
            target_layers,
        )

        # Identify coordination opportunities
        result.coordination_opportunities = self._find_coordination_opportunities(
            result.relationships_found,
            dome_data,
        )

        # Estimate impact
        result.estimated_impact = self._estimate_impact(
            result.relationships_found,
            dome_data,
        )

        # Confidence based on data completeness and relationship strength
        if result.relationships_found:
            avg_strength = sum(
                r.strength for r in result.relationships_found
            ) / len(result.relationships_found)
            data_completeness = len(result.data_points) / max(
                sum(len(r.source_fields) for r in result.relationships_found), 1
            )
            result.confidence = round(
                min(avg_strength * data_completeness, 1.0), 2
            )

        return result

    def find_path(
        self,
        from_layer: int,
        to_layer: int,
        max_hops: int = 3,
    ) -> List[List[CrossLayerRelationship]]:
        """
        Find all paths between two layers through the relationship graph.
        Used to discover indirect connections.
        """
        paths = []
        self._dfs(from_layer, to_layer, [], set(), paths, max_hops)
        return paths

    def _dfs(
        self,
        current: int,
        target: int,
        path: List[CrossLayerRelationship],
        visited: Set[int],
        all_paths: List[List[CrossLayerRelationship]],
        max_hops: int,
    ) -> None:
        """Depth-first search for paths."""
        if len(path) > max_hops:
            return
        if current == target and path:
            all_paths.append(list(path))
            return

        visited.add(current)
        for rel in self._adjacency.get(current, []):
            next_layer = rel.target_layer
            if next_layer not in visited and next_layer != 0:
                path.append(rel)
                self._dfs(next_layer, target, path, visited, all_paths, max_hops)
                path.pop()
        visited.discard(current)

    def get_all_connections(self, layer: int) -> List[CrossLayerRelationship]:
        """Get all relationships involving a specific layer."""
        connections = []
        for rel in self.relationships:
            if rel.source_layer == layer or rel.target_layer == layer:
                connections.append(rel)
            elif rel.source_layer == 0 or rel.target_layer == 0:
                connections.append(rel)
        return connections

    def _generate_recommendations(
        self,
        relationships: List[CrossLayerRelationship],
        dome_data: Dict[int, Dict[str, Any]],
        source_layers: List[int],
        target_layers: List[int],
    ) -> List[str]:
        """Generate actionable recommendations from cross-layer analysis."""
        recs = []

        for rel in relationships:
            if rel.relationship_type == RelationshipType.BARRIER:
                recs.append(
                    f"BARRIER: Layer {rel.source_layer} → Layer {rel.target_layer}. "
                    f"{rel.description[:150]} "
                    f"Action: Address Layer {rel.source_layer} barriers to unlock "
                    f"Layer {rel.target_layer} progress."
                )
            elif rel.relationship_type == RelationshipType.RESOURCE:
                recs.append(
                    f"RESOURCE OPPORTUNITY: Layer {rel.source_layer} → "
                    f"Layer {rel.target_layer}. {rel.description[:150]} "
                    f"Action: Maximize Layer {rel.source_layer} resources to "
                    f"strengthen Layer {rel.target_layer}."
                )
            elif rel.relationship_type == RelationshipType.CAUSAL:
                recs.append(
                    f"CAUSAL LINK: Layer {rel.source_layer} → "
                    f"Layer {rel.target_layer}. {rel.description[:150]} "
                    f"Action: Stabilize Layer {rel.source_layer} to prevent "
                    f"Layer {rel.target_layer} deterioration."
                )
            elif rel.relationship_type == RelationshipType.COORDINATION:
                recs.append(
                    f"COORDINATION REQUIRED: Layers {rel.source_layer} ↔ "
                    f"{rel.target_layer}. {rel.description[:150]} "
                    f"Action: Establish data sharing and synchronized "
                    f"action between these layers."
                )

        return recs

    def _find_coordination_opportunities(
        self,
        relationships: List[CrossLayerRelationship],
        dome_data: Dict[int, Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Find specific coordination opportunities."""
        opportunities = []

        for rel in relationships:
            if rel.strength >= 0.7:
                opportunities.append({
                    "layers": [rel.source_layer, rel.target_layer],
                    "type": rel.relationship_type.value,
                    "strength": rel.strength,
                    "description": rel.description[:200],
                    "priority": "high" if rel.strength >= 0.85 else "medium",
                })

        opportunities.sort(key=lambda x: x["strength"], reverse=True)
        return opportunities

    def _estimate_impact(
        self,
        relationships: List[CrossLayerRelationship],
        dome_data: Dict[int, Dict[str, Any]],
    ) -> Dict[str, float]:
        """Estimate the impact of cross-layer coordination."""
        # Impact score per target layer
        impact = {}
        for rel in relationships:
            target = rel.target_layer
            key = f"layer_{target}"
            current = impact.get(key, 0)
            impact[key] = max(current, rel.strength)

        return impact


def _extract_field(data: Dict[str, Any], field_path: str) -> Any:
    """Extract a nested field from a dict using dot notation."""
    parts = field_path.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        elif hasattr(current, part):
            current = getattr(current, part, None)
        else:
            return None
        if current is None:
            return None
    return current
