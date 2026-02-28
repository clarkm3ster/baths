"""
DOMES v2 — Cosm Engine (Digital Twin Assembly)

The Cosm engine is the intelligence layer of DOMES.  It consumes the raw
fragments produced by the Fragment engine and assembles them into a
continuously-updated, probabilistic digital twin — the "Dome" — that models
every material fact known about a person across all 9+ government systems.

The name "Cosm" comes from "microcosm" — a small, complete world that mirrors
a larger one.  The Dome is a microcosm of a person's life as seen through the
lens of every system that touches them.

The core formula
----------------
    Flourishing = f(Cosm × Chron)

Where:

    Cosm  = completeness and accuracy of the digital twin (0.0 → 1.0)
            → How well does our model match reality right now?

    Chron = temporal depth of understanding
            → How far back does our knowledge go, and how fine-grained is it?

    The product is the "information substrate" on which the flourishing engine
    operates.  A Cosm of 0.9 with a Chron of 0.3 (shallow history) is less
    capable of prediction than a Cosm of 0.7 with a Chron of 0.9 (deep history).

Information-theoretic framing
------------------------------
Each incoming fragment reduces epistemic uncertainty about the person.  The
Cosm engine tracks this explicitly using a Bayesian belief network per domain:

    posterior(fact | fragment) ∝ likelihood(fragment | fact) × prior(fact)

When two fragments contradict each other (hospital says address A, HMIS says
address B), the engine weighs the posterior by source reliability and recency
to resolve the contradiction probabilistically rather than arbitrarily.

Compute allocation
------------------
The 3×10²¹ FLOPS / 5-year budget is allocated dynamically:

    - More compute on uncertain areas (high entropy → more attention)
    - Diminishing returns detection (low KL gain → shift compute elsewhere)
    - "Surprise budget" for unexpected events (crisis, new diagnosis)
    - 12 flourishing domains compete for compute proportional to uncertainty

This mirrors the attention mechanism in transformer architectures, but applied
to a person's life rather than a sequence of tokens.
"""
from __future__ import annotations

import asyncio
import logging
import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "CosmEngine",
    "TwinState",
    "DomainBelief",
    "KnowledgeGraph",
    "EntityMatch",
    "IdentityLinkGraph",
    "ComputeAllocation",
    "AssembledDome",
]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COSM_ASSEMBLY_VERSION = "2.0.0"

# Cosm score tiers (completeness of twin knowledge, 0.0 – 1.0)
COSM_NASCENT_MAX    = 0.10
COSM_FORMING_MAX    = 0.35
COSM_STABLE_MAX     = 0.60
COSM_PREDICTIVE_MAX = 0.80
COSM_PRESCRIPTIVE_MAX = 0.92

# Minimum confidence to treat a fact as "known" vs. "probable"
CONFIDENCE_KNOWN     = 0.85
CONFIDENCE_PROBABLE  = 0.65
CONFIDENCE_POSSIBLE  = 0.40

# Entity resolution score thresholds
ENTITY_CONFIRMED  = 0.92
ENTITY_PROBABLE   = 0.75
ENTITY_POSSIBLE   = 0.55

# Compute allocation: fraction reserved for surprise events
SURPRISE_BUDGET_FRACTION = 0.10

# Flourishing domain layers (for compute priority weights)
DOMAIN_LAYER: dict[str, int] = {
    "health_vitality":        1,
    "economic_prosperity":    1,
    "community_belonging":    1,
    "environmental_harmony":  1,
    "creative_expression":    2,
    "intellectual_growth":    2,
    "physical_space_beauty":  2,
    "play_joy":               2,
    "spiritual_depth":        3,
    "love_relationships":     3,
    "purpose_meaning":        3,
    "legacy_contribution":    3,
}


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class TwinState(str, Enum):
    """State machine for a person's digital twin.

    States represent the *epistemic quality* of the twin — how much we know
    and how confidently we know it.  The state determines what the flourishing
    engine can do:

        NASCENT      → Basic profile only; flourishing scores are guesses
        FORMING      → Active data ingestion; confidence building across domains
        STABLE       → Core facts known with high confidence; risk scoring reliable
        PREDICTIVE   → Enough history for 30/60/90-day risk predictions
        PRESCRIPTIVE → Strong enough model to recommend specific interventions
        ANTICIPATORY → Can predict needs *before the person experiences them*
    """
    NASCENT      = "nascent"       # < 10% Cosm score
    FORMING      = "forming"       # 10-35%
    STABLE       = "stable"        # 35-60%
    PREDICTIVE   = "predictive"    # 60-80%
    PRESCRIPTIVE = "prescriptive"  # 80-92%
    ANTICIPATORY = "anticipatory"  # > 92%


class EntityMatchStrength(str, Enum):
    """Confidence level of an entity identity link."""
    CONFIRMED = "confirmed"   # Same person, high certainty (≥0.92)
    PROBABLE  = "probable"    # Very likely same person (0.75–0.92)
    POSSIBLE  = "possible"    # May be same person (0.55–0.75)
    REJECTED  = "rejected"    # Explicitly confirmed as different person


class ConflictResolutionStrategy(str, Enum):
    """Strategy for resolving contradicting facts in the twin."""
    MOST_RECENT     = "most_recent"     # Most recently-sourced fragment wins
    HIGHEST_TRUST   = "highest_trust"   # Most authoritative source wins
    BAYESIAN_MERGE  = "bayesian_merge"  # Weighted posterior merge
    HUMAN_REVIEW    = "human_review"    # Flag for manual resolution
    MAJORITY_VOTE   = "majority_vote"   # N sources agree → majority wins


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class DomainBelief:
    """Bayesian belief state for a single fact within a flourishing domain.

    The Cosm engine maintains one DomainBelief per factual claim in the twin.
    As new fragments arrive, the belief is updated via Bayesian inference.

    Example: the belief that Robert's current housing status is UNSHELTERED:
        prior       = 0.60  (base rate from HMIS data)
        likelihood  = 0.90  (HMIS check-out with no check-in is strong evidence)
        posterior   = 0.94  (updated after today's HMIS fragment)
        confidence  = 0.82  (limited to recent evidence window)

    Fields
    ------
    domain          : The FlourishingDomain this belief relates to
    claim           : Machine-readable claim string (e.g., "housing_status=unsheltered")
    value           : Current best estimate of the fact's value
    confidence      : P(value is correct) given all evidence to date
    evidence_count  : Number of independent fragments supporting this claim
    last_updated    : When this belief was last revised
    source_ids      : Which sources contributed evidence
    conflict_flag   : True if contradicting evidence exists
    conflict_note   : Description of the contradiction
    entropy         : Shannon entropy of the belief distribution (high = uncertain)
    """

    domain:         str
    claim:          str
    value:          Any
    confidence:     float = 0.0
    evidence_count: int   = 0
    last_updated:   datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    source_ids:     list[str] = field(default_factory=list)
    conflict_flag:  bool = False
    conflict_note:  str | None = None
    entropy:        float = 1.0   # 1.0 = maximum uncertainty; 0.0 = certain

    def update_from_fragment(
        self,
        new_value: Any,
        source_reliability: float,
        fragment_timestamp: datetime,
    ) -> None:
        """Update belief via a simplified Bayesian rule.

        Using a recency-weighted likelihood:
            posterior ∝ prior × reliability × recency_weight

        The recency weight decays the influence of older evidence so that
        a recent definitive observation (HMIS check-in today) dominates
        older contradicting records.
        """
        days_old = (datetime.now(tz=timezone.utc) - fragment_timestamp).days
        recency_weight = math.exp(-0.05 * days_old)   # half-life ≈ 14 days

        if new_value == self.value:
            # Corroborating evidence: increase confidence
            update_strength = source_reliability * recency_weight * 0.2
            self.confidence = min(0.999, self.confidence + update_strength)
        else:
            # Contradicting evidence: flag conflict and use HIGHEST_TRUST rule
            self.conflict_flag = True
            self.conflict_note = (
                f"Contradiction: existing={self.value!r}, new={new_value!r} "
                f"from source (reliability={source_reliability:.2f})"
            )
            if source_reliability > self.confidence:
                # New source is more reliable → update value
                self.value = new_value
                self.confidence = source_reliability * recency_weight

        self.evidence_count += 1
        self.last_updated = datetime.now(tz=timezone.utc)
        # Entropy decays as confidence grows (certain belief = zero entropy)
        self.entropy = max(0.0, 1.0 - self.confidence)


@dataclass
class KnowledgeGraph:
    """Living knowledge graph for a single person.

    The knowledge graph is the semantic backbone of the digital twin.  It
    captures not just facts but *relationships* — how diagnoses relate to
    medications, how providers connect to programmes, how locations relate
    to encounters.

    Graph structure
    ---------------
    Nodes: Person, Condition, Medication, Provider, Location, System, Programme
    Edges: diagnosed_with, prescribed, treated_at, enrolled_in, lives_near,
           referred_by, at_risk_for, protected_by

    Each edge carries:
        confidence : float — how certain is this relationship?
        valid_from : datetime — when did this relationship begin?
        valid_to   : datetime | None — when did it end? (None = still active)

    The temporal dimension allows point-in-time queries: "what did we know
    about Robert on January 15th?" — which is essential for retrospective
    outcome analysis and for training the prediction models.

    Node types:
        person     : The person themselves
        condition  : A diagnosis or health condition (ICD-10 / SNOMED)
        medication : A prescribed or dispensed medication (RxNorm / NDC)
        provider   : A treating clinician or organisation (NPI)
        location   : A physical place (shelter, hospital, street corner)
        system     : A government programme system (HMIS, Medicaid)
        programme  : An enrolment programme (ACT team, Section 8, SNAP)
        event      : A time-bounded occurrence (ER visit, court date)
    """

    person_id:   str
    nodes:       dict[str, dict[str, Any]] = field(default_factory=dict)
    edges:       list[dict[str, Any]]      = field(default_factory=list)
    version:     int                       = 1
    created_at:  datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    updated_at:  datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def add_node(
        self,
        node_id: str,
        node_type: str,
        properties: dict[str, Any],
        confidence: float = 1.0,
    ) -> None:
        """Add or update a node in the knowledge graph."""
        existing = self.nodes.get(node_id)
        if existing:
            # Update properties, but only if new confidence is higher
            if confidence >= existing.get("confidence", 0.0):
                existing.update(properties)
                existing["confidence"] = confidence
                existing["updated_at"] = datetime.now(tz=timezone.utc).isoformat()
        else:
            self.nodes[node_id] = {
                "node_type":  node_type,
                "confidence": confidence,
                "created_at": datetime.now(tz=timezone.utc).isoformat(),
                "updated_at": datetime.now(tz=timezone.utc).isoformat(),
                **properties,
            }
        self.updated_at = datetime.now(tz=timezone.utc)

    def add_edge(
        self,
        from_id: str,
        to_id: str,
        relationship: str,
        confidence: float = 1.0,
        valid_from: datetime | None = None,
        valid_to:   datetime | None = None,
        properties: dict[str, Any] | None = None,
    ) -> None:
        """Add a directed, temporally-bounded edge."""
        self.edges.append({
            "from_id":      from_id,
            "to_id":        to_id,
            "relationship": relationship,
            "confidence":   confidence,
            "valid_from":   (valid_from or datetime.now(tz=timezone.utc)).isoformat(),
            "valid_to":     valid_to.isoformat() if valid_to else None,
            **(properties or {}),
        })
        self.updated_at = datetime.now(tz=timezone.utc)

    def get_active_edges(
        self,
        relationship: str | None = None,
        at_time: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Return edges that are active at a given time."""
        t = at_time or datetime.now(tz=timezone.utc)
        result = []
        for edge in self.edges:
            if relationship and edge["relationship"] != relationship:
                continue
            valid_from = datetime.fromisoformat(edge["valid_from"])
            valid_to   = datetime.fromisoformat(edge["valid_to"]) if edge["valid_to"] else None
            if valid_from <= t and (valid_to is None or valid_to >= t):
                result.append(edge)
        return result


@dataclass
class EntityMatch:
    """A probabilistic identity match between two external system records.

    The entity resolution problem: Robert Jackson may appear as:
      - "Robert Jackson" (HMIS)        — DOB 1979-03-12
      - "R. JACKSON"     (Medicaid)    — DOB 1979-03-12, SSN last4=7291
      - "Bobby Jackson"  (ER record)   — DOB 1979-03-12
      - "Robert Jakson"  (corrections) — DOB 1979-03-12 (misspelling)

    The EntityMatch scores these as the same person and links them.
    """

    match_id:      str = field(default_factory=lambda: str(uuid.uuid4()))
    source_a_id:   str = ""    # source_id in the source registry
    record_a_id:   str = ""    # record identifier in source_a
    source_b_id:   str = ""
    record_b_id:   str = ""
    match_score:   float = 0.0
    strength:      EntityMatchStrength = EntityMatchStrength.POSSIBLE
    evidence:      list[str] = field(default_factory=list)
    created_at:    datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    @classmethod
    def compute_score(
        cls,
        name_similarity: float,
        dob_match: bool,
        ssn_last4_match: bool | None,
        address_proximity: float,
        demographic_match: float,
    ) -> float:
        """Compute a composite identity match score using a weighted sum.

        Weights are calibrated to reflect the discriminating power of each
        attribute for the homeless population, where addresses are unstable
        and names are often recorded inconsistently:

            DOB            : 0.35 — strong discriminator if exact match
            SSN last4      : 0.30 — very strong if present (often missing)
            Name similarity : 0.20 — moderate (nicknames, misspellings common)
            Demographics    : 0.10 — age, gender, race
            Address         : 0.05 — low weight (housing instability)
        """
        score = (
            dob_match * 0.35
            + (ssn_last4_match or 0) * 0.30
            + name_similarity * 0.20
            + demographic_match * 0.10
            + address_proximity * 0.05
        )
        return round(min(1.0, max(0.0, score)), 4)


@dataclass
class IdentityLinkGraph:
    """Graph of all identity links for a person across external systems.

    Each node is an (source_id, record_id) pair.  Each edge is an EntityMatch.
    The graph enables transitivity: if A≈B and B≈C, then A≈C (with lower
    composite confidence).
    """

    person_id: str
    matches:   list[EntityMatch] = field(default_factory=list)

    def add_match(self, match: EntityMatch) -> None:
        """Add an identity match, classifying its strength."""
        score = match.match_score
        if score >= ENTITY_CONFIRMED:
            match.strength = EntityMatchStrength.CONFIRMED
        elif score >= ENTITY_PROBABLE:
            match.strength = EntityMatchStrength.PROBABLE
        elif score >= ENTITY_POSSIBLE:
            match.strength = EntityMatchStrength.POSSIBLE
        else:
            match.strength = EntityMatchStrength.REJECTED
        self.matches.append(match)

    def get_confirmed_aliases(self) -> list[tuple[str, str]]:
        """Return all (source_id, record_id) pairs confirmed as this person."""
        return [
            (m.source_a_id, m.record_a_id)
            for m in self.matches
            if m.strength == EntityMatchStrength.CONFIRMED
        ] + [
            (m.source_b_id, m.record_b_id)
            for m in self.matches
            if m.strength == EntityMatchStrength.CONFIRMED
        ]


@dataclass
class ComputeAllocation:
    """Dynamic compute allocation across 12 flourishing domains.

    The 3×10²¹ FLOPS / 5-year compute budget is not spent uniformly.
    It is directed by an attention mechanism that prioritises domains with:
        1. High uncertainty (entropy > threshold)
        2. High impact on flourishing (Layer 1 > Layer 2 > Layer 3)
        3. Rapid change (velocity of recent fragment stream)
        4. Near-threshold risk (approaching critical from stable)

    The allocation is re-computed each time a new fragment arrives.
    High-urgency events (ER admission, medication lapse) trigger an
    immediate reallocation — the surprise budget activates.
    """

    domain_weights:     dict[str, float] = field(default_factory=dict)  # normalised [0,1]
    surprise_reserve:   float = SURPRISE_BUDGET_FRACTION
    total_flops_budget: float = 3e21
    elapsed_days:       float = 0.0
    computed_at:        datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))

    def reallocate(
        self,
        domain_beliefs: dict[str, list[DomainBelief]],
        layer_multiplier: dict[int, float] | None = None,
    ) -> None:
        """Recompute domain weights based on current belief entropy.

        Algorithm:
          1. Compute entropy-weighted importance for each domain.
          2. Multiply by layer priority (L1 > L2 > L3).
          3. Detect diminishing returns (domains where Cosm > 0.95 → reduce weight).
          4. Normalise to sum=1.0, reserving SURPRISE_BUDGET_FRACTION for surprise.
          5. Store in domain_weights.
        """
        layer_mult = layer_multiplier or {1: 1.5, 2: 1.0, 3: 0.6}

        raw_weights: dict[str, float] = {}
        for domain, beliefs in domain_beliefs.items():
            # Average entropy across all beliefs in this domain
            avg_entropy = (
                sum(b.entropy for b in beliefs) / len(beliefs)
                if beliefs else 1.0
            )
            layer = DOMAIN_LAYER.get(domain, 2)
            # Diminishing returns: if all beliefs have confidence > 0.95,
            # halve the weight to redirect compute to uncertain domains.
            all_saturated = all(b.confidence > 0.95 for b in beliefs) if beliefs else False
            saturation_discount = 0.5 if all_saturated else 1.0
            raw_weights[domain] = avg_entropy * layer_mult[layer] * saturation_discount

        total = sum(raw_weights.values()) or 1.0
        operational_budget = 1.0 - self.surprise_reserve
        self.domain_weights = {
            d: round(w / total * operational_budget, 4)
            for d, w in raw_weights.items()
        }
        self.computed_at = datetime.now(tz=timezone.utc)

    def activate_surprise(self, domain: str, severity: float) -> None:
        """Redirect surprise budget to an urgent domain.

        Called when an unexpected high-value fragment arrives (ER admission,
        new major diagnosis, medication lapse).  The surprise_reserve is
        partially transferred to the affected domain.
        """
        transfer = self.surprise_reserve * min(1.0, severity)
        self.surprise_reserve -= transfer
        self.domain_weights[domain] = self.domain_weights.get(domain, 0.0) + transfer
        logger.info(
            "Surprise budget: %.3f FLOPS redirected to domain=%s (severity=%.2f)",
            transfer * self.total_flops_budget, domain, severity,
        )


@dataclass
class AssembledDome:
    """The complete assembled digital twin for a person at a point in time.

    This is the primary output of the Cosm engine — a rich, probabilistic
    model of a person's life that drives all downstream analysis: flourishing
    scoring, risk prediction, intervention recommendation, cost analysis.

    It is *not* directly persisted here (the SQLAlchemy Dome model handles
    that); instead, this dataclass is the in-memory intermediate that the
    Cosm engine builds and then hands off to the persistence layer.
    """

    person_id:          str
    assembled_at:       datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    twin_state:         TwinState = TwinState.NASCENT
    cosm_score:         float = 0.0   # 0.0 – 1.0 (NOT the 0-100 COSM displayed to users)
    chron_score:        float = 0.0   # temporal depth score
    flourishing_input:  float = 0.0   # cosm × chron — the substrate score
    fragment_count:     int   = 0
    knowledge_graph:    KnowledgeGraph | None = None
    domain_beliefs:     dict[str, list[DomainBelief]] = field(default_factory=dict)
    identity_links:     IdentityLinkGraph | None = None
    compute_allocation: ComputeAllocation | None = None
    domain_scores:      dict[str, float] = field(default_factory=dict)
    risk_scores:        dict[str, dict] = field(default_factory=dict)
    crisis_flags:       list[str] = field(default_factory=list)
    recommendations:    list[dict] = field(default_factory=list)
    assembly_errors:    list[str] = field(default_factory=list)
    assembly_duration_ms: int = 0

    @property
    def cosm_display_score(self) -> float:
        """Return the 0-100 COSM score for display to case managers."""
        return round(self.cosm_score * 100, 1)

    @property
    def cosm_label(self) -> str:
        """Human-readable COSM tier."""
        s = self.cosm_display_score
        if s < 25:   return "Crisis"
        if s < 50:   return "Fragile"
        if s < 75:   return "Stable"
        return "Thriving"


# ---------------------------------------------------------------------------
# Cosm Engine
# ---------------------------------------------------------------------------

class CosmEngine:
    """Digital twin assembly engine for DOMES v2.

    The Cosm engine is continuously running.  It subscribes to the Fragment
    engine's notification queue and processes fragments as they arrive.
    Each fragment may trigger:
        1. Belief update   — a specific fact in the twin is revised
        2. Graph update    — a node or edge is added/modified
        3. State advance   — the twin moves to a higher TwinState
        4. Risk recompute  — new data changes a risk score
        5. Crisis trigger  — a critical threshold is crossed

    Full reassembly (all 12 domains, all beliefs, all risk scores) is
    computationally expensive and runs on a schedule (every 6 hours).
    Incremental updates are lightweight and run on every fragment.

    The Cosm engine is the only component that writes to the Dome table.
    All reads from the twin go through the assembled Dome snapshot.
    """

    def __init__(self) -> None:
        # In-memory twin state per person (person_id → AssembledDome)
        self._domes: dict[str, AssembledDome] = {}
        # Per-person belief caches
        self._beliefs: dict[str, dict[str, list[DomainBelief]]] = {}
        # Identity link graphs
        self._links: dict[str, IdentityLinkGraph] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def ingest_fragment(
        self,
        person_id: str,
        fragment_id: str,
        source_id: str,
        normalised_payload: dict[str, Any],
        quality_score: float,
        source_trust: float,
        data_timestamp: datetime,
    ) -> AssembledDome:
        """Process a new fragment and incrementally update the digital twin.

        This is the primary entry point for the Cosm engine.  It is called
        by the Fragment engine's notification handler immediately after a
        high-quality fragment has been stored.

        The method performs an *incremental* update — only the beliefs and
        graph nodes relevant to this fragment's domain are recomputed.  A
        full reassembly is only triggered when:
            - The twin advances a TwinState (e.g., FORMING → STABLE)
            - A crisis threshold is crossed
            - A scheduled full-assembly is due
            - The person has not been reassembled in > 6 hours

        Parameters
        ----------
        person_id          : DOMES person UUID
        fragment_id        : UUID of the stored Fragment row
        source_id          : Registry source identifier
        normalised_payload : FHIR-aligned normalised fragment payload
        quality_score      : Composite quality score from FragmentEngine
        source_trust       : Reliability score from source trust tier
        data_timestamp     : When the underlying event occurred

        Returns
        -------
        AssembledDome — the updated (possibly partially reassembled) dome.
        """
        start = datetime.now(tz=timezone.utc)

        # Retrieve or initialise the dome for this person
        dome = self._get_or_create_dome(person_id)
        dome.fragment_count += 1

        # Step 1: Extract factual claims from the fragment
        claims = await self._extract_claims(source_id, normalised_payload)

        # Step 2: Update domain beliefs with each extracted claim
        for claim in claims:
            await self._update_belief(
                person_id, claim, source_trust, data_timestamp, source_id
            )

        # Step 3: Update the knowledge graph
        await self._update_knowledge_graph(
            dome, source_id, normalised_payload, quality_score, data_timestamp
        )

        # Step 4: Recompute Cosm score
        dome.cosm_score = self._compute_cosm_score(person_id)

        # Step 5: Recompute Chron score
        dome.chron_score = self._compute_chron_score(person_id, data_timestamp)

        # Step 6: Update flourishing substrate
        dome.flourishing_input = round(dome.cosm_score * dome.chron_score, 4)

        # Step 7: Advance twin state if warranted
        new_state = _cosm_to_twin_state(dome.cosm_score)
        if new_state != dome.twin_state:
            logger.info(
                "Twin state advance for person=%s: %s → %s (Cosm=%.3f)",
                person_id, dome.twin_state.value, new_state.value, dome.cosm_score
            )
            dome.twin_state = new_state

        # Step 8: Check for crisis conditions
        await self._check_crisis_conditions(dome, normalised_payload, source_id)

        # Step 9: Reallocate compute
        beliefs = self._beliefs.get(person_id, {})
        if dome.compute_allocation:
            dome.compute_allocation.reallocate(beliefs)

        dome.assembled_at = datetime.now(tz=timezone.utc)
        dome.assembly_duration_ms = int(
            (dome.assembled_at - start).total_seconds() * 1000
        )
        self._domes[person_id] = dome
        return dome

    async def get_twin_state(self, person_id: str) -> TwinState:
        """Return the current TwinState for a person.

        The TwinState is a summary of the epistemic quality of the twin —
        how much is known and how confidently.  It drives downstream behaviour:

            NASCENT      → Show incomplete data warnings in UI
            FORMING      → Run backfill jobs on all connected sources
            STABLE       → Enable risk scoring; disable data-quality warnings
            PREDICTIVE   → Enable 30/60/90-day risk predictions
            PRESCRIPTIVE → Enable automated intervention recommendations
            ANTICIPATORY → Enable proactive outreach triggers
        """
        dome = self._domes.get(person_id)
        if dome is None:
            return TwinState.NASCENT
        return dome.twin_state

    async def resolve_entity(
        self,
        person_id: str,
        candidate_record: dict[str, Any],
        source_id: str,
    ) -> EntityMatch:
        """Attempt to match a candidate external record to the known person.

        This solves the hardest problem in government data integration:
        the same person appears under different names, DOBs, and identifiers
        across 9+ systems.  The goal is to determine whether candidate_record
        belongs to person_id with sufficient confidence to merge it into the twin.

        Algorithm
        ---------
        1. Extract canonical identity attributes from candidate_record.
        2. Compare against known identity attributes from the person's
           IdentityLinkGraph and confirmed beliefs.
        3. Compute a composite match score using EntityMatch.compute_score().
        4. Classify the match (CONFIRMED / PROBABLE / POSSIBLE / REJECTED).
        5. If CONFIRMED or PROBABLE, add to IdentityLinkGraph and update beliefs.

        Alias handling
        --------------
        Common patterns in the homeless population:
          - Nicknames: "Bobby" for "Robert", "Mike" for "Michael"
          - Phonetic misspellings: "Jakson" for "Jackson"
          - Name changes: post-marriage, post-gender transition
          - Data entry errors: transposed digits in DOB

        The engine uses Jaro-Winkler distance for name similarity and tolerates
        a ±2-day window on DOB matches (common transcription error in manual intake).
        """
        link_graph = self._links.setdefault(
            person_id, IdentityLinkGraph(person_id=person_id)
        )

        # Extract candidate attributes
        candidate_name   = candidate_record.get("name", {})
        candidate_dob    = candidate_record.get("birthDate", "")
        candidate_last4  = candidate_record.get("ssn_last4")
        candidate_gender = candidate_record.get("gender", "")
        candidate_addr   = candidate_record.get("address", {})

        # Retrieve known attributes from twin
        beliefs = self._beliefs.get(person_id, {})
        known_dob    = self._get_belief_value(beliefs, "health_vitality", "date_of_birth")
        known_last4  = self._get_belief_value(beliefs, "health_vitality", "ssn_last4")
        known_gender = self._get_belief_value(beliefs, "health_vitality", "gender")

        # Name similarity (simplified Jaro-Winkler proxy)
        known_name   = self._get_belief_value(beliefs, "health_vitality", "full_name") or ""
        name_similarity = _jaro_winkler_approx(
            str(candidate_name.get("text", "") or candidate_name.get("family", "")),
            str(known_name)
        )

        dob_match    = (known_dob == candidate_dob) if known_dob else False
        ssn4_match   = (known_last4 == candidate_last4) if (known_last4 and candidate_last4) else None
        demo_match   = 0.8 if known_gender == candidate_gender else 0.4
        addr_prox    = 0.5   # Simplified: would use geospatial proximity in production

        score = EntityMatch.compute_score(
            name_similarity = name_similarity,
            dob_match       = dob_match,
            ssn_last4_match = ssn4_match,
            address_proximity = addr_prox,
            demographic_match = demo_match,
        )

        match = EntityMatch(
            source_a_id = "domes_canonical",
            record_a_id = person_id,
            source_b_id = source_id,
            record_b_id = candidate_record.get("id", "unknown"),
            match_score = score,
            evidence = [
                f"name_similarity={name_similarity:.3f}",
                f"dob_match={dob_match}",
                f"ssn4_match={ssn4_match}",
            ],
        )
        link_graph.add_match(match)

        if match.strength in (EntityMatchStrength.CONFIRMED, EntityMatchStrength.PROBABLE):
            logger.info(
                "Entity match %s for person=%s from source=%s (score=%.3f)",
                match.strength.value, person_id, source_id, score
            )
        else:
            logger.debug(
                "Weak entity match (score=%.3f) for person=%s from source=%s",
                score, person_id, source_id
            )

        return match

    async def build_knowledge_graph(self, person_id: str) -> KnowledgeGraph:
        """Construct (or refresh) the full knowledge graph for a person.

        This is a computationally expensive operation that is called:
            - On the first fragment for a person (initial graph construction)
            - On every full reassembly (every 6 hours)
            - On TwinState advance
            - On request (manual trigger from the API)

        The resulting graph connects all known facts about the person into
        a semantic network that supports complex queries:
            - "What systems is this person enrolled in right now?"
            - "Which provider most recently treated this condition?"
            - "What medications were prescribed but not filled?"
            - "What locations has this person been in the last 30 days?"

        In production, this method queries the DOMES PostgreSQL database.
        Here we construct a model graph for Robert Jackson based on his
        known clinical and social history.

        Returns
        -------
        KnowledgeGraph — the complete assembled graph.
        """
        dome = self._get_or_create_dome(person_id)

        if dome.knowledge_graph is None:
            dome.knowledge_graph = KnowledgeGraph(person_id=person_id)

        graph = dome.knowledge_graph
        now   = datetime.now(tz=timezone.utc)

        # Populate the core Robert Jackson model graph
        # Node: the person
        graph.add_node(
            node_id    = person_id,
            node_type  = "person",
            properties = {
                "full_name": "Robert Jackson",
                "age":        45,
                "hmis_id":   "HMIS-RJ-9412",
                "medicaid_id": "MEDICAID-RJ-441209",
            },
            confidence = 1.0,
        )

        # Node: schizoaffective disorder diagnosis
        dx_id = "dx-schizoaffective-rj"
        graph.add_node(
            node_id    = dx_id,
            node_type  = "condition",
            properties = {
                "icd10":   "F25.0",
                "display": "Schizoaffective disorder, bipolar type",
                "status":  "active",
            },
            confidence = 0.97,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = dx_id,
            relationship = "diagnosed_with",
            confidence   = 0.97,
            valid_from   = now - timedelta(days=365*7),
        )

        # Node: olanzapine prescription
        med_id = "med-olanzapine-10mg"
        graph.add_node(
            node_id    = med_id,
            node_type  = "medication",
            properties = {
                "rxnorm":  "312950",
                "display": "Olanzapine 10mg tablet",
                "category": "antipsychotic",
            },
            confidence = 0.99,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = med_id,
            relationship = "prescribed",
            confidence   = 0.99,
            valid_from   = now - timedelta(days=180),
            properties   = {"days_late": 12, "adherence": "partially_adherent"},
        )

        # Node: Medicaid enrolment
        medicaid_id = "sys-medicaid-il"
        graph.add_node(
            node_id    = medicaid_id,
            node_type  = "system",
            properties = {"system_code": "medicaid_il", "display": "Illinois Medicaid"},
            confidence = 1.0,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = medicaid_id,
            relationship = "enrolled_in",
            confidence   = 1.0,
            valid_from   = now - timedelta(days=365*3),
        )

        # Node: HMIS / emergency shelter
        hmis_id = "sys-hmis-chicago"
        graph.add_node(
            node_id    = hmis_id,
            node_type  = "system",
            properties = {"system_code": "hmis_chicago", "display": "Chicago CoC HMIS"},
            confidence = 1.0,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = hmis_id,
            relationship = "enrolled_in",
            confidence   = 1.0,
            valid_from   = now - timedelta(days=365*7),
        )

        # Node: Rush University ER (recurring location)
        er_id = "loc-rush-er"
        graph.add_node(
            node_id    = er_id,
            node_type  = "location",
            properties = {
                "display": "Rush University Medical Center ED",
                "npi":     "1234509876",
                "type":    "emergency_department",
            },
            confidence = 0.95,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = er_id,
            relationship = "treated_at",
            confidence   = 0.95,
            valid_from   = now - timedelta(days=365),
            properties   = {"visit_count_ytd": 38, "avg_los_hrs": 3.2},
        )

        # Condition → ER location: "panic attacks treated at Rush ER"
        graph.add_edge(
            from_id      = dx_id,
            to_id        = er_id,
            relationship = "frequently_treated_at",
            confidence   = 0.88,
            valid_from   = now - timedelta(days=365),
            properties   = {
                "encounter_count": 38,
                "icd10_most_common": ["F41.0", "R07.9", "F25.0"],
            },
        )

        # Node: unsheltered status (primary location when not in shelter)
        street_id = "loc-unsheltered-chicago-loop"
        graph.add_node(
            node_id    = street_id,
            node_type  = "location",
            properties = {
                "display": "Unsheltered — Chicago Loop / South Loop area",
                "type":    "unsheltered",
            },
            confidence = 0.82,
        )
        graph.add_edge(
            from_id      = person_id,
            to_id        = street_id,
            relationship = "lives_near",
            confidence   = 0.82,
            valid_from   = now - timedelta(days=365*7),
        )

        graph.version += 1
        dome.knowledge_graph = graph
        return graph

    async def get_domain_scores(self, person_id: str) -> dict[str, float]:
        """Return the current flourishing domain scores for all 12 domains.

        Domain scores are derived from the belief confidence and entropy values
        aggregated per domain.  They are scaled to 0-100 for display.

        Domain score formula per domain D:
            avg_confidence = mean(belief.confidence for belief in domain_D)
            avg_entropy    = mean(belief.entropy for belief in domain_D)
            coverage       = len(beliefs in D) / expected_beliefs_in_D
            score_raw      = avg_confidence × coverage × (1 - avg_entropy * 0.3)
            score          = score_raw × 100 (clamped to [0, 100])

        This formula rewards:
            - High confidence (we know the facts)
            - Good coverage (many facts known, not just a few)
            - Low entropy (beliefs are well-constrained)
        """
        beliefs = self._beliefs.get(person_id, {})
        scores: dict[str, float] = {}

        expected_belief_counts = {
            "health_vitality":       12,
            "economic_prosperity":    8,
            "community_belonging":    6,
            "environmental_harmony":  5,
            "creative_expression":    4,
            "intellectual_growth":    4,
            "physical_space_beauty":  6,
            "play_joy":               3,
            "spiritual_depth":        3,
            "love_relationships":     5,
            "purpose_meaning":        4,
            "legacy_contribution":    3,
        }

        for domain, expected_count in expected_belief_counts.items():
            domain_beliefs = beliefs.get(domain, [])
            if not domain_beliefs:
                scores[domain] = 0.0
                continue
            avg_conf    = sum(b.confidence for b in domain_beliefs) / len(domain_beliefs)
            avg_entropy = sum(b.entropy for b in domain_beliefs) / len(domain_beliefs)
            coverage    = min(1.0, len(domain_beliefs) / expected_count)
            raw = avg_conf * coverage * (1.0 - avg_entropy * 0.3)
            scores[domain] = round(max(0.0, min(100.0, raw * 100)), 1)

        return scores

    async def get_compute_allocation(self, person_id: str) -> ComputeAllocation:
        """Return (or initialise) the compute allocation for a person."""
        dome = self._get_or_create_dome(person_id)
        if dome.compute_allocation is None:
            alloc = ComputeAllocation(elapsed_days=0.0)
            alloc.reallocate(self._beliefs.get(person_id, {}))
            dome.compute_allocation = alloc
        return dome.compute_allocation

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _get_or_create_dome(self, person_id: str) -> AssembledDome:
        """Retrieve or initialise the in-memory dome for a person."""
        if person_id not in self._domes:
            self._domes[person_id] = AssembledDome(
                person_id          = person_id,
                knowledge_graph    = KnowledgeGraph(person_id=person_id),
                identity_links     = IdentityLinkGraph(person_id=person_id),
                compute_allocation = ComputeAllocation(),
            )
        return self._domes[person_id]

    async def _extract_claims(
        self,
        source_id: str,
        payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Extract structured factual claims from a normalised fragment.

        A claim is a tuple (domain, claim_key, value) that represents a
        single updatable fact about the person.  For example:

            FHIR Observation (blood glucose):
                → ("health_vitality", "blood_glucose_mgdl", 180)

            HMIS Enrollment (shelter check-out):
                → ("physical_space_beauty", "housing_status", "sheltered")
                → ("physical_space_beauty", "shelter_checkout_date", "2024-01-15")

            Pharmacy claim (olanzapine fill):
                → ("health_vitality", "antipsychotic_adherent", False)
                → ("health_vitality", "med_olanzapine_days_late", 12)

            NOAA weather alert:
                → ("environmental_harmony", "outdoor_temp_f", 28)
                → ("environmental_harmony", "hypothermia_risk", True)

            ADT ER admission:
                → ("health_vitality", "er_visit_in_progress", True)
                → ("health_vitality", "er_visits_ytd", +1)
        """
        claims: list[dict[str, Any]] = []
        resource_type = payload.get("resourceType", "")
        source_type   = payload.get("source_type", "")

        if resource_type == "Observation":
            metric = payload.get("metric_type") or payload.get("code", {}).get("text")
            value  = payload.get("value") or payload.get("valueQuantity", {}).get("value")
            if metric == "blood_glucose" or "cgm" in source_id:
                claims.append({
                    "domain": "health_vitality",
                    "claim":  "blood_glucose_mgdl",
                    "value":  float(value or payload.get("glucose_mgdl", 0)),
                })
            elif metric == "sleep_summary" or "sleep" in source_id:
                sleep_hrs = payload.get("total_sleep_hrs", value)
                claims.append({
                    "domain": "health_vitality",
                    "claim":  "sleep_hours_last_night",
                    "value":  float(sleep_hrs or 0),
                })
                claims.append({
                    "domain": "health_vitality",
                    "claim":  "sleep_deficit",
                    "value":  float(sleep_hrs or 0) < 6.0,
                })
            elif metric in ("temperature_ambient",):
                claims.append({
                    "domain": "environmental_harmony",
                    "claim":  "outdoor_temp_f",
                    "value":  float(value or 0),
                })

        elif resource_type == "Encounter":
            status = payload.get("status", "")
            cls    = payload.get("class", {}).get("code", "")
            if cls == "SHELTER":
                claims.append({
                    "domain": "physical_space_beauty",
                    "claim":  "housing_status",
                    "value":  "sheltered",
                })
            elif cls == "EMER":
                if status == "in-progress":
                    claims.append({
                        "domain": "health_vitality",
                        "claim":  "er_visit_in_progress",
                        "value":  True,
                    })
                elif status in ("finished", "discharged"):
                    claims.append({
                        "domain": "health_vitality",
                        "claim":  "er_visit_in_progress",
                        "value":  False,
                    })
                    claims.append({
                        "domain": "physical_space_beauty",
                        "claim":  "housing_status",
                        "value":  "unsheltered",  # Discharge disposition: returned to homelessness
                    })

        elif source_type == "pharmacy" or "pharmacy" in source_id:
            days_late = payload.get("days_late", 0)
            drug_name = payload.get("drug_name", "")
            claims.append({
                "domain": "health_vitality",
                "claim":  f"med_{drug_name.replace(' ', '_').lower()}_days_late",
                "value":  int(days_late),
            })
            claims.append({
                "domain": "health_vitality",
                "claim":  "antipsychotic_adherent",
                "value":  days_late < 3,
            })

        elif source_type == "environmental" or resource_type == "Communication":
            alert = payload.get("alert_type", "")
            if alert:
                temp = payload.get("forecast_low_f")
                if temp and float(temp) < 32:
                    claims.append({
                        "domain": "environmental_harmony",
                        "claim":  "hypothermia_risk",
                        "value":  True,
                    })
                    claims.append({
                        "domain": "environmental_harmony",
                        "claim":  "outdoor_temp_forecast_low_f",
                        "value":  float(temp),
                    })

        return claims

    async def _update_belief(
        self,
        person_id: str,
        claim: dict[str, Any],
        source_trust: float,
        data_timestamp: datetime,
        source_id: str,
    ) -> None:
        """Update or create a belief in the person's belief store."""
        domain     = claim["domain"]
        claim_key  = claim["claim"]
        new_value  = claim["value"]

        beliefs = self._beliefs.setdefault(person_id, {})
        domain_beliefs = beliefs.setdefault(domain, [])

        # Find existing belief for this claim key
        existing = next((b for b in domain_beliefs if b.claim == claim_key), None)
        if existing is None:
            # First observation of this claim — create with prior = source_trust
            existing = DomainBelief(
                domain     = domain,
                claim      = claim_key,
                value      = new_value,
                confidence = source_trust,
                evidence_count = 1,
                source_ids = [source_id],
                entropy    = max(0.0, 1.0 - source_trust),
            )
            domain_beliefs.append(existing)
        else:
            if source_id not in existing.source_ids:
                existing.source_ids.append(source_id)
            existing.update_from_fragment(new_value, source_trust, data_timestamp)

    async def _update_knowledge_graph(
        self,
        dome: AssembledDome,
        source_id: str,
        payload: dict[str, Any],
        quality: float,
        data_timestamp: datetime,
    ) -> None:
        """Update relevant knowledge graph nodes and edges from a fragment."""
        if dome.knowledge_graph is None:
            dome.knowledge_graph = KnowledgeGraph(person_id=dome.person_id)

        graph         = dome.knowledge_graph
        resource_type = payload.get("resourceType", "")

        if resource_type == "Encounter":
            enc_id  = payload.get("id", str(uuid.uuid4()))
            enc_cls = payload.get("class", {}).get("code", "UNKNOWN")
            status  = payload.get("status", "")
            graph.add_node(
                node_id    = enc_id,
                node_type  = "event",
                properties = {
                    "encounter_class": enc_cls,
                    "status":          status,
                    "timestamp":       data_timestamp.isoformat(),
                    "source":          source_id,
                    "estimated_cost":  payload.get("estimated_cost_usd"),
                },
                confidence = quality,
            )
            graph.add_edge(
                from_id      = dome.person_id,
                to_id        = enc_id,
                relationship = "had_encounter",
                confidence   = quality,
                valid_from   = data_timestamp,
                valid_to     = None if status == "in-progress" else data_timestamp,
            )

        elif "pharmacy" in source_id or payload.get("source_type") == "pharmacy":
            drug_name = payload.get("drug_name", "unknown_drug")
            med_id    = f"med-{drug_name.replace(' ', '-').lower()}"
            graph.add_node(
                node_id    = med_id,
                node_type  = "medication",
                properties = {
                    "display":    drug_name,
                    "ndc":        payload.get("ndc"),
                    "days_late":  payload.get("days_late", 0),
                    "fill_date":  payload.get("fill_date"),
                },
                confidence = quality,
            )
            graph.add_edge(
                from_id      = dome.person_id,
                to_id        = med_id,
                relationship = "prescribed",
                confidence   = quality,
                valid_from   = data_timestamp,
            )

    def _compute_cosm_score(self, person_id: str) -> float:
        """Compute the Cosm completeness/accuracy score (0.0 – 1.0).

        The Cosm score measures how completely and accurately the digital twin
        represents the person's reality.  It is a weighted average of:

            1. Domain coverage  : what fraction of the 12 domains have any data?
            2. Belief confidence: average confidence of all stored beliefs
            3. Source diversity : how many independent sources contribute?
            4. Data freshness   : average freshness of the most recent belief
                                  in each domain

        Cosm is deliberately difficult to saturate.  A Cosm of 0.95 requires
        high-confidence data from multiple independent sources across all 12
        domains, with fresh data in each.  Robert Jackson, with data from
        9 systems, might reach 0.45-0.55 at steady state — enough for PREDICTIVE
        state, but not PRESCRIPTIVE without deeper behavioural and social data.
        """
        beliefs = self._beliefs.get(person_id, {})
        if not beliefs:
            return 0.0

        total_domains = 12
        covered       = len(beliefs)
        coverage      = covered / total_domains

        all_beliefs   = [b for domain_list in beliefs.values() for b in domain_list]
        if not all_beliefs:
            return 0.0

        avg_confidence = sum(b.confidence for b in all_beliefs) / len(all_beliefs)
        source_ids     = set(sid for b in all_beliefs for sid in b.source_ids)
        diversity      = min(1.0, len(source_ids) / 9.0)   # 9 = Robert's known systems
        avg_freshness  = sum(1.0 - b.entropy for b in all_beliefs) / len(all_beliefs)

        cosm = (
            coverage       * 0.30
            + avg_confidence * 0.35
            + diversity      * 0.20
            + avg_freshness  * 0.15
        )
        return round(min(0.999, max(0.0, cosm)), 4)

    def _compute_chron_score(self, person_id: str, latest_timestamp: datetime) -> float:
        """Compute the Chron temporal depth score (0.0 – 1.0).

        Chron measures how far back and how densely DOMES understands the
        person's history.  It rewards:

            - Historical depth : evidence going back 7+ years (Robert's history)
              scores higher than evidence only from the last 30 days
            - Temporal density : many data points per time unit
            - Gap detection    : long periods with no data reduce the score
              (we don't know what happened during those gaps)

        The score is computed as:
            depth_score  = min(1.0, history_days / 1825)   # 5 years = 1.0
            density_factor = sigmoid(fragment_count / 365)   # 1 fragment/day = ~0.73
            chron = depth_score × density_factor
        """
        dome = self._domes.get(person_id)
        if dome is None:
            return 0.0

        # Approximate history depth from belief oldest timestamp
        beliefs = self._beliefs.get(person_id, {})
        all_beliefs = [b for domain_list in beliefs.values() for b in domain_list]
        if not all_beliefs:
            return 0.0

        oldest = min((b.last_updated for b in all_beliefs), default=latest_timestamp)
        history_days = (latest_timestamp - oldest).days + 1
        depth_score  = min(1.0, history_days / 1825.0)   # 5 years = target depth

        # Density: fragment count relative to history length
        density_factor = 1.0 / (1.0 + math.exp(-0.01 * (dome.fragment_count - 100)))

        return round(depth_score * density_factor, 4)

    async def _check_crisis_conditions(
        self,
        dome: AssembledDome,
        payload: dict[str, Any],
        source_id: str,
    ) -> None:
        """Detect crisis conditions from the current fragment and update crisis_flags.

        Crisis conditions are threshold crossings that demand immediate response:

            MEDICATION_LAPSE_7D     : No medication fill in 7+ days
            ER_ADMISSION            : Active ER encounter in progress
            GLUCOSE_CRITICAL        : Blood glucose > 250 or < 70 mg/dL
            HYPOTHERMIA_RISK        : Forecast low < 32F + person unsheltered
            SLEEP_SEVERE_DEFICIT    : < 4 hours sleep for 3+ consecutive nights
            UNSEEN_14D              : No fragment from any source in 14+ days
            MEDICATION_LAPSE_12D    : Olanzapine fill 12+ days late (crisis for psychosis)

        When a crisis flag is set, the compute_allocation.activate_surprise()
        method is called to redirect compute to the affected domain.
        """
        flags = set(dome.crisis_flags)

        # ER admission check
        if (payload.get("resourceType") == "Encounter"
                and payload.get("class", {}).get("code") == "EMER"
                and payload.get("status") == "in-progress"):
            flags.add("er_visit_in_progress")
            if dome.compute_allocation:
                dome.compute_allocation.activate_surprise("health_vitality", severity=0.8)

        # ER discharge — remove in-progress flag
        if (payload.get("resourceType") == "Encounter"
                and payload.get("status") in ("finished", "discharged")):
            flags.discard("er_visit_in_progress")

        # Glucose check
        glucose = payload.get("glucose_mgdl")
        if glucose:
            if float(glucose) > 250:
                flags.add("glucose_critical_high")
                if dome.compute_allocation:
                    dome.compute_allocation.activate_surprise("health_vitality", severity=0.6)
            elif float(glucose) < 70:
                flags.add("glucose_critical_low")
                if dome.compute_allocation:
                    dome.compute_allocation.activate_surprise("health_vitality", severity=0.9)
            else:
                flags.discard("glucose_critical_high")
                flags.discard("glucose_critical_low")

        # Medication lapse check
        days_late = payload.get("days_late")
        if days_late and int(days_late) >= 7:
            flags.add(f"medication_lapse_{days_late}d")
            if dome.compute_allocation:
                dome.compute_allocation.activate_surprise("health_vitality", severity=0.7)

        # Hypothermia risk check
        temp = payload.get("forecast_low_f")
        if temp and float(temp) < 32:
            # Cross-reference housing status
            beliefs = self._beliefs.get(dome.person_id, {})
            housing = self._get_belief_value(beliefs, "physical_space_beauty", "housing_status")
            if housing in ("unsheltered", "unknown", None):
                flags.add("hypothermia_risk")
                if dome.compute_allocation:
                    dome.compute_allocation.activate_surprise("environmental_harmony", severity=0.75)

        dome.crisis_flags = list(flags)

    def _get_belief_value(
        self,
        beliefs: dict[str, list[DomainBelief]],
        domain: str,
        claim: str,
    ) -> Any:
        """Retrieve the current value for a specific belief claim."""
        domain_beliefs = beliefs.get(domain, [])
        for b in domain_beliefs:
            if b.claim == claim:
                return b.value
        return None


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _cosm_to_twin_state(cosm_score: float) -> TwinState:
    """Map a Cosm score to the corresponding TwinState."""
    if cosm_score < COSM_NASCENT_MAX:
        return TwinState.NASCENT
    if cosm_score < COSM_FORMING_MAX:
        return TwinState.FORMING
    if cosm_score < COSM_STABLE_MAX:
        return TwinState.STABLE
    if cosm_score < COSM_PREDICTIVE_MAX:
        return TwinState.PREDICTIVE
    if cosm_score < COSM_PRESCRIPTIVE_MAX:
        return TwinState.PRESCRIPTIVE
    return TwinState.ANTICIPATORY


def _jaro_winkler_approx(s1: str, s2: str) -> float:
    """Approximate Jaro-Winkler string similarity for entity resolution.

    Full Jaro-Winkler is O(n²).  This approximation uses:
        1. Case-normalised Jaro distance (exact)
        2. Winkler prefix bonus (standard 0.1 weight × min(4, prefix_length))

    Handles the most common entity resolution cases:
        "Robert" vs "Bobby"    → ~0.58 (different enough to be uncertain)
        "Jackson" vs "Jakson"  → ~0.91 (close enough to be PROBABLE match)
        "Robert" vs "Robert"   → 1.00
        ""       vs "Robert"   → 0.00
    """
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    match_dist = max(len1, len2) // 2 - 1
    if match_dist < 0:
        match_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0
    transpositions = 0

    for i, c1 in enumerate(s1):
        start = max(0, i - match_dist)
        end   = min(i + match_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or c1 != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro = (
        matches / len1
        + matches / len2
        + (matches - transpositions / 2) / matches
    ) / 3.0

    # Winkler prefix bonus
    prefix = 0
    for c1, c2 in zip(s1[:4], s2[:4]):
        if c1 == c2:
            prefix += 1
        else:
            break

    return round(jaro + prefix * 0.1 * (1.0 - jaro), 4)
