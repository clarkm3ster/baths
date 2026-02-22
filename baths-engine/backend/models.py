"""
BATHS Game Engine - Data Models
Player state, productions, portfolio, scoring, IP, bonds
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum


class GameType(str, Enum):
    DOMES = "domes"
    SPHERES = "spheres"


class ProductionStage(str, Enum):
    DEVELOPMENT = "development"
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    POST_PRODUCTION = "post_production"
    DISTRIBUTION = "distribution"


# ── IP Domains ────────────────────────────────────────────────────────

class IPDomain(str, Enum):
    ENTERTAINMENT = "entertainment"
    TECHNOLOGY = "technology"
    FINANCIAL_PRODUCT = "financial_product"
    POLICY = "policy"
    PRODUCT = "product"
    RESEARCH = "research"
    HOUSING = "housing"
    HEALTHCARE = "healthcare"


class IPOutput(BaseModel):
    """Intellectual property generated across 8 domains"""
    domain: IPDomain
    title: str
    description: str
    format: str  # e.g., "documentary", "API", "bond structure", "white paper"
    stage_originated: ProductionStage
    value_driver: str  # what makes this IP valuable


# ── COSM Dimensions (DOMES) ──────────────────────────────────────────

class CosmDimensions(BaseModel):
    """DOMES scoring — 6 production dimensions (minimum = total)"""
    rights: float = 0.0       # Legal landscape — rights acquisition
    research: float = 0.0     # Data systems — market research
    budget: float = 0.0       # Cost landscape — fiscal model
    package: float = 0.0      # Coordination architecture — the package
    deliverables: float = 0.0 # Flourishing outcomes — what gets delivered
    pitch: float = 0.0        # Narrative — the pitch to stakeholders

    @property
    def total(self) -> float:
        """Weakest link principle — dome is only as strong as thinnest point"""
        return min(self.rights, self.research, self.budget,
                   self.package, self.deliverables, self.pitch)


# ── CHRON Dimensions (SPHERES) ────────────────────────────────────────

class ChronDimensions(BaseModel):
    """SPHERES scoring dimensions (m2 x time, evolving to significance density)"""
    unlock: float = 0.0       # Square meters unlocked
    access: float = 0.0       # Public access hours
    permanence: float = 0.0   # Duration multiplier
    catalyst: float = 0.0     # Ripple effects
    policy: float = 0.0       # Policy changes unlocked

    @property
    def total(self) -> float:
        """m2 x time x significance"""
        base = self.unlock * self.access
        significance = (self.permanence + self.catalyst + self.policy) / 3
        return base * (1 + significance)


# ── Bonds ─────────────────────────────────────────────────────────────

class DomeBond(BaseModel):
    """Financial instrument representing dome coordination value"""
    bond_id: str
    subject: str
    face_value: float         # Total coordination savings (delta)
    coupon_rate: float        # Annual yield based on COSM score
    maturity_years: int       # Bond duration
    rating: str               # AAA to B based on dome coverage
    cosm_score: float         # COSM at issuance
    programs_backing: int     # Number of federal programs backing this bond
    yield_to_maturity: float  # Effective yield


class ChronBond(BaseModel):
    """Financial instrument representing sphere activation value"""
    bond_id: str
    parcel: str
    face_value: float         # Economic impact value
    coupon_rate: float        # Annual yield based on CHRON score
    maturity_years: int       # Bond duration
    rating: str               # AAA to B based on permanence + policy
    chron_score: float        # CHRON at issuance
    sqft_backing: float       # Square footage backing this bond
    yield_to_maturity: float  # Effective yield


# ── Production State ──────────────────────────────────────────────────

class ProductionState(BaseModel):
    """Active production state"""
    production_id: str
    game_type: GameType
    subject: str  # Person name (DOMES) or Parcel ID (SPHERES)
    stage: ProductionStage
    progress: float = 0.0  # 0-100
    stage_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CompletedProduction(BaseModel):
    """Completed production record"""
    production_id: str
    game_type: GameType
    subject: str
    cosm: Optional[CosmDimensions] = None
    chron: Optional[ChronDimensions] = None
    ip_outputs: List[IPOutput] = Field(default_factory=list)
    dome_bond: Optional[DomeBond] = None
    chron_bond: Optional[ChronBond] = None
    innovations: List[str] = Field(default_factory=list)
    industries_changed: List[str] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class Portfolio(BaseModel):
    """Player portfolio"""
    domes_completed: List[CompletedProduction] = Field(default_factory=list)
    spheres_completed: List[CompletedProduction] = Field(default_factory=list)
    total_cosm: CosmDimensions = Field(default_factory=CosmDimensions)
    total_chron: ChronDimensions = Field(default_factory=ChronDimensions)
    ip_outputs: List[IPOutput] = Field(default_factory=list)
    dome_bonds: List[DomeBond] = Field(default_factory=list)
    chron_bonds: List[ChronBond] = Field(default_factory=list)
    innovations: List[str] = Field(default_factory=list)
    industries_changed: List[str] = Field(default_factory=list)


class Player(BaseModel):
    """Player state"""
    player_id: str
    name: str
    current_game: Optional[GameType] = None
    active_production: Optional[ProductionState] = None
    portfolio: Portfolio = Field(default_factory=Portfolio)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StageAction(BaseModel):
    """Action to advance production stage"""
    production_id: str
    action: str
    data: Dict[str, Any] = Field(default_factory=dict)


class StageResult(BaseModel):
    """Result of stage action"""
    success: bool
    message: str
    new_stage: Optional[ProductionStage] = None
    progress: float
    data: Dict[str, Any] = Field(default_factory=dict)
