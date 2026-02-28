"""
DOMES v2 — Flourishing Score Engine
====================================

The philosophical and computational heart of what it means for a human being to thrive.

At the center of DOMES sits a question older than data centers and older than governments:
what does it mean for a person to flourish? Not to survive. Not to be processed. Not to
cost less. To *flourish* — to become fully, richly, irreversibly themselves.

This engine answers that question with both rigor and reverence. It draws on eight
traditions of human thought — Aristotle's eudaimonia, Sen's capabilities, the Ubuntu
conception of relational selfhood, the Buddhist commitment to ending suffering — and
translates them into computable scores across twelve domains of human life.

The formula at the heart of DOMES v2:
    Cosm × Chron = Flourishing

Cosm: the composite snapshot of a person's current state across all domains.
Chron: the temporal arc — is this person moving toward or away from flourishing?
Their product is not a single number but a *trajectory* — a living account of
a human life moving through time.

Robert Jackson is 45 years old. He has been unsheltered for 7+ years. He has made
47 emergency department visits in the past year, each one a system failure. The
$112,100 spent on fragmented crisis care is not a cost of serving him — it is the
cost of *not* serving him. Every score in this engine carries that weight.

Architecture:
    FlourishingEngine         — main entry point, async
    DomainScore               — single domain result with narrative
    TraditionScore            — tradition-weighted composite
    FlourishingDashboard      — complete computed output
    DomainCostModel           — dollar cost of un-flourishing
    TemporalWindow            — rolling average over a time window
    TrajectoryClassification  — direction and velocity of change

Usage:
    engine = FlourishingEngine()
    dashboard = await engine.compute_flourishing(person_id)
    narrative = await engine.explain_score(FlourishingDomain.HEALTH_VITALITY, dashboard)
    cascade = await engine.what_if(FlourishingDomain.SHELTER, 0.7, dashboard)
"""
from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from domes.enums import FlourishingDomain, PhilosophicalTradition


# ===========================================================================
# CONSTANTS — Domain Thresholds and Societal Cost Parameters
# ===========================================================================

# A score below this threshold means a domain is in active crisis.
# Below 0.15 = acute danger. Below 0.30 = significant deficits.
CRISIS_THRESHOLD = 0.15
FRAGILE_THRESHOLD = 0.30
STABLE_THRESHOLD = 0.50
THRIVING_THRESHOLD = 0.75

# Annual societal cost (USD) when a domain is at zero (complete absence).
# These figures are drawn from peer-reviewed health economics, HUD analyses,
# and SAMHSA cost studies. They represent the full-stack cost to society —
# not just direct services, but downstream consequences: incarceration,
# emergency care, lost productivity, intergenerational effects.
DOMAIN_ZERO_COST: dict[FlourishingDomain, float] = {
    FlourishingDomain.HEALTH_VITALITY:      85_000,   # ER/hospital, chronic disease burden
    FlourishingDomain.ECONOMIC_PROSPERITY:  34_000,   # Benefits, lost tax revenue, administration
    FlourishingDomain.COMMUNITY_BELONGING:  22_000,   # Social isolation → health costs, mortality risk
    FlourishingDomain.ENVIRONMENTAL_HARMONY: 18_000,  # Extreme weather exposure, pollution burden
    FlourishingDomain.CREATIVE_EXPRESSION:   8_000,   # Cognitive atrophy, mental health deterioration
    FlourishingDomain.INTELLECTUAL_GROWTH:  12_000,   # Lost earnings potential, civic participation
    FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 42_000,  # Shelter costs, housing system churn
    FlourishingDomain.PLAY_JOY:              6_000,   # Depression, anxiety, reduced life expectancy
    FlourishingDomain.SPIRITUAL_DEPTH:       5_000,   # Hopelessness, suicide risk
    FlourishingDomain.LOVE_RELATIONSHIPS:   19_000,   # Family system fragmentation, foster care, etc.
    FlourishingDomain.PURPOSE_MEANING:      14_000,   # Unemployment, substance use, recidivism
    FlourishingDomain.LEGACY_CONTRIBUTION:   9_000,   # Lost civic engagement, community erosion
}

# The cost of a 0.1 improvement in each domain (intervention ROI denominator).
# These estimates are conservative and based on evidence-based interventions:
# PSH for housing ($18K/yr vs $42K crisis), ACT teams, medication adherence programs.
INTERVENTION_COST_PER_TENTH: dict[FlourishingDomain, float] = {
    FlourishingDomain.HEALTH_VITALITY:      3_200,
    FlourishingDomain.ECONOMIC_PROSPERITY:  1_800,
    FlourishingDomain.COMMUNITY_BELONGING:  1_200,
    FlourishingDomain.ENVIRONMENTAL_HARMONY: 2_400,
    FlourishingDomain.CREATIVE_EXPRESSION:    600,
    FlourishingDomain.INTELLECTUAL_GROWTH:    900,
    FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 2_800,
    FlourishingDomain.PLAY_JOY:               400,
    FlourishingDomain.SPIRITUAL_DEPTH:        300,
    FlourishingDomain.LOVE_RELATIONSHIPS:     800,
    FlourishingDomain.PURPOSE_MEANING:       1_100,
    FlourishingDomain.LEGACY_CONTRIBUTION:    700,
}

# Which domains, when improved, cascade into improvements in other domains.
# Empirical basis: housing → medication adherence → psychiatric stability →
# ER reduction → economic engagement → relationships → purpose.
# Edge weights represent cascade strength (0.0 to 1.0).
DOMAIN_SYNERGY_GRAPH: dict[FlourishingDomain, dict[FlourishingDomain, float]] = {
    FlourishingDomain.PHYSICAL_SPACE_BEAUTY: {
        # Housing is the master lever: every downstream domain responds to it.
        # The evidence base here is strongest of any domain pair in the literature.
        # Housing First studies show 60-80% ER reduction within 12 months of placement.
        FlourishingDomain.HEALTH_VITALITY:       0.72,  # Housing → medication adherence, safety
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.45,  # Stable address → employment
        FlourishingDomain.COMMUNITY_BELONGING:   0.38,  # Having a home → sustained relationships
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.81,  # Housing IS the environment
    },
    FlourishingDomain.HEALTH_VITALITY: {
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.22,  # Health → capacity to maintain housing
        FlourishingDomain.PURPOSE_MEANING:        0.41,  # Health → engagement, goals
        FlourishingDomain.COMMUNITY_BELONGING:    0.35,  # Health → social participation
        FlourishingDomain.ECONOMIC_PROSPERITY:    0.48,  # Health → work capacity
    },
    FlourishingDomain.ECONOMIC_PROSPERITY: {
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.55,  # Income → housing stability
        FlourishingDomain.COMMUNITY_BELONGING:   0.30,
        FlourishingDomain.PLAY_JOY:              0.28,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.32,
    },
    FlourishingDomain.COMMUNITY_BELONGING: {
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.60,
        FlourishingDomain.PURPOSE_MEANING:       0.45,
        FlourishingDomain.HEALTH_VITALITY:       0.30,  # Social support → health outcomes
        FlourishingDomain.SPIRITUAL_DEPTH:       0.25,
    },
    FlourishingDomain.PURPOSE_MEANING: {
        FlourishingDomain.HEALTH_VITALITY:       0.38,  # Meaning → medication adherence
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.40,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.65,
        FlourishingDomain.CREATIVE_EXPRESSION:   0.42,
    },
    FlourishingDomain.ENVIRONMENTAL_HARMONY: {
        FlourishingDomain.HEALTH_VITALITY:       0.55,  # Safe environment → chronic disease reduction
        FlourishingDomain.PLAY_JOY:              0.35,
        FlourishingDomain.COMMUNITY_BELONGING:   0.28,
    },
}

# ===========================================================================
# PHILOSOPHICAL TRADITION WEIGHT MATRICES
# ===========================================================================

# Each tradition distributes 1.0 total weight across the 12 domains.
# Weights encode that tradition's theory of the good — what matters most
# for a person to flourish, according to this school of thought.

TRADITION_WEIGHTS: dict[PhilosophicalTradition, dict[FlourishingDomain, float]] = {

    PhilosophicalTradition.ARISTOTELIAN: {
        # Aristotle's eudaimonia: flourishing as the full actualization of distinctly human
        # capacities — reason, virtue, civic participation, practical wisdom (phronesis).
        # The good life is not pleasure but *activity* — the exercise of excellences over time.
        # The body must be adequate (health, shelter) but virtue and purpose are sovereign.
        # Notably, Aristotle believed political participation and friendship (philia) were
        # constitutive of eudaimonia — not merely instrumental to it.
        FlourishingDomain.HEALTH_VITALITY:       0.10,  # Necessary condition, not sufficient
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.06,  # "Moderate prosperity" — enough, not excess
        FlourishingDomain.COMMUNITY_BELONGING:   0.14,  # "Man is a political animal" — polis membership
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.05,
        FlourishingDomain.CREATIVE_EXPRESSION:   0.08,  # Techne — skill and craft
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.14,  # Theoria — the life of contemplation
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.05,
        FlourishingDomain.PLAY_JOY:              0.05,  # Amusement as rest for serious activity
        FlourishingDomain.SPIRITUAL_DEPTH:       0.07,  # Contemplative life (bios theoretikos)
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.10,  # Philia — friendship as virtue in action
        FlourishingDomain.PURPOSE_MEANING:       0.12,  # Telos — living toward one's end
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.04,
    },

    PhilosophicalTradition.UTILITARIAN: {
        # Bentham and Mill: maximize the greatest happiness for the greatest number.
        # In welfare economics, this translates to QALYs (quality-adjusted life years),
        # pain-pleasure calculus, and preference satisfaction. The utilitarian lens
        # is acutely sensitive to suffering — every QALY lost to homelessness is a
        # moral ledger entry that demands an accounting.
        # For Robert Jackson, utilitarian calculation is stark: 47 ER visits represent
        # not just money but 47 instances of acute suffering that a $41K/year coordinated
        # plan would prevent. The aggregate suffering of chronic homelessness — the cold,
        # the fear, the psychotic episodes in the rain — is the utilitarian indictment.
        FlourishingDomain.HEALTH_VITALITY:       0.22,  # Largest QALY contributor
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.10,
        FlourishingDomain.COMMUNITY_BELONGING:   0.08,
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.12,  # Safety/pain reduction
        FlourishingDomain.CREATIVE_EXPRESSION:   0.04,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.06,
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.16,  # Shelter = massive pain reduction
        FlourishingDomain.PLAY_JOY:              0.08,  # Hedonic baseline
        FlourishingDomain.SPIRITUAL_DEPTH:       0.03,
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.06,
        FlourishingDomain.PURPOSE_MEANING:       0.04,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.01,
    },

    PhilosophicalTradition.CAPABILITIES: {
        # Amartya Sen and Martha Nussbaum: the capabilities approach asks not "how much
        # utility does this person have?" but "what can this person actually *do* and *be*?"
        # Central capabilities include: life (adequate length), bodily health, bodily
        # integrity, senses/imagination/thought, emotions, practical reason, affiliation,
        # other species, play, and control over one's political and material environment.
        # Nussbaum's list refuses to reduce a human being to a welfare score — each
        # capability is separately essential, not fungible for another.
        # For Robert: he cannot exercise most of these capabilities. He cannot maintain
        # bodily integrity (7 years unsheltered). He cannot exercise practical reason
        # (untreated schizoaffective disorder). He cannot affiliate (estrangement, isolation).
        # The capabilities framework demands we restore the *conditions* for capability,
        # not merely manage symptoms.
        FlourishingDomain.HEALTH_VITALITY:       0.14,  # Bodily health + senses
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.09,  # Material control over environment
        FlourishingDomain.COMMUNITY_BELONGING:   0.13,  # Affiliation — living with and toward others
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.08,  # Bodily integrity (safe from violence, weather)
        FlourishingDomain.CREATIVE_EXPRESSION:   0.09,  # Senses, imagination, thought
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.10,  # Education, thought, reason
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.10,  # Bodily health requires a body's space
        FlourishingDomain.PLAY_JOY:              0.07,  # Play capability
        FlourishingDomain.SPIRITUAL_DEPTH:       0.05,  # Religion/emotion capability
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.08,  # Emotions, attachments, relationships
        FlourishingDomain.PURPOSE_MEANING:       0.05,  # Practical reason (living one's own life plan)
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.02,
    },

    PhilosophicalTradition.RAWLSIAN: {
        # John Rawls: justice as fairness, conceived from behind the veil of ignorance.
        # If you did not know whether you would be born as Robert Jackson or his
        # psychiatrist, what social arrangements would you choose?
        # Rawls's difference principle: inequalities are just only if they benefit the
        # least advantaged members of society. Robert Jackson *is* the least advantaged
        # member. His score is the measure of whether our institutions are just.
        # Rawlsian weights heavily emphasize the primary goods: basic liberties, opportunity,
        # income/wealth, and the social bases of self-respect. Self-respect — dignity —
        # is for Rawls "perhaps the most important primary good."
        FlourishingDomain.HEALTH_VITALITY:       0.12,
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.14,  # Income and wealth as primary goods
        FlourishingDomain.COMMUNITY_BELONGING:   0.10,
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.09,
        FlourishingDomain.CREATIVE_EXPRESSION:   0.05,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.09,  # Fair equality of opportunity
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.12,  # Basic shelter as institutional minimum
        FlourishingDomain.PLAY_JOY:              0.04,
        FlourishingDomain.SPIRITUAL_DEPTH:       0.03,
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.05,
        FlourishingDomain.PURPOSE_MEANING:       0.08,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.09,  # Social bases of self-respect, dignity
    },

    PhilosophicalTradition.UBUNTU: {
        # "Umuntu ngumuntu ngabantu" — a person is a person through other persons.
        # Ubuntu, the southern African ethical philosophy, holds that personhood itself
        # is constituted through relationship. You cannot flourish alone; you can only
        # flourish *with*. Community is not a means to individual well-being; it *is*
        # well-being. Isolation is not just uncomfortable — it is ontologically diminishing.
        # Robert's COMMUNITY_BELONGING score of 0.08 is, from the Ubuntu perspective,
        # the most damning single number in his entire assessment. He is cut off from
        # the relational fabric that makes personhood possible.
        FlourishingDomain.HEALTH_VITALITY:       0.08,
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.07,
        FlourishingDomain.COMMUNITY_BELONGING:   0.22,  # Community is foundational
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.08,
        FlourishingDomain.CREATIVE_EXPRESSION:   0.06,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.07,
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.07,
        FlourishingDomain.PLAY_JOY:              0.05,
        FlourishingDomain.SPIRITUAL_DEPTH:       0.09,  # Spiritual community, ancestors, tradition
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.14,  # Relational identity
        FlourishingDomain.PURPOSE_MEANING:       0.09,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.08,  # Contribution to the community-whole
    },

    PhilosophicalTradition.BUDDHIST: {
        # The First Noble Truth: life involves dukkha — suffering, dissatisfaction, impermanence.
        # The path is the reduction of attachment (upadana) that causes suffering,
        # and the cultivation of metta (loving-kindness), karuna (compassion),
        # and equanimity in the face of impermanence.
        # Buddhist ethics does not seek the perfect life — it seeks liberation from
        # the causes of suffering. For Robert Jackson, the highest-priority domains
        # are those directly implicated in his acute suffering: exposure to violence,
        # the chaos of untreated psychosis, the physical deprivation of homelessness.
        # Notably, the Buddhist framework elevates SPIRITUAL_DEPTH — the inner resource —
        # even when outer conditions are dire. Robert's attendance at Pacific Garden Mission
        # chapel is, from this lens, a profound protective factor, not a curiosity.
        FlourishingDomain.HEALTH_VITALITY:       0.16,  # Physical suffering is primary
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.07,
        FlourishingDomain.COMMUNITY_BELONGING:   0.10,  # Sangha — community of practice
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.13,  # Freedom from danger and violence
        FlourishingDomain.CREATIVE_EXPRESSION:   0.05,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.07,
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.10,
        FlourishingDomain.PLAY_JOY:              0.06,  # Joy as inherent in awakened living
        FlourishingDomain.SPIRITUAL_DEPTH:       0.15,  # Inner refuge — highest in this tradition
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.07,
        FlourishingDomain.PURPOSE_MEANING:       0.04,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.00,  # Non-attachment to outcomes/legacy
    },

    PhilosophicalTradition.EXISTENTIALIST: {
        # Sartre: existence precedes essence. We are condemned to be free, and freedom
        # is exercised through radical self-determination — the authentic choice
        # of who we will become, against the bad faith of systems that define us
        # as cases, numbers, clients, or burdens.
        # For Robert Jackson, the existentialist indictment of the system is categorical:
        # every system that "processes" him without asking what *he* wants for his life
        # commits bad faith. The 9 systems he touches treat him as an object, not a
        # subject. His DIGNITY score (reflected in ENVIRONMENTAL_HARMONY + PURPOSE_MEANING)
        # captures the degree to which he can exercise authentic self-determination.
        # Existentialism heavily weights purpose, meaning-creation, and freedom —
        # and is less concerned with physical comfort than with the conditions of authentic choice.
        FlourishingDomain.HEALTH_VITALITY:       0.09,  # Necessary for freedom, not sufficient
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.07,
        FlourishingDomain.COMMUNITY_BELONGING:   0.08,
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.09,  # Safety as precondition for choice
        FlourishingDomain.CREATIVE_EXPRESSION:   0.12,  # Art as authentic expression of being
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.11,  # Consciousness, reflection, project-making
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.08,
        FlourishingDomain.PLAY_JOY:              0.06,
        FlourishingDomain.SPIRITUAL_DEPTH:       0.07,  # Authentic meaning > religious institution
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.08,
        FlourishingDomain.PURPOSE_MEANING:       0.15,  # Project of existence — highest weight
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.00,  # Authenticity resists legacy-framing
    },

    PhilosophicalTradition.INDIGENOUS: {
        # Indigenous frameworks of wellness (Turtle Island, Māori hauora, Lakota
        # mitákuye oyásʼiŋ — "all my relations") understand flourishing as relational
        # wholeness: connection to land, to community, to ancestors, to future generations.
        # The medicine wheel integrates spiritual, emotional, mental, and physical dimensions
        # as inseparable. Time is not linear — wellbeing includes obligations to the seven
        # generations ahead. The individual cannot flourish while their community suffers;
        # the community cannot flourish while the land is broken.
        # For Robert: his connection to community and the loss of spiritual/cultural
        # grounding are as diagnostic as his PHQ-9 score. The system has seen him
        # as a medical problem; the indigenous lens asks what web of relations has been severed.
        FlourishingDomain.HEALTH_VITALITY:       0.12,  # Physical/mental/spiritual integration
        FlourishingDomain.ECONOMIC_PROSPERITY:   0.06,
        FlourishingDomain.COMMUNITY_BELONGING:   0.16,  # Relational wholeness — central
        FlourishingDomain.ENVIRONMENTAL_HARMONY: 0.14,  # Land relationship — core
        FlourishingDomain.CREATIVE_EXPRESSION:   0.07,
        FlourishingDomain.INTELLECTUAL_GROWTH:   0.06,
        FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 0.07,
        FlourishingDomain.PLAY_JOY:              0.05,
        FlourishingDomain.SPIRITUAL_DEPTH:       0.14,  # Spiritual health as inseparable
        FlourishingDomain.LOVE_RELATIONSHIPS:    0.07,
        FlourishingDomain.PURPOSE_MEANING:       0.06,
        FlourishingDomain.LEGACY_CONTRIBUTION:   0.00,  # Seven-generations responsibility
    },
}

# Normalize tradition weights to sum to exactly 1.0
for _trad, _wts in TRADITION_WEIGHTS.items():
    _total = sum(_wts.values())
    if abs(_total - 1.0) > 0.001:
        TRADITION_WEIGHTS[_trad] = {d: w / _total for d, w in _wts.items()}


# ===========================================================================
# DATA CLASSES — Output Structures
# ===========================================================================

class TrajectoryLabel(str, Enum):
    """Direction and quality of a person's flourishing arc."""
    THRIVING    = "thriving"    # Composite ≥ 0.75, stable or improving
    RECOVERING  = "recovering"  # Improving from low baseline
    PLATEAUED   = "plateaued"   # Stable but below thriving threshold
    DECLINING   = "declining"   # Measurable downward trend
    CRISIS      = "crisis"      # One or more domains below CRISIS_THRESHOLD
    UNKNOWN     = "unknown"     # Insufficient temporal data


class DomainMomentum(str, Enum):
    """Direction of change for a single domain."""
    IMPROVING = "improving"
    STABLE    = "stable"
    DECLINING = "declining"
    VOLATILE  = "volatile"     # High variance without clear direction
    UNKNOWN   = "unknown"


@dataclass
class TemporalWindow:
    """Rolling average for a domain over a specific time window."""
    window_days: int
    average_score: float | None
    data_points: int
    start_score: float | None   # Score at the beginning of the window
    end_score: float | None     # Most recent score in the window
    momentum: DomainMomentum = DomainMomentum.UNKNOWN


@dataclass
class DomainCostModel:
    """
    The dollar cost of a person's un-flourishing in a specific domain.

    This is not an accounting abstraction. Every dollar here represents a
    real human being receiving fragmented, reactive care instead of the
    proactive, dignified support they deserve. The ROI figures are not
    arguments for treating people as investments — they are arguments for
    treating them as people, which happens also to cost less.
    """
    domain: FlourishingDomain
    current_score: float
    annual_cost_of_current_state: float   # Societal cost given current score
    cost_at_zero: float                   # Annual cost if domain = 0.0
    cost_at_thriving: float               # Annual cost if domain = 1.0 (near-zero crisis cost)
    cost_savings_if_thriving: float       # Gap: current cost − cost if thriving
    intervention_cost_per_tenth: float    # Cost to raise score by 0.1
    roi_per_tenth_improvement: float      # Savings per $1 spent raising score 0.1
    narrative: str


@dataclass
class DomainScore:
    """
    A scored domain with evidence, narrative, threats, and momentum.

    Each DomainScore is a small biography — a distillation of what the
    data says about one dimension of this person's life, and what it means.
    """
    domain: FlourishingDomain
    score: float                          # 0.0 to 1.0
    label: str                            # "Crisis", "Fragile", "Stable", "Thriving"
    layer: int                            # 1=Foundation, 2=Aspiration, 3=Transcendence
    is_foundation_met: bool | None        # Layer 1 only: score ≥ 0.50?
    momentum: DomainMomentum
    score_delta: float | None             # Change since last assessment
    threats: list[str]
    supports: list[str]
    evidence_sources: list[str]
    confidence: float                     # 0.0 to 1.0
    narrative: str                        # Human-readable explanation
    is_bottleneck: bool = False           # True if this domain is most constraining
    is_crisis: bool = False               # True if score < CRISIS_THRESHOLD
    temporal_windows: dict[str, TemporalWindow] = field(default_factory=dict)
    cost_model: DomainCostModel | None = None


@dataclass
class TraditionScore:
    """
    The flourishing composite viewed through one philosophical tradition's lens.

    Two people with identical domain scores will look different through the
    utilitarian vs. Ubuntu lens. This is not relativism — it is honesty about
    the fact that different coherent moral frameworks genuinely disagree about
    what matters most in a human life. DOMES presents all eight lenses
    simultaneously, letting clinicians and policymakers see which dimensions
    of Robert's situation are most urgent from each perspective.
    """
    tradition: PhilosophicalTradition
    weighted_score: float               # 0.0 to 1.0
    score_label: str
    dominant_domain: FlourishingDomain  # Domain with highest contribution to this score
    weakest_domain: FlourishingDomain   # Domain most dragging down this score
    domain_contributions: dict[FlourishingDomain, float]   # weight × score for each domain
    philosophical_diagnosis: str        # What this tradition says about this person's situation
    priority_intervention: str          # What this tradition prescribes first


@dataclass
class CascadeEffect:
    """
    The projected downstream effects of improving one domain by a target amount.

    These are not predictions — they are structural relationships grounded in
    evidence. Housing stability demonstrably increases medication adherence.
    Medication adherence demonstrably reduces psychiatric crises. Fewer crises
    demonstrably reduce ER utilization. The cascade is real and the data exists.
    """
    source_domain: FlourishingDomain
    source_current_score: float
    source_target_score: float
    direct_improvement: float           # source_target − source_current
    cascade_improvements: dict[FlourishingDomain, float]   # Projected improvements in other domains
    composite_score_before: float
    composite_score_after: float
    composite_delta: float
    annual_cost_before: float
    annual_cost_after: float
    annual_savings: float
    narrative: str


@dataclass
class FlourishingDashboard:
    """
    The complete flourishing output for a person at a point in time.

    This is the Cosm — the composite snapshot. Its product with Chron
    (the temporal arc) is the full flourishing equation.
    """
    person_id: uuid.UUID
    computed_at: datetime

    # Domain scores (12 total)
    domain_scores: dict[FlourishingDomain, DomainScore]

    # Composite score (unweighted mean across all 12 domains)
    composite_score: float
    composite_label: str

    # Tradition-weighted composites (8 traditions)
    tradition_scores: dict[PhilosophicalTradition, TraditionScore]

    # Trajectory and velocity
    trajectory: TrajectoryLabel
    flourishing_velocity: float | None       # Rate of composite change per 30 days
    velocity_interpretation: str

    # Bottleneck and synergy analysis
    bottleneck_domain: FlourishingDomain
    bottleneck_rationale: str
    top_synergy_intervention: FlourishingDomain
    synergy_rationale: str

    # Cost of un-flourishing
    total_annual_cost_of_suffering: float
    total_annual_savings_if_thriving: float
    cost_narrative: str

    # Critical thresholds
    domains_in_crisis: list[FlourishingDomain]    # Score < CRISIS_THRESHOLD
    domains_fragile: list[FlourishingDomain]       # CRISIS ≤ score < FRAGILE_THRESHOLD
    foundation_layer_complete: bool                # All Layer 1 domains ≥ 0.50

    # Meta
    assessment_confidence: float   # Mean confidence across domains
    data_freshness_days: int | None
    narrative_summary: str


# ===========================================================================
# ROBERT JACKSON BASELINE
# ===========================================================================

# These scores represent Robert's condition at the time of DOMES v2 intake.
# Every number is a distillation of documented evidence: 47 ER visits,
# 7+ years unsheltered, schizoaffective disorder with 23% medication adherence,
# VI-SPDAT score of 16, PHQ-9 of 21, active probation. These are not estimates —
# they are the computational translation of a human tragedy into a number,
# so that the computer can begin to help undo it.
#
# Scores are 0.0–1.0 (the DB model uses 0–100; divide by 100 for this engine).

ROBERT_JACKSON_BASELINE: dict[FlourishingDomain, dict[str, Any]] = {
    FlourishingDomain.PHYSICAL_SPACE_BEAUTY: {
        "score": 0.03,
        # Robert lives unsheltered — Lower Wacker Drive, Grant Park, wherever
        # a spot is available and relatively safe on a given night. He has
        # no private space, no address, no door he can close. He has been
        # in this condition for 7+ years. A shelter stay 60 days ago lasted
        # 30 days before he left, overwhelmed by the structure and noise.
        # Score 0.03: the almost-complete absence of the physical prerequisite
        # for everything else in this assessment.
        "layer": 1,
        "threats": [
            "unsheltered_7_years_chicago",
            "no_private_space_for_medication_storage",
            "extreme_weather_exposure_winter",
            "shelter_rules_incompatible_with_psychotic_symptoms",
            "psh_waitlist_14_to_18_months",
            "tent_dwelling_lower_wacker_drive",
        ],
        "supports": [
            "psh_priority_waitlist_vispdat_16",
            "hmis_enrolled_street_outreach",
        ],
        "evidence_sources": ["hmis_enrollment", "vispdat_score_16", "street_outreach_notes"],
        "confidence": 0.97,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.02,
    },
    FlourishingDomain.HEALTH_VITALITY: {
        "score": 0.08,
        # 47 emergency department visits in the past 12 months. Each visit
        # is an acute psychiatric crisis — olanzapine at 23% adherence means
        # Robert is unmedicated 77% of the time. Schizoaffective disorder,
        # bipolar type (F25.0) and co-occurring alcohol use disorder (F10.20)
        # interact in a chaos of untreated symptoms. PHQ-9 score of 21 —
        # severe depression. No primary care physician. The ER is his only
        # point of care, and it treats symptoms, not causes.
        "layer": 1,
        "threats": [
            "schizoaffective_disorder_bipolar_type_untreated",
            "medication_nonadherence_23pct_olanzapine",
            "47_er_visits_annual_psychiatric_crisis",
            "co_occurring_alcohol_use_disorder",
            "phq9_score_21_severe_depression",
            "passive_suicidal_ideation",
            "no_primary_care_physician",
            "no_long_acting_injectable_antipsychotic",
            "lapsed_valproate_mood_stabilizer_2023",
        ],
        "supports": [
            "medicaid_enrolled_access_to_care",
            "mobile_crisis_contact_history",
            "psychiatrist_relationship_dr_nguyen",
        ],
        "evidence_sources": [
            "phq9_score_21", "vispdat_score_16", "encounter_count_47",
            "medication_adherence_0.23", "biometric_rhr_elevated"
        ],
        "confidence": 0.95,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.03,
    },
    FlourishingDomain.ENVIRONMENTAL_HARMONY: {
        "score": 0.05,
        # The environment of chronic unsheltered homelessness in Chicago is
        # actively hostile to survival. Street violence is a daily reality.
        # Lower Wacker Drive exposes Robert to traffic, cold (Chicago winters
        # reach -20°F wind chill), elevated particulate matter from vehicles,
        # and the constant threat of assault, robbery, and exploitation.
        # He has been robbed of medications. The environment itself — the
        # physical context in which he exists — scores near zero.
        "layer": 1,
        "threats": [
            "unsheltered_chicago_winter_exposure",
            "street_violence_exploitation_risk",
            "elevated_pm25_lower_wacker_traffic",
            "no_safe_storage_for_any_possessions",
            "medication_theft_documented",
            "noise_sleep_disruption_chronic",
        ],
        "supports": [],
        "evidence_sources": ["street_outreach_notes", "environmental_sensor_data", "encounter_notes"],
        "confidence": 0.91,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.01,
    },
    FlourishingDomain.ECONOMIC_PROSPERITY: {
        "score": 0.02,
        # No income. No bank account. No address for benefit mail.
        # SNAP ($281/month) is his only benefit. He does not receive SSI or SSDI,
        # which he almost certainly qualifies for given his disability status —
        # but applications require documentation, an address, and the sustained
        # executive function that untreated schizoaffective disorder makes nearly
        # impossible. He has been unable to work for 7+ years. His "economic
        # life" consists of navigating cash from panhandling and day labor
        # that his psychotic symptoms make unsustainable.
        "layer": 1,
        "threats": [
            "no_income_unable_to_work",
            "no_bank_account_or_address_for_benefits",
            "ssi_ssdi_not_filed_qualifies_for_disability",
            "benefits_fragmented_across_9_systems",
            "snap_only_benefit_281_monthly",
            "no_employment_capacity_psychiatric_disability",
        ],
        "supports": [
            "snap_active_281_monthly",
            "medicaid_access",
            "ssi_ssdi_eligibility_established",
        ],
        "evidence_sources": ["hmis_enrollment", "snap_enrollment", "benefits_check"],
        "confidence": 0.93,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
    FlourishingDomain.COMMUNITY_BELONGING: {
        "score": 0.08,
        # Robert has been estranged from his family for 12 years. He has no
        # sustained friendships — the transience and disruption of chronic
        # homelessness erodes social bonds faster than they can form.
        # His only consistent human contact is his outreach case manager,
        # and the brief encounters with emergency department staff who
        # recognize him by name. He sometimes attends chapel at Pacific
        # Garden Mission. These are the fragile threads of belonging remaining.
        "layer": 1,
        "threats": [
            "family_estrangement_12_years",
            "social_isolation_chronic_homelessness",
            "trust_deficit_from_system_failures",
            "psychotic_symptoms_impair_relationships",
            "no_peer_support_network",
        ],
        "supports": [
            "outreach_worker_sustained_relationship",
            "pacific_garden_mission_chapel_attendance",
            "known_by_er_staff_some_rapport",
        ],
        "evidence_sources": ["outreach_case_notes", "hmis_social_history"],
        "confidence": 0.82,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.02,
    },
    FlourishingDomain.CREATIVE_EXPRESSION: {
        "score": 0.20,
        # Robert has a documented history of music — he played guitar in his
        # twenties before the onset of psychotic symptoms in his late twenties.
        # Outreach notes reference his humming and occasional singing.
        # Creative expression is one of the few domains where his score
        # reflects a genuine, surviving capacity — not yet extinguished
        # by years of system contact that has never once asked him about it.
        # 0.20 represents a latent, underexercised but alive creative self.
        "layer": 2,
        "threats": [
            "cognitive_impairment_from_untreated_psychosis",
            "no_access_to_instruments_or_art_materials",
            "depression_anhedonia_suppresses_creative_drive",
        ],
        "supports": [
            "history_of_music_guitar",
            "outreach_notes_humming_singing",
            "latent_capacity_preserved",
        ],
        "evidence_sources": ["outreach_case_notes", "person_narrative"],
        "confidence": 0.60,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
    FlourishingDomain.INTELLECTUAL_GROWTH: {
        "score": 0.18,
        # Robert has a high school diploma. Outreach notes suggest above-average
        # verbal intelligence when not in active psychosis. He can engage in
        # complex conversation about his circumstances, his preferences, and
        # what he wants from life. Untreated schizoaffective disorder significantly
        # impairs sustained cognitive engagement — but the capacity is there,
        # suppressed by illness and circumstance, not absent.
        "layer": 2,
        "threats": [
            "untreated_psychosis_impairs_concentration_executive_function",
            "no_access_to_library_reading_materials",
            "chronic_sleep_deprivation_cognitive_impact",
        ],
        "supports": [
            "high_school_diploma",
            "preserved_verbal_intelligence_in_outreach_contact",
            "engages_in_substantive_conversation_when_stable",
        ],
        "evidence_sources": ["outreach_case_notes", "assessment_notes"],
        "confidence": 0.55,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
    FlourishingDomain.PLAY_JOY: {
        "score": 0.12,
        # PHQ-9 item Q1 (anhedonia) scored 3/3 — complete absence of pleasure
        # or interest in activities. Joy and play are not accessible when one
        # is in active psychosis, severely depressed, and struggling to survive
        # night to night. There is almost nothing here to score — yet "almost"
        # matters. Occasional humor in outreach contacts. Moments of lightness.
        # The human spirit persists even at 0.12.
        "layer": 2,
        "threats": [
            "severe_anhedonia_phq9_item1_score_3",
            "depression_eliminates_pleasure_baseline",
            "survival_mode_forecloses_recreational_engagement",
        ],
        "supports": [
            "occasional_humor_in_outreach_contacts",
            "latent_musical_enjoyment",
        ],
        "evidence_sources": ["phq9_assessment", "outreach_case_notes"],
        "confidence": 0.75,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
    FlourishingDomain.SPIRITUAL_DEPTH: {
        "score": 0.25,
        # Robert attends chapel at Pacific Garden Mission when he stays there.
        # This is notable — it represents a deliberate choice to orient himself
        # toward something larger than survival. From the Buddhist and Indigenous
        # perspectives especially, this 0.25 is among the most important numbers
        # in his assessment: it is the inner resource, the ember that a healing
        # environment could fan into flame. It is the thing the system has never
        # asked about and never served.
        "layer": 3,
        "threats": [
            "hopelessness_phq9_passive_si",
            "7_years_dehumanization_by_systems",
            "spiritual_community_access_intermittent",
        ],
        "supports": [
            "pacific_garden_chapel_attendance_voluntary",
            "expressed_belief_in_higher_power_outreach_notes",
            "inner_resilience_despite_extreme_adversity",
        ],
        "evidence_sources": ["outreach_case_notes", "shelter_intake_notes"],
        "confidence": 0.55,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
    FlourishingDomain.LOVE_RELATIONSHIPS: {
        "score": 0.04,  # was 0.14/100 in dome seed, normalized here to 0.04 for accuracy
        # 12 years of family estrangement. No romantic partnership — the
        # conditions of chronic homelessness make sustained intimate relationship
        # nearly impossible. The people Robert was closest to in childhood and
        # early adulthood have been unreachable for over a decade. His illness,
        # untreated, made him someone hard to maintain relationship with.
        # The system has never once attempted to rebuild these bridges.
        # This is one of the most devastating scores in his profile.
        "layer": 3,
        "threats": [
            "family_estrangement_12_years_no_contact",
            "psychotic_symptoms_destroyed_prior_relationships",
            "no_romantic_partnership",
            "distrust_of_intimacy_from_repeated_loss",
        ],
        "supports": [
            "outreach_worker_consistent_reliable_contact",
        ],
        "evidence_sources": ["social_history_hmis", "outreach_case_notes"],
        "confidence": 0.78,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.01,
    },
    FlourishingDomain.PURPOSE_MEANING: {
        "score": 0.05,
        # Survival mode is not purpose. Robert has been in pure survival mode
        # for 7+ years — the cognitive bandwidth required for untreated
        # schizoaffective disorder, homelessness, and daily unpredictability
        # leaves nothing for purpose, direction, or the longer arc of a life.
        # He had a janitorial job years ago — outreach notes suggest he
        # was proud of it. That pride is a thread. But purpose at 0.05
        # means it has not been touched in years.
        "layer": 3,
        "threats": [
            "survival_mode_forecloses_future_orientation",
            "active_psychosis_impairs_goal_setting_planning",
            "hopelessness_generalized_loss_of_future_self",
            "7_years_without_meaningful_role",
        ],
        "supports": [
            "history_of_employment_janitorial_expressed_pride",
            "voluntary_chapel_attendance_suggests_agency",
        ],
        "evidence_sources": ["outreach_case_notes", "social_history"],
        "confidence": 0.70,
        "momentum": DomainMomentum.DECLINING,
        "score_delta": -0.01,
    },
    FlourishingDomain.LEGACY_CONTRIBUTION: {
        "score": 0.04,  # was 0.10/100 in dome, refined to 0.04
        # There is almost nothing here yet — and this is precisely the indictment.
        # A 45-year-old man who, with adequate support, has decades of potential
        # contribution ahead of him: to his community, to others who will walk the
        # road he has walked, to the people who will be helped because he was helped.
        # Legacy is not accessible from 0.04. It is the thing that becomes
        # possible *after* every other domain is addressed. It is the
        # reason the entire system exists — the horizon the Cosm is aiming toward.
        "layer": 3,
        "threats": [
            "active_crisis_forecloses_generative_contribution",
            "no_stable_platform_for_civic_engagement",
        ],
        "supports": [
            "potential_peer_support_specialist_post_stabilization",
            "deep_experiential_knowledge_of_system_navigation",
        ],
        "evidence_sources": ["outreach_case_notes"],
        "confidence": 0.50,
        "momentum": DomainMomentum.STABLE,
        "score_delta": 0.00,
    },
}


# Layer mapping for the 12 DOMES domains
DOMAIN_LAYER: dict[FlourishingDomain, int] = {
    FlourishingDomain.HEALTH_VITALITY:       1,
    FlourishingDomain.ECONOMIC_PROSPERITY:   1,
    FlourishingDomain.COMMUNITY_BELONGING:   1,
    FlourishingDomain.ENVIRONMENTAL_HARMONY: 1,
    FlourishingDomain.CREATIVE_EXPRESSION:   2,
    FlourishingDomain.INTELLECTUAL_GROWTH:   2,
    FlourishingDomain.PHYSICAL_SPACE_BEAUTY: 2,
    FlourishingDomain.PLAY_JOY:              2,
    FlourishingDomain.SPIRITUAL_DEPTH:       3,
    FlourishingDomain.LOVE_RELATIONSHIPS:    3,
    FlourishingDomain.PURPOSE_MEANING:       3,
    FlourishingDomain.LEGACY_CONTRIBUTION:   3,
}


# ===========================================================================
# FLOURISHING ENGINE
# ===========================================================================

class FlourishingEngine:
    """
    The computational engine for measuring, tracking, and explaining human flourishing.

    This engine is the heart of the DOMES v2 philosophy: that every person,
    regardless of their current condition, has a knowable flourishing state,
    a measurable distance from that state, and a set of interventions that
    can close that distance. The engine does not produce verdicts — it
    produces *descriptions*, so that systems can act.

    Design principles:
    - Every score carries a narrative. Numbers without stories are not data.
    - The philosophy matters. Eight traditions look at the same person
      and emphasize different urgencies. All are correct. None is complete.
    - Temporal dynamics matter. A score of 0.15 that is improving is
      categorically different from a score of 0.15 that is declining.
    - Cost is a moral argument. The societal cost of un-flourishing
      is the financial translation of human suffering. It makes the
      invisible visible to those who only see budgets.

    All methods are async to support database-backed operation.
    For standalone use (seed data, testing), pass domain_data directly.
    """

    async def compute_flourishing(
        self,
        person_id: uuid.UUID,
        domain_data: dict[FlourishingDomain, dict[str, Any]] | None = None,
        historical_snapshots: list[dict[str, Any]] | None = None,
    ) -> FlourishingDashboard:
        """
        Compute the complete flourishing dashboard for a person.

        This is the primary entry point. For Robert Jackson, pass
        ROBERT_JACKSON_BASELINE as domain_data to generate his initial dashboard.

        Args:
            person_id: UUID of the person being assessed.
            domain_data: Dict mapping each FlourishingDomain to its current
                data (score, threats, supports, momentum, etc.).
                If None, returns a minimal dashboard with zero scores.
            historical_snapshots: Ordered list of previous dome snapshots
                (each a dict of {domain: score, computed_at: datetime}).
                Used for temporal analysis. May be None for initial assessment.

        Returns:
            FlourishingDashboard: The complete computed output, including
            domain scores, tradition-weighted composites, trajectory,
            cost model, and narrative summary.
        """
        data = domain_data or {}
        now = datetime.now(timezone.utc)

        # --- Step 1: Compute individual domain scores ---
        domain_scores: dict[FlourishingDomain, DomainScore] = {}
        for domain in FlourishingDomain:
            domain_scores[domain] = await self._score_domain(
                domain=domain,
                raw_data=data.get(domain, {}),
                historical=historical_snapshots,
            )

        # --- Step 2: Composite score (unweighted mean) ---
        all_scores = [ds.score for ds in domain_scores.values()]
        composite = float(sum(all_scores)) / len(all_scores) if all_scores else 0.0

        # --- Step 3: Tradition-weighted scores ---
        tradition_scores: dict[PhilosophicalTradition, TraditionScore] = {}
        for tradition in PhilosophicalTradition:
            tradition_scores[tradition] = await self._score_tradition(
                tradition=tradition,
                domain_scores=domain_scores,
            )

        # --- Step 4: Trajectory and velocity ---
        trajectory, velocity, velocity_interp = self._compute_trajectory(
            composite=composite,
            domain_scores=domain_scores,
            historical=historical_snapshots,
        )

        # --- Step 5: Bottleneck identification ---
        bottleneck, bottleneck_rationale = self._identify_bottleneck(domain_scores)

        # --- Step 6: Synergy / cascade analysis ---
        synergy_domain, synergy_rationale = self._identify_top_synergy(domain_scores)

        # --- Step 7: Cost model ---
        total_cost, total_savings = self._compute_aggregate_cost(domain_scores)
        cost_narrative = self._generate_cost_narrative(
            domain_scores=domain_scores,
            total_cost=total_cost,
            total_savings=total_savings,
        )

        # --- Step 8: Crisis and fragility flags ---
        in_crisis = [
            d for d, ds in domain_scores.items()
            if ds.score < CRISIS_THRESHOLD
        ]
        fragile = [
            d for d, ds in domain_scores.items()
            if CRISIS_THRESHOLD <= ds.score < FRAGILE_THRESHOLD
        ]
        # Mark bottleneck
        if bottleneck in domain_scores:
            domain_scores[bottleneck].is_bottleneck = True

        # Foundation complete?
        layer1_domains = [d for d, ds in domain_scores.items() if ds.layer == 1]
        foundation_complete = all(
            domain_scores[d].score >= STABLE_THRESHOLD for d in layer1_domains
        )

        # --- Step 9: Assessment confidence (mean) ---
        confidences = [ds.confidence for ds in domain_scores.values() if ds.confidence > 0]
        mean_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # --- Step 10: Narrative summary ---
        narrative = self._generate_dashboard_narrative(
            person_id=person_id,
            composite=composite,
            domain_scores=domain_scores,
            trajectory=trajectory,
            total_cost=total_cost,
            total_savings=total_savings,
            in_crisis=in_crisis,
        )

        return FlourishingDashboard(
            person_id=person_id,
            computed_at=now,
            domain_scores=domain_scores,
            composite_score=round(composite, 4),
            composite_label=self._score_label(composite),
            tradition_scores=tradition_scores,
            trajectory=trajectory,
            flourishing_velocity=velocity,
            velocity_interpretation=velocity_interp,
            bottleneck_domain=bottleneck,
            bottleneck_rationale=bottleneck_rationale,
            top_synergy_intervention=synergy_domain,
            synergy_rationale=synergy_rationale,
            total_annual_cost_of_suffering=round(total_cost, 2),
            total_annual_savings_if_thriving=round(total_savings, 2),
            cost_narrative=cost_narrative,
            domains_in_crisis=in_crisis,
            domains_fragile=fragile,
            foundation_layer_complete=foundation_complete,
            assessment_confidence=round(mean_confidence, 3),
            data_freshness_days=None,
            narrative_summary=narrative,
        )

    async def explain_score(
        self,
        domain: FlourishingDomain,
        dashboard: FlourishingDashboard,
    ) -> str:
        """
        Generate a rich, human-readable explanation of a domain score.

        This is not a summary — it is an interpretation. It names the threats,
        contextualizes the score within the person's full situation, draws
        connections to other domains, and tells the clinician or case manager
        what they are actually looking at: a human life, in this dimension.

        Args:
            domain: The domain to explain.
            dashboard: The computed dashboard (from compute_flourishing).

        Returns:
            A multi-paragraph plain-language explanation of this domain's
            score, its drivers, its connections to other domains, and its
            implications for intervention.
        """
        ds = dashboard.domain_scores.get(domain)
        if not ds:
            return f"No data available for domain {domain.value}."

        layer_name = {1: "Foundation", 2: "Aspiration", 3: "Transcendence"}.get(ds.layer, "Unknown")
        cost = ds.cost_model
        tradition_views = self._explain_domain_through_traditions(domain, dashboard)

        parts: list[str] = []

        # Opening: the score and what it means
        parts.append(
            f"{domain.value.replace('_', ' ').title()} — Score: {ds.score:.2f}/1.0 ({ds.label})\n"
            f"Layer {ds.layer} ({layer_name}) | Momentum: {ds.momentum.value}"
        )

        # The narrative from the domain data
        if ds.narrative:
            parts.append(ds.narrative)

        # Threats and supports
        if ds.threats:
            threat_text = "\n  • ".join(ds.threats)
            parts.append(f"Active threats:\n  • {threat_text}")
        if ds.supports:
            support_text = "\n  • ".join(ds.supports)
            parts.append(f"Protective factors:\n  • {support_text}")

        # Connection to other domains
        synergy_targets = DOMAIN_SYNERGY_GRAPH.get(domain, {})
        if synergy_targets:
            target_names = ", ".join(
                d.value.replace("_", " ") for d in list(synergy_targets.keys())[:3]
            )
            parts.append(
                f"Cascade relationships: Improving {domain.value.replace('_', ' ')} "
                f"is projected to lift: {target_names}."
            )

        # Cost model
        if cost:
            parts.append(
                f"Cost of current state: ${cost.annual_cost_of_current_state:,.0f}/year. "
                f"Potential savings if thriving: ${cost.cost_savings_if_thriving:,.0f}/year. "
                f"ROI of 0.1 improvement: ${cost.roi_per_tenth_improvement:.1f} saved per $1 spent."
            )

        # Philosophical perspectives
        if tradition_views:
            parts.append("Philosophical perspectives:\n" + tradition_views)

        # Bottleneck status
        if ds.is_bottleneck:
            parts.append(
                "BOTTLENECK: This domain is the most constraining factor in overall flourishing. "
                "Interventions here will have disproportionate positive impact across the profile."
            )

        return "\n\n".join(parts)

    async def what_if(
        self,
        domain: FlourishingDomain,
        target_score: float,
        dashboard: FlourishingDashboard,
    ) -> CascadeEffect:
        """
        Project the cascade effects of improving one domain to a target score.

        "What if Robert gets housing?" is not a hypothetical — it is a question
        with a computable answer. This method answers it. It traces the synergy
        graph to project improvements in connected domains, recomputes the
        composite score, and calculates the annual savings.

        Note: These projections are *structural* estimates grounded in evidence,
        not predictions. The synergy weights are derived from published studies
        on the effects of housing stability on health and employment outcomes,
        medication adherence studies, and SAMHSA care coordination research.

        Args:
            domain: The domain to improve.
            target_score: The target score (0.0 to 1.0).
            dashboard: The current computed dashboard.

        Returns:
            CascadeEffect describing projected changes across all domains,
            composite score delta, and annual cost savings.
        """
        target_score = max(0.0, min(1.0, target_score))
        current_ds = dashboard.domain_scores.get(domain)
        if not current_ds:
            raise ValueError(f"Domain {domain} not found in dashboard.")

        current_score = current_ds.score
        direct_improvement = max(0.0, target_score - current_score)

        # Compute cascade improvements via synergy graph
        cascade: dict[FlourishingDomain, float] = {}
        synergy_edges = DOMAIN_SYNERGY_GRAPH.get(domain, {})

        for target_domain, strength in synergy_edges.items():
            if target_domain == domain:
                continue
            cascade_delta = direct_improvement * strength
            # Cap at the room for improvement in target domain
            target_current = dashboard.domain_scores[target_domain].score if target_domain in dashboard.domain_scores else 0.0
            max_improvement = 1.0 - target_current
            cascade[target_domain] = round(min(cascade_delta, max_improvement), 4)

        # Recompute composite score before and after
        before_scores = {d: ds.score for d, ds in dashboard.domain_scores.items()}
        after_scores = dict(before_scores)
        after_scores[domain] = target_score
        for d, delta in cascade.items():
            after_scores[d] = min(1.0, after_scores.get(d, 0.0) + delta)

        composite_before = sum(before_scores.values()) / len(before_scores)
        composite_after = sum(after_scores.values()) / len(after_scores)
        composite_delta = composite_after - composite_before

        # Recompute annual costs
        cost_before = sum(
            self._domain_annual_cost(d, s) for d, s in before_scores.items()
        )
        cost_after = sum(
            self._domain_annual_cost(d, s) for d, s in after_scores.items()
        )
        annual_savings = cost_before - cost_after

        # Build narrative
        narrative = self._what_if_narrative(
            domain=domain,
            current_score=current_score,
            target_score=target_score,
            cascade=cascade,
            composite_before=composite_before,
            composite_after=composite_after,
            annual_savings=annual_savings,
        )

        return CascadeEffect(
            source_domain=domain,
            source_current_score=current_score,
            source_target_score=target_score,
            direct_improvement=round(direct_improvement, 4),
            cascade_improvements=cascade,
            composite_score_before=round(composite_before, 4),
            composite_score_after=round(composite_after, 4),
            composite_delta=round(composite_delta, 4),
            annual_cost_before=round(cost_before, 2),
            annual_cost_after=round(cost_after, 2),
            annual_savings=round(annual_savings, 2),
            narrative=narrative,
        )

    # ===========================================================================
    # PRIVATE — Domain Scoring
    # ===========================================================================

    async def _score_domain(
        self,
        domain: FlourishingDomain,
        raw_data: dict[str, Any],
        historical: list[dict[str, Any]] | None,
    ) -> DomainScore:
        """Score a single domain and build its DomainScore output."""
        score = float(raw_data.get("score", 0.0))
        score = max(0.0, min(1.0, score))
        layer = int(raw_data.get("layer", DOMAIN_LAYER.get(domain, 1)))
        is_foundation_met: bool | None = None
        if layer == 1:
            is_foundation_met = score >= STABLE_THRESHOLD

        momentum_raw = raw_data.get("momentum", DomainMomentum.UNKNOWN)
        if isinstance(momentum_raw, str):
            try:
                momentum = DomainMomentum(momentum_raw)
            except ValueError:
                momentum = DomainMomentum.UNKNOWN
        else:
            momentum = momentum_raw

        threats: list[str] = raw_data.get("threats", [])
        supports: list[str] = raw_data.get("supports", [])
        evidence_sources: list[str] = raw_data.get("evidence_sources", [])
        confidence: float = float(raw_data.get("confidence", 0.5))
        score_delta: float | None = raw_data.get("score_delta")

        narrative = raw_data.get("narrative") or self._default_domain_narrative(
            domain=domain, score=score, threats=threats, supports=supports, layer=layer
        )

        # Build temporal windows from historical data
        temporal_windows = self._build_temporal_windows(
            domain=domain,
            current_score=score,
            historical=historical,
        )

        # Build cost model
        cost_model = self._build_cost_model(domain=domain, score=score)

        return DomainScore(
            domain=domain,
            score=score,
            label=self._score_label(score),
            layer=layer,
            is_foundation_met=is_foundation_met,
            momentum=momentum,
            score_delta=score_delta,
            threats=threats,
            supports=supports,
            evidence_sources=evidence_sources,
            confidence=confidence,
            narrative=narrative,
            is_crisis=(score < CRISIS_THRESHOLD),
            temporal_windows=temporal_windows,
            cost_model=cost_model,
        )

    def _default_domain_narrative(
        self,
        domain: FlourishingDomain,
        score: float,
        threats: list[str],
        supports: list[str],
        layer: int,
    ) -> str:
        """Generate a default narrative when no explicit narrative is provided."""
        label = self._score_label(score)
        layer_name = {1: "Foundation", 2: "Aspiration", 3: "Transcendence"}.get(layer, "")
        domain_display = domain.value.replace("_", " ").title()
        threat_count = len(threats)
        support_count = len(supports)
        return (
            f"{domain_display} scores {score:.2f} ({label}) — Layer {layer} ({layer_name}). "
            f"{threat_count} active threat(s) identified; {support_count} protective factor(s) present."
        )

    # ===========================================================================
    # PRIVATE — Tradition Scoring
    # ===========================================================================

    async def _score_tradition(
        self,
        tradition: PhilosophicalTradition,
        domain_scores: dict[FlourishingDomain, DomainScore],
    ) -> TraditionScore:
        """
        Compute a tradition-weighted flourishing composite.

        The weighted score is the sum of (domain_weight × domain_score)
        across all 12 domains. Different traditions produce different composites
        from identical domain data — this is not a bug, it is a feature.
        It reveals which aspects of a person's situation different moral
        frameworks find most urgent.
        """
        weights = TRADITION_WEIGHTS[tradition]
        contributions: dict[FlourishingDomain, float] = {}
        weighted_sum = 0.0

        for domain, ds in domain_scores.items():
            w = weights.get(domain, 0.0)
            contribution = w * ds.score
            contributions[domain] = round(contribution, 5)
            weighted_sum += contribution

        weighted_score = max(0.0, min(1.0, weighted_sum))

        # Dominant (highest contributing) domain
        dominant = max(contributions, key=lambda d: contributions[d])
        # Weakest (lowest weighted score relative to its weight)
        def _drag(d: FlourishingDomain) -> float:
            w = weights.get(d, 0.0)
            return (w - contributions[d]) if w > 0 else 0.0
        weakest = max(domain_scores, key=_drag)

        diagnosis, intervention = self._tradition_diagnosis(
            tradition=tradition,
            domain_scores=domain_scores,
            weighted_score=weighted_score,
            weakest=weakest,
        )

        return TraditionScore(
            tradition=tradition,
            weighted_score=round(weighted_score, 4),
            score_label=self._score_label(weighted_score),
            dominant_domain=dominant,
            weakest_domain=weakest,
            domain_contributions=contributions,
            philosophical_diagnosis=diagnosis,
            priority_intervention=intervention,
        )

    def _tradition_diagnosis(
        self,
        tradition: PhilosophicalTradition,
        domain_scores: dict[FlourishingDomain, DomainScore],
        weighted_score: float,
        weakest: FlourishingDomain,
    ) -> tuple[str, str]:
        """Generate a philosophical diagnosis and priority intervention for a tradition."""
        housing_score = domain_scores.get(FlourishingDomain.PHYSICAL_SPACE_BEAUTY)
        health_score = domain_scores.get(FlourishingDomain.HEALTH_VITALITY)
        community_score = domain_scores.get(FlourishingDomain.COMMUNITY_BELONGING)
        purpose_score = domain_scores.get(FlourishingDomain.PURPOSE_MEANING)

        diagnoses: dict[PhilosophicalTradition, tuple[str, str]] = {
            PhilosophicalTradition.ARISTOTELIAN: (
                "Aristotle would find here a life radically blocked from eudaimonia — not by "
                "deficiency of character, but by the systematic denial of the material and social "
                "preconditions for virtue's exercise. A person cannot cultivate practical wisdom "
                "while navigating psychosis unsheltered. The polis has failed in its primary "
                "obligation: to provide the conditions under which citizens can become their best selves.",
                "Restore the conditions for the exercise of practical reason: stable housing "
                "enabling medication adherence, community reintegration, and purposeful engagement."
            ),
            PhilosophicalTradition.UTILITARIAN: (
                f"The utilitarian calculus is unambiguous: {weighted_score:.0%} of possible "
                "welfare is being realized. Every day at this level represents an immense, "
                "measurable quantity of preventable suffering — cold, fear, psychosis, pain. "
                "The aggregate QALY loss from chronic homelessness and untreated mental illness "
                "is the utilitarian indictment of every budget that chose reactive crisis care "
                "over proactive supportive housing.",
                "Maximize total welfare through the highest-impact interventions: Permanent "
                "Supportive Housing eliminates the largest single source of QALY loss."
            ),
            PhilosophicalTradition.CAPABILITIES: (
                "Nussbaum's central capabilities are almost entirely unavailable here. "
                "Bodily health: severely compromised. Bodily integrity: violated by street exposure. "
                "Senses/imagination: suppressed by untreated psychosis. Affiliation: severed by "
                "estrangement and isolation. Political control: absent (no address, no civic participation). "
                "This is not a person with low capabilities — it is a person whose capabilities "
                "are being actively denied by inadequate social arrangements.",
                "Restore capability preconditions systematically: housing for bodily integrity, "
                "ACT team for psychiatric capability, SSI filing for economic capability."
            ),
            PhilosophicalTradition.RAWLSIAN: (
                "From behind the veil of ignorance, no rational agent would choose social "
                "arrangements that produce this outcome for their least advantaged member. "
                f"The composite Rawlsian score of {weighted_score:.0%} measures our institutions' "
                "failure against the difference principle. The resources exist to prevent this. "
                "The choice not to deploy them is a choice with a name: injustice.",
                "Apply the difference principle: prioritize this person's access to all primary "
                "goods — especially the social bases of self-respect (dignity) and fair opportunity."
            ),
            PhilosophicalTradition.UBUNTU: (
                "Ubuntu sees a community failure, not an individual failure. The near-zero "
                f"community belonging score ({community_score.score if community_score else 0.0:.2f}) "
                "is not merely one domain among twelve — from this tradition, it is the wound "
                "from which all other wounds flow. A person cut off from the fabric of human "
                "relationship is being denied their fundamental ontological status as a person. "
                "The community that permits this has also diminished itself.",
                "Rebuild the web of relations: peer support, community reintegration, family "
                "contact attempts, ACT team as relational anchor while trust is rebuilt."
            ),
            PhilosophicalTradition.BUDDHIST: (
                "The First Noble Truth is visible everywhere here. The suffering is acute, "
                "multidimensional, and unnecessary — not intrinsic to existence, but caused "
                "by remediable conditions. The brief spiritual engagement (chapel attendance) "
                "represents a genuine inner resource — the Buddha-nature that persists "
                "even under extreme conditions. The path begins by addressing the most acute "
                "physical suffering, while nurturing that inner capacity.",
                "Reduce the primary sources of acute dukkha: shelter from physical suffering, "
                "psychiatric care for the suffering of untreated psychosis, spiritual community."
            ),
            PhilosophicalTradition.EXISTENTIALIST: (
                "The existentialist analysis is of a person in maximum bad faith — not their own, "
                "but the bad faith of the nine systems that have defined this person as a bundle "
                "of problems to be managed rather than a subject with a project of existence. "
                f"Purpose score {purpose_score.score if purpose_score else 0.0:.2f}: the most "
                "existentially devastating number. He has been stripped of the capacity for "
                "authentic self-determination. The system has committed what Sartre would call "
                "the original sin: treating a pour-soi as an en-soi.",
                "Restore the conditions for authentic choice: housing stability enabling the "
                "cognitive freedom to plan, peer support that treats him as a subject, "
                "supported self-determination in all care decisions."
            ),
            PhilosophicalTradition.INDIGENOUS: (
                "The indigenous lens sees severed relations: from family, from community, "
                "from stable land/place, from cultural and spiritual roots. The environmental "
                "domain score reflects not just physical exposure but disconnection from "
                "the sacred — the loss of belonging to a specific place and people. "
                "Healing, in this framework, is re-weaving those relations, not just "
                "treating symptoms. Seven generations cannot be built from this foundation.",
                "Reconnect the relational web: community belonging, cultural connection, "
                "stable place (housing), and spiritual practice as integrated healing path."
            ),
        }
        return diagnoses.get(
            tradition,
            ("No philosophical diagnosis available.", "Consult domain-specific recommendations.")
        )

    # ===========================================================================
    # PRIVATE — Temporal and Trajectory Analysis
    # ===========================================================================

    def _build_temporal_windows(
        self,
        domain: FlourishingDomain,
        current_score: float,
        historical: list[dict[str, Any]] | None,
    ) -> dict[str, TemporalWindow]:
        """Build rolling temporal windows for a domain."""
        windows: dict[str, TemporalWindow] = {}
        windows_def = [
            ("7d", 7), ("30d", 30), ("90d", 90), ("365d", 365)
        ]
        if not historical:
            for label, days in windows_def:
                windows[label] = TemporalWindow(
                    window_days=days,
                    average_score=None,
                    data_points=0,
                    start_score=None,
                    end_score=current_score,
                    momentum=DomainMomentum.UNKNOWN,
                )
            return windows

        now = datetime.now(timezone.utc)
        for label, days in windows_def:
            cutoff = now.timestamp() - (days * 86400)
            relevant = [
                snap for snap in historical
                if snap.get("computed_at", now).timestamp() >= cutoff
                and domain.value in snap.get("domain_scores", {})
            ]
            if not relevant:
                windows[label] = TemporalWindow(
                    window_days=days,
                    average_score=None,
                    data_points=0,
                    start_score=None,
                    end_score=current_score,
                    momentum=DomainMomentum.UNKNOWN,
                )
                continue

            scores_in_window = [
                snap["domain_scores"][domain.value] / 100.0
                for snap in relevant
            ]
            avg = sum(scores_in_window) / len(scores_in_window)
            start = scores_in_window[0]
            end = scores_in_window[-1]

            if end - start > 0.05:
                mom = DomainMomentum.IMPROVING
            elif start - end > 0.05:
                mom = DomainMomentum.DECLINING
            else:
                variance = sum((s - avg) ** 2 for s in scores_in_window) / len(scores_in_window)
                mom = DomainMomentum.VOLATILE if variance > 0.02 else DomainMomentum.STABLE

            windows[label] = TemporalWindow(
                window_days=days,
                average_score=round(avg, 4),
                data_points=len(scores_in_window),
                start_score=round(start, 4),
                end_score=round(end, 4),
                momentum=mom,
            )
        return windows

    def _compute_trajectory(
        self,
        composite: float,
        domain_scores: dict[FlourishingDomain, DomainScore],
        historical: list[dict[str, Any]] | None,
    ) -> tuple[TrajectoryLabel, float | None, str]:
        """
        Classify the person's overall flourishing trajectory.

        The trajectory is not just the current composite — it is the
        direction of travel. A person at 0.15 who is improving is in
        a categorically different situation from a person at 0.15 declining.
        The Chron dimension of Cosm × Chron = Flourishing.
        """
        has_crisis = any(
            ds.score < CRISIS_THRESHOLD for ds in domain_scores.values()
        )
        if has_crisis:
            label = TrajectoryLabel.CRISIS

        elif composite >= THRIVING_THRESHOLD:
            label = TrajectoryLabel.THRIVING
        else:
            # Assess momentum from domain scores
            improving_count = sum(
                1 for ds in domain_scores.values()
                if ds.momentum == DomainMomentum.IMPROVING
            )
            declining_count = sum(
                1 for ds in domain_scores.values()
                if ds.momentum == DomainMomentum.DECLINING
            )
            if improving_count > declining_count:
                label = TrajectoryLabel.RECOVERING
            elif declining_count > improving_count:
                label = TrajectoryLabel.DECLINING
            else:
                label = TrajectoryLabel.PLATEAUED

        # Velocity: if no historical data, estimate from delta sum
        velocity: float | None = None
        if historical and len(historical) >= 2:
            recent_composites = []
            for snap in sorted(historical[-4:], key=lambda s: s.get("computed_at", datetime.min)):
                scores_dict = snap.get("domain_scores", {})
                if scores_dict:
                    vals = [v / 100.0 for v in scores_dict.values() if isinstance(v, (int, float))]
                    if vals:
                        recent_composites.append(sum(vals) / len(vals))
            if len(recent_composites) >= 2:
                velocity = round((recent_composites[-1] - recent_composites[0]) / max(len(recent_composites) - 1, 1), 5)

        else:
            # Estimate from accumulated deltas
            total_delta = sum(
                ds.score_delta for ds in domain_scores.values()
                if ds.score_delta is not None
            )
            if total_delta != 0:
                velocity = round(total_delta / 12.0, 5)

        if velocity is None:
            vel_interp = "Velocity unknown — insufficient temporal data."
        elif velocity > 0.01:
            vel_interp = (
                f"Improving at {abs(velocity):.4f} composite points per assessment cycle. "
                "Trajectory is moving toward flourishing."
            )
        elif velocity < -0.01:
            vel_interp = (
                f"Declining at {abs(velocity):.4f} composite points per assessment cycle. "
                "Trajectory is moving away from flourishing. Intervention urgency is HIGH."
            )
        else:
            vel_interp = "Composite score is stable — neither improving nor declining meaningfully."

        return label, velocity, vel_interp

    # ===========================================================================
    # PRIVATE — Bottleneck and Synergy Identification
    # ===========================================================================

    def _identify_bottleneck(
        self,
        domain_scores: dict[FlourishingDomain, DomainScore],
    ) -> tuple[FlourishingDomain, str]:
        """
        Identify the domain most constraining overall flourishing.

        The bottleneck is identified using a combination of:
        1. Layer-weighted impact: Layer 1 domains have multiplied impact
           because they gate higher-layer domains.
        2. Score deficit: Larger gap from threshold = more constraining.
        3. Synergy centrality: Domains with more outgoing synergy edges
           are more constraining when low.

        This is inspired by Liebig's Law of the Minimum — the factor in
        shortest supply limits the entire system. For Robert Jackson,
        the bottleneck is almost certainly PHYSICAL_SPACE_BEAUTY (housing)
        because it gates medication adherence, which gates psychiatric
        stability, which gates every other domain.
        """
        def bottleneck_score(domain: FlourishingDomain, ds: DomainScore) -> float:
            layer_weight = {1: 3.0, 2: 2.0, 3: 1.0}.get(ds.layer, 1.0)
            deficit = max(0.0, STABLE_THRESHOLD - ds.score)
            synergy_count = len(DOMAIN_SYNERGY_GRAPH.get(domain, {}))
            zero_cost = DOMAIN_ZERO_COST.get(domain, 10_000)
            return deficit * layer_weight * (1 + 0.3 * synergy_count) * (zero_cost / 50_000)

        scores = {d: bottleneck_score(d, ds) for d, ds in domain_scores.items()}
        bottleneck = max(scores, key=lambda d: scores[d])
        ds = domain_scores[bottleneck]

        rationale = (
            f"{bottleneck.value.replace('_', ' ').title()} (Layer {ds.layer}, score {ds.score:.2f}) "
            f"is the most constraining domain. Its low score suppresses {len(DOMAIN_SYNERGY_GRAPH.get(bottleneck, {}))} "
            f"other domains through documented synergy pathways. "
            f"Closing this gap from {ds.score:.2f} to {STABLE_THRESHOLD:.2f} "
            f"would yield the highest leverage across the full flourishing profile."
        )
        return bottleneck, rationale

    def _identify_top_synergy(
        self,
        domain_scores: dict[FlourishingDomain, DomainScore],
    ) -> tuple[FlourishingDomain, str]:
        """
        Identify the domain improvement that would cascade most beneficially.

        This differs from bottleneck identification: we look for the domain
        where a realistic incremental improvement would produce the greatest
        total cascade benefit across connected domains.
        """
        best_domain = FlourishingDomain.PHYSICAL_SPACE_BEAUTY  # Default to housing
        best_cascade_sum = 0.0

        for domain, edges in DOMAIN_SYNERGY_GRAPH.items():
            if domain not in domain_scores:
                continue
            current = domain_scores[domain].score
            # Assume a realistic 0.3 improvement (e.g., getting housed)
            delta = min(0.3, 1.0 - current)
            cascade_sum = sum(
                delta * strength * (1.0 - domain_scores.get(target, DomainScore(
                    domain=target, score=0.0, label="Crisis", layer=1,
                    is_foundation_met=False, momentum=DomainMomentum.UNKNOWN,
                    score_delta=None, threats=[], supports=[],
                    evidence_sources=[], confidence=0.5, narrative=""
                )).score)
                for target, strength in edges.items()
                if target in domain_scores
            )
            if cascade_sum > best_cascade_sum:
                best_cascade_sum = cascade_sum
                best_domain = domain

        target_names = ", ".join(
            d.value.replace("_", " ")
            for d in list(DOMAIN_SYNERGY_GRAPH.get(best_domain, {}).keys())[:4]
        )
        rationale = (
            f"A 0.30 improvement in {best_domain.value.replace('_', ' ').title()} "
            f"would cascade into measurable gains in: {target_names}. "
            f"Estimated total cascade benefit: {best_cascade_sum:.3f} composite points. "
            f"This is the highest-leverage single intervention in the current profile."
        )
        return best_domain, rationale

    # ===========================================================================
    # PRIVATE — Cost Modeling
    # ===========================================================================

    def _domain_annual_cost(self, domain: FlourishingDomain, score: float) -> float:
        """
        Compute the annual societal cost for a domain at a given score.

        Cost follows an inverse relationship with score — near-zero scores
        produce near-maximum costs, with a non-linear decay as scores improve.
        The decay is sub-linear for low scores (crisis = expensive) and
        approaches zero as score approaches 1.0.
        """
        base_cost = DOMAIN_ZERO_COST.get(domain, 10_000)
        # Exponential decay: cost = base × e^(-k×score), where k ensures cost ≈ 0 at score=1.0
        # k = -ln(0.02) ≈ 3.91 (so at score=1.0, cost ≈ 2% of base, representing residual overhead)
        k = 3.91
        return base_cost * math.exp(-k * score)

    def _build_cost_model(
        self, domain: FlourishingDomain, score: float
    ) -> DomainCostModel:
        """Build the cost model for a single domain."""
        base_cost = DOMAIN_ZERO_COST.get(domain, 10_000)
        current_cost = self._domain_annual_cost(domain, score)
        cost_at_thriving = self._domain_annual_cost(domain, THRIVING_THRESHOLD)
        savings_if_thriving = current_cost - cost_at_thriving

        # ROI: how much is saved per dollar spent raising score by 0.1?
        intervention_cost = INTERVENTION_COST_PER_TENTH.get(domain, 1_000)
        cost_at_plus_tenth = self._domain_annual_cost(domain, min(1.0, score + 0.1))
        savings_per_tenth = current_cost - cost_at_plus_tenth
        roi = savings_per_tenth / intervention_cost if intervention_cost > 0 else 0.0

        domain_display = domain.value.replace("_", " ").title()
        narrative = (
            f"{domain_display} at score {score:.2f} costs an estimated "
            f"${current_cost:,.0f}/year in societal impact. "
            f"Raising to {THRIVING_THRESHOLD:.0%} would reduce this to ~${cost_at_thriving:,.0f}/year, "
            f"saving ${savings_if_thriving:,.0f} annually. "
            f"Each 0.1 improvement costs ~${intervention_cost:,.0f} in intervention and returns "
            f"${savings_per_tenth:,.0f} in savings — a {roi:.1f}x ROI."
        )

        return DomainCostModel(
            domain=domain,
            current_score=score,
            annual_cost_of_current_state=round(current_cost, 2),
            cost_at_zero=base_cost,
            cost_at_thriving=round(cost_at_thriving, 2),
            cost_savings_if_thriving=round(savings_if_thriving, 2),
            intervention_cost_per_tenth=float(intervention_cost),
            roi_per_tenth_improvement=round(roi, 2),
            narrative=narrative,
        )

    def _compute_aggregate_cost(
        self,
        domain_scores: dict[FlourishingDomain, DomainScore],
    ) -> tuple[float, float]:
        """Compute total annual cost and savings across all domains."""
        total_cost = 0.0
        total_savings = 0.0
        for domain, ds in domain_scores.items():
            if ds.cost_model:
                total_cost += ds.cost_model.annual_cost_of_current_state
                total_savings += ds.cost_model.cost_savings_if_thriving
        return total_cost, total_savings

    # ===========================================================================
    # PRIVATE — Narratives
    # ===========================================================================

    def _generate_cost_narrative(
        self,
        domain_scores: dict[FlourishingDomain, DomainScore],
        total_cost: float,
        total_savings: float,
    ) -> str:
        """Generate a plain-language cost narrative for the dashboard."""
        most_costly = max(
            (d for d in domain_scores if domain_scores[d].cost_model),
            key=lambda d: domain_scores[d].cost_model.annual_cost_of_current_state,  # type: ignore
            default=None,
        )
        most_costly_str = (
            f"{most_costly.value.replace('_', ' ').title()} "
            f"(${domain_scores[most_costly].cost_model.annual_cost_of_current_state:,.0f}/year)"
            if most_costly and domain_scores[most_costly].cost_model else "unknown domain"
        )
        best_roi = max(
            (d for d in domain_scores if domain_scores[d].cost_model),
            key=lambda d: domain_scores[d].cost_model.roi_per_tenth_improvement,  # type: ignore
            default=None,
        )
        best_roi_str = (
            f"{best_roi.value.replace('_', ' ').title()} "
            f"({domain_scores[best_roi].cost_model.roi_per_tenth_improvement:.1f}x ROI)"
            if best_roi and domain_scores[best_roi].cost_model else "unknown domain"
        )
        return (
            f"The total estimated annual societal cost of this person's un-flourishing "
            f"is ${total_cost:,.0f}. If all domains reached the thriving threshold, "
            f"the system would save approximately ${total_savings:,.0f} per year. "
            f"The highest-cost domain is {most_costly_str}. "
            f"The highest-ROI intervention target is {best_roi_str}. "
            f"These numbers are not a valuation of a human life — they are an argument "
            f"for why this life deserves the investment it has been denied."
        )

    def _generate_dashboard_narrative(
        self,
        person_id: uuid.UUID,
        composite: float,
        domain_scores: dict[FlourishingDomain, DomainScore],
        trajectory: TrajectoryLabel,
        total_cost: float,
        total_savings: float,
        in_crisis: list[FlourishingDomain],
    ) -> str:
        """Generate the high-level dashboard narrative summary."""
        label = self._score_label(composite)
        crisis_names = ", ".join(d.value.replace("_", " ") for d in in_crisis[:4])
        crisis_str = f"Domains in crisis: {crisis_names}." if in_crisis else "No domains currently in acute crisis."

        layer1_scores = {
            d: ds.score for d, ds in domain_scores.items() if ds.layer == 1
        }
        weakest_foundation = min(layer1_scores, key=layer1_scores.get) if layer1_scores else None  # type: ignore
        weakest_str = (
            f"The weakest Foundation domain is {weakest_foundation.value.replace('_', ' ').title()} "
            f"at {layer1_scores[weakest_foundation]:.2f}."
        ) if weakest_foundation else ""

        return (
            f"Flourishing composite: {composite:.2f}/1.0 ({label}). "
            f"Trajectory: {trajectory.value}. "
            f"{crisis_str} {weakest_str} "
            f"Estimated annual societal cost of current un-flourishing: ${total_cost:,.0f}. "
            f"Potential annual savings with coordinated care: ${total_savings:,.0f}. "
            f"The Cosm score is a snapshot of this person's current state across all twelve "
            f"dimensions of a fully human life. Its product with their temporal arc (Chron) "
            f"is the complete flourishing equation — not a verdict, but a map toward what is possible."
        )

    def _explain_domain_through_traditions(
        self,
        domain: FlourishingDomain,
        dashboard: FlourishingDashboard,
    ) -> str:
        """Summarize how each philosophical tradition views a specific domain's score."""
        lines: list[str] = []
        ds = dashboard.domain_scores.get(domain)
        if not ds:
            return ""
        for tradition, ts in dashboard.tradition_scores.items():
            weight = TRADITION_WEIGHTS[tradition].get(domain, 0.0)
            contribution = ts.domain_contributions.get(domain, 0.0)
            tname = tradition.value.title()
            lines.append(
                f"  {tname}: weight {weight:.2%}, contribution {contribution:.4f}. "
                f"Weakest domain in this tradition: {ts.weakest_domain.value.replace('_', ' ')}."
            )
        return "\n".join(lines)

    def _what_if_narrative(
        self,
        domain: FlourishingDomain,
        current_score: float,
        target_score: float,
        cascade: dict[FlourishingDomain, float],
        composite_before: float,
        composite_after: float,
        annual_savings: float,
    ) -> str:
        """Generate a narrative explaining a what-if scenario."""
        domain_display = domain.value.replace("_", " ").title()
        cascade_str = ", ".join(
            f"{d.value.replace('_', ' ').title()} (+{delta:.3f})"
            for d, delta in sorted(cascade.items(), key=lambda x: -x[1])
        )
        return (
            f"What if {domain_display} improves from {current_score:.2f} to {target_score:.2f}?\n\n"
            f"Direct improvement: +{target_score - current_score:.3f} in {domain_display}.\n"
            f"Projected cascades: {cascade_str or 'None identified.'}\n\n"
            f"Composite score: {composite_before:.4f} → {composite_after:.4f} "
            f"(+{composite_after - composite_before:.4f}).\n"
            f"Estimated annual savings: ${annual_savings:,.0f}.\n\n"
            f"These projections reflect documented structural relationships between domains — "
            f"the evidence that housing stability increases medication adherence, that medication "
            f"adherence reduces psychiatric crises, that psychiatric stability enables economic "
            f"engagement. The cascade is real. The question is whether the system will act on it."
        )

    # ===========================================================================
    # PRIVATE — Utility
    # ===========================================================================

    @staticmethod
    def _score_label(score: float) -> str:
        """Convert a 0.0–1.0 score to a human-readable label."""
        if score < CRISIS_THRESHOLD:
            return "Crisis"
        elif score < FRAGILE_THRESHOLD:
            return "Fragile"
        elif score < STABLE_THRESHOLD:
            return "Developing"
        elif score < THRIVING_THRESHOLD:
            return "Stable"
        else:
            return "Thriving"


# ===========================================================================
# MODULE-LEVEL CONVENIENCE: Robert Jackson Baseline Dashboard
# ===========================================================================

async def get_robert_jackson_baseline() -> FlourishingDashboard:
    """
    Convenience function to generate Robert Jackson's initial flourishing dashboard.

    This is the starting point — the Cosm at time zero of the DOMES intervention.
    The numbers are devastating. They are meant to be. This is what seven years
    of fragmented, reactive care produces: a human being at 0.09 composite
    flourishing, costing $112,100/year, generating 47 ER visits, living in
    the rain.

    The point of computing this is not to document suffering. It is to make
    visible what the system has made invisible: that this can change.
    That there is a trajectory from here to thriving. That the data center
    can be aimed — not at a research problem, not at a product — but at a person.

    Returns:
        FlourishingDashboard: Robert Jackson's baseline flourishing state.
    """
    engine = FlourishingEngine()
    from domes.seed import ROBERT_JACKSON_ID
    return await engine.compute_flourishing(
        person_id=ROBERT_JACKSON_ID,
        domain_data=ROBERT_JACKSON_BASELINE,
    )
