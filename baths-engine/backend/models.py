"""
BATHS Game Engine - Data Models
Player state, productions, portfolio, scoring
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


class CosmDimensions(BaseModel):
    """DOMES scoring dimensions (minimum = total)"""
    legal: float = 0.0
    data: float = 0.0
    fiscal: float = 0.0
    coordination: float = 0.0
    flourishing: float = 0.0
    narrative: float = 0.0
    
    @property
    def total(self) -> float:
        """Weakest link principle — dome is only as strong as thinnest point"""
        return min(self.legal, self.data, self.fiscal, 
                   self.coordination, self.flourishing, self.narrative)


class ChronDimensions(BaseModel):
    """SPHERES scoring dimensions (m² × time, evolving to significance density)"""
    unlock: float = 0.0      # Square meters unlocked
    access: float = 0.0       # Public access hours
    permanence: float = 0.0   # Duration multiplier
    catalyst: float = 0.0     # Ripple effects
    policy: float = 0.0       # Policy changes unlocked
    
    @property
    def total(self) -> float:
        """m² × time × significance"""
        base = self.unlock * self.access
        significance = (self.permanence + self.catalyst + self.policy) / 3
        return base * (1 + significance)


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
    cosm: Optional[CosmDimensions] = None  # If DOMES
    chron: Optional[ChronDimensions] = None  # If SPHERES
    ip_created: List[str] = Field(default_factory=list)
    innovations: List[str] = Field(default_factory=list)
    industries_changed: List[str] = Field(default_factory=list)
    story_packages: List[Dict[str, Any]] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.utcnow)


class Portfolio(BaseModel):
    """Player portfolio"""
    domes_completed: List[CompletedProduction] = Field(default_factory=list)
    spheres_completed: List[CompletedProduction] = Field(default_factory=list)
    total_cosm: CosmDimensions = Field(default_factory=CosmDimensions)
    total_chron: ChronDimensions = Field(default_factory=ChronDimensions)
    ip_created: List[str] = Field(default_factory=list)
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
    action: str  # e.g., "complete_research", "approve_design", "execute_contracts"
    data: Dict[str, Any] = Field(default_factory=dict)


class StageResult(BaseModel):
    """Result of stage action"""
    success: bool
    message: str
    new_stage: Optional[ProductionStage] = None
    progress: float
    data: Dict[str, Any] = Field(default_factory=dict)
