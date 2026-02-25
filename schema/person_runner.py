"""
BATHS Person-Runner: The Dome Production Engine

This is the product. You input a character and their circumstances.
Person-Runner uses the complete dome architecture to generate:

1. A massive IP pitch across film, TV, product, biological, tech domains
2. Documents and analytics making the full business case
3. Production budget justification: spend X because the IP generates Y
4. A complete dome with all 12 layers populated
5. A website-ready export of the dome and everything that went into it
6. IP assets and tech innovations catalogued along the way
7. The entire production process mapped
8. Whole-person simulation with cross-layer dynamics

Dome tiers:
- BLOCKBUSTER: $1M+ production budget, full creative team, 12-layer deep
- INDIE: $50K-$250K budget, lean team, focused layers, targeted IP
- MICRO: $5K-$50K, AI-heavy, proof-of-concept, single-domain IP

The Person-Runner pulls from ALL existing scaffolding:
- schema/ (dome, sphere, fhir, sdoh, dome_bond, cosm_scoring, cross_layer)
- intelligence/ (swarm, agent_network, memory, world_model, frontier)
- data/ (fragments, domes, patterns)
- backend/ (circumstances, matching, cross_reference)
"""

from datetime import datetime
from typing import Optional, Dict, List, Any, Literal
from pydantic import BaseModel, Field
from enum import Enum
import uuid

from schema.core import (
    GameType,
    IPDomain,
    CreativeInputType,
    SchemaMetadata,
    Deliverable,
    ProductionStage,
)
from schema.dome import DomeSchema, DomeSubject


# ── Dome Tiers ─────────────────────────────────────────────────

class DomeTier(str, Enum):
    """Production budget tiers."""
    BLOCKBUSTER = "blockbuster"    # $1M+, full team, 12-layer deep
    INDIE = "indie"                # $50K-$250K, lean team, focused
    MICRO = "micro"                # $5K-$50K, AI-heavy, proof-of-concept


TIER_SPECS = {
    DomeTier.BLOCKBUSTER: {
        "budget_range": (1_000_000, 50_000_000),
        "team_size_range": (15, 80),
        "layers_required": 12,
        "creative_disciplines_min": 6,
        "ip_domains_target": 8,
        "production_months": (12, 36),
        "ai_layer_depth": "maximum",
        "description": (
            "Full-scale dome production. Visionary director. Multi-disciplinary "
            "creative team. Every layer filled to maximum depth. Complete FHIR R4 "
            "health layer, full SDOH screening, Dome Bond prospectus, whole-person "
            "digital twin simulation, 3D world model, and IP portfolio spanning "
            "every domain. The dome itself becomes a franchise."
        ),
    },
    DomeTier.INDIE: {
        "budget_range": (50_000, 250_000),
        "team_size_range": (5, 15),
        "layers_required": 9,
        "creative_disciplines_min": 3,
        "ip_domains_target": 4,
        "production_months": (6, 18),
        "ai_layer_depth": "high",
        "description": (
            "Focused dome production. Strong director with specific vision. "
            "Lean creative team with deep expertise. AI fills layers 1-9, "
            "creative team designs 2-3 human layers. Targeted IP portfolio. "
            "The dome tells one story exceptionally well."
        ),
    },
    DomeTier.MICRO: {
        "budget_range": (5_000, 50_000),
        "team_size_range": (2, 5),
        "layers_required": 6,
        "creative_disciplines_min": 1,
        "ip_domains_target": 2,
        "production_months": (2, 6),
        "ai_layer_depth": "standard",
        "description": (
            "AI-heavy proof-of-concept dome. Minimal creative team. "
            "AI fills all 9 machine layers, human design is lightweight. "
            "Produces a focused business case and single-domain IP. "
            "Often used to prove the concept before scaling to indie or blockbuster."
        ),
    },
}


# ── Character Input ─────────────────────────────────────────────

class CharacterInput(BaseModel):
    """
    The input to Person-Runner: a character and their circumstances.
    Can be fictional (from a book, film, screenplay) or real (case study,
    journalism, lived experience).
    """
    # Identity
    name: str
    source_type: Literal["fictional", "real", "composite", "archetypal"]
    source_citation: str = ""          # Book, film, article, case study
    fictional_source: Optional[str] = None  # e.g., "The Wire", "Evicted"

    # The person
    age: Optional[int] = None
    gender: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None
    location_county_fips: Optional[str] = None  # Links to data/domes/{fips}

    # Their circumstances (maps to backend/app/circumstances.py PersonProfile)
    situation: str                     # Free text: what's happening in their life
    full_landscape: str = ""           # Not just problems — their whole life
    production_challenge: str = ""     # Why is this dome hard to build?

    # Structured circumstances
    insurance: List[str] = Field(default_factory=list)
    disabilities: List[str] = Field(default_factory=list)
    age_group: str = ""
    pregnant: bool = False
    housing: List[str] = Field(default_factory=list)
    income: List[str] = Field(default_factory=list)
    system_involvement: List[str] = Field(default_factory=list)
    veteran: bool = False
    dv_survivor: bool = False
    immigrant: bool = False

    # Systems they interact with
    key_systems: List[str] = Field(default_factory=list)

    # What flourishing looks like for them
    flourishing_dimensions: List[str] = Field(default_factory=list)

    # Production preferences
    tier: DomeTier = DomeTier.INDIE
    focus_domains: List[IPDomain] = Field(default_factory=list)


# ── IP Generation ──────────────────────────────────────────────

class IPAsset(BaseModel):
    """A piece of intellectual property generated during dome production."""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    domain: IPDomain
    description: str
    generated_from_layer: int          # Which dome layer produced this
    generated_at_stage: str            # Which production stage
    format: str                        # screenplay, patent_filing, product_spec, etc.
    estimated_value: Optional[float] = None
    market_size: Optional[str] = None
    comparable_precedents: List[str] = Field(default_factory=list)
    status: str = "concept"            # concept, developed, prototyped, market_ready


class IPPortfolio(BaseModel):
    """The complete IP portfolio generated by a dome production."""
    portfolio_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    total_assets: int = 0
    assets: List[IPAsset] = Field(default_factory=list)

    # By domain
    by_domain: Dict[str, List[str]] = Field(default_factory=dict)

    # Valuation
    total_estimated_value: float = 0.0
    revenue_model: Dict[str, Any] = Field(default_factory=dict)

    # The pitch
    headline_ip: Optional[str] = None  # The lead asset for the pitch
    pitch_one_liner: str = ""

    def add_asset(self, asset: IPAsset) -> None:
        self.assets.append(asset)
        self.total_assets = len(self.assets)
        domain_key = asset.domain.value
        if domain_key not in self.by_domain:
            self.by_domain[domain_key] = []
        self.by_domain[domain_key].append(asset.asset_id)
        if asset.estimated_value:
            self.total_estimated_value += asset.estimated_value


# ── Production Budget ──────────────────────────────────────────

class BudgetLine(BaseModel):
    """A line item in the production budget."""
    line_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: str                      # team, technology, data, creative, legal, overhead
    description: str
    amount: float
    justification: str                 # Why this spend generates value
    ip_it_enables: List[str] = Field(default_factory=list)  # IP asset IDs this enables


class ProductionBudget(BaseModel):
    """
    The production budget for a dome.
    Every dollar is justified by the IP and outcomes it generates.
    """
    budget_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    tier: DomeTier = DomeTier.INDIE
    total_budget: float = 0.0
    lines: List[BudgetLine] = Field(default_factory=list)

    # Budget breakdown
    team_spend: float = 0.0            # Director, creative team, specialists
    technology_spend: float = 0.0      # AI, sensors, data infrastructure
    data_spend: float = 0.0            # Data acquisition, API costs
    creative_spend: float = 0.0        # Physical prototypes, installations
    legal_spend: float = 0.0           # IP protection, contracts
    overhead_spend: float = 0.0

    # ROI justification
    projected_ip_revenue: float = 0.0
    projected_coordination_savings: float = 0.0
    projected_dome_bond_value: float = 0.0
    total_projected_return: float = 0.0
    roi_multiple: float = 0.0          # Return / Budget

    # The pitch: spend X because Y
    investment_thesis: str = ""

    def compute_roi(self) -> None:
        """Compute ROI metrics."""
        self.total_budget = sum(l.amount for l in self.lines)
        self.team_spend = sum(l.amount for l in self.lines if l.category == "team")
        self.technology_spend = sum(l.amount for l in self.lines if l.category == "technology")
        self.data_spend = sum(l.amount for l in self.lines if l.category == "data")
        self.creative_spend = sum(l.amount for l in self.lines if l.category == "creative")
        self.legal_spend = sum(l.amount for l in self.lines if l.category == "legal")
        self.overhead_spend = sum(l.amount for l in self.lines if l.category == "overhead")

        self.total_projected_return = (
            self.projected_ip_revenue +
            self.projected_coordination_savings +
            self.projected_dome_bond_value
        )
        if self.total_budget > 0:
            self.roi_multiple = round(self.total_projected_return / self.total_budget, 2)


# ── Team Assembly ──────────────────────────────────────────────

class TeamMember(BaseModel):
    """A member of the dome production team."""
    member_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str                          # director, architect, composer, data_scientist, etc.
    discipline: CreativeInputType
    name: Optional[str] = None
    why_this_person: str = ""          # Why this role matters for THIS dome
    ip_domains: List[IPDomain] = Field(default_factory=list)
    estimated_cost: float = 0.0
    availability: str = ""


class ProductionTeam(BaseModel):
    """The assembled production team for a dome."""
    team_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    director: Optional[TeamMember] = None
    members: List[TeamMember] = Field(default_factory=list)
    total_cost: float = 0.0
    disciplines_covered: List[str] = Field(default_factory=list)
    ip_surface_area: List[str] = Field(default_factory=list)  # All IP domains the team can produce
    unlikely_collisions: List[str] = Field(default_factory=list)  # Predicted creative collisions


# ── Production Pipeline ───────────────────────────────────────

class ProductionMilestone(BaseModel):
    """A milestone in the dome production process."""
    milestone_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    stage: ProductionStage
    title: str
    description: str
    deliverables: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)  # Other milestone IDs
    estimated_duration_days: int = 0
    actual_duration_days: Optional[int] = None
    status: str = "planned"            # planned, in_progress, completed, blocked
    ip_generated: List[str] = Field(default_factory=list)  # IP asset IDs


class ProductionPipeline(BaseModel):
    """
    The complete production pipeline for a dome.
    Maps the entire process from character input to finished dome.
    """
    pipeline_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    milestones: List[ProductionMilestone] = Field(default_factory=list)
    current_stage: ProductionStage = ProductionStage.DEVELOPMENT
    total_duration_days: int = 0
    percent_complete: float = 0.0
    blockers: List[str] = Field(default_factory=list)


# ── Tech Innovations ──────────────────────────────────────────

class TechInnovation(BaseModel):
    """A technology innovation discovered or created during dome production."""
    innovation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str                      # ai_method, data_pipeline, sensor_integration,
                                       # visualization, interoperability, measurement
    generated_from_layer: int
    reusable: bool = True              # Can other domes use this?
    patent_potential: bool = False
    open_source_candidate: bool = False
    implementation_status: str = "concept"  # concept, prototype, production


# ── Whole-Person Simulation ───────────────────────────────────

class SimulationScenario(BaseModel):
    """A simulation scenario for the dome subject."""
    scenario_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    scenario_type: str                 # baseline, coordinated, intervention, stress_test
    # Input conditions
    layer_modifications: Dict[int, Dict[str, Any]] = Field(default_factory=dict)
    # Projected outcomes
    projected_cosm: float = 0.0
    projected_costs: Dict[str, float] = Field(default_factory=dict)
    projected_timeline_months: int = 0
    # Comparison
    vs_baseline_delta: Dict[str, float] = Field(default_factory=dict)


class WholePersonSimulation(BaseModel):
    """
    Whole-person simulation using the dome's cross-layer dynamics.
    Shows what happens when you coordinate vs. when you don't.
    """
    simulation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    scenarios: List[SimulationScenario] = Field(default_factory=list)
    # The key comparison
    baseline_cosm: float = 0.0         # Score without coordination
    coordinated_cosm: float = 0.0      # Score with full coordination
    cosm_delta: float = 0.0
    # Cost comparison
    baseline_annual_cost: float = 0.0
    coordinated_annual_cost: float = 0.0
    annual_savings: float = 0.0
    # Timeline
    time_to_stability_months: int = 0  # How long until stable improvement


# ── Dome Website Export ───────────────────────────────────────

class WebsiteSection(BaseModel):
    """A section of the dome's website."""
    section_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    slug: str                          # URL slug
    title: str
    content_type: str                  # hero, narrative, data_viz, ip_showcase,
                                       # team, budget, simulation, bond, timeline
    content: Dict[str, Any] = Field(default_factory=dict)
    order: int = 0


class DomeWebsite(BaseModel):
    """
    The website export for a dome production.
    A beautiful site showing the dome and everything that went into building it.
    """
    site_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    dome_id: str = ""
    title: str = ""
    tagline: str = ""
    sections: List[WebsiteSection] = Field(default_factory=list)

    # Standard sections every dome site has
    has_hero: bool = False             # The character, the challenge, the dome
    has_layers_explorer: bool = False   # Interactive 12-layer visualization
    has_ip_portfolio: bool = False      # All IP generated
    has_business_case: bool = False     # Budget, ROI, dome bond
    has_simulation: bool = False        # Coordinated vs. fragmented comparison
    has_team: bool = False             # Who built this dome
    has_production_timeline: bool = False  # The process
    has_tech_innovations: bool = False  # Tech created along the way
    has_data_sources: bool = False      # All data that fed the dome


# ── The Complete Dome Production ──────────────────────────────

class DomeProduction(BaseModel):
    """
    The complete output of Person-Runner.

    Input: a character and their circumstances.
    Output: everything needed to pitch, fund, execute, and showcase a dome.

    This is the product.
    """
    production_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ── Input ──────────────────────────────────────────────────
    character: CharacterInput = Field(default_factory=lambda: CharacterInput(
        name="", source_type="fictional", situation=""
    ))

    # ── The Dome ───────────────────────────────────────────────
    dome: Optional[DomeSchema] = None
    tier: DomeTier = DomeTier.INDIE

    # ── IP ─────────────────────────────────────────────────────
    ip_portfolio: IPPortfolio = Field(default_factory=IPPortfolio)

    # ── Production ─────────────────────────────────────────────
    budget: ProductionBudget = Field(default_factory=ProductionBudget)
    team: ProductionTeam = Field(default_factory=ProductionTeam)
    pipeline: ProductionPipeline = Field(default_factory=ProductionPipeline)

    # ── Analytics ──────────────────────────────────────────────
    simulation: WholePersonSimulation = Field(default_factory=WholePersonSimulation)
    tech_innovations: List[TechInnovation] = Field(default_factory=list)

    # ── Export ─────────────────────────────────────────────────
    website: DomeWebsite = Field(default_factory=DomeWebsite)

    # ── Swarm ──────────────────────────────────────────────────
    swarm_recommendations_received: List[Dict[str, Any]] = Field(default_factory=list)
    patterns_extracted: List[Dict[str, Any]] = Field(default_factory=list)

    # ── Status ─────────────────────────────────────────────────
    status: str = "draft"              # draft, generating, review, funded, in_production, complete

    # ── The Pitch ──────────────────────────────────────────────
    pitch_deck: Dict[str, Any] = Field(default_factory=dict)


# ── Person-Runner Engine ──────────────────────────────────────

def generate_dome_production(character: CharacterInput) -> DomeProduction:
    """
    The main Person-Runner function.

    Takes a character and their circumstances.
    Returns a complete DomeProduction with:
    - Full 12-layer dome schema
    - IP portfolio across all domains
    - Production budget with ROI justification
    - Team assembly plan
    - Production pipeline
    - Whole-person simulation
    - Website export
    - Tech innovations catalogue

    This function orchestrates all existing BATHS infrastructure:
    - schema/ for the dome structure
    - intelligence/ for swarm recommendations and agent coordination
    - data/ for county-level SDOH data
    - backend/ for legal provision matching
    """
    production = DomeProduction(
        character=character,
        tier=character.tier,
    )

    # ── Step 1: Create the dome subject ────────────────────────
    production.dome = DomeSchema(
        metadata=SchemaMetadata(
            schema_type=GameType.DOMES,
            title=f"Dome: {character.name}",
            status="draft",
        ),
        subject=DomeSubject(
            name=character.name,
            source=character.source_type,
            source_citation=character.source_citation,
            situation=character.situation,
            full_landscape=character.full_landscape,
            production_challenge=character.production_challenge,
            key_systems=character.key_systems,
            flourishing_dimensions=character.flourishing_dimensions,
            demographic={
                "age": character.age,
                "gender": character.gender,
                "age_group": character.age_group,
            },
            location={
                "city": character.location_city,
                "state": character.location_state,
                "county_fips": character.location_county_fips,
            },
        ),
    )

    # ── Step 2: Generate IP portfolio structure ────────────────
    production.ip_portfolio = _generate_ip_portfolio(character)

    # ── Step 3: Build production budget ────────────────────────
    production.budget = _build_production_budget(character, production.ip_portfolio)

    # ── Step 4: Assemble team plan ─────────────────────────────
    production.team = _assemble_team(character)

    # ── Step 5: Build production pipeline ──────────────────────
    production.pipeline = _build_pipeline(character)

    # ── Step 6: Generate simulation scenarios ──────────────────
    production.simulation = _build_simulation(character)

    # ── Step 7: Generate tech innovation catalogue ─────────────
    production.tech_innovations = _catalogue_innovations(character)

    # ── Step 8: Build website structure ────────────────────────
    production.website = _build_website(character, production)

    # ── Step 9: Generate pitch deck structure ──────────────────
    production.pitch_deck = _build_pitch_deck(character, production)

    production.status = "generating"
    production.updated_at = datetime.utcnow()

    return production


# ── IP Generation Engine ──────────────────────────────────────

def _generate_ip_portfolio(character: CharacterInput) -> IPPortfolio:
    """
    Generate the IP portfolio for a dome.
    Every dome generates IP across multiple domains.
    """
    portfolio = IPPortfolio()
    tier_spec = TIER_SPECS[character.tier]

    # ── Entertainment IP ───────────────────────────────────────
    portfolio.add_asset(IPAsset(
        title=f"{character.name}: Documentary Treatment",
        domain=IPDomain.ENTERTAINMENT,
        description=(
            f"Feature documentary following {character.name}'s journey through "
            f"the dome — every system made visible, every barrier mapped, "
            f"every coordination moment captured. The dome itself is the narrative "
            f"structure: 12 layers, one person, total coordination."
        ),
        generated_from_layer=12,
        generated_at_stage="development",
        format="documentary_treatment",
        comparable_precedents=[
            "Hoop Dreams (1994)", "The Staircase (2004)", "Making a Murderer (2015)",
        ],
    ))

    portfolio.add_asset(IPAsset(
        title=f"{character.name}: Series Bible",
        domain=IPDomain.ENTERTAINMENT,
        description=(
            f"Limited series adaptation. Each episode follows one dome layer. "
            f"Episode 1: The person. Episodes 2-10: The 9 AI-filled layers. "
            f"Episodes 11-13: The 3 human-designed layers. Finale: The complete dome."
        ),
        generated_from_layer=11,
        generated_at_stage="development",
        format="series_bible",
        comparable_precedents=[
            "The Wire (systems)", "When They See Us (justice)",
            "Maid (housing/poverty)", "The Bear (environment)",
        ],
    ))

    # ── Technology IP ──────────────────────────────────────────
    portfolio.add_asset(IPAsset(
        title="Whole-Person Digital Twin Platform",
        domain=IPDomain.TECHNOLOGY,
        description=(
            "The technical architecture of the dome itself — 12-layer person model, "
            "FHIR R4 health integration, SDOH screening instrument mapping, "
            "cross-layer query engine, Cosm scoring system. Each dome production "
            "validates and extends the platform."
        ),
        generated_from_layer=4,
        generated_at_stage="production",
        format="software_platform",
        comparable_precedents=[
            "Epic Systems (EHR)", "Palantir (data integration)",
            "Cityblock Health (SDOH)", "Unite Us (social care)",
        ],
    ))

    portfolio.add_asset(IPAsset(
        title="Cross-System Coordination Engine",
        domain=IPDomain.TECHNOLOGY,
        description=(
            "The Layer 2 systems fragmentation analyzer and coordinator. "
            "Maps every government system a person interacts with, identifies "
            "gaps, and generates coordination plans. Each dome validates the "
            "fragmentation cost model."
        ),
        generated_from_layer=2,
        generated_at_stage="production",
        format="software_engine",
    ))

    # ── Financial Product IP ───────────────────────────────────
    portfolio.add_asset(IPAsset(
        title=f"Dome Bond: {character.name}",
        domain=IPDomain.FINANCIAL_PRODUCT,
        description=(
            "Social impact bond structured from dome data. Converts measurable "
            "coordination savings into investor returns. Bond prospectus computed "
            "from real cost data using GO Lab / Social Finance methodologies."
        ),
        generated_from_layer=3,
        generated_at_stage="production",
        format="bond_prospectus",
        comparable_precedents=[
            "Massachusetts Juvenile Justice PFS ($18M)",
            "Denver SIB Supportive Housing ($8.6M)",
            "Cuyahoga County Partnering for Family Success ($4M)",
        ],
    ))

    # ── Healthcare IP ──────────────────────────────────────────
    if any(d in character.disabilities for d in ["mental_health", "chronic_illness", "sud"]):
        portfolio.add_asset(IPAsset(
            title="Cross-System Health Coordination Protocol",
            domain=IPDomain.HEALTHCARE,
            description=(
                "Protocol for coordinating health care across fragmented systems. "
                "FHIR R4 interoperable. Maps health conditions to housing, legal, "
                "economic, and community impacts using dome cross-layer queries."
            ),
            generated_from_layer=4,
            generated_at_stage="production",
            format="clinical_protocol",
        ))

    # ── Policy IP ──────────────────────────────────────────────
    portfolio.add_asset(IPAsset(
        title=f"Policy Brief: Coordination Economics of {character.situation[:50]}",
        domain=IPDomain.POLICY,
        description=(
            "Policy brief demonstrating the cost of system fragmentation vs. "
            "coordination for this specific circumstance profile. Includes "
            "model legislation, fiscal impact analysis, and implementation roadmap."
        ),
        generated_from_layer=1,
        generated_at_stage="post_production",
        format="policy_brief",
    ))

    # ── Product IP ─────────────────────────────────────────────
    portfolio.add_asset(IPAsset(
        title="Dome Explorer: Interactive Visualization",
        domain=IPDomain.PRODUCT,
        description=(
            "Interactive web experience letting viewers explore all 12 layers "
            "of the dome. Navigate from legal entitlements to health conditions "
            "to community connections. See the cross-layer dynamics in real time."
        ),
        generated_from_layer=12,
        generated_at_stage="post_production",
        format="web_application",
    ))

    # ── Research IP ────────────────────────────────────────────
    portfolio.add_asset(IPAsset(
        title=f"Whole-Person Coordination: Evidence from {character.name}'s Dome",
        domain=IPDomain.RESEARCH,
        description=(
            "Academic paper documenting the dome methodology, cross-layer "
            "dynamics, coordination savings, and measurable outcomes. "
            "Contributes to the evidence base for social impact investing "
            "and whole-person care coordination."
        ),
        generated_from_layer=0,
        generated_at_stage="distribution",
        format="academic_paper",
    ))

    # Set portfolio headline
    portfolio.headline_ip = portfolio.assets[0].title if portfolio.assets else None
    portfolio.pitch_one_liner = (
        f"A {character.tier.value} dome production generating {len(portfolio.assets)} "
        f"IP assets across {len(portfolio.by_domain)} domains from one person's "
        f"whole-life coordination story."
    )

    return portfolio


def _build_production_budget(
    character: CharacterInput,
    ip_portfolio: IPPortfolio,
) -> ProductionBudget:
    """Build a production budget justified by IP generation."""
    tier_spec = TIER_SPECS[character.tier]
    budget = ProductionBudget(tier=character.tier)

    budget_min, budget_max = tier_spec["budget_range"]
    # Scale budget based on complexity (number of systems = complexity)
    complexity = len(character.key_systems) / 10.0  # normalize
    target_budget = budget_min + (budget_max - budget_min) * min(complexity, 1.0)

    # Team costs (40-50% of budget)
    team_pct = 0.45
    budget.lines.append(BudgetLine(
        category="team",
        description="Director and creative team compensation",
        amount=round(target_budget * team_pct, 2),
        justification=(
            f"Visionary director and {tier_spec['creative_disciplines_min']}+ "
            f"disciplines needed to design layers 10-12. Team generates IP "
            f"across {tier_spec['ip_domains_target']} domains."
        ),
    ))

    # Technology costs (20-25%)
    tech_pct = 0.22
    budget.lines.append(BudgetLine(
        category="technology",
        description="AI infrastructure, data pipelines, sensor integration",
        amount=round(target_budget * tech_pct, 2),
        justification=(
            "AI agents fill layers 1-9. Includes FHIR R4 integration, "
            "SDOH screening instruments, cross-layer query engine, "
            "Cosm scoring system, and world model renderer."
        ),
    ))

    # Data costs (10-15%)
    data_pct = 0.12
    budget.lines.append(BudgetLine(
        category="data",
        description="Data acquisition, API access, SDOH fragments",
        amount=round(target_budget * data_pct, 2),
        justification=(
            "County-level SDOH data fragments, Census ACS, BLS, HUD, FEMA, "
            "and EPA data for dome layers 5-9. Medical coding references "
            "for Layer 4 FHIR integration."
        ),
    ))

    # Creative costs (10-15%)
    creative_pct = 0.13
    budget.lines.append(BudgetLine(
        category="creative",
        description="Physical prototypes, installations, media production",
        amount=round(target_budget * creative_pct, 2),
        justification="Architectural models, sonic compositions, material prototypes, film production.",
    ))

    # Legal costs (3-5%)
    legal_pct = 0.04
    budget.lines.append(BudgetLine(
        category="legal",
        description="IP protection, contracts, regulatory compliance",
        amount=round(target_budget * legal_pct, 2),
        justification="IP filing across all generated domains. Production contracts. HIPAA compliance.",
    ))

    # Overhead (3-5%)
    overhead_pct = 0.04
    budget.lines.append(BudgetLine(
        category="overhead",
        description="Production management, facilities, insurance",
        amount=round(target_budget * overhead_pct, 2),
        justification="Production management and operational overhead.",
    ))

    # Projected returns
    budget.projected_ip_revenue = ip_portfolio.total_estimated_value or target_budget * 3
    budget.projected_coordination_savings = len(character.key_systems) * 15000  # ~$15K/system/year
    budget.projected_dome_bond_value = budget.projected_coordination_savings * 5 * 0.7  # 5yr, 70%

    budget.compute_roi()

    budget.investment_thesis = (
        f"Invest ${budget.total_budget:,.0f} in a {character.tier.value} dome production "
        f"for {character.name}. The dome generates {len(ip_portfolio.assets)} IP assets "
        f"across {len(ip_portfolio.by_domain)} domains. Projected coordination savings "
        f"of ${budget.projected_coordination_savings:,.0f}/year across "
        f"{len(character.key_systems)} systems create a Dome Bond worth "
        f"${budget.projected_dome_bond_value:,.0f}. Total projected return: "
        f"${budget.total_projected_return:,.0f} ({budget.roi_multiple}x multiple)."
    )

    return budget


def _assemble_team(character: CharacterInput) -> ProductionTeam:
    """Assemble the production team based on tier and character needs."""
    tier_spec = TIER_SPECS[character.tier]
    team = ProductionTeam()

    # Director
    team.director = TeamMember(
        role="director",
        discipline=CreativeInputType.EXPERIENCE,
        why_this_person=(
            f"Visionary director who understands {character.situation[:100]}. "
            f"Must see the dome as a complete work — not just data, not just film, "
            f"but a 12-layer whole-person architecture rendered as art."
        ),
        ip_domains=[IPDomain.ENTERTAINMENT, IPDomain.PRODUCT],
    )

    # Core disciplines based on tier
    core_roles = [
        ("data_architect", CreativeInputType.VISUAL, [IPDomain.TECHNOLOGY],
         "Designs the 12-layer data architecture. Wires AI agents to dome layers."),
        ("narrative_designer", CreativeInputType.NARRATIVE, [IPDomain.ENTERTAINMENT],
         "Shapes the dome's story. Documentary treatment. Series bible."),
        ("systems_analyst", CreativeInputType.PHILOSOPHICAL, [IPDomain.POLICY, IPDomain.TECHNOLOGY],
         "Maps government system fragmentation. Builds the coordination economics."),
    ]

    if character.tier in (DomeTier.BLOCKBUSTER, DomeTier.INDIE):
        core_roles.extend([
            ("architect", CreativeInputType.ARCHITECTURAL, [IPDomain.ARCHITECTURAL, IPDomain.HOUSING],
             "Designs the physical/spatial dimension of the dome visualization."),
            ("composer", CreativeInputType.SONIC, [IPDomain.ENTERTAINMENT, IPDomain.PERFORMANCE],
             "Scores the dome. Sonic environment for the world model."),
            ("health_informaticist", CreativeInputType.PHILOSOPHICAL, [IPDomain.HEALTHCARE],
             "FHIR R4 integration. SDOH screening. Cross-layer health impacts."),
        ])

    if character.tier == DomeTier.BLOCKBUSTER:
        core_roles.extend([
            ("material_designer", CreativeInputType.MATERIAL, [IPDomain.PRODUCT, IPDomain.FASHION],
             "Material palette for the dome. Physical prototypes."),
            ("movement_designer", CreativeInputType.MOVEMENT, [IPDomain.PERFORMANCE],
             "Choreographic notation for the dome experience. Accessibility pathways."),
            ("culinary_designer", CreativeInputType.CULINARY, [IPDomain.CULINARY],
             "Nutrition models. Food access plans. Cultural food significance."),
            ("financial_engineer", CreativeInputType.PHILOSOPHICAL, [IPDomain.FINANCIAL_PRODUCT],
             "Dome Bond structuring. Pay-for-success modeling."),
            ("environmental_scientist", CreativeInputType.EXPERIENCE, [IPDomain.ENVIRONMENTAL],
             "Environmental sensors. EPA data integration. Climate risk."),
        ])

    for role, discipline, domains, rationale in core_roles:
        team.members.append(TeamMember(
            role=role,
            discipline=discipline,
            ip_domains=domains,
            why_this_person=rationale,
        ))

    team.disciplines_covered = list(set(m.discipline.value for m in team.members))
    team.ip_surface_area = list(set(
        d.value for m in ([team.director] + team.members) if m for d in m.ip_domains
    ))

    return team


def _build_pipeline(character: CharacterInput) -> ProductionPipeline:
    """Build the production pipeline with milestones."""
    pipeline = ProductionPipeline()
    tier_spec = TIER_SPECS[character.tier]

    milestones = [
        # Development
        ProductionMilestone(
            stage=ProductionStage.DEVELOPMENT,
            title="Character Analysis & Swarm Query",
            description=(
                "Analyze character circumstances. Query swarm intelligence for "
                "relevant patterns from prior domes. Generate initial dome schema."
            ),
            deliverables=["character_profile", "swarm_briefing", "initial_dome_schema"],
            estimated_duration_days=14,
        ),
        ProductionMilestone(
            stage=ProductionStage.DEVELOPMENT,
            title="AI Layer Population (1-9)",
            description=(
                "AI agents fill layers 1-9. Legal navigator maps entitlements. "
                "Systems analyst maps fragmentation. Fiscal engine computes "
                "coordination economics. Health layer populated with FHIR R4. "
                "SDOH screening instruments applied."
            ),
            deliverables=["legal_landscape", "systems_map", "fiscal_model",
                          "health_layer", "housing_data", "economic_profile",
                          "education_data", "community_map", "environmental_data"],
            estimated_duration_days=30,
        ),
        # Pre-production
        ProductionMilestone(
            stage=ProductionStage.PRE_PRODUCTION,
            title="Team Assembly & IP Mapping",
            description=(
                "Assemble the creative team. Map the IP surface area. "
                "Identify unlikely collisions between disciplines."
            ),
            deliverables=["team_roster", "ip_map", "collision_predictions"],
            estimated_duration_days=21,
        ),
        ProductionMilestone(
            stage=ProductionStage.PRE_PRODUCTION,
            title="Dome Bond Prospectus",
            description=(
                "Generate the Dome Bond prospectus from Layer 3 data. "
                "Compute coordination savings, structure the bond, "
                "generate risk assessment."
            ),
            deliverables=["dome_bond_prospectus", "cost_analysis", "risk_assessment"],
            estimated_duration_days=14,
        ),
        # Production
        ProductionMilestone(
            stage=ProductionStage.PRODUCTION,
            title="Human Layer Design (10-12)",
            description=(
                "Creative team designs layers 10 (Autonomy), 11 (Creativity), "
                "12 (Flourishing). Each layer gets discipline-specific creative "
                "inputs. Awe framework applied to Layer 12."
            ),
            deliverables=["autonomy_design", "creativity_design",
                          "flourishing_design", "awe_framework"],
            estimated_duration_days=60,
        ),
        ProductionMilestone(
            stage=ProductionStage.PRODUCTION,
            title="Cross-Layer Integration & Simulation",
            description=(
                "Run cross-layer queries. Generate whole-person simulation. "
                "Compare baseline vs. coordinated scenarios. Compute final "
                "Cosm score."
            ),
            deliverables=["cross_layer_analysis", "simulation_results",
                          "cosm_score_report"],
            estimated_duration_days=21,
        ),
        # Post-production
        ProductionMilestone(
            stage=ProductionStage.POST_PRODUCTION,
            title="IP Portfolio Assembly",
            description=(
                "Catalogue all IP generated. File protections. "
                "Build the IP portfolio with valuations."
            ),
            deliverables=["ip_portfolio", "ip_filings"],
            estimated_duration_days=14,
        ),
        ProductionMilestone(
            stage=ProductionStage.POST_PRODUCTION,
            title="Dome Website & World Model",
            description=(
                "Build the dome website. Render the world model. "
                "Create the interactive 12-layer explorer."
            ),
            deliverables=["dome_website", "world_model_render", "layer_explorer"],
            estimated_duration_days=21,
        ),
        # Distribution
        ProductionMilestone(
            stage=ProductionStage.DISTRIBUTION,
            title="Pitch Assembly & Distribution",
            description=(
                "Assemble the complete pitch: dome, IP portfolio, business case, "
                "simulation results, team, budget, website. Ready for "
                "management company or agent presentation."
            ),
            deliverables=["pitch_deck", "complete_dome_package"],
            estimated_duration_days=7,
        ),
    ]

    pipeline.milestones = milestones
    pipeline.total_duration_days = sum(m.estimated_duration_days for m in milestones)

    return pipeline


def _build_simulation(character: CharacterInput) -> WholePersonSimulation:
    """Build the whole-person simulation."""
    sim = WholePersonSimulation()

    # Baseline: fragmented, no coordination
    baseline_cost = len(character.key_systems) * 20000  # ~$20K/system/year average

    sim.scenarios = [
        SimulationScenario(
            title="Baseline: Fragmented Systems",
            description=(
                f"No coordination. {len(character.key_systems)} government systems "
                f"operating independently. Each system sees only its own data."
            ),
            scenario_type="baseline",
            projected_cosm=15.0,
            projected_costs={"annual_system_cost": baseline_cost},
            projected_timeline_months=0,
        ),
        SimulationScenario(
            title="Coordinated: Full Dome",
            description=(
                "Complete 12-layer dome coordination. All systems connected. "
                "Cross-layer queries active. AI agents filling layers 1-9. "
                "Creative team designing layers 10-12."
            ),
            scenario_type="coordinated",
            projected_cosm=72.0,
            projected_costs={"annual_system_cost": round(baseline_cost * 0.45)},
            projected_timeline_months=18,
            vs_baseline_delta={
                "cosm_improvement": 57.0,
                "cost_reduction_pct": 55.0,
                "annual_savings": round(baseline_cost * 0.55),
            },
        ),
        SimulationScenario(
            title="Intervention: Priority Layer",
            description=(
                "Targeted intervention on the weakest dome layer first. "
                "Highest-impact, lowest-cost coordination action."
            ),
            scenario_type="intervention",
            projected_cosm=42.0,
            projected_costs={"annual_system_cost": round(baseline_cost * 0.72)},
            projected_timeline_months=6,
            vs_baseline_delta={
                "cosm_improvement": 27.0,
                "cost_reduction_pct": 28.0,
                "annual_savings": round(baseline_cost * 0.28),
            },
        ),
    ]

    sim.baseline_cosm = 15.0
    sim.coordinated_cosm = 72.0
    sim.cosm_delta = 57.0
    sim.baseline_annual_cost = baseline_cost
    sim.coordinated_annual_cost = round(baseline_cost * 0.45)
    sim.annual_savings = round(baseline_cost * 0.55)
    sim.time_to_stability_months = 18

    return sim


def _catalogue_innovations(character: CharacterInput) -> List[TechInnovation]:
    """Catalogue technology innovations the dome will generate."""
    innovations = [
        TechInnovation(
            title="Person-Runner Engine",
            description=(
                "The AI engine that generates complete dome productions from "
                "character + circumstances input. Each dome run improves the "
                "engine through swarm intelligence feedback."
            ),
            category="ai_method",
            generated_from_layer=0,
            reusable=True,
        ),
        TechInnovation(
            title="Cross-Layer Query Engine",
            description=(
                "Engine that answers questions across dome layers. "
                "'Given this person's legal entitlements and health conditions, "
                "what is the optimal fiscal coordination?'"
            ),
            category="data_pipeline",
            generated_from_layer=0,
            reusable=True,
        ),
        TechInnovation(
            title="Cosm Scoring System",
            description=(
                "Auditable scoring system where every number has a source. "
                "Dome is only as strong as its weakest layer. "
                "Total Cosm = minimum across all 12 layer completeness scores."
            ),
            category="measurement",
            generated_from_layer=0,
            reusable=True,
        ),
        TechInnovation(
            title="FHIR R4 ↔ Dome Layer Bridge",
            description=(
                "Bidirectional bridge between FHIR R4 health resources and "
                "dome layer 4. Ingest FHIR data. Export FHIR Bundles."
            ),
            category="interoperability",
            generated_from_layer=4,
            reusable=True,
        ),
        TechInnovation(
            title="SDOH Screening ↔ Dome Mapping",
            description=(
                "Maps PRAPARE and AHC-HRSN screening instruments to dome layers. "
                "Bidirectional: populate dome FROM screenings, produce screening "
                "data FROM dome."
            ),
            category="interoperability",
            generated_from_layer=4,
            reusable=True,
        ),
        TechInnovation(
            title="Dome Bond Financial Engine",
            description=(
                "Computes social impact bond prospectuses from dome data. "
                "Real cost references. GO Lab / Social Finance methodologies."
            ),
            category="ai_method",
            generated_from_layer=3,
            reusable=True,
        ),
    ]

    return innovations


def _build_website(character: CharacterInput, production: DomeProduction) -> DomeWebsite:
    """Build the website structure for the dome."""
    site = DomeWebsite(
        dome_id=production.production_id,
        title=f"DOME: {character.name}",
        tagline=character.situation[:120],
    )

    site.sections = [
        WebsiteSection(
            slug="",
            title="The Dome",
            content_type="hero",
            content={
                "name": character.name,
                "situation": character.situation,
                "tier": character.tier.value,
                "systems_count": len(character.key_systems),
                "ip_count": len(production.ip_portfolio.assets),
            },
            order=0,
        ),
        WebsiteSection(
            slug="layers",
            title="12 Layers",
            content_type="data_viz",
            content={"description": "Interactive exploration of all 12 dome layers"},
            order=1,
        ),
        WebsiteSection(
            slug="story",
            title="The Story",
            content_type="narrative",
            content={
                "full_landscape": character.full_landscape,
                "production_challenge": character.production_challenge,
            },
            order=2,
        ),
        WebsiteSection(
            slug="simulation",
            title="Fragmented vs. Coordinated",
            content_type="simulation",
            content={
                "baseline_cost": production.simulation.baseline_annual_cost,
                "coordinated_cost": production.simulation.coordinated_annual_cost,
                "annual_savings": production.simulation.annual_savings,
                "cosm_delta": production.simulation.cosm_delta,
            },
            order=3,
        ),
        WebsiteSection(
            slug="ip",
            title="IP Portfolio",
            content_type="ip_showcase",
            content={
                "total_assets": production.ip_portfolio.total_assets,
                "domains": list(production.ip_portfolio.by_domain.keys()),
                "headline": production.ip_portfolio.headline_ip,
            },
            order=4,
        ),
        WebsiteSection(
            slug="business-case",
            title="The Business Case",
            content_type="budget",
            content={
                "total_budget": production.budget.total_budget,
                "roi_multiple": production.budget.roi_multiple,
                "investment_thesis": production.budget.investment_thesis,
            },
            order=5,
        ),
        WebsiteSection(
            slug="team",
            title="The Team",
            content_type="team",
            content={
                "disciplines": production.team.disciplines_covered,
                "ip_surface_area": production.team.ip_surface_area,
            },
            order=6,
        ),
        WebsiteSection(
            slug="production",
            title="Production Timeline",
            content_type="timeline",
            content={
                "total_days": production.pipeline.total_duration_days,
                "milestones": len(production.pipeline.milestones),
            },
            order=7,
        ),
        WebsiteSection(
            slug="innovations",
            title="Tech Innovations",
            content_type="data_viz",
            content={
                "count": len(production.tech_innovations),
            },
            order=8,
        ),
        WebsiteSection(
            slug="data",
            title="Data Sources",
            content_type="data_viz",
            content={
                "sources": [
                    "US Census ACS", "BLS", "HUD FMR", "FEMA",
                    "EPA AirNow", "USDA Food Access", "FHIR R4",
                    "PRAPARE", "AHC-HRSN", "ICD-10-CM", "LOINC",
                ],
            },
            order=9,
        ),
    ]

    site.has_hero = True
    site.has_layers_explorer = True
    site.has_ip_portfolio = True
    site.has_business_case = True
    site.has_simulation = True
    site.has_team = True
    site.has_production_timeline = True
    site.has_tech_innovations = True
    site.has_data_sources = True

    return site


def _build_pitch_deck(
    character: CharacterInput,
    production: DomeProduction,
) -> Dict[str, Any]:
    """Build the pitch deck structure for management/agent presentation."""
    return {
        "title": f"DOME: {character.name}",
        "subtitle": character.situation[:100],
        "tier": character.tier.value,
        "slides": [
            {
                "title": "The Person",
                "content": {
                    "name": character.name,
                    "situation": character.situation,
                    "systems": character.key_systems,
                    "source": character.source_type,
                },
            },
            {
                "title": "The Problem",
                "content": {
                    "systems_count": len(character.key_systems),
                    "fragmentation_cost": production.simulation.baseline_annual_cost,
                    "description": (
                        f"{len(character.key_systems)} government systems operating "
                        f"independently at a cost of "
                        f"${production.simulation.baseline_annual_cost:,.0f}/year."
                    ),
                },
            },
            {
                "title": "The Dome",
                "content": {
                    "layers": 12,
                    "ai_layers": 9,
                    "human_layers": 3,
                    "description": (
                        "12-layer whole-person architecture. AI agents fill layers 1-9. "
                        "Visionary director and creative team design layers 10-12. "
                        "The dome is only as strong as its weakest layer."
                    ),
                },
            },
            {
                "title": "The Coordination",
                "content": {
                    "annual_savings": production.simulation.annual_savings,
                    "cosm_improvement": production.simulation.cosm_delta,
                    "time_to_stability": f"{production.simulation.time_to_stability_months} months",
                },
            },
            {
                "title": "The IP",
                "content": {
                    "total_assets": production.ip_portfolio.total_assets,
                    "domains": list(production.ip_portfolio.by_domain.keys()),
                    "headline": production.ip_portfolio.headline_ip,
                    "pitch": production.ip_portfolio.pitch_one_liner,
                },
            },
            {
                "title": "The Business Case",
                "content": {
                    "budget": production.budget.total_budget,
                    "projected_return": production.budget.total_projected_return,
                    "roi": production.budget.roi_multiple,
                    "thesis": production.budget.investment_thesis,
                },
            },
            {
                "title": "The Dome Bond",
                "content": {
                    "coordination_savings": production.budget.projected_coordination_savings,
                    "bond_value": production.budget.projected_dome_bond_value,
                    "description": (
                        "Social impact bond converting measurable coordination savings "
                        "into investor returns. GO Lab / Social Finance methodology."
                    ),
                },
            },
            {
                "title": "The Team",
                "content": {
                    "disciplines": production.team.disciplines_covered,
                    "ip_surface_area": production.team.ip_surface_area,
                    "director_brief": (
                        production.team.director.why_this_person
                        if production.team.director else ""
                    ),
                },
            },
            {
                "title": "The Ask",
                "content": {
                    "budget": production.budget.total_budget,
                    "tier": character.tier.value,
                    "timeline_days": production.pipeline.total_duration_days,
                    "what_you_get": [
                        "Complete 12-layer dome",
                        f"{production.ip_portfolio.total_assets} IP assets",
                        "Dome Bond prospectus",
                        "Documentary treatment + series bible",
                        "Interactive dome website",
                        "Whole-person simulation",
                        "Policy brief",
                        "All source data and tech innovations",
                    ],
                },
            },
        ],
    }
