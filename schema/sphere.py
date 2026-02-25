"""
BATHS Gravitational Schema — SPHERE

The place is the gravitational center.
10 layers surround it — each one a dimension of the space.
Layers 1-6: AI agents fill these. Every advancing capability feeds them.
Layers 7-10: Human creative teams design these. This is where art lives.
The sphere is only as alive as its weakest layer.

Layer 1:  Parcel          — ownership, zoning, boundaries, regulatory landscape
Layer 2:  Infrastructure  — utilities, structures, connectivity, access
Layer 3:  Environmental   — soil, air, water, ecology, microclimate
Layer 4:  Economic        — value, revenue, tax, financial instruments
Layer 5:  Social          — demographics, foot traffic, community assets
Layer 6:  Temporal        — history, seasons, time-of-day dynamics
Layer 7:  Activation      — HUMAN DESIGN: what happens in this space
Layer 8:  Permanence      — HUMAN DESIGN: what lasting elements remain
Layer 9:  Policy          — HUMAN DESIGN: what regulatory changes this inspires
Layer 10: Catalyst        — HUMAN DESIGN: what adjacent activations this sparks
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


# ── Base Sphere Layer ────────────────────────────────────────────

class SphereLayer(BaseModel):
    """Base class for all sphere layers. Every layer has the five interfaces."""
    layer_number: int
    layer_name: str
    interfaces: LayerInterface = Field(default_factory=LayerInterface)
    score: LayerScore = Field(default_factory=lambda: LayerScore(layer_number=0, layer_name=""))
    creative_inputs: List[CreativeInput] = Field(default_factory=list)  # For layers 7-10
    notes: str = ""


# ── Layer 1: Parcel ──────────────────────────────────────────────

class ParcelOwnership(BaseModel):
    """Ownership record for a parcel"""
    owner_name: str
    owner_type: str                        # individual, corporate, government, nonprofit, trust
    acquisition_date: Optional[datetime] = None
    acquisition_price: Optional[float] = None
    tax_status: str = ""                   # current, delinquent, exempt, in_rem
    liens: List[str] = Field(default_factory=list)


class ZoningDetail(BaseModel):
    """Zoning classification and restrictions"""
    classification: str                    # R-1, C-2, M-1, etc.
    description: str
    permitted_uses: List[str] = Field(default_factory=list)
    conditional_uses: List[str] = Field(default_factory=list)
    prohibited_uses: List[str] = Field(default_factory=list)
    max_height: Optional[float] = None
    max_lot_coverage: Optional[float] = None
    setback_requirements: Dict[str, float] = Field(default_factory=dict)
    overlay_districts: List[str] = Field(default_factory=list)
    variance_history: List[str] = Field(default_factory=list)


class SphereParcelLayer(SphereLayer):
    """Layer 1: Parcel — ownership, zoning, boundaries, regulatory landscape"""
    layer_number: int = 1
    layer_name: str = "Parcel"
    parcel_id: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    neighborhood: str = ""
    lot_size_sqft: float = 0.0
    lot_dimensions: Dict[str, float] = Field(default_factory=dict)
    coordinates: Optional[Dict[str, float]] = None  # lat, lng
    ownership: Optional[ParcelOwnership] = None
    zoning: Optional[ZoningDetail] = None
    easements: List[str] = Field(default_factory=list)
    adjacent_parcels: List[str] = Field(default_factory=list)
    regulatory_barriers: List[str] = Field(default_factory=list)


# ── Layer 2: Infrastructure ──────────────────────────────────────

class UtilityConnection(BaseModel):
    """A utility connection to the parcel"""
    utility_type: str                      # electric, gas, water, sewer, telecom, fiber
    provider: str
    status: str = "unknown"                # connected, available, unavailable, requires_upgrade
    capacity: Optional[str] = None
    monthly_cost: Optional[float] = None


class StructuralElement(BaseModel):
    """A structural element on the parcel"""
    element_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    element_type: str                      # building, wall, foundation, paving, fence
    condition: str = "unknown"             # good, fair, poor, hazardous, demolished
    age_years: Optional[int] = None
    material: Optional[str] = None
    area_sqft: Optional[float] = None
    inspection_date: Optional[datetime] = None
    inspection_notes: str = ""


class SphereInfrastructureLayer(SphereLayer):
    """Layer 2: Infrastructure — utilities, structures, connectivity, access"""
    layer_number: int = 2
    layer_name: str = "Infrastructure"
    utilities: List[UtilityConnection] = Field(default_factory=list)
    structures: List[StructuralElement] = Field(default_factory=list)
    total_built_sqft: float = 0.0
    connectivity_score: float = 0.0        # Digital connectivity assessment
    ada_accessible: bool = False
    transit_access: Dict[str, Any] = Field(default_factory=dict)
    parking: Dict[str, Any] = Field(default_factory=dict)
    pedestrian_access: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 3: Environmental ───────────────────────────────────────

class SoilAnalysis(BaseModel):
    """Soil analysis results"""
    sample_date: Optional[datetime] = None
    soil_type: str = ""
    contamination: List[str] = Field(default_factory=list)
    remediation_needed: bool = False
    remediation_cost_estimate: Optional[float] = None
    ph_level: Optional[float] = None
    permeability: Optional[str] = None


class EcologyAssessment(BaseModel):
    """Ecology assessment of the parcel"""
    species_present: List[str] = Field(default_factory=list)
    protected_species: List[str] = Field(default_factory=list)
    tree_canopy_coverage: float = 0.0
    impervious_surface_ratio: float = 0.0
    green_infrastructure: List[str] = Field(default_factory=list)
    habitat_value: str = "unknown"         # high, moderate, low, none


class SphereEnvironmentalLayer(SphereLayer):
    """Layer 3: Environmental — soil, air, water, ecology, microclimate"""
    layer_number: int = 3
    layer_name: str = "Environmental"
    soil: Optional[SoilAnalysis] = None
    air_quality_index: Optional[float] = None
    noise_level_db: Optional[float] = None
    water_table_depth: Optional[float] = None
    flood_zone: Optional[str] = None
    microclimate: Dict[str, Any] = Field(default_factory=dict)  # sun exposure, wind patterns
    ecology: Optional[EcologyAssessment] = None
    environmental_hazards: List[str] = Field(default_factory=list)
    epa_brownfield: bool = False
    remediation_status: Optional[str] = None


# ── Layer 4: Economic ────────────────────────────────────────────

class PropertyValuation(BaseModel):
    """Property valuation record"""
    assessed_value: float = 0.0
    market_value: float = 0.0
    valuation_date: Optional[datetime] = None
    valuation_method: str = ""
    comparable_sales: List[Dict[str, Any]] = Field(default_factory=list)
    value_trend: str = ""                  # increasing, stable, decreasing


class ChronBond(BaseModel):
    """Financial instrument representing sphere activation value"""
    bond_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    face_value: float
    coupon_rate: float
    maturity_years: int
    rating: str
    chron_score_at_issuance: float
    sqft_backing: float
    yield_to_maturity: float
    stress_test_results: Dict[str, Any] = Field(default_factory=dict)


class SphereEconomicLayer(SphereLayer):
    """Layer 4: Economic — value, revenue, tax, financial instruments, Chron Bonds"""
    layer_number: int = 4
    layer_name: str = "Economic"
    valuation: Optional[PropertyValuation] = None
    annual_tax: float = 0.0
    tax_delinquent: bool = False
    revenue_projections: Dict[str, Any] = Field(default_factory=dict)
    economic_impact_estimate: float = 0.0
    activation_cost_estimate: float = 0.0
    roi_projection: Dict[str, Any] = Field(default_factory=dict)
    chron_bond: Optional[ChronBond] = None
    nearby_property_impact: Dict[str, Any] = Field(default_factory=dict)


# ── Layer 5: Social ──────────────────────────────────────────────

class DemographicProfile(BaseModel):
    """Demographic profile of surrounding area"""
    population_radius: float = 0.25        # miles
    total_population: int = 0
    median_income: float = 0.0
    poverty_rate: float = 0.0
    age_distribution: Dict[str, float] = Field(default_factory=dict)
    race_ethnicity: Dict[str, float] = Field(default_factory=dict)
    education_levels: Dict[str, float] = Field(default_factory=dict)
    housing_tenure: Dict[str, float] = Field(default_factory=dict)  # own vs rent


class CommunityAsset(BaseModel):
    """A community asset near the parcel"""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    asset_type: str                        # school, park, library, health_center, etc.
    distance_miles: float = 0.0
    description: str = ""


class SphereSocialLayer(SphereLayer):
    """Layer 5: Social — demographics, foot traffic, community assets"""
    layer_number: int = 5
    layer_name: str = "Social"
    demographics: Optional[DemographicProfile] = None
    foot_traffic: Dict[str, Any] = Field(default_factory=dict)  # Hourly/daily patterns
    community_assets: List[CommunityAsset] = Field(default_factory=list)
    community_needs: List[str] = Field(default_factory=list)
    stakeholder_map: Dict[str, Any] = Field(default_factory=dict)
    community_engagement_history: List[Dict[str, Any]] = Field(default_factory=list)
    safety_score: float = 0.0


# ── Layer 6: Temporal ────────────────────────────────────────────

class HistoricalUse(BaseModel):
    """A historical use of the parcel"""
    use_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    period: str                            # e.g. "1950-1975"
    use_type: str                          # residential, industrial, commercial, vacant, agricultural
    description: str
    notable_events: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)


class SeasonalPattern(BaseModel):
    """A seasonal pattern at the parcel"""
    season: str                            # spring, summer, fall, winter
    sun_hours: float = 0.0
    temperature_range: Dict[str, float] = Field(default_factory=dict)
    precipitation: float = 0.0
    foot_traffic_modifier: float = 1.0     # Multiplier on base foot traffic
    activation_suitability: str = ""       # How suitable for activation this season


class SphereTemporalLayer(SphereLayer):
    """Layer 6: Temporal — history, seasons, time-of-day dynamics"""
    layer_number: int = 6
    layer_name: str = "Temporal"
    historical_uses: List[HistoricalUse] = Field(default_factory=list)
    seasonal_patterns: List[SeasonalPattern] = Field(default_factory=list)
    time_of_day_dynamics: Dict[str, Any] = Field(default_factory=dict)  # Morning/afternoon/evening/night
    cultural_significance: List[str] = Field(default_factory=list)
    years_vacant: Optional[int] = None
    temporal_narrative: str = ""           # The story of this place through time


# ── Layer 7: Activation (HUMAN DESIGN REQUIRED) ─────────────────

class ActivationConcept(BaseModel):
    """A specific activation concept for the space"""
    concept_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    experience_type: str                   # installation, performance, gathering, market, garden, etc.
    duration: str                          # permanent, temporary, recurring, pop_up
    capacity: Optional[int] = None
    accessibility: str = ""
    awe_triggers: List[str] = Field(default_factory=list)  # Measurable via environmental psychology
    emotional_journey: List[str] = Field(default_factory=list)  # Arc of visitor experience
    transformation_arc: str = ""           # How visitor changes through the experience


class AweMetric(BaseModel):
    """Measurement from science of awe research"""
    metric_name: str
    measurement_method: str
    baseline: Optional[float] = None
    target: Optional[float] = None
    research_source: str = ""


class SphereActivationLayer(SphereLayer):
    """Layer 7: Activation — HUMAN DESIGN REQUIRED

    What happens in this space. Not just programming —
    the complete experience design informed by science of awe,
    experience design research, and measurable awe metrics.
    """
    layer_number: int = 7
    layer_name: str = "Activation"
    # Human-designed
    activation_concepts: List[ActivationConcept] = Field(default_factory=list)
    experience_design: Dict[str, Any] = Field(default_factory=dict)
    awe_metrics: List[AweMetric] = Field(default_factory=list)
    awe_research_sources: List[str] = Field(default_factory=list)
    design_rationale: str = ""


# ── Layer 8: Permanence (HUMAN DESIGN REQUIRED) ─────────────────

class PermanentElement(BaseModel):
    """A lasting element that remains after activation"""
    element_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    element_type: str                      # physical, cultural, institutional, ecological
    description: str
    lifespan: str                          # years, decades, permanent
    maintenance_requirements: str = ""
    community_ownership: str = ""          # Who stewards this element


class SpherePermanenceLayer(SphereLayer):
    """Layer 8: Permanence — HUMAN DESIGN REQUIRED

    What lasting elements remain — physical and cultural.
    The sphere's permanence is what compounds over time.
    """
    layer_number: int = 8
    layer_name: str = "Permanence"
    # Human-designed
    permanent_elements: List[PermanentElement] = Field(default_factory=list)
    cultural_permanence: Dict[str, Any] = Field(default_factory=dict)
    institutional_permanence: Dict[str, Any] = Field(default_factory=dict)
    ecological_permanence: Dict[str, Any] = Field(default_factory=dict)
    stewardship_model: str = ""
    design_rationale: str = ""


# ── Layer 9: Policy (HUMAN DESIGN REQUIRED) ──────────────────────

class PolicyChange(BaseModel):
    """A policy change this activation inspires"""
    policy_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    policy_level: str                      # municipal, county, state, federal
    policy_type: str                       # ordinance, regulation, executive_order, legislation
    status: str = "proposed"               # proposed, drafted, introduced, passed, implemented
    ordinance_text: str = ""
    jurisdiction: str = ""
    replicability_score: float = 0.0       # 0-100, how easily other jurisdictions can adopt


class SpherePolicyLayer(SphereLayer):
    """Layer 9: Policy — HUMAN DESIGN REQUIRED

    What regulatory changes this activation inspires.
    Model ordinances that other jurisdictions can adopt.
    """
    layer_number: int = 9
    layer_name: str = "Policy"
    # Human-designed
    policy_changes: List[PolicyChange] = Field(default_factory=list)
    ordinance_models: List[Dict[str, Any]] = Field(default_factory=list)
    regulatory_innovation: str = ""
    policy_brief: str = ""
    design_rationale: str = ""


# ── Layer 10: Catalyst (HUMAN DESIGN REQUIRED) ──────────────────

class AdjacentActivation(BaseModel):
    """An adjacent activation this sphere sparks"""
    activation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    location: str                          # Address or area
    distance_miles: float = 0.0
    connection_type: str                   # inspired_by, extension_of, complementary, responsive
    status: str = "potential"              # potential, planned, active, completed
    network_effect: str = ""               # How this connects back


class SphereCatalystLayer(SphereLayer):
    """Layer 10: Catalyst — HUMAN DESIGN REQUIRED

    What adjacent activations this sparks. Network effects.
    One sphere activates others. The ripple is the catalyst.
    """
    layer_number: int = 10
    layer_name: str = "Catalyst"
    # Human-designed
    adjacent_activations: List[AdjacentActivation] = Field(default_factory=list)
    network_effects: Dict[str, Any] = Field(default_factory=dict)
    ripple_radius: float = 0.0             # How far the catalyst reaches (miles)
    economic_multiplier: float = 1.0       # Economic multiplier effect
    catalyst_narrative: str = ""
    design_rationale: str = ""


# ── Complete Sphere Schema ───────────────────────────────────────

class SphereSubject(BaseModel):
    """The place at the gravitational center"""
    address: str
    neighborhood: str
    city: str
    state: str = ""
    parcel_id: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None  # lat, lng
    lot_size_sqft: float = 0.0
    history: str                           # What this space has been
    opportunity: str                       # What activation could look like
    community_context: str                 # Who lives nearby, what they need
    constraints: List[str] = Field(default_factory=list)


class SphereSchema(BaseModel):
    """Complete SPHERE schema — a place as gravitational center with 10 layers.

    The sphere is only as alive as its weakest layer.
    Every layer has five interfaces: Ingest, Process, State, Act, Export.
    Every layer has an AI capability map.
    Layers 1-6 are AI-fillable. Layers 7-10 require human design.
    """
    metadata: SchemaMetadata = Field(
        default_factory=lambda: SchemaMetadata(schema_type=GameType.SPHERES, title="")
    )
    subject: SphereSubject = Field(default_factory=lambda: SphereSubject(
        address="", neighborhood="", city="",
        history="", opportunity="", community_context=""
    ))

    # The 10 layers
    parcel: SphereParcelLayer = Field(default_factory=SphereParcelLayer)
    infrastructure: SphereInfrastructureLayer = Field(default_factory=SphereInfrastructureLayer)
    environmental: SphereEnvironmentalLayer = Field(default_factory=SphereEnvironmentalLayer)
    economic: SphereEconomicLayer = Field(default_factory=SphereEconomicLayer)
    social: SphereSocialLayer = Field(default_factory=SphereSocialLayer)
    temporal: SphereTemporalLayer = Field(default_factory=SphereTemporalLayer)
    activation: SphereActivationLayer = Field(default_factory=SphereActivationLayer)
    permanence: SpherePermanenceLayer = Field(default_factory=SpherePermanenceLayer)
    policy: SpherePolicyLayer = Field(default_factory=SpherePolicyLayer)
    catalyst: SphereCatalystLayer = Field(default_factory=SphereCatalystLayer)

    def get_layer(self, number: int) -> SphereLayer:
        """Get a layer by number (1-10)"""
        layers = {
            1: self.parcel, 2: self.infrastructure, 3: self.environmental,
            4: self.economic, 5: self.social, 6: self.temporal,
            7: self.activation, 8: self.permanence,
            9: self.policy, 10: self.catalyst,
        }
        return layers[number]

    def all_layers(self) -> List[SphereLayer]:
        """All 10 layers in order"""
        return [self.get_layer(i) for i in range(1, 11)]

    def weakest_layer(self) -> SphereLayer:
        """The sphere is only as alive as its weakest layer"""
        return min(self.all_layers(), key=lambda l: l.score.completeness)

    def total_score(self) -> float:
        """Minimum completeness across all layers"""
        scores = [l.score.completeness for l in self.all_layers()]
        return min(scores) if scores else 0.0

    def ai_fillable_layers(self) -> List[SphereLayer]:
        """Layers 1-6: AI agents fill these"""
        return [self.get_layer(i) for i in range(1, 7)]

    def human_design_layers(self) -> List[SphereLayer]:
        """Layers 7-10: human creative teams design these"""
        return [self.get_layer(i) for i in range(7, 11)]


# ── AI Capability Maps ──────────────────────────────────────────

SPHERE_LAYER_DEFINITIONS: List[LayerDefinition] = [
    LayerDefinition(
        layer_number=1,
        name="Parcel",
        description="Ownership, zoning, boundaries, regulatory landscape",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=1,
            layer_name="Parcel",
            capabilities=[
                AICapability(
                    name="parcel_database_agent",
                    description="Agentic AI navigating parcel databases, deed records, and property registries",
                    category="agentic_ai",
                    maturity="available",
                    providers=["County assessor APIs", "Regrid", "CoreLogic"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="zoning_analysis_agent",
                    description="AI analysis of zoning codes, overlay districts, and permitted uses",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="ownership_research_agent",
                    description="Tracing ownership history, liens, and encumbrances",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="permit_filing_agent",
                    description="Computer use agent filing permits and variance applications",
                    category="computer_use",
                    maturity="emerging",
                    feeds_interface="act",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=2,
        name="Infrastructure",
        description="Utilities, structures, connectivity, access",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=2,
            layer_name="Infrastructure",
            capabilities=[
                AICapability(
                    name="utility_mapping_agent",
                    description="Mapping utility connections, capacity, and upgrade paths",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="structural_analysis_ai",
                    description="AI-assisted structural analysis from photos, plans, and inspections",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="connectivity_assessment",
                    description="Digital connectivity and broadband assessment",
                    category="analysis",
                    maturity="available",
                    providers=["FCC Broadband Map", "Ookla"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="drone_site_survey",
                    description="Drone-based site survey and 3D mapping",
                    category="robotics",
                    maturity="emerging",
                    feeds_interface="ingest",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=3,
        name="Environmental",
        description="Soil, air, water, ecology, microclimate",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=3,
            layer_name="Environmental",
            capabilities=[
                AICapability(
                    name="epa_sensor_integration",
                    description="EPA environmental monitoring and brownfield database integration",
                    category="sensor",
                    maturity="available",
                    providers=["EPA Envirofacts", "EPA ECHO", "EPA Brownfields"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="soil_analysis_ai",
                    description="AI interpretation of soil samples and contamination assessment",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="microclimate_modeling",
                    description="Microclimate modeling — sun exposure, wind, urban heat island",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="ecology_assessment_ai",
                    description="AI assessment of local ecology, species, and habitat value",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=4,
        name="Economic",
        description="Value, revenue, tax, financial instruments, Chron Bonds",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=4,
            layer_name="Economic",
            capabilities=[
                AICapability(
                    name="property_value_modeling",
                    description="AI property valuation and comparable sales analysis",
                    category="financial_ai",
                    maturity="available",
                    providers=["Zillow API", "CoreLogic", "HouseCanary"],
                    feeds_interface="process",
                ),
                AICapability(
                    name="revenue_projection_agent",
                    description="Revenue and economic impact projection for activations",
                    category="financial_ai",
                    maturity="emerging",
                    feeds_interface="process",
                ),
                AICapability(
                    name="tax_analysis_agent",
                    description="Property tax analysis, TIF districts, abatement opportunities",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="chron_bond_structuring",
                    description="Financial AI structuring Chron Bonds from activation value",
                    category="financial_ai",
                    maturity="emerging",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=5,
        name="Social",
        description="Demographics, foot traffic, community assets",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=5,
            layer_name="Social",
            capabilities=[
                AICapability(
                    name="demographic_analysis_agent",
                    description="Census and ACS demographic analysis for surrounding area",
                    category="analysis",
                    maturity="available",
                    providers=["Census API", "ACS", "PolicyMap"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="foot_traffic_modeling",
                    description="Foot traffic modeling from mobile data and transit patterns",
                    category="analysis",
                    maturity="available",
                    providers=["SafeGraph", "Placer.ai"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="community_asset_mapping",
                    description="Mapping nearby schools, parks, libraries, health centers",
                    category="agentic_ai",
                    maturity="available",
                    providers=["Google Places", "OpenStreetMap", "211"],
                    feeds_interface="ingest",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=6,
        name="Temporal",
        description="History, seasons, time-of-day dynamics",
        schema_type=GameType.SPHERES,
        ai_capability_map=AICapabilityMap(
            layer_number=6,
            layer_name="Temporal",
            capabilities=[
                AICapability(
                    name="historical_use_research",
                    description="AI research into historical land use from Sanborn maps, deed records, newspapers",
                    category="agentic_ai",
                    maturity="available",
                    providers=["Library of Congress", "Newspapers.com", "local archives"],
                    feeds_interface="ingest",
                ),
                AICapability(
                    name="seasonal_pattern_analysis",
                    description="Analysis of seasonal patterns — weather, activity, suitability",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
                AICapability(
                    name="time_of_day_dynamics",
                    description="Modeling time-of-day dynamics — light, activity, safety",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=7,
        name="Activation",
        description="What happens in this space — experience design + science of awe",
        schema_type=GameType.SPHERES,
        human_design_required=True,
        human_design_description="What happens in this space, informed by science of awe, experience design research, awe metrics",
        ai_capability_map=AICapabilityMap(
            layer_number=7,
            layer_name="Activation",
            human_design_required=True,
            human_design_description="What happens in this space",
            capabilities=[
                AICapability(
                    name="experience_design_research",
                    description="Research agent scanning awe science, environmental psychology literature",
                    category="research",
                    maturity="available",
                    feeds_interface="ingest",
                    human_required=True,
                ),
                AICapability(
                    name="awe_measurement",
                    description="Sensor-based measurement of awe responses (physiological, behavioral)",
                    category="sensor",
                    maturity="speculative",
                    feeds_interface="ingest",
                    human_required=True,
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=8,
        name="Permanence",
        description="What lasting elements remain — physical and cultural",
        schema_type=GameType.SPHERES,
        human_design_required=True,
        human_design_description="What lasting elements remain, physical and cultural",
        ai_capability_map=AICapabilityMap(
            layer_number=8,
            layer_name="Permanence",
            human_design_required=True,
            human_design_description="What lasting elements remain",
            capabilities=[
                AICapability(
                    name="material_durability_analysis",
                    description="AI analysis of material durability and maintenance projections",
                    category="analysis",
                    maturity="available",
                    feeds_interface="process",
                    human_required=True,
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=9,
        name="Policy",
        description="What regulatory changes this activation inspires — model ordinances",
        schema_type=GameType.SPHERES,
        human_design_required=True,
        human_design_description="What regulatory changes this activation inspires, model ordinances",
        ai_capability_map=AICapabilityMap(
            layer_number=9,
            layer_name="Policy",
            human_design_required=True,
            human_design_description="What regulatory changes this inspires",
            capabilities=[
                AICapability(
                    name="policy_precedent_research",
                    description="Research agent scanning policy databases for precedents and models",
                    category="research",
                    maturity="available",
                    feeds_interface="ingest",
                    human_required=True,
                ),
                AICapability(
                    name="model_ordinance_drafting",
                    description="AI-assisted drafting of model ordinances from activation outcomes",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                    human_required=True,
                ),
            ],
        ),
    ),
    LayerDefinition(
        layer_number=10,
        name="Catalyst",
        description="What adjacent activations this sparks — network effects",
        schema_type=GameType.SPHERES,
        human_design_required=True,
        human_design_description="What adjacent activations this sparks, network effects",
        ai_capability_map=AICapabilityMap(
            layer_number=10,
            layer_name="Catalyst",
            human_design_required=True,
            human_design_description="What adjacent activations this sparks",
            capabilities=[
                AICapability(
                    name="network_effect_modeling",
                    description="Modeling ripple effects and adjacent activation potential",
                    category="analysis",
                    maturity="emerging",
                    feeds_interface="process",
                    human_required=True,
                ),
                AICapability(
                    name="adjacent_parcel_scanning",
                    description="Scanning adjacent parcels for activation readiness",
                    category="agentic_ai",
                    maturity="available",
                    feeds_interface="ingest",
                    human_required=True,
                ),
            ],
        ),
    ),
]
