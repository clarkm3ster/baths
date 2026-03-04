new project: SPHERE/OS: Complete Claude Code Multi-Agent Prompt:

bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude
text
You are the lead architect for SPHERE/OS — a platform that transforms vacant public 
land into programmable material environments called "Spheres." The platform:

1. Maps all publicly owned/vacant/unused land (starting with Philadelphia)
2. Proposes film/TV/short-form productions that activate each site
3. Uses programmable materials to tell stories (materials ARE the narrative medium)
4. Persists as a "living sound stage" for future creators after production wraps
5. Opens to public booking in time slices: minutes, hours, days, months, years

**Economic model**: Film/TV production budgets (months-long shoots) fund the material 
installation. After wrap, those materials persist and the public books time slices 
against infrastructure amortized by Hollywood capital.

**Material innovation context**: The platform integrates TRL 6-8 systems from recent 
research — acoustic metamaterials (reconfigure <25ms), subtractive digital olfaction 
(40-component blender), 4D printed deployables (MIT Self-Assembly Lab), electrochromic 
surfaces, haptic arrays, phase-change thermal panels, shape-memory elements. NOT 
inventing new molecules per booking — reprogramming pre-certified smart materials.

---

## TEAM STRUCTURE

Create an agent team with **7 teammates**. Require plan approval before ANY teammate 
writes code. Only approve plans that include:
- Test coverage (pytest for backend, Playwright for frontend)
- Clear file ownership (no two teammates modify the same file)
- Dependency diagram showing how their module integrates
- OpenAPI spec fragment for any API endpoints

**Critical coordination rules**:
- If two teammates need shared models → `src/shared/` (only @infra writes it)
- API contracts BEFORE implementation → collect OpenAPI specs → unified doc
- No agent can spawn sub-agents (Agent Teams limitation)
- All Python: 3.12+, Pydantic v2, FastAPI 0.115+, SQLAlchemy 2.0 async
- Frontend: Node 20+, Next.js 15, TypeScript strict mode

---

### @land-cartographer
**Scope**: `src/land/`, `src/data-ingestion/`, `tests/land/`, `db/migrations/land/`

**Mission**: Build the public land intelligence engine that discovers, ingests, and 
scores every vacant/public parcel for Sphere activation potential.

**Data sources to integrate** (Philadelphia first, architect for national):
1. **Philadelphia Vacant Property Indicators** (OpenDataPhilly)
   - API: `data-phl.opendata.arcgis.com/datasets/vacant-indicators-land`
   - GeoJSON endpoint with ~40K parcels
   - Fields: OPA_ID (parcel ID), VACANT_BLDG_COUNT, VACANT_LAND_COUNT, geometry

2. **Philadelphia Land Bank** (PHL Land Bank inventory)
   - CSV/API of city-owned vacant lots available for reuse
   - Fields: address, disposition_status, strategic_plan

3. **Regrid Nationwide Parcels** (regrid.com API)
   - 158M+ parcels covering all 3,200+ US counties
   - 143 standardized fields: ownership, zoning, buildings, tax assessment
   - Use free tier (5K parcels/day) or mock the interface for demo

4. **OpenStreetMap** (Overpass API)
   - Supplementary geometry, amenities, land use tags
   - Query: `[out:json];area["name"="Philadelphia"]->.a;(way["landuse"="brownfield"](area.a););out geom;`

5. **US Census TIGER/Line** (census.gov shapefiles)
   - Block group boundaries for demographic context
   - Transit stop locations (proximity scoring)

**Core models** (SQLAlchemy + PostGIS):

```python
class ParcelRecord(Base):
    __tablename__ = "parcels"
    __table_args__ = {"schema": "land"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source: Mapped[str]  # "philly_vacant" | "regrid" | "landbank"
    external_id: Mapped[str]  # source-specific ID (e.g., OPA_ID)
    geometry: Mapped[Geometry] = mapped_column(Geometry("POLYGON", srid=4326))
    centroid: Mapped[Geometry] = mapped_column(Geometry("POINT", srid=4326), index=True)
    
    # Ownership
    ownership_type: Mapped[str]  # "city" | "state" | "federal" | "land_bank" | "tax_delinquent"
    owner_name: Mapped[str | None]
    
    # Physical
    area_sqft: Mapped[float]
    street_frontage_ft: Mapped[float | None]
    zoning: Mapped[str | None]  # Philadelphia codes: RSA-1..5, CMX-1..5, ICMX, SP-ENT
    
    # Vacancy indicators
    vacancy_score: Mapped[float]  # 0-1 (aggregated from multiple signals)
    vacant_building_count: Mapped[int] = mapped_column(default=0)
    vacant_land_indicator: Mapped[bool] = mapped_column(default=False)
    last_activity_date: Mapped[datetime | None]
    
    # Context
    census_block_group: Mapped[str | None]
    transit_proximity_ft: Mapped[float | None]  # distance to nearest transit stop
    environmental_flags: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])  # ["brownfield", "flood_zone"]
    
    # Sphere viability (computed)
    sphere_viability_score: Mapped[float | None]  # 0-1 (ML model output)
    sphere_viability_updated_at: Mapped[datetime | None]
    
    # Relationships
    cluster_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("land.parcel_clusters.id"))
    cluster: Mapped["ParcelCluster"] = relationship(back_populates="parcels")


class ParcelCluster(Base):
    __tablename__ = "parcel_clusters"
    __table_args__ = {"schema": "land"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    geometry: Mapped[Geometry] = mapped_column(Geometry("MULTIPOLYGON", srid=4326))
    total_area_sqft: Mapped[float]
    parcel_count: Mapped[int]
    avg_viability_score: Mapped[float]
    
    parcels: Mapped[list["ParcelRecord"]] = relationship(back_populates="cluster")
Viability scoring algorithm:

python
def calculate_sphere_viability_score(parcel: ParcelRecord) -> float:
    """
    ML model (or rule-based for MVP) that scores 0-1 based on:
    
    - lot_size (min 2000 sqft for micro-sphere, 5000+ preferred, 50000+ for full sphere)
    - street_visibility proxy (street_frontage_ft / area_sqft ratio)
    - pedestrian_traffic proxy (transit_proximity_ft < 500ft = boost)
    - environmental_contamination_risk (brownfield flag = penalty)
    - utility_access proxy (within city limits = assume available)
    - zoning_compatibility (CMX-3+, SP-ENT, ICMX = boost; residential = penalty)
    - neighborhood_density (census block group population density)
    - cluster_potential (adjacent vacant parcels within 200ft)
    
    Returns float 0-1
    """
Clustering algorithm:

Use DBSCAN on parcel centroids (epsilon=200ft, min_samples=2)

Create ParcelCluster records for groups of 2+ contiguous vacant parcels

Useful for identifying sites where 3-4 small lots could combine into a larger Sphere

REST API (FastAPI):

python
GET  /api/land/parcels?city=philadelphia&min_score=0.7&min_area=5000&bbox=-75.28,39.87,-75.13,40.14
     → Returns GeoJSON FeatureCollection with scoring metadata

GET  /api/land/parcels/{id}/viability
     → Returns detailed viability breakdown with factor contributions

GET  /api/land/clusters?city=philadelphia&max_radius_ft=500
     → Returns clusters of adjacent vacant parcels

POST /api/land/parcels/{id}/activate
     → Marks parcel as "Sphere candidate" (status transition)

POST /api/land/ingest/philly-vacant
     → Triggers ingestion job for Philadelphia Vacant Property Indicators API
Tech stack:

Python 3.12, FastAPI 0.115+, SQLAlchemy 2.0 async, GeoAlchemy2

PostGIS (PostgreSQL + geometry extensions)

shapely, geopandas for geometry operations

httpx for async API calls

Alembic for migrations

pytest + pytest-asyncio for tests

Docker:

text
# docker-compose.yml (you create this)
services:
  postgres:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: sphere_os
      POSTGRES_USER: sphere
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
Tests (pytest):

Mock all external APIs (Regrid, Overpass, ArcGIS)

Test clustering with synthetic Philadelphia-shaped parcel data

Test GeoJSON output validates against RFC 7946

Test viability scoring edge cases (tiny lots, huge lots, brownfields)

Deliverables:

src/land/models.py (SQLAlchemy models above)

src/land/api.py (FastAPI routes)

src/land/ingestion.py (data pipeline for each source)

src/land/scoring.py (viability scoring logic)

src/land/clustering.py (DBSCAN spatial clustering)

db/migrations/land/001_initial_schema.sql (Alembic migration)

tests/land/test_api.py, tests/land/test_scoring.py, tests/land/test_clustering.py

README_land.md explaining the data sources and scoring algorithm

@story-architect
Scope: src/productions/, src/ai-engine/, tests/productions/, db/migrations/productions/

Mission: Build the AI engine that generates film/TV/short-form production proposals
where programmable materials ARE the narrative medium. Each proposal includes a
"material script" — a timeline of material state changes synced to story beats.

Core philosophical framework (encode this in your system prompts):

Material Dramaturgy — materials have the same narrative structure as characters:

ACT STRUCTURE: Setup (establish baseline material state) → Confrontation (disrupt
expectations, shift materials) → Resolution (new material equilibrium)

CHARACTER ARCS: Each material system is a character. A wall that starts opaque and
slowly becomes transparent over 90 minutes IS a character arc about revelation.

RHYTHM: Haptic pulses, acoustic reverb changes, scent intensity curves create pacing.

CONTRAST: Juxtaposing material states creates meaning (warm→cold, rough→smooth,
silent→cacophonous).

Core models (SQLAlchemy):

python
class ProductionProposal(Base):
    __tablename__ = "production_proposals"
    __table_args__ = {"schema": "productions"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    parcel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("land.parcels.id"))
    
    # Production metadata
    title: Mapped[str]
    logline: Mapped[str]  # 1-2 sentence story summary
    genre: Mapped[str]  # "sci-fi" | "drama" | "thriller" | "experimental"
    format: Mapped[str]  # "feature_film" | "series" | "short" | "installation" | "hybrid"
    
    # Narrative concept
    narrative_concept: Mapped[str]  # 2-3 paragraph story description
    
    # Material script (the key innovation)
    material_script: Mapped[list[dict]] = mapped_column(JSONB)  # list of MaterialCue dicts
    
    # Site requirements
    min_area_sqft: Mapped[float]
    required_utilities: Mapped[list[str]] = mapped_column(ARRAY(String))  # ["power", "water"]
    crew_size_estimate: Mapped[int]
    
    # Budget & timeline
    estimated_budget_low_usd: Mapped[int]
    estimated_budget_high_usd: Mapped[int]
    production_timeline_weeks: Mapped[int]
    
    # Legacy modes (how the Sphere persists after production)
    legacy_modes: Mapped[list[str]] = mapped_column(ARRAY(String))
    # Options: "living_soundstage", "public_installation", "community_space", "research_lab"
    
    # AI generation metadata
    generated_by_model: Mapped[str]  # "claude-sonnet-4" | "claude-opus-4.6"
    creative_brief: Mapped[str | None]  # optional user input that shaped generation
    generated_at: Mapped[datetime]


class MaterialCue(TypedDict):
    """
    A single material state change at a specific story beat.
    Stored in ProductionProposal.material_script as JSONB.
    """
    beat_id: str  # e.g., "act1_inciting_incident", "climax", "denouement"
    timestamp_range: tuple[float, float] | str  # (start_sec, end_sec) or "persistent"
    
    material_system: str  # enum below
    target_property: str  # what parameter we're controlling
    value_curve: list[float]  # parameter values over time (keyframes)
    
    narrative_function: str  # "builds_tension" | "reveals_character" | "marks_time_passage"


# Material system types available (from research brief)
MATERIAL_SYSTEMS = Literal[
    "acoustic_metamaterial",      # tunable reverb, directional sound, <25ms switching
    "haptic_surface",              # LRA-based floor/wall, <25ms latency
    "olfactory_synthesis",         # 40-component subtractive scent (10-20 min clearing)
    "electrochromic_surface",      # switchable glass opacity/color (1-5 sec)
    "projection_mapping",          # LED + projectors (baseline visual layer)
    "phase_change_panel",          # thermal regulation panels (5-30 min)
    "shape_memory_element",        # SMP textiles, panels (5-30 min activation)
    "4d_printed_deployable",       # MIT Self-Assembly Lab model (30-60 min)
    "bioluminescent_coating",      # persistent living layer (not reconfigurable per-booking)
]


class MaterialPalette(TypedDict):
    """
    The set of material systems available for a Sphere, organized by TRL tier.
    """
    tier_1_deployable_now: list[str]      # TRL 7-9
    tier_2_near_term: list[str]           # TRL 5-7 (2-4 year horizon)
    tier_3_long_term: list[str]           # TRL 3-5 (5-10 year horizon)


# Default palette for most Spheres
DEFAULT_MATERIAL_PALETTE: MaterialPalette = {
    "tier_1_deployable_now": [
        "acoustic_metamaterial",
        "olfactory_synthesis",
        "electrochromic_surface",
        "projection_mapping",
        "phase_change_panel",
    ],
    "tier_2_near_term": [
        "haptic_surface",
        "shape_memory_element",
        "4d_printed_deployable",
    ],
    "tier_3_long_term": [
        "bioluminescent_coating",
    ],
}
AI generation pipeline (Anthropic SDK):

python
from anthropic import AsyncAnthropic

async def generate_production_proposal(
    parcel: ParcelRecord,
    creative_brief: str | None = None,
    tier_filter: list[int] | None = None,  # [1][2] = only Tier 1-2 materials
    format: str | None = None,  # "series" | "short" | None (AI decides)
) -> ProductionProposal:
    """
    Use Claude API to generate a production proposal where materials tell the story.
    
    System prompt should include:
    - The parcel's geometry, area, zoning, neighborhood context
    - Philadelphia's cultural history relevant to this neighborhood
    - The MaterialPalette available at each TRL tier
    - The Material Dramaturgy framework (acts, arcs, rhythm, contrast)
    - The constraint that materials serve NARRATIVE function, not decoration
    - Physical transition times for each material (olfactory is the bottleneck)
    
    The model should output structured JSON matching ProductionProposal schema.
    """
    
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    
    # Build system prompt
    system_prompt = f"""
You are a material dramaturg creating film/TV productions where programmable materials 
ARE the narrative medium.

SITE CONTEXT:
- Location: Philadelphia, {parcel.area_sqft} sqft vacant lot
- Neighborhood: {parcel.census_block_group} (derive cultural context)
- Zoning: {parcel.zoning}
- Street frontage: {parcel.street_frontage_ft} ft

MATERIAL PALETTE (Tier {tier_filter or '1-3'}):
{format_material_palette(tier_filter)}

MATERIAL DRAMATURGY FRAMEWORK:
1. Materials have ACTS (setup → confrontation → resolution)
2. Materials have CHARACTER ARCS (a wall's transparency journey is a character arc)
3. Materials have RHYTHM (haptic pulses sync to narrative pacing)
4. Materials create MEANING through CONTRAST (warm→cold, rough→smooth)

PHYSICAL CONSTRAINTS:
- Acoustic metamaterials switch in <25ms
- Olfactory needs 10-20 min to clear between scent profiles
- 4D printed elements need 30-60 min for shape changes
- Electrochromic glass switches in 1-5 sec
- Plan material transitions to respect these limits

TASK:
Generate a {format or 'film/TV/short-form'} production proposal where the story is TOLD 
THROUGH material transformations. Create a material_script with MaterialCues at each 
story beat explaining what materials do and WHY (narrative function).

Output strict JSON matching this schema:
{ProductionProposal.model_json_schema()}
"""
    
    # Generate
    response = await client.messages.create(
        model="claude-sonnet-4",  # or "claude-opus-4.6" for more ambitious concepts
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": creative_brief or "Propose a production for this site."}
        ],
    )
    
    # Parse response JSON into ProductionProposal
    proposal_data = json.loads(response.content.text)
    proposal = ProductionProposal(**proposal_data, parcel_id=parcel.id)
    
    return proposal
REST API:

python
POST /api/productions/generate
     Body: { parcel_id, creative_brief?, tier_filter?:, format?: "series" }[1][2]
     → Generates ProductionProposal, saves to DB, returns full JSON

GET  /api/productions/{id}
     → Returns ProductionProposal with full material_script

GET  /api/productions/{id}/material-script
     → Returns just the material_script timeline (for visualization)

POST /api/productions/{id}/iterate
     Body: { feedback: "make it darker and more claustrophobic" }
     → Regenerates proposal with user notes, creates new version
Tech stack:

Python 3.12, FastAPI 0.115+, Pydantic v2

Anthropic SDK (claude-sonnet-4 or claude-opus-4.6)

PostgreSQL JSONB for material_script storage

SQLAlchemy 2.0 async

Tests:

Mock Claude API responses with realistic fixtures

Test that generated proposals always include ≥1 MaterialCue per act

Test that tier_filter correctly limits available material systems

Test that material_script timeline has no temporal gaps

Test that transition times respect physical constraints (e.g., no olfactory changes <10 min apart)

Deliverables:

src/productions/models.py (SQLAlchemy models)

src/productions/api.py (FastAPI routes)

src/productions/generator.py (Claude API integration)

src/ai-engine/prompts/material_dramaturgy.txt (system prompt template)

tests/productions/test_api.py, tests/productions/test_generator.py

tests/fixtures/claude_responses.json (mock API responses)

README_productions.md explaining Material Dramaturgy framework

@sphere-scheduler
Scope: src/scheduling/, src/bookings/, tests/scheduling/, db/migrations/scheduling/

Mission: Build the temporal operating system that manages how Spheres divide their
time across production mode, public bookings, and community access — with material
transition planning as the core scheduling constraint.

Key insight: Unlike a hotel room (fixed 30-min turnover), a Sphere's transition time
is variable and depends on WHICH materials are changing and BY HOW MUCH.

Material transition time matrix (from research brief):

Material System	Min Transition	Max Transition	Bottleneck?
Acoustic metamaterial	0.025 sec	60 sec	No
Electrochromic surface	1 sec	5 sec	No
Projection/lighting	0.1 sec	10 sec	No
Haptic surface	0.025 sec	5 sec	No
Olfactory (scent clear)	600 sec	1200 sec	YES
Thermal (PCM)	300 sec	1800 sec	Sometimes
Shape memory elements	300 sec	3600 sec	Sometimes
4D printed deployables	1800 sec	3600 sec	Sometimes
Bioluminescent (persist)	N/A	N/A	N/A
Core models:

python
class Sphere(Base):
    __tablename__ = "spheres"
    __table_args__ = {"schema": "scheduling"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    parcel_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("land.parcels.id"))
    name: Mapped[str]
    
    # Status
    status: Mapped[str]  # "planning" | "construction" | "active_production" | 
                         # "legacy_soundstage" | "public_access" | "dormant"
    
    # Installed material systems (what hardware is physically present)
    material_inventory: Mapped[list[str]] = mapped_column(ARRAY(String))
    # e.g., ["acoustic_metamaterial", "olfactory_synthesis", "projection_mapping"]
    
    # Current operating mode
    current_mode: Mapped[str]  # "production" | "public" | "community" | "maintenance"
    
    # Base state (the "default" material configuration)
    base_state: Mapped[dict] = mapped_column(JSONB)  # MaterialConfiguration dict
    
    # Relationships
    time_slices: Mapped[list["TimeSlice"]] = relationship(back_populates="sphere")


class MaterialConfiguration(TypedDict):
    """
    A snapshot of all material states at a point in time.
    Stored in Sphere.base_state and TimeSlice.material_config as JSONB.
    """
    # Acoustic
    acoustic_reverb_time_seconds: float  # 0.5-5.0
    acoustic_absorption_profile: list[float]  # [0-1] by frequency band (125Hz, 250, 500, 1k, 2k, 4k, 8k)
    
    # Visual
    wall_color_rgb: tuple[int, int, int]
    wall_opacity: float  # 0-1 (electrochromic)
    light_color_temp_kelvin: int  # 2700-6500
    light_intensity_lux: int  # 50-1000
    
    # Haptic
    floor_haptic_pattern: str  # "off" | "gentle_rain" | "heartbeat" | "earthquake"
    floor_haptic_intensity: float  # 0-1
    
    # Olfactory
    scent_profile: dict[str, Any]
    # {
    #   "primary": "petrichor" | "cedar" | "coffee" | "ozone" | None,
    #   "secondary": str | None,
    #   "intensity": float 0-1
    # }
    
    # Thermal
    thermal_target_celsius: float  # 16-28
    
    # Shape memory (if installed)
    shape_memory_elements: list[dict]
    # [{"element_id": "wall_panel_3", "target_curvature": float 0-1}]


class TimeSlice(Base):
    __tablename__ = "time_slices"
    __table_args__ = {"schema": "scheduling"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    sphere_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scheduling.spheres.id"))
    
    # Temporal bounds (15-min minimum resolution)
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    
    # Mode
    mode: Mapped[str]  # "production" | "public" | "community" | "maintenance" | "transition"
    
    # Material configuration during this slice
    material_config: Mapped[dict] = mapped_column(JSONB)  # MaterialConfiguration dict
    
    # Transition buffer (calculated)
    transition_buffer_minutes: Mapped[int]  # time needed to reprogram materials from 
                                             # previous slice's config to this config
    
    # Booking reference
    booking_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("scheduling.bookings.id"))
    
    # Relationships
    sphere: Mapped["Sphere"] = relationship(back_populates="time_slices")
    booking: Mapped["Booking"] = relationship(back_populates="time_slices")


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"schema": "scheduling"}
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID]  # FK to users table (not in scope for this agent)
    sphere_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scheduling.spheres.id"))
    
    # Requested vs actual
    material_request: Mapped[dict] = mapped_column(JSONB)  # what user wants
    material_actual: Mapped[dict] = mapped_column(JSONB)   # what's achievable
    
    # Pricing
    pricing_usd: Mapped[float]  # calculated from duration × material_complexity × demand
    
    # Status
    status: Mapped[str]  # "pending" | "confirmed" | "active" | "completed" | "cancelled"
    
    # Relationships
    time_slices: Mapped[list["TimeSlice"]] = relationship(back_populates="booking")
Transition time calculator:

python
def calculate_transition_time(
    from_config: MaterialConfiguration,
    to_config: MaterialConfiguration,
    material_inventory: list[str],
) -> int:
    """
    Calculate minimum transition time in seconds between two material configurations.
    
    Returns the MAX of all individual material transition times (they can't happen
    fully in parallel due to shared control systems and safety protocols).
    
    Key insight: Olfactory is almost always the bottleneck (600-1200 sec).
    """
    
    transition_times = []
    
    # Acoustic metamaterial
    if "acoustic_metamaterial" in material_inventory:
        if from_config["acoustic_reverb_time_seconds"] != to_config["acoustic_reverb_time_seconds"]:
            transition_times.append(60)  # conservative; could be <1 sec for small changes
    
    # Olfactory (THE BOTTLENECK)
    if "olfactory_synthesis" in material_inventory:
        if from_config["scent_profile"]["primary"] != to_config["scent_profile"]["primary"]:
            transition_times.append(1200)  # 20 min for full scent clearing via HVAC
        elif from_config["scent_profile"]["intensity"] != to_config["scent_profile"]["intensity"]:
            transition_times.append(600)   # 10 min for intensity adjustment
    
    # Electrochromic
    if "electrochromic_surface" in material_inventory:
        if from_config["wall_opacity"] != to_config["wall_opacity"]:
            transition_times.append(5)
    
    # Haptic
    if "haptic_surface" in material_inventory:
        if from_config["floor_haptic_pattern"] != to_config["floor_haptic_pattern"]:
            transition_times.append(5)
    
    # Thermal (PCM)
    if "phase_change_panel" in material_inventory:
        temp_delta = abs(from_config["thermal_target_celsius"] - to_config["thermal_target_celsius"])
        if temp_delta > 0:
            transition_times.append(int(300 + temp_delta * 60))  # ~300-1800 sec
    
    # Shape memory
    if "shape_memory_element" in material_inventory:
        # Check if any element's target curvature changed
        from_elements = {e["element_id"]: e["target_curvature"] for e in from_config["shape_memory_elements"]}
        to_elements = {e["element_id"]: e["target_curvature"] for e in to_config["shape_memory_elements"]}
        if from_elements != to_elements:
            transition_times.append(1800)  # 30 min for shape memory activation
    
    # 4D printed deployables
    if "4d_printed_deployable" in material_inventory:
        # Assume any deployable change requires max time
        transition_times.append(3600)  # 60 min
    
    return max(transition_times) if transition_times else 0  # seconds
Conflict resolution:

python
async def find_available_slots(
    sphere_id: uuid.UUID,
    desired_start: datetime,
    desired_end: datetime,
    material_request: MaterialConfiguration,
) -> list[dict]:
    """
    Given a booking request, return available time slots that:
    1. Don't conflict with existing bookings
    2. Include sufficient transition buffer from previous slice
    
    If desired slot is unavailable, suggest alternatives:
    - Shift time forward/backward
    - Reduce material complexity (less scent = faster transitions)
    - Suggest different Sphere
    """
    
    sphere = await get_sphere(sphere_id)
    existing_slices = await get_time_slices(sphere_id, date_range=(desired_start, desired_end))
    
    # Check for conflicts
    conflicts = [s for s in existing_slices if slices_overlap(s, desired_start, desired_end)]
    
    if not conflicts:
        # Calculate transition time from previous slice
        prev_slice = await get_previous_slice(sphere_id, desired_start)
        transition_time_sec = calculate_transition_time(
            prev_slice.material_config if prev_slice else sphere.base_state,
            material_request,
            sphere.material_inventory,
        )
        
        # Check if there's enough buffer
        if prev_slice:
            actual_buffer_sec = (desired_start - prev_slice.end_time).total_seconds()
            if actual_buffer_sec < transition_time_sec:
                # Not enough time to transition
                suggested_start = prev_slice.end_time + timedelta(seconds=transition_time_sec)
                return [{"available": False, "reason": "insufficient_transition_buffer",
                         "suggested_start": suggested_start}]
        
        return [{"available": True, "transition_time_minutes": transition_time_sec // 60}]
    
    else:
        # Propose alternatives
        alternatives = []
        
        # Option 1: Shift time forward
        next_available = conflicts[-1].end_time + timedelta(seconds=1800)  # 30 min buffer
        alternatives.append({"type": "shift_time", "suggested_start": next_available})
        
        # Option 2: Reduce material complexity (remove olfactory if present)
        if material_request.get("scent_profile", {}).get("primary"):
            simplified_request = {**material_request, "scent_profile": {"primary": None, "intensity": 0}}
            alternatives.append({
                "type": "simplify_materials",
                "material_request": simplified_request,
                "note": "Removing scent reduces transition time to ~5 minutes"
            })
        
        # Option 3: Suggest different Sphere
        other_spheres = await find_spheres_with_availability(desired_start, desired_end)
        alternatives.extend([{"type": "different_sphere", "sphere_id": s.id} for s in other_spheres[:3]])
        
        return alternatives
REST API:

python
GET  /api/spheres/{id}/schedule?date_range=2026-03-15T00:00:00Z,2026-03-22T00:00:00Z
     → Returns all TimeSlices in date range with material configs

POST /api/spheres/{id}/bookings
     Body: { user_id, desired_start, desired_end, material_request: MaterialConfiguration }
     → Creates Booking if available, or returns alternatives if conflict

GET  /api/spheres/{id}/availability?duration=2h&material_complexity=medium
     → Returns next N available slots with sufficient transition buffers

PUT  /api/bookings/{id}/material-config
     Body: { material_request: MaterialConfiguration }
     → Updates requested config (recalculates transition times)

GET  /api/spheres/{id}/transition-time?from_config={...}&to_config={...}
     → Returns calculated transition time in seconds (for frontend preview)
Tech stack:

Python 3.12, FastAPI 0.115+, SQLAlchemy 2.0 async

PostgreSQL JSONB for material configs

Redis for availability caching (optional)

Celery for async transition planning (optional)

Consider interval tree library for efficient overlap detection

Tests:

Test that no two bookings overlap

Test that transition buffers are always respected

Test transition time calculator for every material system combo

Test conflict resolution returns valid alternatives

Load test: 1000 concurrent booking requests

Deliverables:

src/scheduling/models.py (Sphere, TimeSlice, Booking, MaterialConfiguration)

src/scheduling/api.py (FastAPI routes)

src/scheduling/transitions.py (transition time calculator)

src/scheduling/conflicts.py (conflict detection + resolution)

tests/scheduling/test_transitions.py, tests/scheduling/test_conflicts.py, tests/scheduling/test_api.py

README_scheduling.md explaining the temporal operating system

@material-orchestrator
Scope: src/materials/, src/hardware-abstraction/, tests/materials/

Mission: Build the hardware abstraction layer that translates high-level
MaterialConfiguration objects into control signals for actual material systems. This is
the bridge between scheduling and physical hardware.

Since we don't have real hardware yet, build a full simulation layer that:

Maintains realistic internal state for each material system

Transitions take physically accurate time (use asyncio.sleep)

Introduces random failures at configurable probability

Streams real-time state via WebSocket (this IS the investor demo)

Architecture:

python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

class MaterialSystemType(str, Enum):
    ACOUSTIC_METAMATERIAL = "acoustic_metamaterial"
    HAPTIC_SURFACE = "haptic_surface"
    OLFACTORY_SYNTHESIS = "olfactory_synthesis"
    ELECTROCHROMIC_SURFACE = "electrochromic_surface"
    PROJECTION_MAPPING = "projection_mapping"
    PHASE_CHANGE_PANEL = "phase_change_panel"
    SHAPE_MEMORY_ELEMENT = "shape_memory_element"
    DEPLOYABLE_4D = "4d_printed_deployable"
    BIOLUMINESCENT_COATING = "bioluminescent_coating"


class DriverResponse(TypedDict):
    success: bool
    system_type: MaterialSystemType
    current_state: dict[str, Any]
    transition_time_seconds: float
    errors: list[str]


class ValidationResult(TypedDict):
    valid: bool
    errors: list[str]
    warnings: list[str]


class MaterialDriver(ABC):
    """Abstract base class for all material system drivers."""
    
    system_type: MaterialSystemType
    trl: int  # Technology Readiness Level (1-9)
    
    @abstractmethod
    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        """Send control signals to hardware (or simulator)."""
        pass
    
    @abstractmethod
    async def read_state(self) -> dict[str, Any]:
        """Read current material state from sensors (or simulator)."""
        pass
    
    @abstractmethod
    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        """Check if requested config is achievable within hardware limits."""
        pass
    
    @abstractmethod
    async def emergency_reset(self) -> None:
        """Return to safe base state immediately (for safety monitor)."""
        pass
Concrete driver implementations (simulated):

python
class AcousticMetamaterialDriver(MaterialDriver):
    """
    Controls LRA (Linear Resonant Actuator) arrays to create tunable acoustic properties.
    Research basis: Nature Communications 2025 paper on light-responsive elastic metamaterials.
    """
    
    system_type = MaterialSystemType.ACOUSTIC_METAMATERIAL
    trl = 7  # Lab-scale prototypes demonstrated
    
    def __init__(self):
        self.current_reverb_time = 1.5  # seconds
        self.current_absorption_profile = [0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3]  # 7 freq bands
    
    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        target_reverb = config.get("acoustic_reverb_time_seconds", self.current_reverb_time)
        target_absorption = config.get("acoustic_absorption_profile", self.current_absorption_profile)
        
        # Simulate electrical switching (physically <25ms per actuator)
        await asyncio.sleep(0.06)  # 60ms for array of actuators
        
        self.current_reverb_time = target_reverb
        self.current_absorption_profile = target_absorption
        
        return DriverResponse(
            success=True,
            system_type=self.system_type,
            current_state={"reverb_time": target_reverb, "absorption_profile": target_absorption},
            transition_time_seconds=0.06,
            errors=[],
        )
    
    async def read_state(self) -> dict[str, Any]:
        return {"reverb_time": self.current_reverb_time, "absorption_profile": self.current_absorption_profile}
    
    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        errors = []
        warnings = []
        
        reverb = config.get("acoustic_reverb_time_seconds")
        if reverb and not (0.5 <= reverb <= 5.0):
            errors.append(f"Reverb time {reverb} out of range [0.5, 5.0]")
        
        absorption = config.get("acoustic_absorption_profile")
        if absorption and len(absorption) != 7:
            errors.append(f"Absorption profile must have 7 frequency bands")
        
        return ValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)
    
    async def emergency_reset(self) -> None:
        self.current_reverb_time = 1.5
        self.current_absorption_profile = [0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.3]


class OlfactorySynthesisDriver(MaterialDriver):
    """
    Controls 40-component scent blender via subtractive synthesis.
    Research basis: Digital Olfaction Society 2024 Best Innovation Award.
    """
    
    system_type = MaterialSystemType.OLFACTORY_SYNTHESIS
    trl = 6  # Engineering prototypes demonstrated in lab
    
    def __init__(self):
        self.current_scent_primary = None
        self.current_scent_secondary = None
        self.current_intensity = 0.0
        self.hvac_clearing_time_sec = 1200  # 20 min worst case
    
    async def apply_config(self, config: dict[str, Any]) -> DriverResponse:
        scent_profile = config.get("scent_profile", {})
        target_primary = scent_profile.get("primary")
        target_intensity = scent_profile.get("intensity", 0.0)
        
        # If changing scent (not just intensity), need full HVAC clearing cycle
        if target_primary != self.current_scent_primary and self.current_scent_primary is not None:
            await asyncio.sleep(self.hvac_clearing_time_sec)  # 20 min scent clearing
        elif target_primary == self.current_scent_primary and target_intensity != self.current_intensity:
            await asyncio.sleep(600)  # 10 min for intensity adjustment
        
        self.current_scent_primary = target_primary
        self.current_intensity = target_intensity
        
        return DriverResponse(
            success=True,
            system_type=self.system_type,
            current_state={"primary": target_primary, "intensity": target_intensity},
            transition_time_seconds=self.hvac_clearing_time_sec if target_primary != self.current_scent_primary else 600,
            errors=[],
        )
    
    async def read_state(self) -> dict[str, Any]:
        return {"primary": self.current_scent_primary, "intensity": self.current_intensity}
    
    async def validate_config(self, config: dict[str, Any]) -> ValidationResult:
        # Implement VOC safety limits, etc.
        return ValidationResult(valid=True, errors=[], warnings=[])
    
    async def emergency_reset(self) -> None:
        self.current_scent_primary = None
        self.current_intensity = 0.0


# Implement similar drivers for:
# - ElectrochromicSurfaceDriver
# - HapticSurfaceDriver
# - ProjectionMappingDriver
# - PhaseChangePanelDriver
# - ShapeMemoryElementDriver
# - Deployable4DDriver
# - BioluminescentCoatingDriver (read-only, reports health)
Orchestrator (coordinates all drivers):

python
class MaterialOrchestrator:
    """Coordinates all material drivers for a Sphere."""
    
    def __init__(self, sphere_id: uuid.UUID, material_inventory: list[str]):
        self.sphere_id = sphere_id
        self.drivers: dict[MaterialSystemType, MaterialDriver] = {}
        
        # Instantiate drivers based on inventory
        for system_type_str in material_inventory:
            system_type = MaterialSystemType(system_type_str)
            self.drivers[system_type] = self._create_driver(system_type)
    
    def _create_driver(self, system_type: MaterialSystemType) -> MaterialDriver:
        match system_type:
            case MaterialSystemType.ACOUSTIC_METAMATERIAL:
                return AcousticMetamaterialDriver()
            case MaterialSystemType.OLFACTORY_SYNTHESIS:
                return OlfactorySynthesisDriver()
            # ... etc for all drivers
    
    async def apply_configuration(
        self,
        target: MaterialConfiguration,
        transition_plan: list[str],  # ordered list of system types to transition
    ) -> dict[str, DriverResponse]:
        """
        Execute a full material state transition.
        
        Applies changes in the order specified by transition_plan to minimize
        total changeover time. Monitors all drivers for errors. Implements
        rollback on partial failure.
        """
        
        responses = {}
        
        for system_type_str in transition_plan:
            system_type = MaterialSystemType(system_type_str)
            driver = self.drivers.get(system_type)
            
            if not driver:
                continue
            
            # Extract relevant config subset for this driver
            driver_config = self._extract_driver_config(target, system_type)
            
            # Validate before applying
            validation = await driver.validate_config(driver_config)
            if not validation["valid"]:
                # ROLLBACK: revert all previous changes
                await self._rollback(responses.keys())
                raise MaterialOrchestrationError(f"Validation failed for {system_type}: {validation['errors']}")
            
            # Apply
            try:
                response = await driver.apply_config(driver_config)
                responses[system_type] = response
            except Exception as e:
                # ROLLBACK
                await self._rollback(responses.keys())
                raise MaterialOrchestrationError(f"Driver {system_type} failed: {e}")
        
        return responses
    
    async def _rollback(self, applied_systems: list[MaterialSystemType]) -> None:
        """Emergency rollback: reset all systems that were already transitioned."""
        for system_type in applied_systems:
            driver = self.drivers.get(system_type)
            if driver:
                await driver.emergency_reset()
    
    def _extract_driver_config(self, full_config: MaterialConfiguration, system_type: MaterialSystemType) -> dict:
        """Extract the subset of MaterialConfiguration relevant to this driver."""
        # Map MaterialConfiguration fields to driver-specific keys
        # ...implementation details...
WebSocket state streaming (THE DEMO):

python
from fastapi import WebSocket

@app.websocket("/api/spheres/{sphere_id}/material-stream")
async def material_state_stream(websocket: WebSocket, sphere_id: uuid.UUID):
    """
    Real-time material state updates at 10Hz.
    This is the live demo that shows investors what Sphere orchestration looks like.
    """
    
    await websocket.accept()
    
    orchestrator = await get_orchestrator(sphere_id)
    
    try:
        while True:
            # Read current state from all drivers
            state = {}
            for system_type, driver in orchestrator.drivers.items():
                state[system_type.value] = await driver.read_state()
            
            # Send to client
            await websocket.send_json({
                "sphere_id": str(sphere_id),
                "timestamp": datetime.utcnow().isoformat(),
                "material_state": state,
            })
            
            await asyncio.sleep(0.1)  # 10Hz update rate
    
    except WebSocketDisconnect:
        pass
Safety monitor:

python
class SafetyMonitor:
    """Continuous monitoring during any active booking."""
    
    async def monitor(self, sphere_id: uuid.UUID, orchestrator: MaterialOrchestrator):
        while True:
            # Check all drivers for safety violations
            for system_type, driver in orchestrator.drivers.items():
                state = await driver.read_state()
                
                # Olfactory VOC limits
                if system_type == MaterialSystemType.OLFACTORY_SYNTHESIS:
                    intensity = state.get("intensity", 0)
                    if intensity > 0.8:
                        logger.warning(f"Olfactory intensity {intensity} approaching limit")
                        # Could auto-adjust or trigger alert
                
                # Thermal bounds
                if system_type == MaterialSystemType.PHASE_CHANGE_PANEL:
                    temp = state.get("temperature_celsius", 21)
                    if temp < 16 or temp > 28:
                        logger.error(f"Thermal system out of safe range: {temp}°C")
                        await orchestrator._rollback(orchestrator.drivers.keys())
                        raise SafetyViolationError(f"Temperature {temp}°C")
            
            await asyncio.sleep(1.0)  # Check every second
REST + WebSocket API:

python
GET  /api/spheres/{id}/material-state
     → Current state of all material systems (JSON snapshot)

WS   /api/spheres/{id}/material-stream
     → Real-time state updates at 10Hz (WebSocket)

POST /api/spheres/{id}/material-command
     Body: { system_type, config }
     → Direct driver command (for testing/calibration)

POST /api/spheres/{id}/emergency-reset
     → Triggers emergency_reset() on all drivers

GET  /api/materials/drivers
     → List available driver types with TRL info
Tech stack:

Python 3.12, FastAPI 0.115+, WebSockets, asyncio

Pydantic for all models

structlog for structured logging

(Future) MQTT or ROS2 for real hardware integration

Tests:

Test that orchestrator applies configs in correct order

Test rollback on partial driver failure

Test that simulator produces realistic transition timing

Test safety monitor triggers emergency reset on threshold violations

Test WebSocket stream delivers ≥10Hz updates

Deliverables:

src/materials/drivers/base.py (MaterialDriver ABC)

src/materials/drivers/acoustic.py, olfactory.py, etc. (all 9 drivers)

src/materials/orchestrator.py (MaterialOrchestrator)

src/materials/safety.py (SafetyMonitor)

src/materials/api.py (REST + WebSocket routes)

tests/materials/test_drivers.py, test_orchestrator.py, test_safety.py

README_materials.md explaining the hardware abstraction architecture

@public-portal
Scope: src/frontend/, tests/frontend/

Mission: Build the Next.js web application where the public discovers Spheres,
explores AI-generated production proposals, and books time slices with a visual material
configuration builder.

Pages/views:

1. Map Explorer (app/page.tsx)
Full-screen interactive map showing vacant land + active Spheres.

Tech: Mapbox GL JS or MapLibre + Deck.gl for rendering 40K+ parcels

Layers:

Vacant parcels (color-coded by sphere_viability_score — red=low, green=high)

Active Spheres (glowing animated markers)

Transit overlay (optional toggle)

Zoning overlay (optional toggle)

Interactions:

Click parcel → show popup with details + "What could this become?" button

"What could this become?" → triggers /api/productions/generate → shows AI proposal in modal

Click active Sphere → navigate to Sphere detail page

Filter: min_score, min_area, zoning_code

Implementation:

tsx
'use client';

import { useEffect, useState } from 'react';
import Map, { Source, Layer, Popup } from 'react-map-gl';
import { ParcelRecord, SphereViabilityScore } from '@/types';

export default function MapExplorer() {
  const [parcels, setParcels] = useState<ParcelRecord[]>([]);
  const [selectedParcel, setSelectedParcel] = useState<ParcelRecord | null>(null);
  
  // Fetch parcels from /api/land/parcels?bbox=...
  // Render as GeoJSON layer with data-driven styling based on sphere_viability_score
  
  return (
    <Map
      mapboxAccessToken={process.env.NEXT_PUBLIC_MAPBOX_TOKEN}
      initialViewState={{
        longitude: -75.1652,
        latitude: 39.9526,
        zoom: 11,
      }}
      style={{ width: '100vw', height: '100vh' }}
      mapStyle="mapbox://styles/mapbox/dark-v11"
    >
      <Source id="parcels" type="geojson" data={parcelsGeoJSON}>
        <Layer
          id="parcels-fill"
          type="fill"
          paint={{
            'fill-color': [
              'interpolate',
              ['linear'],
              ['get', 'sphere_viability_score'],
              0, '#ff0000',
              0.5, '#ffff00',
              1, '#00ff00',
            ],
            'fill-opacity': 0.6,
          }}
        />
      </Source>
      
      {selectedParcel && (
        <Popup
          longitude={selectedParcel.centroid.coordinates}
          latitude={selectedParcel.centroid.coordinates}[1]
          onClose={() => setSelectedParcel(null)}
        >
          <ParcelPopup parcel={selectedParcel} />
        </Popup>
      )}
    </Map>
  );
}
2. Sphere Detail Page (app/spheres/[id]/page.tsx)
Sections:

Hero: 3D material state visualization (Three.js)

Shows a simplified 3D model of the Sphere space

Real-time material colors, textures, acoustic visualization

Connects to WebSocket /api/spheres/{id}/material-stream for live updates

Timeline: visual schedule showing production blocks, public bookings, transitions

Horizontal timeline component (similar to Google Calendar month view)

Color-coded by mode (production=blue, public=green, community=purple, transition=gray)

"Book a Slice" CTA → opens booking modal

Production history: carousel of past films/shows that used this Sphere

Material inventory: grid of installed systems with TRL badges

Three.js material viz:

tsx
'use client';

import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { useWebSocket } from '@/hooks/useWebSocket';

export function MaterialVisualization({ sphereId }: { sphereId: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { data: materialState } = useWebSocket(`/api/spheres/${sphereId}/material-stream`);
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    // Initialize Three.js scene
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.current });
    
    // Create a simple room geometry (box)
    const roomGeometry = new THREE.BoxGeometry(10, 5, 10);
    const roomMaterial = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      opacity: 0.5,
      transparent: true,
    });
    const room = new THREE.Mesh(roomGeometry, roomMaterial);
    scene.add(room);
    
    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      
      // Update material properties based on materialState
      if (materialState) {
        // Wall color from electrochromic surface
        const [r, g, b] = materialState.wall_color_rgb || ;
        roomMaterial.color.setRGB(r / 255, g / 255, b / 255);
        roomMaterial.opacity = materialState.wall_opacity || 0.5;
        
        // Could add acoustic visualization (particles, waves)
        // Could add scent visualization (colored fog)
      }
      
      renderer.render(scene, camera);
    }
    animate();
    
    return () => {
      renderer.dispose();
    };
  }, [materialState]);
  
  return <canvas ref={canvasRef} className="w-full h-96" />;
}
3. Booking Flow (app/spheres/[id]/book/page.tsx)
Steps:

Select date/time range (date picker + time slider)

Material configuration builder (the key UX innovation):

Visual sliders for each material property

Real-time 3D preview showing what the Sphere will look like

Pricing calcula

[Message truncated - exceeded 50,000 character limit]