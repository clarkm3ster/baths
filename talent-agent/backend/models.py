"""
Chron Talent Agent — Data Models
Talent profiles, principals, teams, projects, IP tracking, productions
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid


# ── Enums ────────────────────────────────────────────────────────

class GameType(str, Enum):
    DOMES = "domes"
    SPHERES = "spheres"


class ProductionStage(str, Enum):
    DEVELOPMENT = "development"
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    POST_PRODUCTION = "post_production"
    DISTRIBUTION = "distribution"


class Availability(str, Enum):
    AVAILABLE = "available"
    ON_PRODUCTION = "on_production"
    LIMITED = "limited"
    UNAVAILABLE = "unavailable"


class ProjectStatus(str, Enum):
    SOURCED = "sourced"           # Brief created, not yet assigned
    ASSEMBLING = "assembling"     # Principal assigned, team being built
    IN_PRODUCTION = "in_production"  # Active production
    COMPLETED = "completed"
    PUBLISHED = "published"       # Published to domes.cc or spheres.land


class IPDomain(str, Enum):
    ENTERTAINMENT = "entertainment"
    TECHNOLOGY = "technology"
    FINANCIAL_PRODUCT = "financial_product"
    POLICY = "policy"
    PRODUCT = "product"
    RESEARCH = "research"
    HOUSING = "housing"
    HEALTHCARE = "healthcare"
    URBAN_DESIGN = "urban_design"
    REAL_ESTATE = "real_estate"
    FASHION = "fashion"
    CULINARY = "culinary"
    ARCHITECTURAL = "architectural"
    PERFORMANCE = "performance"


# ── Body of Work ─────────────────────────────────────────────────

class WorkItem(BaseModel):
    """A single piece of work in someone's body of work"""
    title: str
    description: str
    year: Optional[int] = None
    link: Optional[str] = None
    medium: str  # e.g. "film", "building", "book", "software", "performance"


# ── Talent Profile ───────────────────────────────────────────────

class TalentProfile(BaseModel):
    """A person on the roster, profiled by practice not role"""
    talent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    contact: Optional[str] = None
    bio: str  # What they do, how they see, what they bring
    body_of_work: List[WorkItem] = Field(default_factory=list)
    domains_of_practice: List[str] = Field(default_factory=list)
    approach: str = ""  # Design philosophy, what they see that others miss
    availability: Availability = Availability.AVAILABLE
    # Production history
    productions_completed: List[str] = Field(default_factory=list)  # project_ids
    total_cosm: float = 0.0
    total_chron: float = 0.0
    # What they bring to a table
    capabilities: List[str] = Field(default_factory=list)
    # Tags for resonance matching
    resonance_tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Principal ────────────────────────────────────────────────────

class Principal(BaseModel):
    """Top-tier production leader — the producing director"""
    principal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    bio: str
    vision: str  # What their productions look and feel like
    game_type: Optional[GameType] = None  # Some principals do both
    body_of_work: List[WorkItem] = Field(default_factory=list)
    signature_style: str = ""  # What makes their productions distinctive
    productions_led: List[str] = Field(default_factory=list)  # project_ids
    total_cosm: float = 0.0
    total_chron: float = 0.0
    availability: Availability = Availability.AVAILABLE
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Project Brief ────────────────────────────────────────────────

class CharacterBrief(BaseModel):
    """A character brief for DOMES — sourced from real documentation"""
    name: str
    source: str  # Book, film, journalism, case study
    source_citation: str  # Full citation
    situation: str  # Their circumstances
    full_landscape: str  # Their full life — not just their problems
    production_challenge: str  # What makes this dome interesting to build
    key_systems: List[str] = Field(default_factory=list)  # Government systems involved
    flourishing_dimensions: List[str] = Field(default_factory=list)  # Which dimensions of flourishing are at stake


class ParcelBrief(BaseModel):
    """A parcel brief for SPHERES — sourced from real data"""
    address: str
    neighborhood: str
    city: str = "Philadelphia"
    parcel_id: Optional[str] = None
    zoning: str = ""
    lot_size_sqft: float = 0.0
    history: str  # What this space has been
    opportunity: str  # What activation could look like
    community_context: str  # Who lives nearby, what they need
    constraints: List[str] = Field(default_factory=list)  # Zoning, environmental, access


class ProjectBrief(BaseModel):
    """A project brief — the assignment for a team"""
    project_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game_type: GameType
    title: str
    character: Optional[CharacterBrief] = None  # DOMES
    parcel: Optional[ParcelBrief] = None  # SPHERES
    status: ProjectStatus = ProjectStatus.SOURCED
    principal_id: Optional[str] = None
    team_ids: List[str] = Field(default_factory=list)  # talent_ids
    # Production tracking
    current_stage: Optional[ProductionStage] = None
    production_id: Optional[str] = None  # links to baths-engine production
    production_number: int = 1  # Which production run (different teams can run the same project)
    # Stage log — the record of what happened at each stage
    stage_log: List[Dict[str, Any]] = Field(default_factory=list)
    # Scores
    cosm_score: float = 0.0
    chron_score: float = 0.0
    # IP generated
    ip_outputs: List[Dict[str, Any]] = Field(default_factory=list)
    # Timeline
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


# ── Team Assembly ────────────────────────────────────────────────

class ResonanceMatch(BaseModel):
    """Why a specific talent resonates with a specific project"""
    talent_id: str
    talent_name: str
    resonance_score: float  # 0-100
    reasoning: str  # What their practice brings to this production
    capabilities_matched: List[str] = Field(default_factory=list)
    unlikely_value: str = ""  # What unexpected value they bring


class TeamRecommendation(BaseModel):
    """A recommended team for a project"""
    project_id: str
    principal_id: str
    principal_name: str
    members: List[ResonanceMatch] = Field(default_factory=list)
    team_strength: str = ""  # Why this combination works
    unlikely_collisions: List[str] = Field(default_factory=list)  # Unexpected pairings
    capabilities_coverage: Dict[str, bool] = Field(default_factory=dict)
    ip_surface_area: List[str] = Field(default_factory=list)  # Expected IP domains


# ── IP Tracking ──────────────────────────────────────────────────

class IPItem(BaseModel):
    """A single piece of intellectual property"""
    ip_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: IPDomain
    title: str
    description: str
    format: str  # e.g. "documentary treatment", "bond structure", "API"
    project_id: str
    production_title: str
    practitioner_id: str  # talent who produced it
    practitioner_name: str
    practice: str  # What practice produced this
    stage_originated: ProductionStage
    value_driver: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Leaderboard ──────────────────────────────────────────────────

class LeaderboardEntry(BaseModel):
    """Leaderboard entry for a talent or principal"""
    id: str
    name: str
    role: str  # "talent" or "principal"
    productions_completed: int = 0
    total_cosm: float = 0.0
    total_chron: float = 0.0
    flourishing: float = 0.0
    ip_count: int = 0
    ip_domains: List[str] = Field(default_factory=list)
    domains_of_practice: List[str] = Field(default_factory=list)
