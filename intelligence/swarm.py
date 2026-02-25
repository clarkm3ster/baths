"""
BATHS Intelligence — Swarm Intelligence System

Every completed dome makes every future dome smarter.
Every completed sphere makes every future sphere smarter.

This is the technical moat. Anyone can build a dashboard.
Nobody else has a collective intelligence system where every human
life documented makes the next documentation richer, faster, and
more effective. The swarm is what makes this a company, not a project.

Architecture:
1. PATTERN EXTRACTION — automatic pattern mining from completed productions
2. KNOWLEDGE BASE — structured, queryable, versioned pattern store
3. ACTIVE RECOMMENDATIONS — context-aware suggestions for new productions
4. REINFORCEMENT LOOP — recommendations that work get stronger, failures get weaker
5. CROSS-DOME/SPHERE ANALYTICS — systemic insights across the portfolio

This is REAL CODE that EXECUTES. Run simulations. Extract patterns.
Query the knowledge base. Verify recommendations improve scores.
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid
import hashlib


# ── Pattern Types ───────────────────────────────────────────────

class PatternType(str, Enum):
    """Types of patterns the swarm extracts."""
    LEGAL = "legal"
    SYSTEMS = "systems"
    FISCAL = "fiscal"
    HEALTH = "health"
    HOUSING = "housing"
    COORDINATION = "coordination"
    CREATIVE = "creative"
    INNOVATION = "innovation"
    AWE = "awe"
    COST = "cost"
    TEAM = "team"
    POLICY = "policy"
    REGULATORY = "regulatory"
    ACTIVATION = "activation"
    ECONOMICS = "economics"


class CircumstanceType(str, Enum):
    """Types of person circumstances for dome indexing."""
    FOSTER_CARE = "foster_care"
    CHRONIC_HOMELESSNESS = "chronic_homelessness"
    DISABILITY = "disability"
    JUSTICE_INVOLVED = "justice_involved"
    SINGLE_PARENT = "single_parent"
    VETERAN = "veteran"
    AGING = "aging"
    SUBSTANCE_USE = "substance_use"
    IMMIGRANT_REFUGEE = "immigrant_refugee"
    DOMESTIC_VIOLENCE = "domestic_violence"
    YOUTH_AGING_OUT = "youth_aging_out"
    MENTAL_HEALTH = "mental_health"


class SiteType(str, Enum):
    """Types of site characteristics for sphere indexing."""
    VACANT_LOT = "vacant_lot"
    ABANDONED_COMMERCIAL = "abandoned_commercial"
    UNDERUSED_PUBLIC = "underused_public"
    BROWNFIELD = "brownfield"
    CORNER_LOT = "corner_lot"
    LINEAR_CORRIDOR = "linear_corridor"
    WATERFRONT = "waterfront"
    INDUSTRIAL = "industrial"


# ── Pattern ─────────────────────────────────────────────────────

class SwarmPattern(BaseModel):
    """
    A pattern extracted from completed productions.
    This is the atom of swarm intelligence.
    """
    pattern_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pattern_type: PatternType
    game_type: str                     # "domes" or "spheres"

    # Content
    description: str                   # The pattern itself
    evidence: str                      # What data supports it
    mechanism: str = ""                # Why this pattern exists

    # Indexing
    circumstance_types: List[str] = Field(default_factory=list)
    site_types: List[str] = Field(default_factory=list)
    layers: List[int] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    geography: Optional[str] = None

    # Confidence (updated by reinforcement loop)
    source_dome_ids: List[str] = Field(default_factory=list)
    confidence: float = 0.5            # 0-1, increases with confirmation
    impact_score: float = 0.0          # How much it moves Cosm/Chron
    times_recommended: int = 0
    times_adopted: int = 0
    times_rejected: int = 0
    avg_score_when_adopted: float = 0.0
    avg_score_when_rejected: float = 0.0

    # Versioning
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    @property
    def adoption_rate(self) -> float:
        """What percentage of recommendations were adopted."""
        total = self.times_adopted + self.times_rejected
        if total == 0:
            return 0.0
        return self.times_adopted / total

    @property
    def effectiveness(self) -> float:
        """
        How effective this pattern is. Combines confidence with
        observed score improvements when adopted vs rejected.
        """
        if self.times_adopted == 0:
            return self.confidence
        score_delta = self.avg_score_when_adopted - self.avg_score_when_rejected
        normalized_delta = max(-1, min(1, score_delta / 30.0))  # Normalize to -1..1
        return min(1.0, max(0, self.confidence + normalized_delta * 0.3))


# ── Knowledge Base ──────────────────────────────────────────────

class SwarmKnowledgeBase:
    """
    The structured, queryable, versioned pattern store.

    Every pattern is indexed by: circumstance type, layer, geography,
    score impact, team composition.

    Patterns are versioned — as new domes confirm or contradict,
    confidence scores update.
    """

    def __init__(self):
        self.patterns: Dict[str, SwarmPattern] = {}
        self._by_type: Dict[PatternType, List[str]] = {}
        self._by_circumstance: Dict[str, List[str]] = {}
        self._by_layer: Dict[int, List[str]] = {}
        self._by_game_type: Dict[str, List[str]] = {}
        self._recommendations_log: List[Dict] = []

    def store_pattern(self, pattern: SwarmPattern) -> None:
        """Store a pattern and index it."""
        # Check for existing similar pattern
        existing = self._find_similar(pattern)
        if existing:
            # Merge with existing pattern — increase confidence
            existing.source_dome_ids.extend(pattern.source_dome_ids)
            existing.confidence = min(1.0, existing.confidence + 0.1)
            existing.version += 1
            existing.last_updated = datetime.utcnow()
            return

        self.patterns[pattern.pattern_id] = pattern

        # Index
        pt = pattern.pattern_type
        if pt not in self._by_type:
            self._by_type[pt] = []
        self._by_type[pt].append(pattern.pattern_id)

        for circ in pattern.circumstance_types:
            if circ not in self._by_circumstance:
                self._by_circumstance[circ] = []
            self._by_circumstance[circ].append(pattern.pattern_id)

        for layer in pattern.layers:
            if layer not in self._by_layer:
                self._by_layer[layer] = []
            self._by_layer[layer].append(pattern.pattern_id)

        gt = pattern.game_type
        if gt not in self._by_game_type:
            self._by_game_type[gt] = []
        self._by_game_type[gt].append(pattern.pattern_id)

    def query(
        self,
        game_type: Optional[str] = None,
        pattern_type: Optional[PatternType] = None,
        circumstance_types: Optional[List[str]] = None,
        site_types: Optional[List[str]] = None,
        layers: Optional[List[int]] = None,
        min_confidence: float = 0.3,
        limit: int = 20,
    ) -> List[SwarmPattern]:
        """
        Query the knowledge base for relevant patterns.
        Returns patterns ranked by relevance and confidence.
        """
        candidates: Dict[str, float] = {}  # pattern_id → relevance score

        # Score all patterns
        for pid, pattern in self.patterns.items():
            if pattern.confidence < min_confidence:
                continue

            score = 0.0

            # Game type match
            if game_type and pattern.game_type == game_type:
                score += 5.0
            elif game_type and pattern.game_type != game_type:
                score += 1.0  # Cross-pollination still has value

            # Pattern type match
            if pattern_type and pattern.pattern_type == pattern_type:
                score += 3.0

            # Circumstance match
            if circumstance_types:
                overlap = set(circumstance_types) & set(pattern.circumstance_types)
                score += len(overlap) * 4.0

            # Site type match
            if site_types:
                overlap = set(site_types) & set(pattern.site_types)
                score += len(overlap) * 4.0

            # Layer match
            if layers:
                overlap = set(layers) & set(pattern.layers)
                score += len(overlap) * 2.0

            # Confidence boost
            score *= (0.5 + pattern.confidence * 0.5)

            # Effectiveness boost
            score *= (0.5 + pattern.effectiveness * 0.5)

            if score > 0:
                candidates[pid] = score

        # Sort by score, return top N
        ranked = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return [self.patterns[pid] for pid, _ in ranked[:limit]]

    def _find_similar(self, pattern: SwarmPattern) -> Optional[SwarmPattern]:
        """Find an existing pattern that's similar enough to merge."""
        # Use keyword overlap as similarity measure
        new_kw = set(k.lower() for k in pattern.keywords)
        if not new_kw:
            return None

        for existing in self.patterns.values():
            if existing.pattern_type != pattern.pattern_type:
                continue
            if existing.game_type != pattern.game_type:
                continue
            existing_kw = set(k.lower() for k in existing.keywords)
            if not existing_kw:
                continue
            overlap = new_kw & existing_kw
            union = new_kw | existing_kw
            similarity = len(overlap) / len(union) if union else 0
            if similarity > 0.6:
                return existing

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "total_patterns": len(self.patterns),
            "by_type": {k.value: len(v) for k, v in self._by_type.items()},
            "by_game_type": {k: len(v) for k, v in self._by_game_type.items()},
            "by_circumstance": {k: len(v) for k, v in self._by_circumstance.items()},
            "avg_confidence": round(
                sum(p.confidence for p in self.patterns.values()) / max(len(self.patterns), 1), 3
            ),
            "total_recommendations_made": sum(
                p.times_recommended for p in self.patterns.values()
            ),
        }


# ── Pattern Extractor ───────────────────────────────────────────

class PatternExtractor:
    """
    Extracts patterns from completed dome/sphere productions.
    This runs AUTOMATICALLY after every production completes.
    """

    def extract_dome_patterns(
        self,
        dome_data: Dict[str, Any],
        stage_outputs: List[Dict],
        final_scores: Dict[str, Any],
        team_data: Dict[str, Any],
        project_id: str,
    ) -> List[SwarmPattern]:
        """
        Extract all patterns from a completed dome production.
        """
        patterns = []
        circumstance_types = self._infer_circumstances(dome_data)

        # ── Legal patterns ──────────────────────────────────────
        legal = dome_data.get("layer_1", dome_data.get("legal", {}))
        entitlements = legal.get("entitlements", [])
        if entitlements:
            # Pattern: which provisions were most impactful
            high_value = [e for e in entitlements if e.get("annual_value", 0) > 5000]
            if high_value:
                patterns.append(SwarmPattern(
                    pattern_type=PatternType.LEGAL,
                    game_type="domes",
                    description=(
                        f"High-value provisions for {', '.join(circumstance_types[:3])}: "
                        f"{', '.join(e.get('program_name', '') for e in high_value[:5])}. "
                        f"Total value: ${sum(e.get('annual_value', 0) for e in high_value):,.0f}/yr."
                    ),
                    evidence=f"From dome {project_id}: {len(high_value)} provisions > $5K/yr",
                    mechanism="These provisions consistently appear for this circumstance profile",
                    circumstance_types=circumstance_types,
                    layers=[1],
                    keywords=["legal", "provisions", "entitlements"] + [
                        e.get("program_name", "").lower() for e in high_value
                    ],
                    source_dome_ids=[project_id],
                    confidence=0.5,
                    impact_score=sum(e.get("annual_value", 0) for e in high_value),
                ))

            # Pattern: eligibility pathway success
            approved = [e for e in entitlements if e.get("application_status") == "approved"]
            if approved:
                patterns.append(SwarmPattern(
                    pattern_type=PatternType.LEGAL,
                    game_type="domes",
                    description=(
                        f"Successful eligibility pathways: "
                        f"{', '.join(e.get('program_name', '') for e in approved[:5])}. "
                        f"Approval rate: {len(approved)}/{len(entitlements)} = "
                        f"{len(approved)/len(entitlements):.0%}"
                    ),
                    evidence=f"Dome {project_id}: {len(approved)} approvals",
                    circumstance_types=circumstance_types,
                    layers=[1],
                    keywords=["eligibility", "approval", "pathway"],
                    source_dome_ids=[project_id],
                    confidence=0.4,
                ))

        # ── Systems patterns ────────────────────────────────────
        systems = dome_data.get("layer_2", dome_data.get("systems", {}))
        sys_list = systems.get("systems", [])
        frag_index = systems.get("fragmentation_index", 0)
        gaps = systems.get("cross_system_gaps", [])

        if gaps:
            patterns.append(SwarmPattern(
                pattern_type=PatternType.SYSTEMS,
                game_type="domes",
                description=(
                    f"System gaps for {', '.join(circumstance_types[:2])}: "
                    f"{'; '.join(gaps[:5])}. "
                    f"Fragmentation index: {frag_index:.2f}."
                ),
                evidence=f"Dome {project_id}: {len(gaps)} cross-system gaps",
                mechanism="These systems consistently fail to connect for this profile",
                circumstance_types=circumstance_types,
                layers=[2],
                keywords=["systems", "fragmentation", "gaps", "coordination"],
                source_dome_ids=[project_id],
                confidence=0.5,
            ))

        # ── Fiscal patterns ─────────────────────────────────────
        fiscal = dome_data.get("layer_3", dome_data.get("fiscal", {}))
        coord_savings = fiscal.get("coordination_savings", 0)
        frag_cost = fiscal.get("cost_of_fragmentation", 0)

        if coord_savings > 0:
            patterns.append(SwarmPattern(
                pattern_type=PatternType.FISCAL,
                game_type="domes",
                description=(
                    f"Coordination savings for {', '.join(circumstance_types[:2])}: "
                    f"${coord_savings:,.0f}/yr. "
                    f"Fragmentation costs: ${frag_cost:,.0f}/yr."
                ),
                evidence=f"Dome {project_id}",
                circumstance_types=circumstance_types,
                layers=[3],
                keywords=["savings", "coordination", "cost", "fragmentation"],
                source_dome_ids=[project_id],
                confidence=0.5,
                impact_score=coord_savings,
            ))

        # ── Health patterns ─────────────────────────────────────
        health = dome_data.get("layer_4", dome_data.get("health", {}))
        conditions = health.get("conditions", [])
        if conditions:
            condition_names = [
                c.get("condition", c.get("code", {}).get("text", ""))
                for c in conditions
            ]
            patterns.append(SwarmPattern(
                pattern_type=PatternType.HEALTH,
                game_type="domes",
                description=(
                    f"Health profile for {', '.join(circumstance_types[:2])}: "
                    f"{', '.join(cn for cn in condition_names if cn)[:200]}"
                ),
                evidence=f"Dome {project_id}: {len(conditions)} conditions",
                circumstance_types=circumstance_types,
                layers=[4],
                keywords=["health", "conditions"] + [cn.lower() for cn in condition_names if cn],
                source_dome_ids=[project_id],
                confidence=0.4,
            ))

        # ── Coordination patterns ───────────────────────────────
        # Which cross-layer relationships matter most
        scores = final_scores.get("dimensions", {})
        if scores:
            weakest = min(scores.items(), key=lambda x: x[1]) if scores else ("", 0)
            strongest = max(scores.items(), key=lambda x: x[1]) if scores else ("", 0)
            patterns.append(SwarmPattern(
                pattern_type=PatternType.COORDINATION,
                game_type="domes",
                description=(
                    f"Score profile for {', '.join(circumstance_types[:2])}: "
                    f"Weakest dimension: {weakest[0]} ({weakest[1]}). "
                    f"Strongest: {strongest[0]} ({strongest[1]}). "
                    f"Total Cosm: {final_scores.get('total', 0)}."
                ),
                evidence=f"Dome {project_id} final scores",
                circumstance_types=circumstance_types,
                layers=list(range(1, 13)),
                keywords=["coordination", "score", "cosm", weakest[0], strongest[0]],
                source_dome_ids=[project_id],
                confidence=0.5,
                impact_score=final_scores.get("total", 0),
            ))

        # ── Innovation patterns ─────────────────────────────────
        unlikely = team_data.get("unlikely_collisions", [])
        ip_domains = team_data.get("ip_surface_area", [])
        if unlikely:
            patterns.append(SwarmPattern(
                pattern_type=PatternType.INNOVATION,
                game_type="domes",
                description=(
                    f"Innovation pattern: {len(unlikely)} unlikely collisions. "
                    f"IP domains: {', '.join(ip_domains[:5])}. "
                    f"Team size: {team_data.get('member_count', 0)}."
                ),
                evidence=f"Dome {project_id}: {'; '.join(unlikely[:3])}",
                circumstance_types=circumstance_types,
                layers=[],
                keywords=["innovation", "unlikely", "ip"] + ip_domains[:5],
                source_dome_ids=[project_id],
                confidence=0.4,
            ))

        return patterns

    def extract_sphere_patterns(
        self,
        sphere_data: Dict[str, Any],
        stage_outputs: List[Dict],
        final_scores: Dict[str, Any],
        project_id: str,
    ) -> List[SwarmPattern]:
        """Extract patterns from a completed sphere production."""
        patterns = []
        site_types = self._infer_site_types(sphere_data)

        parcel = sphere_data.get("parcel", {})
        zoning = parcel.get("zoning", "")
        neighborhood = parcel.get("neighborhood", "")

        # Regulatory patterns
        if zoning:
            patterns.append(SwarmPattern(
                pattern_type=PatternType.REGULATORY,
                game_type="spheres",
                description=(
                    f"Regulatory outcome for {zoning} in {neighborhood}: "
                    f"Final Chron: {final_scores.get('total', 0)}"
                ),
                evidence=f"Sphere {project_id}",
                site_types=site_types,
                layers=[1, 2],
                keywords=["zoning", "regulatory", "permit", zoning.lower(), neighborhood.lower()],
                source_dome_ids=[project_id],
                confidence=0.5,
                geography=neighborhood,
            ))

        # Awe patterns
        for stage_out in stage_outputs:
            for d in stage_out.get("deliverables", []):
                desc = d.get("description", "").lower()
                awe_signals = ["awe", "vastness", "accommodation", "effervescence", "moral beauty"]
                if sum(1 for s in awe_signals if s in desc) >= 2:
                    patterns.append(SwarmPattern(
                        pattern_type=PatternType.AWE,
                        game_type="spheres",
                        description=f"Awe design: {d.get('description', '')[:200]}",
                        evidence=f"Sphere {project_id}, stage {stage_out.get('stage', '')}",
                        site_types=site_types,
                        layers=[5, 6, 7],
                        keywords=["awe"] + [s for s in awe_signals if s in desc],
                        source_dome_ids=[project_id],
                        confidence=0.4,
                        geography=neighborhood,
                    ))
                    break

        # Activation patterns
        scores = final_scores.get("dimensions", {})
        if scores:
            patterns.append(SwarmPattern(
                pattern_type=PatternType.ACTIVATION,
                game_type="spheres",
                description=(
                    f"Activation result for {', '.join(site_types[:2])} "
                    f"in {neighborhood}: Chron {final_scores.get('total', 0)}"
                ),
                evidence=f"Sphere {project_id} scores",
                site_types=site_types,
                layers=list(range(1, 11)),
                keywords=["activation", "sphere", neighborhood.lower()],
                source_dome_ids=[project_id],
                confidence=0.5,
                impact_score=final_scores.get("total", 0),
                geography=neighborhood,
            ))

        return patterns

    def _infer_circumstances(self, dome_data: Dict[str, Any]) -> List[str]:
        """Infer circumstance types from dome data."""
        circumstances = []
        subject = dome_data.get("subject", dome_data.get("character", {}))

        # Check situation description and key systems
        situation = (subject.get("situation", "") + " " +
                     subject.get("production_challenge", "")).lower()
        systems = [s.lower() if isinstance(s, str) else s.get("system_name", "").lower()
                   for s in dome_data.get("key_systems", subject.get("key_systems", []))]

        keyword_to_circ = {
            "foster": "foster_care", "aging out": "youth_aging_out",
            "homeless": "chronic_homelessness", "shelter": "chronic_homelessness",
            "disability": "disability", "disabled": "disability",
            "incarcerat": "justice_involved", "prison": "justice_involved",
            "juvenile": "justice_involved",
            "single parent": "single_parent", "single mother": "single_parent",
            "veteran": "veteran", "military": "veteran",
            "substance": "substance_use", "addiction": "substance_use",
            "immigrant": "immigrant_refugee", "refugee": "immigrant_refugee",
            "domestic violence": "domestic_violence", "abuse": "domestic_violence",
            "mental health": "mental_health", "depression": "mental_health",
            "elderly": "aging", "senior": "aging",
        }

        text = situation + " " + " ".join(systems)
        for keyword, circ in keyword_to_circ.items():
            if keyword in text and circ not in circumstances:
                circumstances.append(circ)

        return circumstances or ["general"]

    def _infer_site_types(self, sphere_data: Dict[str, Any]) -> List[str]:
        """Infer site types from sphere data."""
        types = []
        parcel = sphere_data.get("parcel", {})
        desc = (parcel.get("opportunity", "") + " " +
                parcel.get("community_context", "")).lower()

        keyword_to_site = {
            "vacant lot": "vacant_lot", "vacant": "vacant_lot",
            "commercial": "abandoned_commercial", "storefront": "abandoned_commercial",
            "park": "underused_public", "public space": "underused_public",
            "brownfield": "brownfield", "contaminated": "brownfield",
            "corner": "corner_lot",
            "corridor": "linear_corridor",
            "waterfront": "waterfront", "river": "waterfront",
            "industrial": "industrial",
        }

        for keyword, site_type in keyword_to_site.items():
            if keyword in desc and site_type not in types:
                types.append(site_type)

        return types or ["vacant_lot"]


# ── Recommendation Engine ───────────────────────────────────────

class SwarmRecommendation(BaseModel):
    """A recommendation from the swarm to a new production."""
    recommendation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pattern_id: str
    pattern_type: str
    layer: int = 0
    recommendation: str
    evidence_summary: str
    confidence: float = 0.0
    source_dome_count: int = 0
    adopted: Optional[bool] = None     # Filled in after production completes
    score_impact: Optional[float] = None


class RecommendationEngine:
    """
    Produces context-aware recommendations for new productions
    based on the knowledge base.
    """

    def __init__(self, knowledge_base: SwarmKnowledgeBase):
        self.kb = knowledge_base

    def recommend_for_dome(
        self,
        character_data: Dict[str, Any],
        key_systems: List[str],
        flourishing_dimensions: List[str],
    ) -> List[SwarmRecommendation]:
        """
        Generate recommendations for a new dome production.
        """
        # Infer circumstance types
        extractor = PatternExtractor()
        circumstances = extractor._infer_circumstances({
            "subject": character_data,
            "key_systems": key_systems,
        })

        recommendations = []

        # Query each pattern type
        for ptype in [PatternType.LEGAL, PatternType.SYSTEMS, PatternType.FISCAL,
                      PatternType.HEALTH, PatternType.HOUSING, PatternType.COORDINATION,
                      PatternType.CREATIVE, PatternType.INNOVATION]:

            patterns = self.kb.query(
                game_type="domes",
                pattern_type=ptype,
                circumstance_types=circumstances,
                min_confidence=0.3,
                limit=3,
            )

            for pattern in patterns:
                rec = SwarmRecommendation(
                    pattern_id=pattern.pattern_id,
                    pattern_type=ptype.value,
                    layer=pattern.layers[0] if pattern.layers else 0,
                    recommendation=pattern.description,
                    evidence_summary=(
                        f"Based on {len(pattern.source_dome_ids)} prior domes "
                        f"with similar circumstances ({', '.join(circumstances[:3])}). "
                        f"Confidence: {pattern.confidence:.0%}. "
                        f"Effectiveness: {pattern.effectiveness:.0%}."
                    ),
                    confidence=pattern.confidence,
                    source_dome_count=len(pattern.source_dome_ids),
                )
                recommendations.append(rec)

                # Track that this pattern was recommended
                pattern.times_recommended += 1

        # Sort by confidence
        recommendations.sort(key=lambda r: r.confidence, reverse=True)
        return recommendations

    def recommend_for_sphere(
        self,
        parcel_data: Dict[str, Any],
    ) -> List[SwarmRecommendation]:
        """Generate recommendations for a new sphere production."""
        extractor = PatternExtractor()
        site_types = extractor._infer_site_types({"parcel": parcel_data})

        recommendations = []

        for ptype in [PatternType.REGULATORY, PatternType.ACTIVATION,
                      PatternType.AWE, PatternType.ECONOMICS]:

            patterns = self.kb.query(
                game_type="spheres",
                pattern_type=ptype,
                site_types=site_types,
                min_confidence=0.3,
                limit=3,
            )

            for pattern in patterns:
                rec = SwarmRecommendation(
                    pattern_id=pattern.pattern_id,
                    pattern_type=ptype.value,
                    layer=pattern.layers[0] if pattern.layers else 0,
                    recommendation=pattern.description,
                    evidence_summary=(
                        f"Based on {len(pattern.source_dome_ids)} prior spheres "
                        f"with similar site types ({', '.join(site_types[:3])}). "
                        f"Confidence: {pattern.confidence:.0%}."
                    ),
                    confidence=pattern.confidence,
                    source_dome_count=len(pattern.source_dome_ids),
                )
                recommendations.append(rec)
                pattern.times_recommended += 1

        recommendations.sort(key=lambda r: r.confidence, reverse=True)
        return recommendations


# ── Reinforcement Loop ──────────────────────────────────────────

class ReinforcementLoop:
    """
    The reinforcement loop updates pattern confidence based on
    whether recommendations that were adopted produced better scores
    than those that were rejected.

    This is what makes the swarm genuinely learn, not just accumulate data.
    """

    def __init__(self, knowledge_base: SwarmKnowledgeBase):
        self.kb = knowledge_base

    def update_from_production(
        self,
        recommendations: List[SwarmRecommendation],
        final_cosm: float,
    ) -> Dict[str, Any]:
        """
        After a production completes, update pattern confidence
        based on which recommendations were adopted and the final score.
        """
        updates = {"patterns_updated": 0, "confidence_changes": []}

        for rec in recommendations:
            pattern = self.kb.patterns.get(rec.pattern_id)
            if not pattern:
                continue

            if rec.adopted is True:
                pattern.times_adopted += 1
                # Running average of scores when adopted
                n = pattern.times_adopted
                pattern.avg_score_when_adopted = (
                    (pattern.avg_score_when_adopted * (n - 1) + final_cosm) / n
                )
                # Boost confidence
                old_conf = pattern.confidence
                pattern.confidence = min(1.0, pattern.confidence + 0.05)
                updates["confidence_changes"].append({
                    "pattern_id": pattern.pattern_id,
                    "old": old_conf,
                    "new": pattern.confidence,
                    "reason": "adopted",
                })

            elif rec.adopted is False:
                pattern.times_rejected += 1
                n = max(pattern.times_rejected, 1)
                pattern.avg_score_when_rejected = (
                    (pattern.avg_score_when_rejected * (n - 1) + final_cosm) / n
                )

                # If rejected recommendations led to HIGHER scores,
                # the pattern might not be as good as thought
                if (pattern.times_adopted > 0 and
                        final_cosm > pattern.avg_score_when_adopted):
                    old_conf = pattern.confidence
                    pattern.confidence = max(0.1, pattern.confidence - 0.08)
                    updates["confidence_changes"].append({
                        "pattern_id": pattern.pattern_id,
                        "old": old_conf,
                        "new": pattern.confidence,
                        "reason": "rejected_scored_higher",
                    })

            pattern.last_updated = datetime.utcnow()
            updates["patterns_updated"] += 1

        return updates


# ── Cross-Dome Analytics ────────────────────────────────────────

class SwarmAnalytics:
    """
    Cross-dome and cross-sphere analytics.
    Produces systemic insights from the entire portfolio.
    """

    def __init__(self, knowledge_base: SwarmKnowledgeBase):
        self.kb = knowledge_base

    def systemic_gap_detection(self) -> List[Dict[str, Any]]:
        """
        Detect systemic gaps — problems that appear across ALL domes.
        These are not person-specific issues but system-level failures.
        """
        gaps = []
        system_patterns = self.kb.query(
            pattern_type=PatternType.SYSTEMS,
            min_confidence=0.3,
            limit=100,
        )

        # Find gaps that appear in multiple domes
        gap_descriptions: Dict[str, List[str]] = {}  # description → dome_ids
        for pattern in system_patterns:
            # Use first 100 chars as key for similarity
            key = pattern.description[:100].lower()
            if key not in gap_descriptions:
                gap_descriptions[key] = []
            gap_descriptions[key].extend(pattern.source_dome_ids)

        for desc_key, dome_ids in gap_descriptions.items():
            unique_domes = list(set(dome_ids))
            if len(unique_domes) >= 2:
                gaps.append({
                    "description": desc_key,
                    "dome_count": len(unique_domes),
                    "dome_ids": unique_domes,
                    "systemic": len(unique_domes) >= 3,
                    "recommendation": "This is a systemic issue, not person-specific. Policy intervention required.",
                })

        gaps.sort(key=lambda x: x["dome_count"], reverse=True)
        return gaps

    def policy_innovation_surfacing(self) -> List[Dict[str, Any]]:
        """
        Find policy recommendations that emerge independently across domes.
        """
        policy_patterns = self.kb.query(
            pattern_type=PatternType.POLICY,
            min_confidence=0.3,
            limit=100,
        )
        legal_patterns = self.kb.query(
            pattern_type=PatternType.LEGAL,
            min_confidence=0.3,
            limit=100,
        )

        all_patterns = policy_patterns + legal_patterns
        innovations = []

        for pattern in all_patterns:
            if len(pattern.source_dome_ids) >= 2:
                innovations.append({
                    "description": pattern.description,
                    "dome_count": len(pattern.source_dome_ids),
                    "confidence": pattern.confidence,
                    "impact": pattern.impact_score,
                    "recommendation": (
                        f"This pattern emerged independently in "
                        f"{len(pattern.source_dome_ids)} domes. "
                        f"Consider as legislative priority."
                    ),
                })

        innovations.sort(key=lambda x: x["dome_count"], reverse=True)
        return innovations

    def cost_pattern_mapping(self) -> Dict[str, Any]:
        """Map cost patterns across all domes."""
        fiscal_patterns = self.kb.query(
            pattern_type=PatternType.FISCAL,
            min_confidence=0.3,
            limit=100,
        )

        total_savings = 0.0
        count = 0
        by_circumstance: Dict[str, List[float]] = {}

        for pattern in fiscal_patterns:
            if pattern.impact_score > 0:
                total_savings += pattern.impact_score
                count += 1
                for circ in pattern.circumstance_types:
                    if circ not in by_circumstance:
                        by_circumstance[circ] = []
                    by_circumstance[circ].append(pattern.impact_score)

        return {
            "avg_coordination_savings": round(total_savings / max(count, 1), 2),
            "total_savings_observed": total_savings,
            "observations": count,
            "by_circumstance": {
                circ: {
                    "avg_savings": round(sum(vals) / len(vals), 2),
                    "observations": len(vals),
                }
                for circ, vals in by_circumstance.items()
            },
        }

    def innovation_frontier(self) -> Dict[str, Any]:
        """Map the innovation frontier across productions."""
        innovation_patterns = self.kb.query(
            pattern_type=PatternType.INNOVATION,
            min_confidence=0.2,
            limit=100,
        )

        ip_domains_seen: Dict[str, int] = {}
        for pattern in innovation_patterns:
            for kw in pattern.keywords:
                if kw in ["entertainment", "technology", "financial_product",
                          "policy", "healthcare", "urban_design", "fashion",
                          "culinary", "architectural"]:
                    ip_domains_seen[kw] = ip_domains_seen.get(kw, 0) + 1

        return {
            "total_innovation_patterns": len(innovation_patterns),
            "ip_domain_frequency": dict(sorted(
                ip_domains_seen.items(), key=lambda x: x[1], reverse=True
            )),
        }

    def learning_curve(self) -> List[Dict[str, Any]]:
        """
        Compute the learning curve — how scores improve as more
        productions complete.
        """
        # Collect all score-bearing patterns ordered by creation
        scored = [
            p for p in self.kb.patterns.values()
            if p.impact_score > 0
        ]
        scored.sort(key=lambda p: p.created_at)

        curve = []
        running_total = 0.0
        for i, p in enumerate(scored, 1):
            running_total += p.impact_score
            curve.append({
                "production_number": i,
                "score": p.impact_score,
                "running_avg": round(running_total / i, 1),
                "patterns_available": len([
                    q for q in scored[:i]
                ]),
                "timestamp": p.created_at.isoformat(),
            })

        return curve
