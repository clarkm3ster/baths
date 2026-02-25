"""
BATHS Intelligence System — Data Models

These are not schema descriptions. These are data structures for a system
that genuinely learns. Every completed project deposits learnings. Every
new project withdraws them. The system gets measurably smarter over time.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid


# ── Maturity Levels ─────────────────────────────────────────────

class ResearchMaturity(str, Enum):
    """How close a capability is to deployment in BATHS."""
    THEORETICAL = "theoretical"      # Published research, no implementation
    LAB = "lab"                      # Working prototype in controlled conditions
    PILOT = "pilot"                  # Tested in real-world conditions, limited scale
    PRODUCTION = "production"        # Deployed and reliable
    FRONTIER = "frontier"            # Beyond current capability, actively tracked


class LearningType(str, Enum):
    """What kind of insight was produced."""
    FINDING = "finding"              # A factual discovery about a person/place/system
    METHOD = "method"                # A way of doing something that worked
    FAILURE = "failure"              # Something that didn't work and why
    CONNECTION = "connection"         # A link between two things nobody expected
    PATTERN = "pattern"              # A recurring structure across multiple projects
    POLICY_INSIGHT = "policy_insight"  # Something that changes how policy should work
    AWE_INSIGHT = "awe_insight"      # Something about what produces awe
    COST_INSIGHT = "cost_insight"    # Something about what things actually cost


class WorldModelDomain(str, Enum):
    """What aspect of the world this knowledge is about."""
    LEGAL = "legal"
    FISCAL = "fiscal"
    HEALTH = "health"
    HOUSING = "housing"
    EDUCATION = "education"
    EMPLOYMENT = "employment"
    COMMUNITY = "community"
    ENVIRONMENT = "environment"
    ZONING = "zoning"
    INFRASTRUCTURE = "infrastructure"
    ECOLOGY = "ecology"
    ECONOMICS = "economics"
    DEMOGRAPHICS = "demographics"
    CULTURE = "culture"
    AWE = "awe"


# ── Cross-Project Learning ──────────────────────────────────────

class Learning(BaseModel):
    """
    A single insight extracted from a completed project.
    This is the atom of cross-project intelligence.
    """
    learning_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    learning_type: LearningType
    # Where it came from
    source_project_id: str
    source_project_title: str
    source_game_type: str  # "domes" or "spheres"
    source_stage: str
    source_capability: str
    source_practitioner: str
    # The insight itself
    insight: str                     # The actual learning, in plain language
    evidence: str                    # What in the deliverable supports this
    confidence: float = 0.5          # 0-1, increases when corroborated by other projects
    # How it transfers
    applicable_domains: List[WorldModelDomain] = Field(default_factory=list)
    applicable_game_types: List[str] = Field(default_factory=list)  # which game types benefit
    transferability: float = 0.5     # 0-1, how well this applies to other projects
    # Keywords for retrieval
    keywords: List[str] = Field(default_factory=list)
    # Lifecycle
    times_applied: int = 0           # How many subsequent projects used this
    times_corroborated: int = 0      # How many projects confirmed this
    times_contradicted: int = 0      # How many projects found the opposite
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_applied_at: Optional[datetime] = None

    @property
    def reliability(self) -> float:
        """How reliable this learning is, based on corroboration."""
        if self.times_applied == 0:
            return self.confidence
        corr_rate = self.times_corroborated / max(self.times_applied, 1)
        contra_rate = self.times_contradicted / max(self.times_applied, 1)
        return min(1.0, self.confidence + (corr_rate * 0.3) - (contra_rate * 0.4))


class ProjectMemory(BaseModel):
    """
    Everything the system learned from a single completed project.
    This is what gets deposited after play_full_game completes.
    """
    project_id: str
    project_title: str
    game_type: str
    principal_name: str
    team_size: int
    # Extracted learnings
    learnings: List[Learning] = Field(default_factory=list)
    # Aggregate metrics
    cosm_score: float = 0.0
    chron_score: float = 0.0
    weakest_dimension: str = ""
    strongest_dimension: str = ""
    # What made this project distinctive
    key_innovations: List[str] = Field(default_factory=list)
    unexpected_connections: List[str] = Field(default_factory=list)
    # Metadata
    completed_at: datetime = Field(default_factory=datetime.utcnow)


# ── World Models ────────────────────────────────────────────────

class PersonKnowledge(BaseModel):
    """
    Accumulated knowledge about a type of person/situation.
    Not about ONE person — about patterns across people in similar circumstances.
    This is how domes learn from other domes.
    """
    knowledge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # What situation this knowledge applies to
    system_tags: List[str] = Field(default_factory=list)     # e.g. ["housing court", "TANF", "Medicaid"]
    dimension_tags: List[str] = Field(default_factory=list)  # e.g. ["stability", "health", "education"]
    circumstance_tags: List[str] = Field(default_factory=list)  # e.g. ["single parent", "disability", "eviction"]
    # The accumulated knowledge
    system_interaction_patterns: Dict[str, str] = Field(default_factory=dict)
    # e.g. {"housing court + TANF": "recertification timelines conflict 68% of the time"}
    coordination_insights: List[str] = Field(default_factory=list)
    cost_patterns: Dict[str, float] = Field(default_factory=dict)
    # e.g. {"fragmentation_tax_hours_per_week": 12.5, "coordination_savings_annual": 14200}
    flourishing_pathways: List[str] = Field(default_factory=list)
    # What actually works for people in these circumstances
    awe_design_insights: List[str] = Field(default_factory=list)
    # What produces awe in dome contexts
    # Source tracking
    source_project_ids: List[str] = Field(default_factory=list)
    observation_count: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class PlaceKnowledge(BaseModel):
    """
    Accumulated knowledge about a type of place/site.
    Not about ONE parcel — about patterns across places with similar characteristics.
    This is how spheres learn from other spheres.
    """
    knowledge_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # What kind of place this knowledge applies to
    zoning_tags: List[str] = Field(default_factory=list)      # e.g. ["RSA-5", "CMX-2", "industrial"]
    neighborhood_tags: List[str] = Field(default_factory=list)  # e.g. ["Kensington", "North Philadelphia"]
    site_tags: List[str] = Field(default_factory=list)        # e.g. ["vacant lot", "brownfield", "corner"]
    size_range: tuple = (0, 999999)                           # sqft range
    # The accumulated knowledge
    regulatory_patterns: Dict[str, str] = Field(default_factory=dict)
    # e.g. {"variance_success_rate": "78% for community use", "avg_permit_timeline_days": "127"}
    activation_patterns: List[str] = Field(default_factory=list)
    economics_patterns: Dict[str, float] = Field(default_factory=dict)
    # e.g. {"avg_activation_cost_per_sqft": 12.50, "foot_traffic_multiplier": 3.2}
    awe_trigger_effectiveness: Dict[str, float] = Field(default_factory=dict)
    # e.g. {"nature": 4.3, "collective_effervescence": 4.1, "accommodation": 4.5}
    community_impact_patterns: List[str] = Field(default_factory=list)
    # Source tracking
    source_project_ids: List[str] = Field(default_factory=list)
    observation_count: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# ── Frontier Research ───────────────────────────────────────────

class FrontierCapability(BaseModel):
    """
    A specific AI/technology capability tracked by the frontier researcher.
    Maps to specific BATHS layer needs.
    """
    capability_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    # Classification
    category: str  # e.g. "robotics", "world_models", "agent_networks", "embodied_ai"
    maturity: ResearchMaturity
    # Where it maps in BATHS
    applicable_layers_dome: List[int] = Field(default_factory=list)  # 1-12
    applicable_layers_sphere: List[int] = Field(default_factory=list)  # 1-10
    applicable_capabilities: List[str] = Field(default_factory=list)
    # e.g. ["legal_navigation", "activation_design"]
    # Research provenance
    key_papers: List[str] = Field(default_factory=list)
    key_labs: List[str] = Field(default_factory=list)
    key_benchmarks: List[str] = Field(default_factory=list)
    # Integration potential
    integration_path: str = ""  # How this could be integrated into BATHS
    dependencies: List[str] = Field(default_factory=list)
    estimated_timeline: str = ""  # When this could be production-ready
    # Evolution tracking
    maturity_history: List[Dict[str, Any]] = Field(default_factory=list)
    # [{"date": "2025-01", "maturity": "theoretical", "note": "..."}]
    last_reviewed: datetime = Field(default_factory=datetime.utcnow)


class ResearchFrontier(BaseModel):
    """
    The full frontier map — everything the researcher is tracking.
    """
    frontier_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    capabilities: List[FrontierCapability] = Field(default_factory=list)
    # Meta-trends
    convergence_zones: List[Dict[str, Any]] = Field(default_factory=list)
    # Where multiple capabilities are converging toward BATHS-relevant breakthroughs
    paradigm_shifts: List[str] = Field(default_factory=list)
    # Fundamental changes in what's possible
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# ── Agent Network ───────────────────────────────────────────────

class AgentCapabilityProfile(BaseModel):
    """
    What a specialist agent can do. This is the building block
    for multi-agent coordination on complex BATHS tasks.
    """
    agent_type: str  # e.g. "legal_navigator", "parcel_researcher", "awe_designer"
    description: str
    # What tools/APIs this agent can use
    tool_access: List[str] = Field(default_factory=list)
    # What data this agent can read/write
    data_access: List[str] = Field(default_factory=list)
    # What it produces
    output_types: List[str] = Field(default_factory=list)
    # Dependencies
    requires_agents: List[str] = Field(default_factory=list)
    # Performance
    tasks_completed: int = 0
    avg_quality_score: float = 0.0


class AgentTask(BaseModel):
    """A task assigned to an agent in the network."""
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: str
    task_description: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"  # pending, running, completed, failed
    parent_task_id: Optional[str] = None
    child_task_ids: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


# ── System Evolution ────────────────────────────────────────────

class IntelligenceMetrics(BaseModel):
    """
    Tracks how smart the system is getting over time.
    This is the evidence that the system evolves.
    """
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    # Volume
    total_projects_completed: int = 0
    total_learnings_stored: int = 0
    total_cross_project_transfers: int = 0
    # Quality
    avg_learning_confidence: float = 0.0
    avg_learning_reliability: float = 0.0
    corroboration_rate: float = 0.0        # % of learnings confirmed by later projects
    # Coverage
    person_knowledge_entries: int = 0
    place_knowledge_entries: int = 0
    frontier_capabilities_tracked: int = 0
    capabilities_at_production: int = 0
    # Impact
    avg_cosm_improvement: float = 0.0      # How much better domes get over time
    avg_chron_improvement: float = 0.0     # How much better spheres get over time
    insight_reuse_rate: float = 0.0        # % of available learnings used by new projects
    # Agent network
    active_agent_types: int = 0
    tasks_completed_by_agents: int = 0
