"""
BATHS Gravitational Schema — Core Types

Every layer in every dome and sphere shares these interfaces.
This is the grammar of the architecture.
"""

from datetime import datetime
from typing import Optional, Dict, List, Any, Literal
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


class DataModality(str, Enum):
    """What kind of data flows into a layer"""
    STRUCTURED = "structured"       # JSON, CSV, database records
    UNSTRUCTURED = "unstructured"   # Documents, PDFs, legal filings
    GEOSPATIAL = "geospatial"       # GIS, coordinates, parcels
    TEMPORAL = "temporal"           # Time series, sensor streams
    MEDIA = "media"                 # Images, video, audio, 3D models
    SENSOR = "sensor"              # IoT, wearable, environmental
    CREATIVE = "creative"          # Design files, compositions, notation


class IngestMode(str, Enum):
    """How data arrives"""
    STATIC_PULL = "static_pull"         # One-time fetch from database/API
    PERIODIC_BATCH = "periodic_batch"   # Scheduled refresh
    REAL_TIME_STREAM = "real_time_stream"  # Live data feed
    MANUAL_ENTRY = "manual_entry"       # Human input
    AGENT_DISCOVERY = "agent_discovery" # AI agent found this


class CreativeInputType(str, Enum):
    """Types of creative input for human-designed layers"""
    ARCHITECTURAL = "architectural"       # 3D models, spatial designs
    SONIC = "sonic"                       # Compositions, soundscapes
    MATERIAL = "material"                 # Textile specs, material palettes
    NARRATIVE = "narrative"               # Scripts, treatments, story arcs
    MOVEMENT = "movement"                 # Choreographic notation, pathways
    VISUAL = "visual"                     # Graphic systems, data viz as art
    CULINARY = "culinary"                 # Nutrition models, menu designs
    PHILOSOPHICAL = "philosophical"       # Frameworks for flourishing
    EXPERIENCE = "experience"             # Awe triggers, emotional journeys


class IPDomain(str, Enum):
    """Domains of intellectual property"""
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
    ENVIRONMENTAL = "environmental"
    EDUCATION = "education"


# ── AI Capability Mapping ────────────────────────────────────────

class AICapability(BaseModel):
    """A specific AI capability that feeds a layer"""
    capability_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str                              # e.g. "legal_database_navigation"
    description: str                       # What this capability does
    category: str                          # e.g. "agentic_ai", "computer_use", "analysis"
    maturity: Literal["available", "emerging", "speculative"] = "available"
    providers: List[str] = Field(default_factory=list)  # Known providers/tools
    feeds_interface: Literal["ingest", "process", "act"] = "process"
    autonomous: bool = False               # Can operate without human oversight
    human_required: bool = False           # Requires human design/decision


class AICapabilityMap(BaseModel):
    """Complete AI capability map for a layer"""
    layer_number: int
    layer_name: str
    capabilities: List[AICapability] = Field(default_factory=list)
    human_design_required: bool = False    # Layers 10-12 (DOME), 7-10 (SPHERE)
    human_design_description: str = ""     # What the human designs


# ── Five Layer Interfaces ────────────────────────────────────────

class DataSource(BaseModel):
    """A data source feeding into a layer"""
    source_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    url: Optional[str] = None
    modality: DataModality
    mode: IngestMode
    refresh_interval_seconds: Optional[int] = None  # For periodic batch
    last_fetched: Optional[datetime] = None
    agent_id: Optional[str] = None         # If discovered/fetched by an agent
    schema_hint: Optional[Dict[str, Any]] = None  # Expected data shape


class IngestInterface(BaseModel):
    """INGEST: accepts data from any source, any modality, any time scale"""
    sources: List[DataSource] = Field(default_factory=list)
    total_records: int = 0
    last_ingest: Optional[datetime] = None
    quality_score: float = 0.0             # 0-100, data quality assessment


class ProcessStep(BaseModel):
    """A processing step performed by an AI agent"""
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: str                        # e.g. "cleaning", "enrichment", "cross_reference"
    description: str
    input_sources: List[str] = Field(default_factory=list)  # source_ids
    output_format: str = ""
    last_run: Optional[datetime] = None
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    result_summary: Optional[str] = None


class ProcessInterface(BaseModel):
    """PROCESS: AI agents that clean, enrich, cross-reference, analyze, generate"""
    steps: List[ProcessStep] = Field(default_factory=list)
    insights_generated: int = 0
    last_processed: Optional[datetime] = None


class StateSnapshot(BaseModel):
    """A point-in-time snapshot of layer state"""
    snapshot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: Dict[str, Any] = Field(default_factory=dict)
    version: int = 1
    trigger: str = ""                      # What caused this snapshot


class StateInterface(BaseModel):
    """STATE: queryable current snapshot with full temporal history"""
    current: Dict[str, Any] = Field(default_factory=dict)
    history: List[StateSnapshot] = Field(default_factory=list)
    version: int = 0
    last_updated: Optional[datetime] = None


class Action(BaseModel):
    """An action that can be taken to improve this layer"""
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    action_type: str                       # e.g. "application", "connection", "intervention"
    executable_by_agent: bool = False      # Can a computer use agent do this?
    agent_instructions: Optional[str] = None  # If executable, how
    url: Optional[str] = None              # Portal or form URL
    deadline: Optional[datetime] = None
    status: Literal["available", "in_progress", "completed", "blocked", "expired"] = "available"
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    priority: Literal["critical", "high", "medium", "low"] = "medium"


class ActInterface(BaseModel):
    """ACT: actions to improve this layer — executable by computer use agents"""
    actions: List[Action] = Field(default_factory=list)
    completed_count: int = 0
    pending_count: int = 0
    blocked_count: int = 0


class Deliverable(BaseModel):
    """An exportable deliverable from a layer"""
    deliverable_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    format: str                            # "report", "bond", "visualization", "policy_brief", etc.
    ip_domain: Optional[IPDomain] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    file_path: Optional[str] = None
    world_model_ready: bool = False        # Exportable to world model renderer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    practitioner_id: Optional[str] = None
    practitioner_name: Optional[str] = None
    practice: Optional[str] = None


class ExportInterface(BaseModel):
    """EXPORT: generates deliverables — reports, bonds, visualizations, creative assets"""
    deliverables: List[Deliverable] = Field(default_factory=list)
    world_model_data: Dict[str, Any] = Field(default_factory=dict)  # Structured for 3D rendering


class LayerInterface(BaseModel):
    """The five interfaces every layer has"""
    ingest: IngestInterface = Field(default_factory=IngestInterface)
    process: ProcessInterface = Field(default_factory=ProcessInterface)
    state: StateInterface = Field(default_factory=StateInterface)
    act: ActInterface = Field(default_factory=ActInterface)
    export: ExportInterface = Field(default_factory=ExportInterface)


# ── Temporal Architecture ────────────────────────────────────────

class TemporalEntry(BaseModel):
    """A change event in the temporal stream"""
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    layer_number: int
    layer_name: str
    event_type: str                        # "data_change", "action_completed", "alert", "insight"
    description: str
    severity: Literal["info", "warning", "critical"] = "info"
    data_before: Optional[Dict[str, Any]] = None
    data_after: Optional[Dict[str, Any]] = None
    triggered_by: str = ""                 # "agent", "human", "monitor", "external"
    autonomous_action_taken: Optional[str] = None


class MonitorConfig(BaseModel):
    """Configuration for an autonomous monitoring agent"""
    monitor_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    layer_number: int
    watch_type: str                        # "legislation", "funding", "health", "market", "environment"
    description: str
    check_interval_seconds: int = 3600
    alert_conditions: List[str] = Field(default_factory=list)
    autonomous_mode: bool = False          # If true, can trigger actions without human approval
    last_check: Optional[datetime] = None


class TemporalState(BaseModel):
    """The living temporal dimension of a schema"""
    timeline: List[TemporalEntry] = Field(default_factory=list)
    monitors: List[MonitorConfig] = Field(default_factory=list)
    trajectory: Dict[str, Any] = Field(default_factory=dict)  # Modeled future states
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: Optional[datetime] = None


# ── World Model Export ───────────────────────────────────────────

class WorldModelExport(BaseModel):
    """Data formatted for world model rendering (Three.js/Cesium now, Genie/DeepMind later)"""
    schema_type: GameType
    schema_id: str
    title: str
    layers: Dict[int, Dict[str, Any]] = Field(default_factory=dict)  # Layer num → render data
    spatial_anchors: List[Dict[str, Any]] = Field(default_factory=list)  # 3D positions
    temporal_range: Optional[Dict[str, Any]] = None  # start, end, keyframes
    render_hints: Dict[str, Any] = Field(default_factory=dict)  # Renderer-specific hints
    format_version: str = "1.0"


# ── Creative Input ───────────────────────────────────────────────

class IPAttribution(BaseModel):
    """Attribution for creative IP"""
    practitioner_id: str
    practitioner_name: str
    practice: str
    ip_domain: IPDomain
    layer_completeness_score: float = 0.0  # How much this fills the layer (0-100)


class CreativeInput(BaseModel):
    """A creative input for human-designed layers"""
    input_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input_type: CreativeInputType
    title: str
    description: str
    content: Dict[str, Any] = Field(default_factory=dict)  # The actual creative content
    files: List[str] = Field(default_factory=list)           # File paths (models, audio, etc.)
    attribution: Optional[IPAttribution] = None
    layer_number: int
    world_model_renderable: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── Layer Definition ─────────────────────────────────────────────

class LayerDefinition(BaseModel):
    """Static definition of a layer — what it is, what feeds it"""
    layer_number: int
    name: str
    description: str
    schema_type: GameType
    human_design_required: bool = False
    human_design_description: str = ""
    ai_capability_map: AICapabilityMap = Field(default_factory=lambda: AICapabilityMap(layer_number=0, layer_name=""))
    scoring_weight: float = 1.0


class LayerScore(BaseModel):
    """Score for a single layer"""
    layer_number: int
    layer_name: str
    completeness: float = 0.0              # 0-100, how filled is this layer
    quality: float = 0.0                   # 0-100, quality of data/design
    coverage: float = 0.0                  # 0-100, how many interfaces are active
    ai_utilization: float = 0.0            # 0-100, how many AI capabilities are active
    human_design_score: float = 0.0        # 0-100, for layers requiring human design
    actions_completed_ratio: float = 0.0   # Completed / total available actions


class SchemaMetadata(BaseModel):
    """Metadata for a complete schema instance"""
    schema_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    schema_type: GameType
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None       # Principal or team ID
    production_id: Optional[str] = None
    project_id: Optional[str] = None
    version: int = 1
    status: Literal["draft", "active", "completed", "archived"] = "draft"
    is_auto_generated: bool = False        # True if generated from patterns
    source_pattern_id: Optional[str] = None  # If auto-generated, which pattern
    layer_scores: List[LayerScore] = Field(default_factory=list)
    total_score: float = 0.0               # Minimum across all layers (weakest link)
    temporal: TemporalState = Field(default_factory=TemporalState)
    world_model: Optional[WorldModelExport] = None
