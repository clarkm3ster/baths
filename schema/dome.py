"""
BATHS Gravitational Schema — DOME

The person is the gravitational center.
12 layers surround them — each one a dimension of their life.
Layers 1-9: AI agents fill these. Every advancing capability feeds them.
Layers 10-12: Human creative teams design these. This is where art lives.
The dome is only as strong as its weakest layer.

Layer 1:  Legal        — every right, every entitlement, every pathway
Layer 2:  Systems      — every government system, every portal, every form
Layer 3:  Fiscal       — every cost, every saving, every financial instrument
Layer 4:  Health       — every diagnosis, every treatment, every trajectory
Layer 5:  Housing      — every structure, every system, every environment
Layer 6:  Economic     — every job, every skill, every income path
Layer 7:  Education    — every credential, every learning path, every opportunity
Layer 8:  Community    — every connection, every asset, every risk
Layer 9:  Environment  — every sensor, every reading, every exposure
Layer 10: Autonomy     — HUMAN DESIGN: what autonomy means for THIS person
Layer 11: Creativity   — HUMAN DESIGN: how THIS person makes meaning
Layer 12: Flourishing  — HUMAN DESIGN: what flourishing looks like HERE
"""

from datetime import datetime
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid

from schema.core import (
    GameType,
    LayerInterface,
    LayerDefinition,
    AICapability,
    AICapabilityMap,
    CreativeInput,
    SchemaMetadata,
    TemporalState,
    WorldModelExport,
    LayerScore,
    IPDomain,
)


# ── Base Dome Layer ──────────────────────────────────────────────

class DomeLayer(BaseModel):
    """Base class for all dome layers. Every layer has the five interfaces."""
    layer_number: int
    layer_name: str
    interfaces: LayerInterface = Field(default_factory=LayerInterface)
    score: LayerScore = Field(default_factory=lambda: LayerScore(layer_number=0, layer_name=""))
    creative_inputs: List[CreativeInput] = Field(default_factory=list)  # For layers 10-12
    notes: str = ""


# ── Layer 1: Legal ───────────────────────────────────────────────

class LegalEntitlement(BaseModel):
    """A specific legal right or entitlement"""
    entitlement_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    program_name: str
    agency: str
    eligibility_status: str = "unknown"    # eligible, ineligible, pending, unknown
    application_status: str = "not_started"  # not_started, in_progress, approved, denied, appealing
    annual_value: float = 0.0
    application_url: Optional[str] = None
    deadline: Optional[datetime] = None
    requirements: List[str] = Field(default_factory=list)
    barriers: List[str] = Field(default_factory=list)


class DomeLegalLayer(DomeLayer):
    """Layer 1: Legal landscape — rights, entitlements, pathways"""
    layer_number: int = 1
    layer_name: str = "Legal"
    entitlements: List[LegalEntitlement] = Field(default_factory=list)
    total_entitled_value: float = 0.0
    total_accessed_value: float = 0.0
    access_gap: float = 0.0               # Entitled - Accessed
    legal_barriers: List[str] = Field(default_factory=list)
    pending_applications: int = 0
    active_cases: int = 0


# ── Layer 2: Systems ─────────────────────────────────────────────

class GovernmentSystem(BaseModel):
    """A government system this person interacts with"""
    system_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    system_name: str
    agency: str
    portal_url: Optional[str] = None
    identity_verified: bool = False
    account_active: bool = False
    last_interaction: Optional[datetime] = None
    fragmentation_score: float = 0.0       # How disconnected from other systems
    data_shared_with: List[str] = Field(default_factory=list)  # Other system IDs


class DomeSystemsLayer(DomeLayer):
    """Layer 2: Systems — government portals, identity, cross-system coordination"""
    layer_number: int = 2
    layer_name: str = "Systems"
    systems: List[GovernmentSystem] = Field(default_factory=list)
    total_systems: int = 0
    connected_systems: int = 0
    fragmentation_index: float = 0.0       # Overall disconnection measure
    identity_documents: List[str] = Field(default_factory=list)
    cross_system_gaps: List[str] = Field(default_factory=list)


# ── Layer 3: Fiscal ──────────────────────────────────────────────

class FiscalStream(BaseModel):
    """An income or expense stream"""
    stream_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    stream_type: str                       # "income", "expense", "benefit", "debt"
    amount: float
    frequency: str                         # "monthly", "annual", "one_time"
    source: str
    stable: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class DomeBond(BaseModel):
    """Financial instrument representing dome coordination value"""
    bond_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    face_value: float
    coupon_rate: float
    maturity_years: int
    rating: str
    cosm_score_at_issuance: float
    programs_backing: int
    yield_to_maturity: float
    stress_test_results: Dict[str, Any] = Field(default_factory=dict)


class DomeFiscalLayer(DomeLayer):
    """Layer 3: Fiscal — costs, savings, bonds, financial instruments"""
    layer_number: int = 3
    layer_name: str = "Fiscal"
    income_streams: List[FiscalStream] = Field(default_factory=list)
    expense_streams: List[FiscalStream] = Field(default_factory=list)
    total_monthly_income: float = 0.0
    total_monthly_expenses: float = 0.0
    coordination_savings: float = 0.0      # Delta from dome coordination
    cost_of_fragmentation: float = 0.0     # What disconnection costs
    dome_bond: Optional[DomeBond] = None
    financial_trajectory: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 4: Health ──────────────────────────────────────────────

class HealthCondition(BaseModel):
    """A health condition or need"""
    condition_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    condition: str
    severity: str = "moderate"             # mild, moderate, severe, critical
    treatment_status: str = "unknown"      # unknown, untreated, in_treatment, managed, resolved
    providers: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    barriers_to_care: List[str] = Field(default_factory=list)


class DomeHealthLayer(DomeLayer):
    """Layer 4: Health — diagnostics, treatment, trajectory, personalized medicine"""
    layer_number: int = 4
    layer_name: str = "Health"
    conditions: List[HealthCondition] = Field(default_factory=list)
    insurance_status: str = "unknown"
    insurance_type: Optional[str] = None
    primary_care: bool = False
    mental_health_access: bool = False
    dental_access: bool = False
    vision_access: bool = False
    drug_interactions: List[str] = Field(default_factory=list)
    wellness_score: float = 0.0
    health_trajectory: Dict[str, Any] = Field(default_factory=dict)
    wearable_data: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 5: Housing ─────────────────────────────────────────────

class HousingUnit(BaseModel):
    """Housing situation details"""
    unit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    address: Optional[str] = None
    unit_type: str = ""                    # apartment, house, shelter, transitional, none
    tenure: str = ""                       # own, rent, subsidized, temporary, homeless
    monthly_cost: float = 0.0
    condition_score: float = 0.0           # 0-100
    safety_score: float = 0.0
    environmental_hazards: List[str] = Field(default_factory=list)
    accessibility_features: List[str] = Field(default_factory=list)


class DomeHousingLayer(DomeLayer):
    """Layer 5: Housing — structure, systems, environment, smart building"""
    layer_number: int = 5
    layer_name: str = "Housing"
    current_housing: Optional[HousingUnit] = None
    housing_history: List[HousingUnit] = Field(default_factory=list)
    eviction_history: int = 0
    housing_stability_score: float = 0.0
    voucher_status: Optional[str] = None
    waitlist_positions: Dict[str, int] = Field(default_factory=dict)
    environmental_sensors: Dict[str, Any] = Field(default_factory=dict)  # Air quality, lead, mold
    climate_risk: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 6: Economic ────────────────────────────────────────────

class Employment(BaseModel):
    """Employment record"""
    employment_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employer: Optional[str] = None
    position: Optional[str] = None
    employment_type: str = ""              # full_time, part_time, gig, unemployed
    hourly_rate: float = 0.0
    hours_per_week: float = 0.0
    benefits: List[str] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    barriers: List[str] = Field(default_factory=list)


class DomeEconomicLayer(DomeLayer):
    """Layer 6: Economic — employment, skills, income trajectory"""
    layer_number: int = 6
    layer_name: str = "Economic"
    current_employment: Optional[Employment] = None
    employment_history: List[Employment] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    skills_gaps: List[str] = Field(default_factory=list)
    training_opportunities: List[str] = Field(default_factory=list)
    income_trajectory: Dict[str, Any] = Field(default_factory=dict)
    market_demand_match: float = 0.0       # How well skills match local demand


# ── Layer 7: Education ───────────────────────────────────────────

class EducationRecord(BaseModel):
    """Education record"""
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    institution: str
    level: str                             # elementary, secondary, ged, associate, bachelor, etc.
    status: str                            # completed, in_progress, withdrawn, planned
    year_completed: Optional[int] = None
    field: Optional[str] = None


class DomeEducationLayer(DomeLayer):
    """Layer 7: Education — credentials, learning paths, opportunity matching"""
    layer_number: int = 7
    layer_name: str = "Education"
    education_history: List[EducationRecord] = Field(default_factory=list)
    highest_level: str = ""
    current_enrollment: Optional[str] = None
    children_education: List[Dict[str, Any]] = Field(default_factory=list)  # Dependents' education
    learning_opportunities: List[str] = Field(default_factory=list)
    credential_gaps: List[str] = Field(default_factory=list)
    personalized_pathways: List[Dict[str, Any]] = Field(default_factory=list)


# ── Layer 8: Community ───────────────────────────────────────────

class CommunityConnection(BaseModel):
    """A community connection or resource"""
    connection_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    connection_type: str                   # family, friend, organization, faith, neighbor
    strength: str = "moderate"             # strong, moderate, weak
    resource_type: Optional[str] = None    # childcare, transport, emotional, financial
    reciprocal: bool = False               # Does person also give to this connection


class DomeCommunityLayer(DomeLayer):
    """Layer 8: Community — connections, assets, isolation risk"""
    layer_number: int = 8
    layer_name: str = "Community"
    connections: List[CommunityConnection] = Field(default_factory=list)
    community_assets: List[str] = Field(default_factory=list)
    isolation_risk_score: float = 0.0      # 0-100, higher = more isolated
    support_network_strength: float = 0.0
    neighborhood: Optional[str] = None
    community_organizations: List[str] = Field(default_factory=list)
    social_capital_score: float = 0.0


# ── Layer 9: Environment ─────────────────────────────────────────

class EnvironmentalReading(BaseModel):
    """An environmental sensor reading"""
    reading_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sensor_type: str                       # air_quality, water_quality, noise, lead, mold
    value: float
    unit: str
    safe_threshold: float
    location: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str                            # EPA, local, wearable, home_sensor


class DomeEnvironmentLayer(DomeLayer):
    """Layer 9: Environment — EPA sensors, air/water quality, food access, FEMA"""
    layer_number: int = 9
    layer_name: str = "Environment"
    readings: List[EnvironmentalReading] = Field(default_factory=list)
    air_quality_index: Optional[float] = None
    water_quality_score: Optional[float] = None
    food_access_score: float = 0.0         # USDA food desert metric
    flood_risk: Optional[str] = None
    heat_island_risk: Optional[str] = None
    nearest_park_distance: Optional[float] = None  # miles
    walkability_score: float = 0.0
    environmental_justice_score: float = 0.0
    fema_risk_data: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 10: Autonomy (HUMAN DESIGN REQUIRED) ──────────────────

class FrictionPoint(BaseModel):
    """A barrier between person and resources"""
    friction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    barrier: str
    resource_blocked: str
    severity: float = 0.0                  # 0-100
    removable_by_dome: bool = False
    removal_strategy: Optional[str] = None
    layers_affected: List[int] = Field(default_factory=list)


class DomeAutonomyLayer(DomeLayer):
    """Layer 10: Autonomy — HUMAN DESIGN REQUIRED

    What autonomy means for THIS person. Not abstract freedom —
    the specific ability to navigate their world without friction.
    AI agents map the friction. Humans design what autonomy looks like.
    """
    layer_number: int = 10
    layer_name: str = "Autonomy"
    # AI-mapped
    friction_points: List[FrictionPoint] = Field(default_factory=list)
    total_friction_score: float = 0.0      # Aggregate barrier measurement
    agency_indicators: Dict[str, Any] = Field(default_factory=dict)
    # Human-designed
    autonomy_definition: str = ""          # What autonomy means for THIS person
    autonomy_design: Dict[str, Any] = Field(default_factory=dict)
    design_rationale: str = ""


# ── Layer 11: Creativity (HUMAN DESIGN REQUIRED) ─────────────────

class CulturalResource(BaseModel):
    """A cultural resource in this person's landscape"""
    resource_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    resource_type: str                     # institution, practice, tradition, space, community
    relevance: str
    accessible: bool = True
    distance: Optional[float] = None


class DomeCreativityLayer(DomeLayer):
    """Layer 11: Creativity — HUMAN DESIGN REQUIRED

    How THIS person makes meaning. Not imposed creativity —
    the forms of expression, joy, and meaning-making that are already theirs.
    AI agents map cultural resources. Humans design meaning frameworks.
    """
    layer_number: int = 11
    layer_name: str = "Creativity"
    # AI-mapped
    cultural_resources: List[CulturalResource] = Field(default_factory=list)
    cultural_landscape: Dict[str, Any] = Field(default_factory=dict)
    # Human-designed
    meaning_framework: str = ""            # How this person makes meaning
    expression_forms: List[str] = Field(default_factory=list)
    creative_design: Dict[str, Any] = Field(default_factory=dict)
    design_rationale: str = ""


# ── Layer 12: Flourishing (HUMAN DESIGN REQUIRED) ────────────────

class FlourishingDimension(BaseModel):
    """A dimension of flourishing for this person"""
    dimension_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    definition: str                        # What this dimension means for THIS person
    current_state: float = 0.0             # 0-100
    target_state: float = 0.0              # 0-100
    contributing_layers: List[int] = Field(default_factory=list)
    trajectory: str = ""                   # improving, stable, declining


class DomeFlourishingLayer(DomeLayer):
    """Layer 12: Flourishing — HUMAN DESIGN REQUIRED

    What flourishing looks like HERE, for THIS person.
    The world model renders the complete dome — all 12 layers unified.
    Informed by science of awe and environmental psychology.
    Life trajectory simulation. Not a score — a living rendering.
    """
    layer_number: int = 12
    layer_name: str = "Flourishing"
    # Integrative
    flourishing_dimensions: List[FlourishingDimension] = Field(default_factory=list)
    life_trajectory: Dict[str, Any] = Field(default_factory=dict)
    # Human-designed
    flourishing_definition: str = ""       # What flourishing looks like for THIS person
    awe_research: Dict[str, Any] = Field(default_factory=dict)  # Science of awe inputs
    environmental_psychology: Dict[str, Any] = Field(default_factory=dict)
    world_model_design: Dict[str, Any] = Field(default_factory=dict)  # 3D environment spec
    design_rationale: str = ""


# ── Complete Dome Schema ─────────────────────────────────────────

class DomeSubject(BaseModel):
    """The person at the gravitational center"""
    name: str
    source: str                            # Book, film, journalism, case study
    source_citation: str
    situation: str
    full_landscape: str                    # Their full life — not just problems
    production_challenge: str
    key_systems: List[str] = Field(default_factory=list)
    flourishing_dimensions: List[str] = Field(default_factory=list)
    demographic: Dict[str, Any] = Field(default_factory=dict)
    location: Dict[str, Any] = Field(default_factory=dict)


class DomeSchema(BaseModel):
    """Complete DOME schema — a person as gravitational center with 12 layers.

    The dome is only as strong as its weakest layer.
    Every layer has five interfaces: Ingest, Process, State, Act, Export.
    Every layer has an AI capability map.
    Layers 1-9 are AI-fillable. Layers 10-12 require human design.
    """
    metadata: SchemaMetadata = Field(
        default_factory=lambda: SchemaMetadata(schema_type=GameType.DOMES, title="")
    )
    subject: DomeSubject = Field(default_factory=lambda: DomeSubject(
        name="", source="", source_citation="", situation="",
        full_landscape="", production_challenge=""
    ))

    # The 12 layers
    legal: DomeLegalLayer = Field(default_factory=DomeLegalLayer)
    systems: DomeSystemsLayer = Field(default_factory=DomeSystemsLayer)
    fiscal: DomeFiscalLayer = Field(default_factory=DomeFiscalLayer)
    health: DomeHealthLayer = Field(default_factory=DomeHealthLayer)
    housing: DomeHousingLayer = Field(default_factory=DomeHousingLayer)
    economic: DomeEconomicLayer = Field(default_factory=DomeEconomicLayer)
    education: DomeEducationLayer = Field(default_factory=DomeEducationLayer)
    community: DomeCommunityLayer = Field(default_factory=DomeCommunityLayer)
    environment: DomeEnvironmentLayer = Field(default_factory=DomeEnvironmentLayer)
    autonomy: DomeAutonomyLayer = Field(default_factory=DomeAutonomyLayer)
    creativity: DomeCreativityLayer = Field(default_factory=DomeCreativityLayer)
    flourishing: DomeFlourishingLayer = Field(default_factory=DomeFlourishingLayer)

    def get_layer(self, number: int) -> DomeLayer:
        """Get a layer by number (1-12)"""
        layers = {
            1: self.legal, 2: self.systems, 3: self.fiscal,
            4: self.health, 5: self.housing, 6: self.economic,
            7: self.education, 8: self.community, 9: self.environment,
            10: self.autonomy, 11: self.creativity, 12: self.flourishing,
        }
        return layers[number]

    def all_layers(self) -> List[DomeLayer]:
        """All 12 layers in order"""
        return [self.get_layer(i) for i in range(1, 13)]

    def weakest_layer(self) -> DomeLayer:
        """The dome is only as strong as its weakest layer"""
        return min(self.all_layers(), key=lambda l: l.score.completeness)

    def total_score(self) -> float:
        """Minimum completeness across all layers"""
        scores = [l.score.completeness for l in self.all_layers()]
        return min(scores) if scores else 0.0

    def ai_fillable_layers(self) -> List[DomeLayer]:
        """Layers 1-9: AI agents fill these"""
        return [self.get_layer(i) for i in range(1, 10)]

    def human_design_layers(self) -> List[DomeLayer]:
        """Layers 10-12: human creative teams design these"""
        return [self.get_layer(i) for i in range(10, 13)]


# ── AI Capability Maps ──────────────────────────────────────────

DOME_LAYER_DEFINITIONS: List[LayerDefinition] = [
    LayerDefinition(
        layer_number=1,
        name="Legal",
        description="Every right, every entitlement, every pathway",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=1,
            layer_name="Legal",
            capabilities=[
                AICapability(
                    name="legal_database_navigation",
                    description="Agentic AI navigating legal databases (Westlaw, LexisNexis, state statutes)",
                    category="agentic_ai",
                    maturity="available",
                    providers=["Westlaw Edge AI", "CaseText", "Harvey"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="benefits_eligibility_screening",
                    description="Automated screening across federal/state benefit programs",
                    category="analysis",
                    maturity="available",
                    providers=["Benefits.gov API", "SingleStop", "Aunt Bertha"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="application_filing_agent",
                    description="Computer use agents filing applications on government portals",
                    category="computer_use",
                    maturity="emerging",
                    providers=["Anthropic Computer Use", "OpenAI Operator"],
                    feeds_interface="act",
                    autonomous=False,
                ),
                AICapability(
                    name="legal_document_analysis",
                    description="NLP extraction of rights and obligations from legal documents",
                    category="analysis",
                    maturity="available",
                    providers=["Claude", "GPT-4"],
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=2,
        name="Systems",
        description="Every government system, every portal, every form",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=2,
            layer_name="Systems",
            capabilities=[
                AICapability(
                    name="portal_navigation_agent",
                    description="Computer use agents navigating government portals (SSA, SNAP, Medicaid)",
                    category="computer_use",
                    maturity="emerging",
                    providers=["Anthropic Computer Use", "OpenAI Operator"],
                    feeds_interface="act",
                ),
                AICapability(
                    name="cross_system_identity_resolution",
                    description="Resolving identity across fragmented government systems",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="form_completion_agent",
                    description="AI agents completing government forms with verified data",
                    category="computer_use",
                    maturity="emerging",
                    feeds_interface="act",
                ),
                AICapability(
                    name="system_fragmentation_analysis",
                    description="Mapping disconnections between government systems",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=3,
        name="Fiscal",
        description="Every cost, every saving, every financial instrument",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=3,
            layer_name="Fiscal",
            capabilities=[
                AICapability(
                    name="dome_bond_structuring",
                    description="Financial AI structuring Dome Bonds from coordination savings",
                    category="financial_ai",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="cost_modeling_agent",
                    description="Modeling cost of fragmentation vs. coordination",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="stress_testing_agent",
                    description="Stress testing dome bond structures against scenarios",
                    category="financial_ai",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="benefit_cliff_analysis",
                    description="Modeling benefit cliffs and income trajectory impacts",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=4,
        name="Health",
        description="Every diagnosis, every treatment, every trajectory",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=4,
            layer_name="Health",
            capabilities=[
                AICapability(
                    name="medical_ai_diagnostics",
                    description="AI-assisted diagnostic analysis from medical records",
                    category="medical_ai",
                    maturity="available",
                    providers=["Google Health AI", "PathAI", "Tempus"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="genomic_analysis",
                    description="Genomic data analysis for personalized medicine",
                    category="medical_ai",
                    maturity="emerging",
                    providers=["Illumina DRAGEN", "23andMe"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="wearable_sensor_integration",
                    description="Real-time health data from wearable devices",
                    category="sensor",
                    maturity="available",
                    providers=["Apple HealthKit", "Fitbit", "Oura"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="drug_interaction_modeling",
                    description="AI modeling of drug interactions and side effects",
                    category="medical_ai",
                    maturity="available",
                    providers=["DrugBank", "Epocrates"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="surgical_robotics_coordination",
                    description="Coordination with robotic surgical systems",
                    category="medical_ai",
                    maturity="speculative",
                    feeds_interface="act",
                ),
                AICapability(
                    name="personalized_medicine_agent",
                    description="AI agents generating personalized treatment recommendations",
                    category="medical_ai",
                    maturity="emerging",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=5,
        name="Housing",
        description="Every structure, every system, every environment",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=5,
            layer_name="Housing",
            capabilities=[
                AICapability(
                    name="environmental_sensors",
                    description="IoT sensors for air quality, lead, mold, radon in housing",
                    category="sensor",
                    maturity="available",
                    providers=["PurpleAir", "Awair", "Airthings"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="smart_building_systems",
                    description="Smart home/building management and monitoring",
                    category="sensor",
                    maturity="available",
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="drone_inspection",
                    description="Drone-based structural inspection and assessment",
                    category="robotics",
                    maturity="emerging",
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="climate_risk_modeling",
                    description="Climate risk assessment for housing location",
                    category="analysis",
                    maturity="available",
                    providers=["ClimateCheck", "First Street Foundation"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="housing_search_agent",
                    description="AI agent searching and filtering housing options",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="act",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=6,
        name="Economic",
        description="Every job, every skill, every income path",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=6,
            layer_name="Economic",
            capabilities=[
                AICapability(
                    name="employment_market_agent",
                    description="AI agents scanning employment markets and matching opportunities",
                    category="agentic_ai",
                    maturity="available",
                    providers=["LinkedIn AI", "Indeed", "ZipRecruiter"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="skills_gap_analysis",
                    description="AI analysis of skills gaps against market demand",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="income_trajectory_modeling",
                    description="Modeling income trajectories based on career paths",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="job_application_agent",
                    description="Computer use agent applying to jobs",
                    category="computer_use",
                    maturity="emerging",
                    feeds_interface="act",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=7,
        name="Education",
        description="Every credential, every learning path, every opportunity",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=7,
            layer_name="Education",
            capabilities=[
                AICapability(
                    name="personalized_learning_agent",
                    description="AI tutors and personalized learning path generators",
                    category="agentic_ai",
                    maturity="available",
                    providers=["Khan Academy AI", "Duolingo", "Coursera"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="credential_verification",
                    description="AI verification of credentials and equivalencies",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="opportunity_matching",
                    description="Matching education opportunities to person's trajectory",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="scholarship_search_agent",
                    description="AI agent scanning scholarship and financial aid databases",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="act",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=8,
        name="Community",
        description="Every connection, every asset, every risk",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=8,
            layer_name="Community",
            capabilities=[
                AICapability(
                    name="social_network_analysis",
                    description="Mapping social support networks and connection strength",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="community_asset_mapping",
                    description="Mapping community resources, organizations, and assets",
                    category="agentic_ai",
                    maturity="available",
                    providers=["211 API", "Aunt Bertha", "community databases"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="isolation_risk_detection",
                    description="Detecting social isolation risk factors",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=9,
        name="Environment",
        description="Every sensor, every reading, every exposure",
        schema_type=GameType.DOMES,
        ai_capability_map=AICapabilityMap(
            layer_number=9,
            layer_name="Environment",
            capabilities=[
                AICapability(
                    name="epa_sensor_network",
                    description="EPA AirNow, water quality monitoring networks",
                    category="sensor",
                    maturity="available",
                    providers=["EPA AirNow API", "EPA ECHO", "Water Quality Portal"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="hyperlocal_air_water_quality",
                    description="Hyperlocal air and water quality assessment",
                    category="sensor",
                    maturity="available",
                    providers=["PurpleAir", "Clarity Movement"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="usda_food_access",
                    description="USDA food access and food desert analysis",
                    category="analysis",
                    maturity="available",
                    providers=["USDA Food Access Research Atlas"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="fema_realtime",
                    description="FEMA real-time disaster and risk monitoring",
                    category="sensor",
                    maturity="available",
                    providers=["FEMA API", "National Weather Service"],
                    feeds_interface="ingest",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=10,
        name="Autonomy",
        description="What autonomy means for THIS person — friction mapping + human design",
        schema_type=GameType.DOMES,
        human_design_required=True,
        human_design_description="Friction mapping agents measure barriers between person and resources. Human design required for what autonomy means for this person.",
        ai_capability_map=AICapabilityMap(
            layer_number=10,
            layer_name="Autonomy",
            human_design_required=True,
            human_design_description="What autonomy means for THIS person",
            capabilities=[
                AICapability(
                    name="friction_mapping_agent",
                    description="Measuring barriers between person and resources across all layers",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="barrier_removal_agent",
                    description="Identifying and executing barrier removal strategies",
                    category="agentic_ai",
                    maturity="emerging",
                    feeds_interface="act",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=11,
        name="Creativity",
        description="How THIS person makes meaning — cultural mapping + human design",
        schema_type=GameType.DOMES,
        human_design_required=True,
        human_design_description="Cultural resource mapping by AI. Human design required for how this person makes meaning.",
        ai_capability_map=AICapabilityMap(
            layer_number=11,
            layer_name="Creativity",
            human_design_required=True,
            human_design_description="How THIS person makes meaning",
            capabilities=[
                AICapability(
                    name="cultural_resource_mapping",
                    description="Mapping cultural institutions, practices, and resources",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="ingest",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=12,
        name="Flourishing",
        description="What flourishing looks like HERE — world model + human design",
        schema_type=GameType.DOMES,
        human_design_required=True,
        human_design_description="World model rendering of complete dome, life trajectory simulation. Human design required for what flourishing looks like, informed by science of awe and environmental psychology.",
        ai_capability_map=AICapabilityMap(
            layer_number=12,
            layer_name="Flourishing",
            human_design_required=True,
            human_design_description="What flourishing looks like for THIS person",
            capabilities=[
                AICapability(
                    name="world_model_rendering",
                    description="Rendering complete dome as navigable 3D environment",
                    category="world_model",
                    maturity="speculative",
                    providers=["Google Genie", "DeepMind", "Three.js", "Cesium"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="life_trajectory_simulation",
                    description="Simulating life trajectories across all 12 layers",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="awe_research_integration",
                    description="Integrating science of awe and environmental psychology research",
                    category="research",
                    maturity="available",
                    feeds_interface="ingest",
                    human_required=True,
                ),
            ],
        ),
    ),
]
