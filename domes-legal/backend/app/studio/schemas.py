"""Pydantic v2 schemas for the Dome Studio (Showrunner Layer)."""
from __future__ import annotations

from datetime import date, datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

CharacterType = Literal["real", "fictional", "composite", "scenario"]
ConsentTier = Literal["tier1_public", "tier2_personal", "tier3_sensitive", "tier4_highest"]
ProductionMedium = Literal[
    "film", "short", "doc", "series", "installation",
    "live_event", "product", "game", "interactive",
]

# ── Character ──────────────────────────────────────────────────────

class CharacterProfile(BaseModel):
    character_id: str
    character_type: CharacterType
    name_or_alias: str
    consent_tier: ConsentTier
    fictionalization_rules: dict = Field(default_factory=dict)
    circumstances_summary: str = ""
    initial_conditions: dict = Field(default_factory=dict)

class CharacterCreate(BaseModel):
    character_type: CharacterType
    name_or_alias: str
    consent_tier: ConsentTier
    fictionalization_rules: dict = Field(default_factory=dict)
    circumstances_summary: str = ""
    initial_conditions: dict = Field(default_factory=dict)

# ── Talent ─────────────────────────────────────────────────────────

class TalentRole(BaseModel):
    person_or_entity: str
    role: str
    rate_type: Literal["day", "week", "flat", "salary", "vendor"]
    rate: float

# ── Production Stage ───────────────────────────────────────────────

class ProductionStage(BaseModel):
    stage: Literal["development", "pre_production", "production", "post", "distribution"]
    start_date: str
    end_date: str
    cost_cap: float
    deliverables: list[str] = Field(default_factory=list)
    risk_register: list[str] = Field(default_factory=list)

# ── Production ─────────────────────────────────────────────────────

class Production(BaseModel):
    production_id: str
    title: str
    medium: ProductionMedium
    character_id: str
    stage: Literal["greenlit", "in_progress", "paused", "shipped"]
    stages: list[ProductionStage] = Field(default_factory=list)
    team: list[TalentRole] = Field(default_factory=list)
    budget_total: float = 0.0
    financing_sources: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductionCreate(BaseModel):
    title: str
    medium: ProductionMedium
    character_id: str
    stage: Literal["greenlit", "in_progress", "paused", "shipped"] = "greenlit"
    stages: list[ProductionStage] = Field(default_factory=list)
    team: list[TalentRole] = Field(default_factory=list)
    budget_total: float = 0.0
    financing_sources: list[str] = Field(default_factory=list)

# ── Gap Tracking ───────────────────────────────────────────────────

class GapItem(BaseModel):
    gap_id: str
    production_id: str
    character_id: str
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    area: Literal[
        "metrics", "connectors", "ledger", "forecast",
        "scenario", "settlement", "validation", "consent", "ux",
    ]
    severity: Literal["low", "medium", "high", "blocking"]
    description: str
    reproduction_steps: list[str] = Field(default_factory=list)
    proposed_fix: Optional[str] = None
    owner_module: Optional[str] = None
    status: Literal["new", "triaged", "planned", "in_progress", "shipped", "wont_fix"] = "new"

class GapItemCreate(BaseModel):
    character_id: str
    area: Literal[
        "metrics", "connectors", "ledger", "forecast",
        "scenario", "settlement", "validation", "consent", "ux",
    ]
    severity: Literal["low", "medium", "high", "blocking"]
    description: str
    reproduction_steps: list[str] = Field(default_factory=list)
    proposed_fix: Optional[str] = None
    owner_module: Optional[str] = None

class GapTriage(BaseModel):
    status: Optional[str] = None
    proposed_fix: Optional[str] = None
    owner_module: Optional[str] = None

# ── IP Assets ──────────────────────────────────────────────────────

class IPAsset(BaseModel):
    asset_id: str
    production_id: str
    asset_type: Literal[
        "script", "footage", "cut", "poster", "soundtrack",
        "prototype", "dataset_synthetic", "curriculum", "installation_plan",
    ]
    title: str
    storage_uri: Optional[str] = None
    contributors: list[str] = Field(default_factory=list)
    rights: dict = Field(default_factory=dict)

class IPAssetCreate(BaseModel):
    asset_type: Literal[
        "script", "footage", "cut", "poster", "soundtrack",
        "prototype", "dataset_synthetic", "curriculum", "installation_plan",
    ]
    title: str
    storage_uri: Optional[str] = None
    contributors: list[str] = Field(default_factory=list)
    rights: dict = Field(default_factory=dict)

# ── Learning Packages ──────────────────────────────────────────────

class LearningPackage(BaseModel):
    learning_id: str
    production_id: str
    summary: str
    gap_ids: list[str] = Field(default_factory=list)
    proposed_os_changes: list[str] = Field(default_factory=list)
    validation_needed: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class LearningPackageCreate(BaseModel):
    summary: str
    gap_ids: list[str] = Field(default_factory=list)
    proposed_os_changes: list[str] = Field(default_factory=list)
    validation_needed: list[str] = Field(default_factory=list)

# ── Backlog View ───────────────────────────────────────────────────

class BacklogView(BaseModel):
    """Gaps grouped by severity, area, and owner_module for triage."""
    by_severity: dict[str, list[GapItem]] = Field(default_factory=dict)
    by_area: dict[str, list[GapItem]] = Field(default_factory=dict)
    by_owner_module: dict[str, list[GapItem]] = Field(default_factory=dict)
    total: int = 0
