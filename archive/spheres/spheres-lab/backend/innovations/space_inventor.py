"""
SPHERES Innovation Laboratory — Space Inventor domain.

Spatial-invention seed innovations and generator templates for radically
reimagining what a "space" can be in Philadelphia.  These six Sphere concepts
push beyond vacant-lot remediation into water, time, augmented reality,
weather, underground infrastructure, and the overlooked thresholds between
existing structures.
"""

# ---------------------------------------------------------------------------
# Seed Innovations — 6 wild, imaginative Sphere-branded spatial inventions
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # 1 — Water Spheres
    {
        "title": "Water Spheres",
        "summary": (
            "Floating platform concepts for the Delaware and Schuylkill rivers. "
            "Modular 40x60-foot decks with native gardens, a performance stage, "
            "and a covered gathering area. Anchored with marine-grade mooring "
            "systems and accessible by gangway from existing piers. Each platform "
            "is a self-contained public space on the water — a sphere of civic "
            "life untethered from land."
        ),
        "category": "spatial-invention",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "review",
        "details": {
            "square_footage": 2400,
            "materials": [
                "marine-grade aluminum frame with hot-dip galvanized steel substructure",
                "closed-cell polyethylene float drums (48x48x16 in, 1800 lb buoyancy each)",
                "composite decking (recycled HDPE/wood fiber, non-slip texture)",
                "native wetland planters (coir-lined steel troughs with reed, sedge, iris)",
                "retractable fabric canopy (marine-grade Sunbrella, wind-rated to 45 mph)",
                "portable performance stage riser system (4x8 ft interlocking panels)",
                "LED perimeter lighting (solar-charged, IP68 waterproof)",
                "marine-grade mooring chain, swivels, and concrete anchor blocks (4-ton)",
            ],
            "installation_time": (
                "8-12 weeks for fabrication and float assembly; 2 weeks for on-water "
                "positioning, mooring installation, and gangway connection to pier"
            ),
            "cost_per_unit": 285000,
            "capacity": "80 seated / 150 standing per platform module",
            "concept_rendering_notes": (
                "Render as a low-profile wooden deck floating at pier-height on the "
                "Schuylkill near Bartram's Garden. Native grasses sway in planters "
                "along the perimeter. A fabric canopy billows over the gathering "
                "area at one end. A small stage faces rows of moveable chairs. "
                "String lights arc overhead. The city skyline glows in the background. "
                "Gangway connects to an existing concrete pier with ADA-compliant slope."
            ),
            "site_requirements": [
                "US Army Corps of Engineers Section 10 permit (navigable waterway)",
                "US Coast Guard private aids to navigation approval",
                "Pennsylvania DEP Chapter 105 water obstruction permit",
                "Philadelphia Water Department stormwater exemption (floating structure)",
                "Minimum 6-foot water depth at mean low tide",
                "Existing pier or bulkhead within 60 feet for gangway connection",
                "ADA-compliant gangway with maximum 1:12 slope at all tide levels",
                "Liability insurance rider for over-water public assembly",
            ],
        },
        "tags": [
            "water",
            "floating",
            "river",
            "delaware",
            "schuylkill",
            "platform",
            "marine",
            "public-space",
        ],
    },
    # 2 — Temporal Spheres
    {
        "title": "Temporal Spheres",
        "summary": (
            "Time-locked activations that create urgency and ritual. Dawn-only "
            "sound baths (5:30-7:00 AM). Midnight-only outdoor film screenings "
            "(11:00 PM-1:00 AM). Solstice-only fire installations. Equinox-only "
            "seed ceremonies. Full-moon drum circles. Each activation type builds "
            "its own following and community — a sphere of belonging defined not "
            "by place but by when you show up."
        ),
        "category": "spatial-invention",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 5,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "square_footage": 3000,
            "materials": [
                "crystal and Tibetan singing bowls (set of 12, tuned to C-major scale)",
                "portable outdoor cinema rig (inflatable 16-ft screen, 5000-lumen projector)",
                "fire-pit steel cauldrons (36-in diameter, NFPA-compliant spark screens)",
                "heirloom seed kits (50 packets of regionally adapted open-pollinated varieties)",
                "djembe and frame drums (community set of 30, weather-resistant synthetic heads)",
                "portable PA system (battery-powered, 500W, directional speakers)",
                "LED pathway markers (solar stakes, amber-only to preserve night atmosphere)",
                "wool blankets and yoga mats (loaner fleet of 40)",
            ],
            "installation_time": (
                "90 minutes setup / 60 minutes teardown per activation; all equipment "
                "fits in a single cargo van and is fully portable"
            ),
            "cost_per_unit": 4500,
            "capacity": "30-60 participants per activation depending on type",
            "concept_rendering_notes": (
                "Five vignettes: (1) Dawn sound bath — silhouettes of 30 people "
                "lying on mats in a vacant lot as pink light breaks over rowhouse "
                "rooftops, singing bowls glowing. (2) Midnight film — faces lit by "
                "a projected film on an inflatable screen, blankets everywhere, "
                "stars above. (3) Solstice fire — a steel cauldron blazing in the "
                "center of a circle of people, shadows dancing on brick walls. "
                "(4) Equinox seeds — hands pressing seeds into soil in small pots, "
                "a table of seedlings, morning light. (5) Full-moon drums — a drum "
                "circle under a bright moon on an open lot, the city quiet around them."
            ),
            "site_requirements": [
                "Vacant lot or park with minimum 3,000 sq ft open area",
                "For dawn/midnight events: residential noise buffer of 150+ feet or "
                "written neighbor consent from adjacent blocks",
                "For fire installations: Philadelphia Fire Department open-burn permit "
                "and on-site extinguisher (minimum 10-lb ABC rated)",
                "For film screenings: ASCAP/BMI blanket license or public-domain content",
                "Portable restroom within 200 feet for events exceeding 1 hour",
                "Liability insurance covering public assembly (minimum $1M per occurrence)",
                "Community ambassador present at every activation for safety and welcome",
            ],
        },
        "tags": [
            "temporal",
            "ritual",
            "dawn",
            "midnight",
            "solstice",
            "equinox",
            "full-moon",
            "sound-bath",
            "community",
        ],
    },
    # 3 — Invisible Spheres
    {
        "title": "Invisible Spheres",
        "summary": (
            "An augmented-reality overlay that shows activation designs on empty "
            "lots through your phone camera. Point at any vacant lot and see a "
            "proposed pocket park, garden, or gathering space rendered in full 3D "
            "with realistic materials, lighting, and people. Community members can "
            "vote on designs, leave comments pinned to specific spots, and watch "
            "the winning concept get built. Integrates with SPHERES-viz WebGL "
            "episodes so the same 3D assets flow between web and AR."
        ),
        "category": "spatial-invention",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "square_footage": 0,
            "materials": [
                "ARKit/ARCore native mobile application (iOS 16+ / Android 13+)",
                "LiDAR-scanned 3D base meshes of 200+ Philadelphia vacant lots",
                "PBR material library (concrete, brick, wood, planting, water, steel)",
                "Animated human figures for scale and activity visualization",
                "Cloud-hosted design asset pipeline (glTF 2.0, Draco-compressed)",
                "SPHERES-viz WebGL episode bridge API for shared 3D scene graph",
                "GPS + visual-inertial odometry for sub-meter placement accuracy",
                "Firebase backend for community votes, comments, and moderation",
            ],
            "installation_time": (
                "6-month development cycle for MVP; each new lot scan takes 2 hours "
                "of on-site LiDAR capture and 1 week of 3D processing; new design "
                "proposals can be authored and published in 2-3 days by trained "
                "SPHERES design fellows"
            ),
            "cost_per_unit": 120000,
            "capacity": (
                "Unlimited concurrent users per lot; voting system supports city-wide "
                "participation; design library scales to 1,000+ lots over 3 years"
            ),
            "concept_rendering_notes": (
                "Show a split-screen: left half is a phone camera view of a weedy "
                "vacant lot on a North Philadelphia block; right half is the same "
                "view through the app with a lush pocket park overlaid — raised "
                "beds, a small pavilion, string lights, people sitting on benches. "
                "A voting UI floats at the bottom: thumbs up/down, comment bubble. "
                "In the corner, a 'See in SPHERES-viz' button links to the full "
                "WebGL fly-through of the design."
            ),
            "site_requirements": [
                "Each lot requires a one-time LiDAR scan (iPad Pro or iPhone Pro with LiDAR)",
                "GPS coordinates and Philadelphia OPA parcel ID for database linkage",
                "Street-level photo documentation (8 cardinal/intercardinal angles)",
                "Lot must be accessible from public sidewalk for AR viewing (no trespass)",
                "City Wi-Fi or cellular coverage sufficient for AR asset streaming",
                "Community engagement session before publishing designs for a new lot",
                "Moderation policy for user-generated comments (hate-speech filter, review queue)",
            ],
        },
        "tags": [
            "augmented-reality",
            "AR",
            "3D",
            "community-design",
            "voting",
            "SPHERES-viz",
            "WebGL",
            "vacant-lot",
            "digital",
        ],
    },
    # 4 — Weather Spheres
    {
        "title": "Weather Spheres",
        "summary": (
            "Activations designed FOR weather, not despite it. Rain concerts that "
            "exploit the acoustic properties of rain falling on different surfaces "
            "— metal, wood, stone, water. Snow art installations that appear only "
            "during snowfall, with stencils and colored-water sprayers revealing "
            "patterns as flakes accumulate. Fog gardens planted with species that "
            "create visible microclimates in morning mist. Wind harps — aeolian "
            "string instruments strung across vacant lots that sing only when the "
            "wind blows."
        ),
        "category": "spatial-invention",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "review",
        "details": {
            "square_footage": 4000,
            "materials": [
                "rain-concert surface array: corrugated steel panels, cedar planks, "
                "slate tiles, shallow stone basins (each 4x8 ft, angled at 15 degrees)",
                "snow-art stencil kit: laser-cut HDPE stencils (4x4 ft), food-grade "
                "colorant sprayers, reflective ground markers for stencil placement",
                "fog-garden plant palette: giant miscanthus, Joe-Pye weed, ironweed, "
                "switchgrass, river birch (high transpiration species for mist effect)",
                "aeolian wind harps: marine-grade stainless steel wire (0.015-0.045 in), "
                "resonating cedar sound boxes (12x6x6 in), galvanized steel guy-wire "
                "masts (16 ft tall, ground-anchored)",
                "weather monitoring station (anemometer, rain gauge, temp/humidity sensor)",
                "SMS/app alert system for weather-triggered activation notifications",
            ],
            "installation_time": (
                "Rain concert surfaces: 2 weeks fabrication, 1 week installation. "
                "Snow art stencils: pre-cut and stored, deployed in 30 minutes when "
                "snow forecast confirmed. Fog garden: 1 full planting season to "
                "establish. Wind harps: 3 days per installation including mast "
                "anchoring and wire tuning."
            ),
            "cost_per_unit": 22000,
            "capacity": (
                "Rain concerts: 50-80 listeners seated under adjacent covered area. "
                "Snow art: neighborhood-scale viewing (visible from street). "
                "Fog gardens: contemplative walking for 10-20 at a time. "
                "Wind harps: audible within 200-foot radius, unlimited passive listeners."
            ),
            "concept_rendering_notes": (
                "Four panels: (1) Rain concert — overhead view of angled metal, wood, "
                "and stone surfaces in a grid pattern on a vacant lot, rain falling, "
                "people huddled under a canopy at the edge listening with eyes closed. "
                "(2) Snow art — aerial drone shot of a vacant lot with a massive "
                "geometric mandala appearing in fresh snow, colored lines radiating "
                "outward, neighborhood kids at the edges watching. (3) Fog garden — "
                "early morning, dense mist rising from tall grasses and wildflowers "
                "on a lot between rowhouses, a figure walking a path barely visible. "
                "(4) Wind harps — wires catching golden-hour light between two steel "
                "masts on an open lot, a person leaning close to a cedar sound box, "
                "hair blowing."
            ),
            "site_requirements": [
                "Rain concert: lot with drainage slope away from adjacent structures; "
                "adjacent covered viewing area or deployable canopy",
                "Snow art: flat lot minimum 4,000 sq ft with street visibility; "
                "food-grade colorant only (FDA-approved, biodegradable)",
                "Fog garden: lot with eastern exposure for morning sun/mist interaction; "
                "soil capable of supporting deep-rooted perennials (no hardpan)",
                "Wind harps: open lot with minimum 80-ft clear span for wire runs; "
                "no overhead power lines within 30 feet; structural engineering review "
                "for mast anchoring in Philadelphia clay soils",
                "Weather station data feed for automated activation alerts",
                "Community notification system (SMS opt-in list) for weather-triggered events",
            ],
        },
        "tags": [
            "weather",
            "rain",
            "snow",
            "fog",
            "wind",
            "acoustic",
            "aeolian",
            "ephemeral",
            "climate",
        ],
    },
    # 5 — Underground Spheres
    {
        "title": "Underground Spheres",
        "summary": (
            "Repurposing Philadelphia's abandoned subway stations, utility tunnels, "
            "and basement vaults as subterranean activation spaces. Cave-like "
            "meditation rooms with natural acoustics and controlled darkness. "
            "Underground markets selling goods made in the tunnels themselves. "
            "Mycology labs growing gourmet and medicinal mushrooms in the perpetual "
            "dark and stable humidity of forgotten infrastructure."
        ),
        "category": "spatial-invention",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "review",
        "details": {
            "square_footage": 6000,
            "materials": [
                "structural shoring and stabilization (steel I-beams, concrete underpinning)",
                "waterproofing membrane system (bentonite clay + HDPE sheet, drainage mat)",
                "HVAC forced-air ventilation with HEPA filtration and CO2 monitoring",
                "emergency egress lighting and wayfinding (photoluminescent strips, battery backup)",
                "acoustic treatment panels (recycled cotton batts in perforated steel frames)",
                "mushroom cultivation shelving (stainless steel metro racks, 4-tier, 6-ft)",
                "substrate mixing station (pasteurization drum, grain spawn prep area)",
                "low-voltage LED grow lights (red/blue spectrum, timer-controlled)",
                "meditation room furnishings (wool cushions, beeswax candles, sound system)",
            ],
            "installation_time": (
                "12-18 months including structural assessment, environmental remediation "
                "(asbestos/lead abatement if present), waterproofing, ventilation "
                "installation, and buildout of program spaces. Phased opening: "
                "mycology lab first (month 12), meditation rooms (month 15), "
                "market space (month 18)."
            ),
            "cost_per_unit": 450000,
            "capacity": (
                "Meditation rooms: 15-20 per session. Underground market: 200 visitors "
                "per hour with 12 vendor stalls. Mycology lab: 3-5 cultivators "
                "producing 200 lbs/week of oyster, shiitake, and lion's mane mushrooms."
            ),
            "concept_rendering_notes": (
                "Three scenes: (1) Meditation room — a vaulted brick tunnel with "
                "warm amber light pooling on cushions arranged in a circle, people "
                "sitting in stillness, condensation glistening on century-old brick. "
                "(2) Underground market — a long tunnel with vendor stalls in arched "
                "alcoves, string lights overhead, shoppers browsing mushrooms, "
                "fermented foods, and handmade goods. The ceiling curves overhead "
                "like a cathedral. (3) Mycology lab — blue-white LED glow on rows of "
                "shelving bags, fat oyster mushroom clusters bursting from substrate "
                "blocks, a cultivator in an apron taking notes on a clipboard."
            ),
            "site_requirements": [
                "Structural engineering assessment of tunnel/vault integrity (load rating)",
                "Environmental Phase II assessment (asbestos, lead paint, PCBs, radon)",
                "SEPTA or Philadelphia Water Department access agreement (depending on tunnel owner)",
                "Philadelphia L&I special permit for below-grade public assembly",
                "Fire marshal approval with two-point emergency egress and suppression system",
                "Continuous air-quality monitoring (CO2, CO, particulates, humidity)",
                "Flood risk assessment and sump-pump backup system",
                "ADA-accessible entry (elevator or ramp to grade, maximum 1:12 slope)",
                "Insurance carrier willing to underwrite subterranean public occupancy",
            ],
        },
        "tags": [
            "underground",
            "subterranean",
            "tunnel",
            "subway",
            "vault",
            "meditation",
            "mycology",
            "mushroom",
            "market",
            "adaptive-reuse",
        ],
    },
    # 6 — Threshold Spheres
    {
        "title": "Threshold Spheres",
        "summary": (
            "The spaces between — activating the edges, boundaries, and transitions "
            "that everyone walks past and nobody thinks to use. The 3-foot gap "
            "between two rowhouses. The 18-inch strip between sidewalk and street. "
            "The rooftop parapet edge. The underside of a fire escape. Micro-"
            "activations in leftover space: a single chair and reading lamp in a "
            "rowhouse gap, a moss garden in a tree-pit, a wind chime installation "
            "on a fire escape."
        ),
        "category": "spatial-invention",
        "impact_level": 3,
        "feasibility": 5,
        "novelty": 5,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "square_footage": 50,
            "materials": [
                "rowhouse-gap kit: weatherproof folding chair, clip-on solar reading "
                "lamp, wall-mounted book box, narrow planter (6x36 in) with shade ferns",
                "curb-strip kit: modular moss tiles (12x12 in, pre-grown on mesh backing), "
                "miniature pollinator plugs (creeping thyme, sedum, clover), edging stones",
                "rooftop-edge kit: wind-rated planter boxes (self-watering, 8x36 in), "
                "aeolian chimes (anodized aluminum tubes, stainless steel cable), "
                "solar-powered LED strip (warm white, adhesive-mount)",
                "fire-escape kit: hanging fabric planter (UV-resistant canvas, 3-gallon), "
                "clip-on bird feeder, small wind spinner",
                "tree-pit kit: coir fiber mat, shade-tolerant moss plugs, miniature "
                "fairy-garden elements (ceramic, weatherproof), interpretive mini-sign",
            ],
            "installation_time": (
                "15-45 minutes per micro-activation depending on type; all kits "
                "fit in a backpack or small tote bag; no tools beyond a screwdriver "
                "and zip ties required"
            ),
            "cost_per_unit": 150,
            "capacity": (
                "1-3 people per activation (by design — these are intimate, personal "
                "moments of discovery); cumulative impact at scale when 100+ micro-"
                "activations dot a neighborhood"
            ),
            "concept_rendering_notes": (
                "A collage of tiny moments: (1) A narrow gap between two brick "
                "rowhouses — just wide enough for a single wooden chair, a clip-on "
                "lamp, and a small shelf of books. A person reads in this private "
                "sliver of space, sky visible as a thin blue strip above. (2) A "
                "tree pit on a busy sidewalk transformed into a miniature moss "
                "garden with tiny ceramic mushrooms and a hand-lettered sign: "
                "'Threshold Sphere #47.' (3) A fire-escape landing with a hanging "
                "canvas planter overflowing with trailing nasturtiums, a wind "
                "spinner catching light. (4) The 18-inch curb strip between "
                "sidewalk and street blooming with creeping thyme, bees hovering. "
                "(5) A rooftop parapet edge lined with slim planters and aluminum "
                "chimes catching the wind."
            ),
            "site_requirements": [
                "Property owner consent for any installation attached to a building",
                "No obstruction of pedestrian right-of-way (maintain 4-ft clear sidewalk)",
                "No obstruction of fire-escape egress path (NFPA 101 compliance)",
                "Lightweight materials only for fire-escape and rooftop installations "
                "(under 5 lbs per attachment point)",
                "Rowhouse-gap installations require verification that gap is not an active "
                "utility easement (check with PGW and PECO)",
                "Curb-strip plantings must comply with Philadelphia Streets Department "
                "tree-pit regulations (no height above 18 inches)",
                "All installations removable without damage to host structure",
            ],
        },
        "tags": [
            "threshold",
            "edge",
            "boundary",
            "micro",
            "gap",
            "curb-strip",
            "fire-escape",
            "rooftop",
            "intimate",
            "tactical-urbanism",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator Templates — 8 parameterised templates for producing new wild
# spatial concepts in the Sphere idiom
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # 1 — Elemental Sphere Generator
    {
        "title": "Elemental Sphere Generator",
        "summary": (
            "Template for creating new Sphere activations based on a single "
            "natural element — water, fire, earth, air, light, darkness, sound, "
            "or silence. Each element becomes the organizing principle for the "
            "space, the program, and the community that forms around it."
        ),
        "category": "spatial-invention",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [2, 5],
        "novelty_range": [4, 5],
        "details": {
            "element_options": [
                "water (rain harvesting, mist, fountains, ice)",
                "fire (controlled burns, candle ceremonies, forging, cooking)",
                "earth (soil, clay, stone, planting, digging, composting)",
                "air (wind, breath, kites, pneumatic instruments, ventilation)",
                "light (solar, bioluminescence, projection, shadow, reflection)",
                "darkness (sensory deprivation, stargazing, night ecology, sleep)",
                "sound (acoustic design, field recording, live music, silence as sound)",
                "silence (meditation, anechoic spaces, sign-language gatherings)",
            ],
            "square_footage_range": [50, 10000],
            "cost_range": [100, 50000],
            "activation_duration_options": [
                "flash (under 1 hour)",
                "session (1-4 hours)",
                "day-long (sunrise to sunset or sunset to sunrise)",
                "season-long (permanent installation for one season)",
            ],
            "design_principles": [
                "Single element as constraint breeds creativity — do not mix",
                "The element must be experientially dominant, not decorative",
                "Community forms around shared elemental experience",
                "Site selection driven by where the element naturally concentrates",
            ],
        },
        "tags": ["elemental", "generative", "constraint-based", "ritual"],
    },
    # 2 — Temporal Frequency Generator
    {
        "title": "Temporal Frequency Generator",
        "summary": (
            "Template for designing time-locked activations at any frequency — "
            "from once-per-century to every-15-minutes. The template provides "
            "a framework for choosing temporal frequency, building anticipation, "
            "and designing the activation to match the emotional register of "
            "its recurrence."
        ),
        "category": "spatial-invention",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "frequency_spectrum": [
                "every 15 minutes (ambient, meditative, background)",
                "hourly (clock-tower tradition, marking time)",
                "daily at specific hour (dawn, noon, dusk, midnight)",
                "weekly (sabbath rhythm, market day, community night)",
                "monthly (full moon, new moon, first Friday)",
                "seasonal (solstice, equinox, harvest, planting)",
                "annual (anniversary, festival, memorial)",
                "once-per-decade (time capsule opening, generational ritual)",
                "once-per-century (aspirational, legacy, mythic)",
            ],
            "anticipation_design": [
                "countdown signage or digital display",
                "progressive physical transformation of site (e.g., plants growing)",
                "community storytelling and oral tradition between activations",
                "artifact from previous activation displayed as relic",
            ],
            "emotional_register_mapping": {
                "high_frequency": "calm, ambient, atmospheric, background hum of life",
                "medium_frequency": "communal, anticipated, marked on calendars",
                "low_frequency": "sacred, mythic, once-in-a-lifetime, pilgrimage-worthy",
            },
            "design_principles": [
                "Rarer activations demand higher production value and emotional weight",
                "Frequent activations should be low-maintenance and self-sustaining",
                "Always publish the schedule — anticipation is half the experience",
                "Leave a physical trace between activations (artifact, marker, patina)",
            ],
        },
        "tags": ["temporal", "frequency", "ritual", "anticipation", "schedule"],
    },
    # 3 — AR Spatial Overlay Generator
    {
        "title": "AR Spatial Overlay Generator",
        "summary": (
            "Template for producing new augmented-reality design overlays for "
            "any vacant lot, building facade, or public space in Philadelphia. "
            "Defines the pipeline from site scan to 3D asset creation to "
            "community voting to physical construction."
        ),
        "category": "spatial-invention",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "site_scan_methods": [
                "LiDAR point cloud (iPad Pro / iPhone Pro)",
                "photogrammetry from drone imagery (DJI Mini 4 Pro)",
                "manual measurement with GPS ground-truth points",
                "Philadelphia OpenDataPhilly GIS parcel boundary import",
            ],
            "design_asset_types": [
                "landscape design (plantings, grading, water features, paths)",
                "architectural intervention (pavilion, stage, market stall, shelter)",
                "art installation (sculpture, mural, light installation, sound piece)",
                "infrastructure (seating, lighting, signage, utilities)",
            ],
            "community_engagement_pipeline": [
                "site scan and baseline documentation",
                "design charrette (in-person or virtual) to generate 3-5 concepts",
                "AR overlay publication for community viewing and voting (2-week window)",
                "vote tabulation and winning-design announcement",
                "physical implementation planning and fundraising",
            ],
            "design_principles": [
                "Every AR overlay must be buildable — no purely fantastical renderings",
                "Include realistic cost estimate visible in the AR experience",
                "Voting weighted toward residents within 3-block radius of site",
                "Designs must comply with Philadelphia zoning and building codes",
            ],
        },
        "tags": ["AR", "augmented-reality", "community-design", "pipeline", "voting"],
    },
    # 4 — Weather-Responsive Activation Generator
    {
        "title": "Weather-Responsive Activation Generator",
        "summary": (
            "Template for designing activations that are triggered by or designed "
            "around specific weather conditions. Provides frameworks for rain, "
            "snow, fog, wind, heat, and cold activations with material palettes "
            "and notification systems."
        ),
        "category": "spatial-invention",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "weather_trigger_types": [
                "rain (light drizzle, steady rain, downpour — each a different activation)",
                "snow (flurries, accumulating, blizzard)",
                "fog (morning mist, dense fog, freezing fog)",
                "wind (breeze 5-15 mph, gusty 15-30 mph, gale 30+ mph)",
                "heat (above 90F — cooling activations, shade structures, misting)",
                "cold (below 25F — warming stations, fire circles, hot-drink service)",
                "clear sky at night (stargazing, moon viewing, shadow play)",
            ],
            "notification_infrastructure": [
                "weather API integration (OpenWeatherMap, NWS) for automated triggers",
                "SMS subscriber list with opt-in by weather type",
                "social media auto-post when conditions are met",
                "physical weather vane or wind sock at site as ambient indicator",
            ],
            "material_palette_by_weather": {
                "rain": "metal surfaces, resonant materials, waterproof seating, rain gauges",
                "snow": "stencils, colorant sprayers, snow-brick molds, sled tracks",
                "fog": "tall grasses, water features, diffused lighting, fog horns",
                "wind": "kites, windsocks, aeolian instruments, fabric streamers, pinwheels",
            },
            "design_principles": [
                "The weather IS the activation — human additions should amplify, not replace",
                "Safety protocols for each weather type (lightning, black ice, wind chill)",
                "Cancellation thresholds clearly defined (e.g., no wind harps above 50 mph)",
                "Post-weather documentation (photos, recordings) shared with community",
            ],
        },
        "tags": ["weather", "responsive", "rain", "snow", "fog", "wind", "trigger"],
    },
    # 5 — Subterranean Space Reclamation Generator
    {
        "title": "Subterranean Space Reclamation Generator",
        "summary": (
            "Template for identifying, assessing, and activating underground "
            "spaces in Philadelphia — from abandoned subway infrastructure to "
            "basement vaults to utility tunnels. Provides the regulatory, "
            "structural, and programmatic framework for bringing hidden spaces "
            "to public life."
        ),
        "category": "spatial-invention",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [1, 3],
        "novelty_range": [5, 5],
        "details": {
            "space_type_options": [
                "abandoned subway station (SEPTA Broad Street or Market-Frankford lines)",
                "decommissioned utility tunnel (water, steam, electrical)",
                "basement vault under demolished building (common in Center City)",
                "disused rail tunnel (Reading Railroad, Pennsylvania Railroad remnants)",
                "underground parking structure (obsolete, structurally sound)",
                "storm drain chamber (oversized junction boxes in older system)",
            ],
            "assessment_checklist": [
                "structural integrity report by licensed PE",
                "environmental Phase II (asbestos, lead, PCBs, radon, methane)",
                "hydrology survey (water intrusion, flood history, water table depth)",
                "air quality baseline (CO2, CO, particulates, humidity, temperature)",
                "ownership and access rights determination",
                "ADA accessibility pathway feasibility",
                "emergency egress code compliance analysis (IBC Chapter 10)",
            ],
            "program_archetypes": [
                "contemplative (meditation, sensory deprivation, silence retreat)",
                "cultivation (mushroom farming, root-cellar storage, fermentation lab)",
                "cultural (gallery, performance, recording studio, speakeasy cinema)",
                "commercial (underground market, artisan workshop, wine/cheese aging)",
            ],
            "design_principles": [
                "Preserve the character of found space — patina, materiality, acoustics",
                "Ventilation is non-negotiable: minimum 20 CFM per occupant",
                "Two-means-of-egress minimum for any public-assembly occupancy",
                "Phased activation: start small, prove concept, expand incrementally",
            ],
        },
        "tags": ["underground", "subterranean", "adaptive-reuse", "infrastructure", "assessment"],
    },
    # 6 — Threshold and Edge-Space Generator
    {
        "title": "Threshold and Edge-Space Generator",
        "summary": (
            "Template for identifying and activating the overlooked residual "
            "spaces in the urban fabric — gaps, strips, edges, parapets, "
            "undersides, and transitions. Provides a taxonomy of threshold "
            "types and micro-activation kits for each."
        ),
        "category": "spatial-invention",
        "time_horizon": "near",
        "impact_range": [2, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [4, 5],
        "details": {
            "threshold_taxonomy": [
                "rowhouse gap (3-12 inches between party walls)",
                "curb strip (12-24 inches between sidewalk and street)",
                "tree pit (3x3 to 4x6 feet, existing or new)",
                "fire-escape landing (3x4 feet, load-limited)",
                "rooftop parapet (6-18 inches wide, linear)",
                "alley mouth (transition zone between street and alley)",
                "stoop-to-sidewalk (the 3-foot social zone in front of rowhouse steps)",
                "fence line (the vertical plane between adjacent properties)",
                "loading-dock lip (elevated platform facing sidewalk, often unused)",
                "bridge underside (sheltered, acoustically resonant, often forgotten)",
            ],
            "kit_types": [
                "reading nook (chair, lamp, book box)",
                "moss garden (pre-grown tiles, shade plugs, edging)",
                "sound installation (chimes, bells, resonant objects)",
                "pollinator strip (creeping thyme, sedum, clover plugs)",
                "light installation (solar LED, fairy lights, reflective surfaces)",
                "artifact display (weatherproof vitrine, rotating community objects)",
                "scent garden (herbs in micro-planters: lavender, rosemary, mint)",
            ],
            "design_principles": [
                "Smallness is the point — resist the urge to scale up",
                "Each activation should reward close looking and slow discovery",
                "Numbering system creates a collectible, map-able network",
                "Installation must be reversible with zero damage to host structure",
            ],
        },
        "tags": ["threshold", "edge", "micro", "taxonomy", "kit", "residual-space"],
    },
    # 7 — Sensory Sphere Generator
    {
        "title": "Sensory Sphere Generator",
        "summary": (
            "Template for designing activations that foreground a single sense — "
            "smell, touch, taste, hearing, or sight — or deliberately remove "
            "one sense to heighten the others. Creates spaces that are defined "
            "by sensory experience rather than physical boundary."
        ),
        "category": "spatial-invention",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "sense_focus_options": [
                "smell (scent gardens, incense paths, fermentation, baking, rain on earth)",
                "touch (texture walls, barefoot paths, water, sand, fur, bark, stone)",
                "taste (foraging walks, flavor stations, communal cooking, fermentation)",
                "hearing (sound walks, acoustic architecture, silence, field recording)",
                "sight (light installations, color fields, shadow play, darkness)",
            ],
            "sense_removal_options": [
                "blindfolded experience (guided touch/sound/smell walk)",
                "silent experience (sign-language-only gathering, no spoken word)",
                "darkness experience (underground or blackout space, non-visual)",
                "stillness experience (no movement allowed, observation only)",
            ],
            "spatial_boundary_methods": [
                "scent radius (how far does the lavender carry?)",
                "sound radius (where does the music fade into city noise?)",
                "light boundary (the edge of the projection, the shadow line)",
                "temperature gradient (the warmth of the fire circle's edge)",
            ],
            "design_principles": [
                "The sensory experience IS the architecture — no walls needed",
                "Name the boundary: 'you are inside the sphere when you can smell the bread'",
                "Accessibility review for each sense focus (alternatives for disabled visitors)",
                "Sensory consent: always inform participants what to expect before entry",
            ],
        },
        "tags": ["sensory", "smell", "touch", "taste", "hearing", "sight", "experiential"],
    },
    # 8 — Impossible Sphere Generator
    {
        "title": "Impossible Sphere Generator",
        "summary": (
            "Template for generating spatial concepts that seem impossible but "
            "are technically feasible with creative engineering, regulatory "
            "negotiation, or community willpower. The purpose is to push the "
            "boundary of what Philadelphians believe is possible in their city "
            "and to produce at least one 'impossible' concept per quarter that "
            "actually gets built."
        ),
        "category": "spatial-invention",
        "time_horizon": "far",
        "impact_range": [5, 5],
        "feasibility_range": [1, 3],
        "novelty_range": [5, 5],
        "details": {
            "impossibility_categories": [
                "regulatory impossible (needs a law changed or a new permit type created)",
                "engineering impossible (needs novel structural or material solution)",
                "economic impossible (needs new funding mechanism or value capture model)",
                "social impossible (needs community trust or coalition that doesn't yet exist)",
                "perceptual impossible (needs people to see familiar space in a new way)",
                "temporal impossible (needs a timescale longer than any funder's cycle)",
            ],
            "feasibility_unlocking_strategies": [
                "find the one precedent (somewhere in the world, someone has done this)",
                "reframe the regulation (it's not a building, it's a temporary art installation)",
                "build the coalition first, then the thing (200 supporters before 1 permit)",
                "prototype at micro-scale (prove it works in a 10x10 area, then scale)",
                "partner with a university (research exemptions, student labor, credibility)",
                "make it reversible (the #1 argument that unlocks cautious regulators)",
            ],
            "concept_seeding_prompts": [
                "What if the Delaware River were a public park?",
                "What if you could walk underground from Kensington to University City?",
                "What if every vacant lot in a zip code activated on the same night?",
                "What if a building could be made entirely of living plants?",
                "What if Philadelphia had a space that existed only in augmented reality?",
                "What if a public space were designed to last exactly 100 years?",
            ],
            "design_principles": [
                "Start with the impossible version, then negotiate toward feasibility",
                "Document the journey from impossible to built — that story is the art",
                "Every impossible sphere needs a champion: one person who won't let it die",
                "Failure to build is acceptable; failure to imagine is not",
            ],
        },
        "tags": [
            "impossible",
            "visionary",
            "boundary-pushing",
            "moonshot",
            "generative",
            "aspirational",
        ],
    },
]
