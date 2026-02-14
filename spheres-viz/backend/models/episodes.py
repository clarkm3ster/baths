"""
SPHERES — Episode Data Model & Content
=======================================
Ten episodes. Ten dormant spaces in Philadelphia.
Each one waiting to be activated, filmed, and left better than we found it.

This is the complete narrative bible for the SPHERES visual experience.
"""

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class Coordinates(BaseModel):
    lat: float
    lng: float


class EstimatedCost(BaseModel):
    low: int
    high: int


class Episode(BaseModel):
    id: int
    slug: str
    title: str
    subtitle: str
    location: str
    neighborhood: str
    coordinates: Coordinates
    genre: str
    genre_color: str

    # Narrative
    logline: str
    opening_text: str
    narrative_arc: str
    the_moment: str

    # Space
    current_state: str
    activation_concept: str
    activation_description: str

    # Permanence
    permanent_elements: list[str]
    permanence_percentage: int
    permanence_narrative: str

    # Production
    estimated_cost: EstimatedCost
    timeline_weeks: int
    permits_needed: list[str]

    # Impact
    community_impact: str
    jobs_created: int
    people_served: int

    # Visual
    color_palette: list[str]
    atmosphere: str
    ambient_sounds: list[str]


class EpisodeSummary(BaseModel):
    id: int
    slug: str
    title: str
    subtitle: str
    location: str
    neighborhood: str
    genre: str
    genre_color: str
    color_palette: list[str]
    estimated_cost: EstimatedCost
    permanence_percentage: int


class EpisodeStats(BaseModel):
    total_episodes: int
    total_cost_low: int
    total_cost_high: int
    total_jobs_created: int
    total_people_served: int
    average_permanence: float
    neighborhoods: list[str]
    genres: list[str]


# ---------------------------------------------------------------------------
# Episode Content — The Complete Narrative Bible
# ---------------------------------------------------------------------------

EPISODES: list[Episode] = [

    # ======================================================================
    # EPISODE 1 — WATERFRONT: "The Floating Theater"
    # ======================================================================
    Episode(
        id=1,
        slug="waterfront",
        title="The Floating Theater",
        subtitle="Where the river remembers how to sing",
        location="Pier 68, Delaware River Waterfront",
        neighborhood="South Philadelphia Waterfront",
        coordinates=Coordinates(lat=39.9133, lng=-75.1416),
        genre="Magical Realism",
        genre_color="#6366F1",

        logline=(
            "An abandoned industrial pier on the Delaware River becomes a floating "
            "performance space where a barge-mounted stage rises with the tide and the "
            "audience watches from the restored pier edge — and for one night, the whole "
            "river glows."
        ),

        opening_text=(
            "Pier 68 hasn't been used in forty years. The concrete is cracked. "
            "The bollards are rusted into abstract sculpture. But stand here at twilight "
            "and watch the light hit the water and you'll understand — this place has "
            "been rehearsing."
        ),

        narrative_arc=(
            "We open on the pier at dawn. A drone shot rising from the waterline reveals "
            "the full scope of the decay — collapsed fencing, weeds forcing through concrete, "
            "a faded NO TRESPASSING sign hanging by one bolt. But the camera keeps rising, "
            "and we see the city behind it, and the sun coming up behind that, and we "
            "understand: this pier is not abandoned. It is waiting.\n\n"
            "The middle act follows two storylines: the construction crew building the "
            "floating stage (a barge fitted with a performance deck, light rigging, and "
            "sound system) and the community performers rehearsing across the city — a "
            "West Philly spoken word collective, a Kensington mariachi band, a Germantown "
            "gospel choir, a young cellist from South Philly who's never performed in public "
            "before. They don't know they'll share the same stage. They don't know the stage "
            "floats.\n\n"
            "The final act is the night itself. The barge is anchored thirty feet from "
            "the pier. A gangway connects them. The audience sits on tiered seating built "
            "along the pier's edge, and others line the riverbank with blankets. As the sun "
            "sets, the first performer walks the gangway. The stage lights come up and reflect "
            "in the river, doubling everything. Between acts, biodegradable luminescent dye "
            "releases into the current, and the Delaware glows a soft, impossible blue. The "
            "cellist plays last. She is alone on the floating stage, the city behind her, the "
            "glowing river beneath her, and she plays something that sounds like everything "
            "this pier has been waiting forty years to say."
        ),

        the_moment=(
            "The cellist reaches the bridge of her piece. She closes her eyes. The barge "
            "rocks gently beneath her — you can see it in the way her bow sways, the way "
            "the reflection of her stage light dances on the water. The audience has gone "
            "completely silent. Eight hundred people, and the only sound is a cello and "
            "the river. Then the luminescent dye catches the current and a wave of soft blue "
            "light rolls downstream past the stage, and she opens her eyes and sees it, and "
            "she smiles without stopping, and the camera pulls back to show the whole scene — "
            "the glowing river, the lit stage, the crowd on the pier, the city blazing behind "
            "it all — and you understand that this is what cities are for."
        ),

        current_state=(
            "Pier 68 is a decommissioned industrial pier extending roughly 300 feet into "
            "the Delaware River. The surface is reinforced concrete, heavily weathered but "
            "structurally sound according to the 2019 Delaware River Waterfront Corporation "
            "assessment. Chain-link fencing with rusted padlocks blocks public access. The pier "
            "is flanked by active marine terminals to the north and the Walmart parking lot to "
            "the south. At low tide, the river reveals the pier's original timber pilings beneath "
            "the concrete cap. There is no lighting, no seating, no signage. At night it is "
            "completely dark. During the day, fishermen sometimes cut through the fence."
        ),

        activation_concept="Floating performance venue with barge-mounted stage and restored pier audience seating",

        activation_description=(
            "The activation transforms Pier 68 into a waterfront amphitheater in two parts: the "
            "pier itself becomes the audience space, with tiered bench seating along both edges "
            "and a central promenade, all built from reclaimed lumber and marine-grade hardware. "
            "String lights arc overhead between new timber posts. The concrete surface is power-washed "
            "and sealed, with painted wayfinding and embedded LED path markers. A temporary "
            "sound system is rigged along the pier's spine.\n\n"
            "Thirty feet off the pier's end, a 40-by-60-foot barge is anchored as the floating "
            "stage. The barge is fitted with a non-slip performance deck, a 20-foot lighting truss, "
            "a weatherproof sound system, and a backdrop scrim for projections. A 40-foot aluminum "
            "gangway connects the barge to the pier, rising and falling with the tide. Along the "
            "riverbank to the south, a sloped lawn area is cleared and graded for blanket seating, "
            "with food trucks positioned along the access road. Portable restroom facilities are "
            "stationed at the pier entrance. The entire installation is designed to be assembled in "
            "72 hours and operated for a two-week performance run."
        ),

        permanent_elements=[
            "Floating dock system with modular connection points",
            "Waterfront path lighting (solar-powered LED bollards)",
            "Restored and sealed pier decking with painted wayfinding",
            "Public boat launch ramp at pier's south edge",
            "Timber bench seating along pier edges (12 benches)",
            "Electrical infrastructure with waterproof junction boxes",
        ],

        permanence_percentage=45,

        permanence_narrative=(
            "A year later, the barge is gone but the pier is unrecognizable. The restored "
            "concrete surface is clean and sealed. Twelve timber benches line both edges, "
            "each one engraved with a line from a poem performed on opening night. Solar-powered "
            "LED bollards mark the path from the street to the pier's tip. The floating dock "
            "system remains, and on summer weekends, kayakers launch from the south ramp. A "
            "fisherman who used to cut through the fence now walks through the open gate, sits "
            "on a bench, and casts his line from a pier that finally belongs to everyone. The "
            "city added it to the Schuylkill-to-Delaware trail map. There is a small plaque at "
            "the entrance that reads: THE RIVER REMEMBERS."
        ),

        estimated_cost=EstimatedCost(low=180000, high=350000),
        timeline_weeks=12,
        permits_needed=[
            "Delaware River Waterfront Corporation site license",
            "US Coast Guard marine event permit",
            "City of Philadelphia special event permit",
            "PA DEP environmental clearance (luminescent dye)",
            "Philadelphia Water Department stormwater review",
            "Temporary structure permit (tiered seating)",
        ],

        community_impact=(
            "The waterfront activation creates a new public gathering space in a part of South "
            "Philadelphia that has been walled off from the river by industrial fencing for decades. "
            "Residents of Pennsport, Whitman, and the surrounding neighborhoods gain a direct "
            "connection to the Delaware that most have never experienced. The performance series "
            "features exclusively Philadelphia-based artists, with priority given to performers "
            "from underrepresented neighborhoods, providing both paid performance opportunities "
            "and citywide visibility.\n\n"
            "The permanent infrastructure — dock system, path lighting, restored decking, and "
            "boat launch — transforms Pier 68 from a fenced-off liability into a public asset. "
            "The Delaware River Waterfront Corporation has expressed interest in incorporating "
            "the pier into their long-term trail network. Local fishing communities gain legal "
            "access. Kayak and rowing clubs gain a launch point. The economic ripple includes "
            "increased foot traffic to nearby businesses on Oregon Avenue during the performance "
            "run, estimated at 15,000 unique visitors over two weeks."
        ),

        jobs_created=35,
        people_served=15000,

        color_palette=["#6366F1", "#818CF8", "#1E1B4B", "#C7D2FE"],
        atmosphere=(
            "Twilight. The sun has just set but the sky is still lit — deep indigo in the east, "
            "burnt amber in the west. Fog is beginning to roll off the river, softening the edges "
            "of everything. The city skyline is a wall of warm light behind the pier. The water is "
            "dark and glassy, reflecting the string lights overhead in long, rippling lines. The "
            "air smells like river water and creosote and something sweet from the food trucks. "
            "It is the kind of evening where the world feels like it is holding its breath."
        ),
        ambient_sounds=[
            "River water lapping against pier pilings",
            "Distant boat horn on the Delaware",
            "String lights buzzing faintly in the wind",
            "Muffled laughter from the crowd",
            "A cello tuning — one long, searching note",
            "The creak of the barge against its mooring lines",
        ],
    ),

    # ======================================================================
    # EPISODE 2 — VACANT LOT: "Cinema Garden"
    # ======================================================================
    Episode(
        id=2,
        slug="cinema-garden",
        title="The Cinema Garden",
        subtitle="Where stories grow from the ground up",
        location="2300 N Front Street, Kensington",
        neighborhood="Kensington",
        coordinates=Coordinates(lat=39.9873, lng=-75.1253),
        genre="Documentary",
        genre_color="#00C853",

        logline=(
            "An overgrown vacant lot in Kensington becomes an outdoor cinema ringed by "
            "community garden beds — movies play against a permanent screening wall while "
            "tomatoes ripen beside the projector and the neighborhood gathers on a patch "
            "of earth that used to hold nothing but broken glass."
        ),

        opening_text=(
            "There's a lot on Front Street where a rowhome used to be. The foundation is "
            "still there if you look — a rectangle of old concrete beneath the weeds. Someone "
            "dumped a mattress here last spring. Someone else planted sunflowers along the fence. "
            "Both things are true about this block."
        ),

        narrative_arc=(
            "The documentary opens with a single, unbroken shot: the camera sits at ground "
            "level in the vacant lot, pointed up through the weeds at the sky. Voices fade in — "
            "neighbors talking about what this lot used to be, what it could be, what it is now. "
            "A child's hand reaches into frame and pulls a dandelion. We hear the wish. Then "
            "we cut to a title card: SIX WEEKS EARLIER.\n\n"
            "The middle follows the transformation in real time, documentary-style. We watch "
            "the lot get cleared, the soil tested, the garden beds built by a crew of neighbors "
            "who have never built anything together before. A retired carpenter from the block "
            "teaches a teenager how to use a miter saw. A woman who has lived on this street for "
            "forty years plants the first tomato seedling and cries, and when asked why, she says "
            "'Because someone finally asked us what we wanted.' The screening wall goes up — a "
            "16-foot-wide, 10-foot-tall concrete and stucco wall at the lot's north end, painted "
            "matte white, permanent. The projector is tested. The image is sharp against the wall "
            "at dusk.\n\n"
            "The final act is the first screening night. The lot is unrecognizable. Twelve raised "
            "garden beds ring the perimeter, each one planted and labeled. The center is clear — "
            "a gravel and grass surface with blankets, lawn chairs, bean bags. Kids are running "
            "between the beds. Someone is grilling. The projector comes on and the first film is "
            "a documentary made by students at nearby Kensington High about the history of this "
            "exact block. The audience watches their own street on screen, projected against a wall "
            "that didn't exist two months ago, surrounded by tomato plants that are already "
            "six inches tall."
        ),

        the_moment=(
            "The student documentary reaches a segment where elderly residents describe the "
            "block in the 1970s — the corner store, the block parties, the families. An old "
            "woman in the audience recognizes herself in archival footage. She is twenty-three "
            "in the photo, standing on the very ground where she now sits in a lawn chair. She "
            "gasps. Her granddaughter, sitting beside her, grabs her hand. The camera catches "
            "both of their faces lit by the projector — the old woman's eyes shining, the "
            "teenager's mouth open — and in the background, the garden beds, the neighbors, "
            "the screen showing a street that is the same street, and you realize this isn't "
            "a movie night. It's a mirror."
        ),

        current_state=(
            "The lot at 2300 N Front Street is approximately 2,400 square feet — the footprint "
            "of a demolished rowhome. The foundation slab remains, cracked and partially buried "
            "under years of accumulated soil and debris. The lot is unfenced on the street side "
            "and bordered by standing rowhomes on both sides and a cinder block wall at the rear. "
            "Vegetation is dense: ailanthus saplings, ragweed, and volunteer sunflowers planted "
            "by a neighbor. There is visible dumping — construction debris, a stripped bicycle "
            "frame, black trash bags. The lot is owned by the Philadelphia Land Bank and has been "
            "vacant since 2009. Despite the neglect, the soil beneath the debris is surprisingly "
            "healthy — a testament to the volunteer plants that have been quietly rehabilitating "
            "the ground for fifteen years."
        ),

        activation_concept="Outdoor cinema and community garden with permanent screening wall",

        activation_description=(
            "The lot is cleared of debris and the existing foundation slab is jackhammered and "
            "removed. Soil is tested and amended with compost and clean topsoil. Twelve raised "
            "garden beds (4x8 feet each) are constructed from rot-resistant cedar along the lot's "
            "three walled edges, creating a U-shape that frames a central gathering area. Each bed "
            "is 18 inches tall, ADA-accessible, and fitted with drip irrigation connected to a "
            "rainwater cistern mounted on the rear wall. A community tool shed is built in the "
            "northeast corner — a small, lockable structure holding shovels, gloves, seeds, and "
            "a first-aid kit.\n\n"
            "At the lot's north end, a permanent screening wall is constructed: 16 feet wide, "
            "10 feet tall, built on a reinforced concrete footer with a stucco-over-CMU finish "
            "painted projector-white. The wall doubles as a community mural surface when not in "
            "use for screenings. A weatherproof projector housing is mounted on a post at the "
            "lot's south end, aimed at the wall, with a lockable power connection. The central "
            "area between the beds is surfaced with crushed gravel over landscape fabric, with a "
            "grass strip down the center. String lights are hung between the adjacent rowhomes. "
            "A small wooden stage (8x12 feet) sits at the base of the screening wall for live "
            "introductions and performances."
        ),

        permanent_elements=[
            "12 raised cedar garden beds with drip irrigation",
            "Permanent screening wall (16x10 ft, stucco-over-CMU)",
            "Rainwater cistern and irrigation system",
            "Community tool shed with locking hardware",
            "Crushed gravel and grass ground surface",
            "Weatherproof projector housing and mount",
            "Small wooden performance stage (8x12 ft)",
            "String light posts and electrical hookups",
        ],

        permanence_percentage=85,

        permanence_narrative=(
            "A year later, the Cinema Garden is the most used space on the block. The garden "
            "beds are in full production — three are managed by the elementary school two blocks "
            "away, four by individual families, and five by a newly formed community garden "
            "collective that sells produce at a Saturday stand on the sidewalk. The screening "
            "wall hosts Friday Movie Nights from May through October, programmed by a rotating "
            "committee of neighbors. In the off-season, the wall displays a mural painted by "
            "local teenagers. The tool shed is always in use. The lot that held nothing now feeds "
            "the block, entertains it, and gives it a reason to come outside. A developer offered "
            "to buy the parcel. The neighborhood association said no."
        ),

        estimated_cost=EstimatedCost(low=45000, high=95000),
        timeline_weeks=8,
        permits_needed=[
            "Philadelphia Land Bank temporary use agreement",
            "L&I zoning use permit (community garden / assembly)",
            "Philadelphia Water Department stormwater management review",
            "Streets Department sidewalk occupancy (screening nights)",
            "Health Department food safety (if produce sold)",
        ],

        community_impact=(
            "Kensington has the highest concentration of vacant lots in Philadelphia — over "
            "1,200 in a single zip code. Each one is a wound in the streetscape, a gap where "
            "a home and a family used to be. The Cinema Garden directly addresses two of the "
            "neighborhood's most pressing needs: access to fresh food and access to safe, free "
            "community gathering space. The garden beds will produce an estimated 800 pounds "
            "of vegetables per season. The screening nights provide a regular, family-friendly "
            "event that requires no money to attend.\n\n"
            "The model is explicitly designed to be replicable. Every design decision — the "
            "cedar bed dimensions, the screening wall construction, the irrigation system — is "
            "documented and open-sourced. If Cinema Garden works on Front Street, it can work on "
            "any of Kensington's 1,200 vacant lots. The episode itself serves as a how-to "
            "documentary. The permanent infrastructure ensures the space outlasts the production. "
            "And the community garden collective formed during filming has already incorporated "
            "as a nonprofit."
        ),

        jobs_created=12,
        people_served=3500,

        color_palette=["#22C55E", "#166534", "#F0FDF4", "#86EFAC"],
        atmosphere=(
            "Summer dusk in Kensington. The sky is the color of a ripe peach. Fireflies are "
            "starting — just a few, blinking low over the garden beds. The air is warm and thick "
            "and smells like fresh soil and tomato leaves and someone grilling chicken on the "
            "sidewalk. Kids are chasing each other between the beds. A woman is watering the basil. "
            "The projector hasn't come on yet but the screen wall is glowing faintly pink from the "
            "sunset. String lights are on. Lawn chairs are arranged in messy rows. There is the "
            "particular energy of a neighborhood gathering — everyone talking, no one in charge, "
            "everything exactly right."
        ),
        ambient_sounds=[
            "Crickets beginning their evening chorus",
            "Children laughing and running on gravel",
            "A garden hose filling a watering can",
            "Spanish-language radio from an open window",
            "The click and hum of a film projector warming up",
            "Ice clinking in a cooler",
        ],
    ),

    # ======================================================================
    # EPISODE 3 — ROOFTOP: "Sky Park"
    # ======================================================================
    Episode(
        id=3,
        slug="rooftop",
        title="The Sky Park",
        subtitle="The city is the canvas and the sky is the ceiling",
        location="929 Arch Street Parking Garage, Chinatown",
        neighborhood="Chinatown",
        coordinates=Coordinates(lat=39.9544, lng=-75.1560),
        genre="Action",
        genre_color="#FF6B6B",

        logline=(
            "The top floor of a parking garage on the edge of Chinatown becomes a temporary "
            "skate park, urban art gallery, and rooftop concert venue where the whole city "
            "spreads out below and the only rule is that you have to make something before "
            "you leave."
        ),

        opening_text=(
            "Nobody looks up. That's the thing about cities — we walk through canyons of "
            "concrete and glass and never once think about what's on top. The roof of 929 Arch "
            "is the size of a football field. It's been holding parked cars for thirty years. "
            "Tonight it holds the sky."
        ),

        narrative_arc=(
            "The episode opens with a drone rising fast — street level, second floor, third, "
            "fourth — and then it clears the roofline and the whole city detonates into view. "
            "The Benjamin Franklin Bridge. The Comcast tower. The Art Museum on its hill. "
            "Chinatown's red gates directly below. And here, on this concrete slab in the sky, "
            "nothing. Just empty parking spaces and oil stains and a chain-link fence at the "
            "edge. But the camera holds, and music builds, and we understand: this is the "
            "before.\n\n"
            "The build-out is fast and kinetic — matching the episode's genre. Time-lapse of "
            "modular skate ramps being trucked up the garage ramps. Graffiti artists arriving "
            "with crates of spray cans. A sound crew rigging speakers to the stairwell housing. "
            "Rails being bolted down. A half-pipe assembled in sections. Safety netting going up "
            "along the edges. Meanwhile, we follow three stories: a 16-year-old skater from South "
            "Philly who's been skating parking lots his whole life and can't believe he's about to "
            "skate a rooftop; a muralist from Chinatown who's been commissioned to paint a 60-foot "
            "dragon across the garage's west wall; and a DJ from North Philly who builds her set "
            "from field recordings of the city.\n\n"
            "The activation is a single, blazing Saturday. The rooftop opens at 3 PM. Skaters hit "
            "the ramps. Artists are painting live on every available surface. The DJ starts at "
            "golden hour and the whole rooftop becomes a block party in the sky. The skater lands "
            "a trick he's been working on for a year, six stories above Arch Street. The dragon "
            "mural is finished as the sun sets behind it. And the DJ drops a beat built from "
            "Chinatown street sounds — vendors calling, woks sizzling, firecrackers — and the "
            "crowd loses its mind."
        ),

        the_moment=(
            "Golden hour. The skater drops into the half-pipe for his final run. The DJ is "
            "playing. The muralist is finishing the dragon's eye — a single stroke of gold paint. "
            "The crowd lines the half-pipe's edge. The skater pumps once, twice, launches — and "
            "the camera follows him into the air. For one suspended second he is above the "
            "half-pipe, above the crowd, above the rooftop, and behind him is the entire city "
            "of Philadelphia lit up by the setting sun. He grabs the board. He rotates. He lands. "
            "The crowd erupts. The dragon's eye gleams wet and gold. And the camera pulls back "
            "to show the whole rooftop — color and motion and music and people — a party on top "
            "of the world that nobody knew was possible six hours ago."
        ),

        current_state=(
            "929 Arch Street is a five-story concrete parking structure on the northern edge of "
            "Chinatown. The top floor is an open-air level with approximately 18,000 square feet "
            "of usable concrete surface. It is bordered by a 42-inch concrete parapet wall on "
            "all sides with chain-link fence extensions to 8 feet. The surface is in fair condition — "
            "typical wear patterns, oil staining, painted parking lines fading. The stairwell "
            "and elevator housing create a rectangular structure near the center. There are no "
            "amenities: no seating, no shade, no lighting beyond the stairwell fixtures. The "
            "top floor is typically 30-40% occupied on weekdays and nearly empty on weekends. "
            "Views are unobstructed in all four directions."
        ),

        activation_concept="Rooftop skate park, live art gallery, and concert venue with 360-degree city views",

        activation_description=(
            "The top floor is cleared of vehicles for a two-week period. Modular skate ramps, "
            "rails, and a 12-foot half-pipe are trucked up the garage ramps and assembled on the "
            "south end of the roof. The ramps are commercial-grade prefabricated units bolted to "
            "weighted steel bases — no drilling into the existing structure. Rubber safety surfacing "
            "surrounds all skate elements. Safety netting rises along the parapet walls to 12 feet.\n\n"
            "The north end becomes the art gallery and performance space: a DJ booth built on a "
            "raised platform near the stairwell housing, a 60-foot mural wall constructed from "
            "scaffold frames and plywood panels along the west parapet, and a dozen easel stations "
            "for live painting. Temporary shade structures (tensile fabric canopies) cover the "
            "gathering areas. A portable bar serves water, sodas, and food from Chinatown restaurants "
            "below. The stairwell housing walls are wrapped in projection screens for nighttime "
            "visual art. LED strip lights line every surface edge, transitioning from warm gold "
            "at sunset to electric red and blue after dark. A temporary elevator capacity increase "
            "permit allows for crowd flow management."
        ),

        permanent_elements=[
            "Public rooftop access stairwell improvements (lighting, signage, paint)",
            "Permanent art installations (3 commissioned sculptures)",
            "Safety railing upgrades along all parapet walls",
            "Sealed and painted rooftop surface with anti-slip coating",
            "Permanent electrical hookups for future events (4 weatherproof panels)",
            "60-foot dragon mural on west-facing exterior wall (visible from street)",
        ],

        permanence_percentage=35,

        permanence_narrative=(
            "The skate ramps are gone, the DJ booth dismantled, the shade canopies packed away. "
            "But the rooftop is different now. The surface has been sealed and coated — no more "
            "oil stains, no more fading lines. Instead, a geometric pattern in red and gold "
            "covers the floor, visible from the buildings above. Three sculptures remain: steel "
            "abstractions of skaters in motion, bolted to the parapet wall, catching the light. "
            "The dragon mural blazes on the west wall, visible from three blocks away. The garage "
            "owner, who was skeptical, now hosts a monthly 'Rooftop Sessions' event — live music, "
            "food trucks from Chinatown, open to the public. The top floor is no longer just "
            "parking. It is a place. The 16-year-old skater brings his friends here to watch the "
            "sunset. They sit on the parapet wall with their boards and talk about what's next."
        ),

        estimated_cost=EstimatedCost(low=85000, high=200000),
        timeline_weeks=6,
        permits_needed=[
            "Property owner agreement and insurance rider",
            "L&I temporary assembly permit (rooftop)",
            "Philadelphia Fire Department occupancy review",
            "Streets Department loading zone permits (equipment delivery)",
            "Noise variance permit (amplified sound above grade)",
            "Temporary structure permit (shade canopies, half-pipe)",
        ],

        community_impact=(
            "Chinatown is one of Philadelphia's most space-constrained neighborhoods — dense, "
            "vibrant, and critically short on public gathering areas and youth recreation. The Sky "
            "Park activation provides both, temporarily converting dead infrastructure into living "
            "community space. The skate park component directly serves the area's underserved youth "
            "population, offering free programming in a safe, supervised environment. The art gallery "
            "and mural components elevate Chinatown's already rich visual culture, providing "
            "commissioned work opportunities for local artists.\n\n"
            "The permanent improvements benefit the neighborhood long after filming ends. The dragon "
            "mural becomes a landmark visible from Race Street, reinforcing Chinatown's cultural "
            "identity against ongoing development pressure. The rooftop access improvements create "
            "a new public viewpoint. And the monthly events established during filming generate "
            "ongoing foot traffic and revenue for Chinatown restaurants and shops. The episode also "
            "documents the neighborhood's fight against the proposed arena project, weaving the "
            "Sky Park into the larger story of a community defending its right to exist."
        ),

        jobs_created=22,
        people_served=5000,

        color_palette=["#EF4444", "#F97316", "#FEF2F2", "#7F1D1D"],
        atmosphere=(
            "Golden hour on a rooftop. The sun is a red disk sinking behind the Art Museum, "
            "painting every surface in warm amber. The wind is constant up here — five stories "
            "above street level, it pushes your hair back and carries the sound of Chinatown "
            "rising from below: vendors, traffic, the clatter of a restaurant kitchen's exhaust "
            "fan. The sky is enormous. The city is a toy model spread to every horizon. Wheels "
            "crack against concrete. Spray cans hiss. Bass reverberates off the stairwell housing. "
            "Everything is motion and color and height and the giddy, vertiginous feeling of "
            "being somewhere you're not supposed to be."
        ),
        ambient_sounds=[
            "Skateboard wheels grinding on concrete",
            "Spray paint cans shaking — the rattle of the mixing ball",
            "Wind gusting across the open rooftop",
            "Bass-heavy music from the DJ booth",
            "Crowd cheering after a landed trick",
            "The distant hum of the city five stories below",
        ],
    ),

    # ======================================================================
    # EPISODE 4 — ALLEY: "The Corridor"
    # ======================================================================
    Episode(
        id=4,
        slug="alley",
        title="The Light Alley",
        subtitle="Walk through someone else's dreams",
        location="Quarry Street, Old City",
        neighborhood="Old City",
        coordinates=Coordinates(lat=39.9519, lng=-75.1426),
        genre="Mystery",
        genre_color="#E040FB",

        logline=(
            "A narrow service alley in Old City becomes an immersive art walk where projection "
            "mapping transforms both walls into living paintings, spatial sound follows your "
            "footsteps, and each section is a different artist's world — you walk through "
            "someone else's dreams and emerge on the other side changed."
        ),

        opening_text=(
            "Quarry Street is fourteen feet wide and one block long. It connects two worlds — "
            "the tourist bustle of 2nd Street and the quiet residential stretch of 3rd. Most "
            "people walk past it. The ones who walk through it walk fast. Tonight, they will "
            "walk slowly."
        ),

        narrative_arc=(
            "The episode opens in darkness. Literal darkness — the screen is black. We hear "
            "footsteps on wet pavement. A breath. Then a sliver of light appears, growing, "
            "and we realize we are walking into the alley from one end. The walls begin to glow. "
            "Shapes move. Color blooms. And a voice whispers: 'This way.'\n\n"
            "The middle act profiles five artists, each assigned a 40-foot section of the alley. "
            "A video artist from West Philly who maps coral reef growth patterns onto brick. A "
            "sound designer from Germantown who creates spatial audio that follows you — whispers "
            "in your left ear, music in your right, silence in between. A painter from North Philly "
            "who has never worked digitally before and is learning projection mapping in real time, "
            "translating her canvas work into building-scale animation. A poet from South Philly "
            "whose words scroll up the walls as you walk, pacing themselves to your speed. And a "
            "photographer from Kensington who projects portraits of alley residents — the people "
            "who use this space every day — at human scale on the walls, so you walk among giants.\n\n"
            "The final act is opening night. The alley is transformed. No signage, no tickets — "
            "just a glow visible from each end of the block. People are drawn in. They enter alone "
            "or in pairs. They walk slowly. The coral blooms around them. The whispers follow. The "
            "words scroll. The portraits watch. And at the alley's midpoint, all five installations "
            "overlap for ten feet — a sensory crescendo where every artist's work collides — and "
            "then you emerge on the other side, back into the ordinary city, blinking."
        ),

        the_moment=(
            "A woman enters the alley alone. She doesn't know what this is. The camera follows "
            "her from behind — we see what she sees. The first section: coral growing up the "
            "walls, pulsing with bioluminescent light. She reaches out to touch it. Her hand "
            "passes through the projection and casts a shadow-shape that the algorithm interprets "
            "as a new coral branch, growing from her fingertips. She laughs — a startled, "
            "delighted sound that echoes off the narrow walls. She walks deeper. The whispers "
            "start. The words appear. The portraits loom. And at the overlap zone, she stops. "
            "Everything is happening at once — color, sound, text, faces — and her eyes are wide "
            "and wet and she is standing completely still in the middle of a fourteen-foot-wide "
            "alley in Old City and the world is pouring over her and she whispers, 'Oh.' Just "
            "that. Just 'oh.' And it is enough."
        ),

        current_state=(
            "Quarry Street is a one-block service alley running east-west between 2nd and 3rd "
            "Streets in Old City. It is approximately 14 feet wide and 400 feet long, paved in "
            "asphalt with Belgian block gutters. The buildings on both sides are 3-4 story brick "
            "commercial structures, most with blank side walls facing the alley. There are loading "
            "docks, HVAC units, and dumpsters along the north wall. The south wall is largely "
            "uninterrupted brick. Lighting is minimal — two cobra-head streetlights at the "
            "intersections and nothing in between. The alley is a through-street for vehicles "
            "but sees little traffic after business hours. At night it is dark, quiet, and "
            "largely avoided."
        ),

        activation_concept="Immersive projection-mapped art walk with spatial audio and interactive installations",

        activation_description=(
            "The alley is closed to vehicle traffic for the installation period. Both walls "
            "are cleaned and prepped — surfaces power-washed, temporary mounting hardware installed "
            "for projectors and speakers. Ten high-lumen projectors are mounted on custom brackets "
            "at 40-foot intervals along the roofline, each covering a section of both walls. "
            "A network of 24 directional speakers is mounted at ear height along both walls, "
            "creating distinct sound zones that transition as visitors walk. Motion sensors at "
            "each section boundary trigger audio transitions and allow interactive projection "
            "responses. The ground is cleaned, re-sealed, and lit with recessed LED strip lights "
            "along both edges, creating a subtle runway effect.\n\n"
            "Each of the five 40-foot sections is a complete environment: unique visuals on both "
            "walls, unique spatial audio, and unique interactive logic. The overlap zone at the "
            "center blends all five feeds. A custom software system, built by a Temple University "
            "digital media team, manages the synchronization. The installation runs nightly from "
            "8 PM to midnight for three weeks. No tickets. No entry fee. You simply walk in from "
            "either end. Capacity is managed by gentle volunteers at each entrance who maintain "
            "spacing between visitors for optimal experience."
        ),

        permanent_elements=[
            "Weatherproof LED lighting infrastructure along both walls",
            "Concealed power conduits with access panels every 40 feet",
            "Artist display mounting system (flush-mount brackets on both walls)",
            "Wayfinding signage and alley naming plaque",
            "Sealed and leveled alley surface",
            "Motion-sensor lighting triggers (repurposed for safety lighting)",
        ],

        permanence_percentage=30,

        permanence_narrative=(
            "The projectors are gone. The speakers are packed away. The artists have moved on "
            "to new walls. But Quarry Street is no longer dark. The LED lighting system remains — "
            "warm white at night, casting the brick walls in a gentle glow that makes the alley "
            "feel safe for the first time in decades. The mounting brackets wait on the walls, "
            "and a rotating series of local artists use them to hang work — paintings, photographs, "
            "textile pieces — creating a permanent outdoor gallery that changes quarterly. The "
            "power conduits make future installations trivial. The motion sensors trigger the "
            "lights when someone enters, so the alley wakes up when you walk in. A small plaque "
            "at the 2nd Street entrance reads: THE CORRIDOR — A QUARRY STREET GALLERY. People "
            "who used to walk past now walk through. And sometimes, on quiet nights, they walk "
            "slowly."
        ),

        estimated_cost=EstimatedCost(low=65000, high=150000),
        timeline_weeks=8,
        permits_needed=[
            "Streets Department temporary street closure permit",
            "Old City District approval",
            "Adjacent property owner agreements (projector/speaker mounting)",
            "L&I electrical permit (power conduit installation)",
            "Philadelphia Art Commission review (public art in historic district)",
            "Noise permit (amplified sound in residential area)",
        ],

        community_impact=(
            "Old City is a neighborhood defined by its arts identity — galleries, First Friday "
            "events, the historic district designation. But that identity has eroded as galleries "
            "close and commercial rents push artists out. The Corridor reactivates Old City's "
            "artistic mission in a space that costs nothing to occupy — a public right-of-way. "
            "The five commissioned artists receive meaningful fees for original work shown to "
            "an estimated 8,000 visitors over the three-week run. The Temple University "
            "collaboration provides graduate students with professional production experience.\n\n"
            "The permanent lighting and mounting infrastructure transforms Quarry Street from "
            "a service alley into a viable gallery space — the only outdoor, rent-free exhibition "
            "venue in Old City. The quarterly rotation program, managed by the Old City District "
            "after filming, provides ongoing exhibition opportunities for emerging artists. The "
            "improved lighting and foot traffic also address a long-standing safety concern: "
            "the alley's darkness made it a site for illegal dumping and other problems. Light, "
            "it turns out, is the most effective community development tool there is."
        ),

        jobs_created=18,
        people_served=8000,

        color_palette=["#A855F7", "#7C3AED", "#1E1B4B", "#DDD6FE"],
        atmosphere=(
            "Night. Wet night — it rained an hour ago and the asphalt is slicked with reflected "
            "light. The alley is narrow enough that you can touch both walls if you stretch your "
            "arms. Neon and purple light spills from the projections, painting the wet ground in "
            "shifting color. The air is cool and still — sheltered from the wind by the buildings "
            "on both sides. You can hear the city at both ends of the alley, but in the middle, "
            "there is only the art: the hum of speakers, the whisper of voices, the pulse of "
            "light on old brick. It feels like being inside a living thing. It feels like the "
            "alley is breathing."
        ),
        ambient_sounds=[
            "Footsteps on wet asphalt, echoing between brick walls",
            "Low-frequency electronic ambient hum",
            "Whispered poetry fragments from directional speakers",
            "Distant traffic muffled by the buildings",
            "The quiet buzz of projector fans overhead",
            "A gasp from someone seeing the overlap zone for the first time",
        ],
    ),

    # ======================================================================
    # EPISODE 5 — PARK: "The Sound Garden"
    # ======================================================================
    Episode(
        id=5,
        slug="sound-garden",
        title="The Sound Garden",
        subtitle="Where the wind learns to play",
        location="FDR Park, Northwest Corner",
        neighborhood="South Philadelphia",
        coordinates=Coordinates(lat=39.9063, lng=-75.1768),
        genre="Fantasy",
        genre_color="#00E5FF",

        logline=(
            "A forgotten corner of FDR Park becomes a garden of playable sound sculptures — "
            "bronze bells, wind harps, percussion stones, a whisper dish spanning fifty feet — "
            "where couples come to listen, children make music without knowing it, and the "
            "boundary between instrument and landscape disappears."
        ),

        opening_text=(
            "There's a place in FDR Park where the path ends and the meadow begins. The "
            "mowers don't come here. The joggers turn back. It's just grass and sky and the "
            "sound of the wind doing nothing in particular. We're going to teach the wind "
            "to sing."
        ),

        narrative_arc=(
            "The episode opens with sound. No image — just sound. Wind through grass. A bird. "
            "A distant plane. Then, slowly, a new sound: a resonant, bell-like tone that seems "
            "to come from the earth itself. The image fades in — sunrise over the meadow, dew "
            "on the grass, and in the middle distance, a bronze form catching the first light. "
            "We don't know what it is yet. We only know it is singing.\n\n"
            "The middle act interweaves two timelines: the fabrication of the sculptures in a "
            "North Philadelphia metal shop (a sculptor and her team of welders creating instruments "
            "the size of trees) and the love story at the center of the episode — a couple, both "
            "musicians, both deaf, who communicate through vibration and touch. They are consultants "
            "on the project, ensuring every sculpture is not just audible but tactile. We watch them "
            "test prototypes — hands on bronze, feeling the resonance, signing to each other about "
            "pitch and duration. The sculptor learns from them. The sculptures change. What was "
            "designed to be heard is redesigned to be felt.\n\n"
            "The final act is the garden's opening on a spring morning. Eight sculptures are "
            "installed across the meadow, connected by a winding accessible path. Children find "
            "them first — running from one to the next, striking, spinning, pushing, pulling. "
            "A bronze bell tree rings when the wind blows. A stone marimba plays when you drag "
            "a mallet across its keys. A whisper dish — two parabolic reflectors facing each "
            "other across fifty feet — carries a whispered word from one side to the other with "
            "perfect clarity. The deaf couple stands at the bell tree, hands on the bronze, "
            "eyes closed, feeling the vibrations pass through the metal into their palms. The "
            "camera holds on their hands. The sound is enormous. The image is quiet. And you "
            "understand that music was never about hearing."
        ),

        the_moment=(
            "Late afternoon. The park is full. The couple stands at opposite ends of the whisper "
            "dish — fifty feet apart, facing each other across a field of wildflowers. The woman "
            "places her hands on the dish's rim. The man leans in and whispers something. The "
            "parabolic reflector catches his words and sends them across the distance. She can't "
            "hear them. But she feels the vibration in the bronze under her hands. Her eyes are "
            "closed. Her fingers read the metal. And then she smiles — a smile so specific, so "
            "knowing, that we understand she received the message perfectly. The camera stays on "
            "her face. We never learn what he said. We don't need to."
        ),

        current_state=(
            "The northwest corner of FDR Park is approximately two acres of unmaintained meadow "
            "bordered by a tree line to the north and the park's internal road to the south. The "
            "grass is tall and uncut, punctuated by volunteer wildflowers — chicory, Queen Anne's "
            "lace, goldenrod in season. A deteriorated asphalt path enters from the south but ends "
            "abruptly after 200 feet, its remaining length consumed by vegetation. There are no "
            "benches, no trash cans, no lighting. The area floods slightly in heavy rain due to "
            "poor drainage. Despite the neglect, it is beautiful — a pocket of genuine meadowland "
            "within a city park, with open sky and a gentle slope that catches the morning sun. "
            "Birders come here. Dog walkers occasionally. It is one of the quietest places in "
            "South Philadelphia."
        ),

        activation_concept="Interactive sound sculpture garden with accessible pathways and native plantings",

        activation_description=(
            "Eight custom-fabricated sound sculptures are installed across the two-acre meadow, "
            "each one a musical instrument at landscape scale. The Bell Tree: a 12-foot bronze "
            "trunk with tuned bell branches that ring in the wind. The Stone Marimba: a 20-foot "
            "arc of graduated granite bars on steel supports, played with attached mallets. The "
            "Wind Harp: a 15-foot vertical steel frame strung with aircraft cable that sings "
            "in moving air. The Whisper Dish: two 6-foot parabolic bronze reflectors on posts, "
            "facing each other across 50 feet. The Rain Drum: a concave steel canopy that "
            "amplifies rainfall into rhythmic percussion. The Singing Stones: a cluster of "
            "basalt columns at varying heights that resonate when struck. The Tone Dial: a "
            "bronze sundial whose shadow triggers different tones as the sun moves. The Drift: "
            "a set of hanging aluminum tubes that chime as air currents shift.\n\n"
            "A winding accessible pathway (crushed stone, 5 feet wide, ADA-compliant grade) "
            "connects all eight sculptures in a loop that takes approximately 20 minutes to walk. "
            "Native meadow plantings — black-eyed Susan, butterfly milkweed, little bluestem — "
            "are established along the path edges. Six benches are placed at intervals, each "
            "positioned for optimal listening. The existing drainage is improved with a bioswale "
            "along the path's lower edge. Night lighting is minimal and warm — low bollards "
            "along the path only, preserving the meadow's darkness."
        ),

        permanent_elements=[
            "8 sound sculptures (bronze, steel, granite, aluminum)",
            "Accessible crushed-stone pathway loop (approximately 1,200 feet)",
            "6 cedar bench seats at listening stations",
            "Native meadow plantings along path edges",
            "Bioswale drainage improvement",
            "Low bollard path lighting (solar-powered)",
            "Interpretive signage at each sculpture (tactile and Braille)",
            "Maintenance endowment fund (established during production)",
        ],

        permanence_percentage=95,

        permanence_narrative=(
            "A year later, the Sound Garden is one of the most visited corners of FDR Park. The "
            "sculptures have weathered beautifully — the bronze has developed a green patina, the "
            "steel has a warm rust tone, the granite is unchanged. The meadow plantings have "
            "established and the wildflowers have naturalized along the path. Children who visited "
            "on opening day now come weekly, dragging parents and friends. A music teacher from "
            "Girard Academic brings her class every fall. The whisper dish is a proposal spot — "
            "at least four couples have gotten engaged across its fifty-foot span. The maintenance "
            "endowment covers annual tuning and cleaning. The sculptures play on. The wind has "
            "learned to sing. And in the early morning, before the joggers arrive, you can stand "
            "at the center of the garden and hear every instrument at once — a quiet, accidental "
            "symphony made of nothing but air and metal and the turning of the earth."
        ),

        estimated_cost=EstimatedCost(low=120000, high=280000),
        timeline_weeks=16,
        permits_needed=[
            "Philadelphia Parks & Recreation installation permit",
            "Philadelphia Art Commission public art review",
            "Fairmount Park Conservancy partnership agreement",
            "ADA compliance review (pathway and tactile signage)",
            "PA DEP stormwater management review (bioswale)",
            "Underground utility locate and clearance",
        ],

        community_impact=(
            "South Philadelphia's park infrastructure is aging and underinvested. FDR Park itself "
            "is in the middle of a long-delayed master plan process that has left many corners of "
            "the park in limbo. The Sound Garden activates a neglected area with permanent "
            "infrastructure that aligns with the park's master plan goals: accessible pathways, "
            "native plantings, and unique programming that draws visitors from across the city. "
            "The sound sculptures serve as both public art and educational tools — schools use them "
            "for music, physics, and ecology lessons.\n\n"
            "The accessibility focus is deliberate and structural. Every sculpture is designed to "
            "be experienced through touch as well as hearing, making the garden one of the few "
            "fully inclusive music spaces in Philadelphia. The pathway is wheelchair-accessible. "
            "The signage is in Braille and tactile relief. The collaboration with the Deaf "
            "community during design ensures that the garden works for everyone, not as an "
            "afterthought but as a founding principle. The maintenance endowment, funded by "
            "production budget and community fundraising, ensures the sculptures will play for "
            "decades."
        ),

        jobs_created=15,
        people_served=25000,

        color_palette=["#EC4899", "#F9A8D4", "#FDF2F8", "#831843"],
        atmosphere=(
            "Early morning, just after sunrise. The meadow is soaked in golden light that comes "
            "in low and horizontal, turning every blade of grass into a filament. Dew covers "
            "everything — the bronze sculptures are beaded with water that catches the light like "
            "jewels. Mist hangs at knee height across the meadow, drifting slowly. Birdsong is "
            "layered and complex — cardinals, sparrows, a mockingbird cycling through borrowed "
            "melodies. Underneath, the wind harps hum a low, resonant drone that blends so "
            "perfectly with the natural soundscape that you can't tell where nature ends and "
            "the sculpture begins. The air smells like wet grass and warm metal. The world is "
            "still. The garden is playing."
        ),
        ambient_sounds=[
            "Wind harp sustaining a low harmonic drone",
            "Bronze bells chiming gently in the breeze",
            "Birdsong — cardinal, sparrow, mockingbird",
            "Grass rustling in the wind",
            "Distant laughter from children at the stone marimba",
            "A single clear tone from the whisper dish ringing into silence",
        ],
    ),

    # ======================================================================
    # EPISODE 6 — UNDERPASS: "The Wall"
    # ======================================================================
    Episode(
        id=6,
        slug="underpass",
        title="The Wall",
        subtitle="Climb out of the dark",
        location="Columbus Boulevard under I-95, Northern Liberties",
        neighborhood="Northern Liberties",
        coordinates=Coordinates(lat=39.9652, lng=-75.1349),
        genre="Adventure",
        genre_color="#76FF03",

        logline=(
            "A dark concrete underpass beneath I-95 becomes a lit bouldering gym and youth "
            "center where climbing walls rise twenty feet on both sides, rubber matting covers "
            "the ground, and every afternoon a generation of kids who've never left the neighborhood "
            "learn what it feels like to reach for something higher."
        ),

        opening_text=(
            "Interstate 95 is a scar. Everyone in Philadelphia knows this. It cut the city off "
            "from its own river fifty years ago and we've been living with the wound ever since. "
            "But scars are strong. Scars are where the healing happened. And underneath this "
            "particular scar, there is a cathedral of concrete with twenty-foot ceilings and "
            "no one inside."
        ),

        narrative_arc=(
            "The episode opens with sound design: the roar of highway traffic, layered and "
            "rhythmic, almost musical. The camera moves through the underpass in a slow tracking "
            "shot — concrete pillars at regular intervals, the overhead deck creating a massive "
            "ceiling, puddles reflecting the distant daylight at both ends. It is vast and dim "
            "and strangely beautiful, like a brutalist temple.\n\n"
            "The middle act follows the transformation and three young people from the neighborhood. "
            "A 14-year-old who's never been to a climbing gym — they cost $30 a visit and there "
            "isn't one within walking distance. A 17-year-old who's about to drop out of school "
            "and whose mother begs the program director to 'just give him something to do with "
            "his hands.' And a 12-year-old who is scared of everything — heights, strangers, the "
            "dark — and who has been dared by her older brother to try. We watch the climbing walls "
            "go up: 20-foot panels of textured plywood bolted to steel frames against both walls "
            "of the underpass, color-coded routes from beginner to advanced, top-rope anchors, "
            "bouldering sections at human scale. Rubber safety matting rolls out over the concrete. "
            "LED panels mounted to the highway structure overhead fill the space with warm light "
            "for the first time in its existence.\n\n"
            "The final act is the youth program's first week. The 14-year-old touches a climbing "
            "hold for the first time and climbs to the top on her third try. The 17-year-old, "
            "quiet and skeptical, becomes obsessed with route-setting — the puzzle of it, the "
            "geometry, the way you have to think with your body. The 12-year-old stands at the "
            "base of the wall for twenty minutes before she touches it. Then she climbs three feet. "
            "Then she lets go and falls onto the mat and gets up and does it again. And again. By "
            "Friday she's at eight feet. By the end of the month she's at the top."
        ),

        the_moment=(
            "The 12-year-old is climbing. It is her tenth session. She is twelve feet up — "
            "higher than she has ever been. Her hands are chalked white. Her jaw is clenched. "
            "Below her, the other kids are watching. The instructor is spotting. Her brother, "
            "who dared her, is recording on his phone. She reaches for the next hold. Her foot "
            "slips. She catches herself. The kids below gasp. She hangs by her fingertips for "
            "two seconds — an eternity at twelve years old — and then she pulls herself up. "
            "One more move. One more. And then her hand slaps the top of the wall and she "
            "screams — not fear, not pain, just pure uncontainable triumph — and the sound "
            "echoes off the concrete ceiling of the underpass and mixes with the cheering below "
            "and the traffic above and for one moment, underneath a highway that was built to "
            "destroy this neighborhood, a twelve-year-old girl is the highest thing in the world."
        ),

        current_state=(
            "The underpass at Columbus Boulevard beneath I-95 is approximately 200 feet wide and "
            "60 feet deep, with a ceiling height of 20-24 feet. The concrete support columns are "
            "spaced at 30-foot intervals. The floor is poured concrete, cracked and uneven, with "
            "standing water in several depressions. The space is used informally for parking and "
            "occasionally for illegal dumping. Lighting is limited to whatever daylight penetrates "
            "from the open sides. The concrete walls and columns show years of graffiti, some of "
            "it genuinely beautiful. Traffic noise from I-95 above is constant but not overwhelming — "
            "the massive concrete structure absorbs more sound than it transmits. The space is "
            "owned by PennDOT and is not currently permitted for any use."
        ),

        activation_concept="Indoor bouldering gym and youth recreation center beneath the highway",

        activation_description=(
            "The underpass is cleaned, leveled, and sealed. Standing water is addressed with "
            "improved drainage channels cut into the concrete floor. Twenty-foot climbing wall "
            "panels are constructed against both long walls of the underpass — prefabricated "
            "plywood-over-steel-frame panels with commercial-grade climbing holds, bolted to "
            "the existing concrete structure. Four bouldering sections (12 feet high, no ropes "
            "needed) and two top-rope sections (20 feet, with permanent anchor bolts) provide "
            "a range of difficulty. Routes are color-coded: green for beginner, blue for "
            "intermediate, orange for advanced, red for expert. 4-inch rubber safety matting "
            "covers the entire floor area beneath the walls.\n\n"
            "The center of the space becomes the community area: folding tables for homework "
            "help, a check-in desk, equipment storage lockers, and a small DJ booth built into "
            "a repurposed shipping container that also houses the program office. LED panel lights "
            "are mounted to the underside of the highway deck, controlled by a dimmer system "
            "that can shift from bright daylight (for climbing) to warm ambient (for evening "
            "events). A portable restroom trailer is stationed at the eastern entrance. The "
            "youth program runs weekday afternoons from 3-7 PM with certified climbing "
            "instructors, free of charge, open to anyone under 18."
        ),

        permanent_elements=[
            "Climbing wall panels on both walls (20 ft height)",
            "4-inch rubber safety surfacing over entire floor",
            "LED panel lighting system mounted to highway deck",
            "Electrical infrastructure (permanent conduit to city power)",
            "Improved drainage channels in concrete floor",
            "Permanent anchor bolts for top-rope climbing",
            "Painted and sealed concrete surfaces",
        ],

        permanence_percentage=60,

        permanence_narrative=(
            "A year later, the shipping container office is still there, but it has been joined "
            "by two more: one for equipment storage, one converted into a tiny snack bar run by "
            "a neighborhood mom. The climbing walls are in constant use. The youth program, now "
            "funded by a combination of city recreation grants and private donations, runs five "
            "days a week and has served over 400 kids. The 17-year-old who was about to drop out "
            "is now a paid route-setter — he designs the climbing paths that other kids follow. "
            "The 12-year-old leads the beginner sessions on Tuesdays. The underpass, once the "
            "darkest place in Northern Liberties, is now the brightest. A PennDOT official, "
            "visiting for an inspection, stood in the middle of the climbing gym and said, 'We "
            "have two hundred underpasses in this city. I had no idea they could be this.' The "
            "program director handed him a proposal for three more locations."
        ),

        estimated_cost=EstimatedCost(low=150000, high=320000),
        timeline_weeks=10,
        permits_needed=[
            "PennDOT encroachment permit (use of highway right-of-way)",
            "City of Philadelphia recreation facility license",
            "L&I structural review (wall panel attachment to highway structure)",
            "Philadelphia Fire Department safety inspection",
            "ADA compliance review",
            "Youth program licensing (Department of Human Services)",
            "Electrical permit (permanent power connection)",
        ],

        community_impact=(
            "Northern Liberties has undergone rapid gentrification, but the blocks east of "
            "I-95 remain largely low-income and underserved. The highway itself is the dividing "
            "line — a physical barrier that separates the new restaurants and condos from the "
            "older rowhomes and public housing. The Wall turns that barrier into a bridge. By "
            "placing a free youth recreation facility directly beneath the highway, the activation "
            "claims the space that divides the neighborhood and converts it into the space that "
            "serves the neighborhood.\n\n"
            "The climbing program addresses a critical gap: there are no free indoor recreation "
            "facilities within a half-mile radius for the 2,000+ young people in the 19125 zip "
            "code. The nearest climbing gym charges $28 per session. The Wall is free, walkable, "
            "and open every weekday afternoon. Beyond recreation, the program includes homework "
            "help, mentorship, and — for older teens — paid positions as route-setters and junior "
            "instructors. The physical transformation of the underpass also demonstrates a model "
            "for PennDOT's statewide underpass reuse initiative, potentially unlocking similar "
            "spaces in cities across Pennsylvania."
        ),

        jobs_created=20,
        people_served=8000,

        color_palette=["#F59E0B", "#FBBF24", "#78350F", "#FEF3C7"],
        atmosphere=(
            "Late afternoon. The underpass is in dramatic chiaroscuro — bright daylight pouring "
            "in from both open sides, deep shadow in the center where the LED panels create pools "
            "of warm amber light. The concrete columns cast long diagonal shadows across the "
            "climbing walls. Chalk dust hangs in the air where a shaft of sunlight catches it, "
            "turning it gold. The sound is layered: the constant white noise of traffic above, "
            "the thud of feet on rubber matting, the click of carabiners, music from the DJ "
            "booth — something with bass and energy — and over all of it, the sound of kids. "
            "Talking, laughing, challenging each other, counting holds out loud. It is loud and "
            "alive and warm and the concrete cathedral that was built to carry cars now carries "
            "something better."
        ),
        ambient_sounds=[
            "Highway traffic — a constant, rhythmic roar from above",
            "Climbing shoes scraping textured plywood",
            "Chalk being clapped off hands",
            "Kids counting holds out loud — 'seven, eight, nine —'",
            "Bass-heavy music from the DJ booth",
            "The metallic click of a carabiner locking",
        ],
    ),

    # ======================================================================
    # EPISODE 7 — MARKET: "The Night Market"
    # ======================================================================
    Episode(
        id=7,
        slug="night-market",
        title="The Night Market",
        subtitle="Three blocks of the world on one street",
        location="Broad Street, Cecil B. Moore to Susquehanna",
        neighborhood="North Philadelphia",
        coordinates=Coordinates(lat=39.9793, lng=-75.1555),
        genre="Ensemble Comedy",
        genre_color="#FFD740",

        logline=(
            "Three blocks of North Broad Street shut down every Saturday night and become "
            "a night market with sixty vendor stalls, live music at every intersection, food "
            "from twenty countries, and the beautiful chaos of a neighborhood that has been "
            "waiting for the world to notice it already has everything."
        ),

        opening_text=(
            "Broad Street is the widest road in Philadelphia. Fourteen lanes at its widest "
            "point. Built for parades. Built for spectacle. But in North Philadelphia, "
            "between Cecil B. Moore and Susquehanna, Broad Street is mostly empty after dark. "
            "The width that was meant to impress just makes it feel lonelier. "
            "We are going to fill it."
        ),

        narrative_arc=(
            "The episode is structured as an ensemble comedy — multiple storylines weaving "
            "through a single chaotic event, all of them funny, all of them true. We open "
            "on a Saturday morning. The vendors are arriving. A Senegalese woman is unpacking "
            "jollof rice equipment. A Mexican family is assembling a taco stand. A Vietnamese "
            "grandmother is arranging spring rolls with military precision. A Temple University "
            "student is setting up a table to sell the hot sauce he makes in his dorm room. "
            "They don't know each other. They are about to share a street.\n\n"
            "The middle act follows the market's first four hours through six perspectives: the "
            "vendors (competing, cooperating, trading food across stalls), the musicians (three "
            "bands at three intersections, their sounds overlapping in the middle blocks), the "
            "organizer (a North Philly native who has been planning this for two years and is "
            "now watching it either succeed or collapse in real time), the neighbors (longtime "
            "residents who range from ecstatic to skeptical), the cook-off (an impromptu "
            "competition between the jollof rice vendor and the taco vendor for 'best $5 plate,' "
            "judged by the crowd), and the kid (a 10-year-old who is working his mother's "
            "lemonade stand and by 10 PM has made $340 and discovered capitalism).\n\n"
            "The final act is the last hour. The crowd has peaked — the market is shoulder-to-"
            "shoulder on Broad Street, something this stretch hasn't seen in decades. The bands "
            "are all playing simultaneously and somehow it works. The cook-off is a draw (the "
            "crowd demands both vendors win). The organizer, standing on a milk crate at the "
            "Cecil B. Moore intersection, watches the street he grew up on full of people and "
            "light and food and music, and he calls his mother, who is watching from her window "
            "three blocks away, and he says, 'Mom, look outside.' And she says, 'Baby, I've been "
            "looking all night.'"
        ),

        the_moment=(
            "11 PM. The market is at full roar. The camera finds the 10-year-old at his lemonade "
            "stand. His cash box is overflowing. His mother is laughing. He has a line six people "
            "deep. He is wearing a bow tie he put on at 9 PM because he said a businessman needs "
            "to look professional. The Senegalese vendor walks over and hands him a plate of jollof "
            "rice. He hands her a lemonade. No money changes hands. They clink cup to plate like "
            "a toast. The camera pulls back and we see the full three blocks — sixty stalls, three "
            "bands, a thousand people, all of Broad Street lit up and alive — and the boy turns "
            "back to his next customer and says, 'Welcome to the Night Market, what can I get you,' "
            "with the confidence of someone who has been doing this his entire life, which, in a "
            "way, he has. He's been waiting. They all have."
        ),

        current_state=(
            "This stretch of North Broad Street — from Cecil B. Moore Avenue to Susquehanna "
            "Avenue — is three blocks of mixed commercial and residential frontage. The street "
            "itself is six lanes wide with a center median. Many ground-floor commercial spaces "
            "are vacant or shuttered. Traffic is moderate during the day and light at night. The "
            "sidewalks are wide but underused. Temple University's campus begins one block north, "
            "creating a stark boundary between institutional investment and neighborhood disinvestment. "
            "The surrounding blocks are home to a dense, diverse residential population — "
            "African American, Caribbean, West African, Latino, and Southeast Asian communities "
            "all within walking distance. There is extraordinary culinary talent on these blocks. "
            "There is no venue for it."
        ),

        activation_concept="Weekly open-air night market with 60 vendor stalls, three live music stages, and food from 20 countries",

        activation_description=(
            "Three blocks of Broad Street are closed to vehicle traffic every Saturday from "
            "4 PM to midnight for an eight-week run. Sixty vendor stalls are arranged in two "
            "rows down the center of the street, creating a wide pedestrian corridor on both "
            "sides. Stalls are 10x10 popup tents with standardized signage, provided to vendors "
            "at no cost. Vendor selection prioritizes neighborhood residents, immigrant-owned "
            "food businesses, and local makers. Each stall receives a folding table, two chairs, "
            "an electrical hookup (generator-powered distribution), and a trash/recycling station.\n\n"
            "Three performance stages are positioned at each intersection (Cecil B. Moore, "
            "Jefferson, and Susquehanna), each with a PA system, stage lights, and a rotating "
            "lineup of local bands curated by genre: R&B/soul at Cecil B. Moore, Afrobeat/global "
            "at Jefferson, hip-hop/jazz at Susquehanna. String lights are hung between the "
            "streetlight poles down the entire three-block stretch. Portable restroom trailers "
            "are stationed at both ends. First aid is provided by Temple University EMS students. "
            "Security is handled by a community safety team trained in de-escalation, supplemented "
            "by off-duty Philadelphia police at intersections."
        ),

        permanent_elements=[
            "Vendor electrical hookups embedded in center median (60 outlets)",
            "Improved drainage along curb lines (three blocks)",
            "Market pavilion at Cecil B. Moore intersection (permanent steel-and-fabric structure)",
            "Permanent vendor storage facility (converted shipping container, secured)",
            "Enhanced streetlight fixtures with banner mounting hardware",
            "Painted crosswalk murals at all three intersections",
        ],

        permanence_percentage=40,

        permanence_narrative=(
            "The eight-week run ends but the market doesn't. The community, having tasted what "
            "Broad Street can be, refuses to let it go. A neighborhood business association forms. "
            "They secure a recurring street closure permit. The Night Market becomes monthly — "
            "first Saturday of every month, April through November. The permanent pavilion at "
            "Cecil B. Moore hosts a weekday farmers market. The vendor electrical hookups make "
            "setup trivial. The painted crosswalk murals — designed by Temple art students — have "
            "become a neighborhood landmark, shared thousands of times on social media. The boy "
            "with the lemonade stand now has a proper cart. He's saving for a food truck. His "
            "mother says he does math homework without being asked now because he needs to count "
            "his revenue. Broad Street, the widest road in Philadelphia, finally has something "
            "worth crossing it for."
        ),

        estimated_cost=EstimatedCost(low=200000, high=450000),
        timeline_weeks=14,
        permits_needed=[
            "Streets Department block party / street closure permit (recurring)",
            "Philadelphia Health Department temporary food vendor licenses (60)",
            "PLCB special occasion permit (if alcohol served)",
            "Noise permit (amplified sound, three stages)",
            "SEPTA bus reroute coordination",
            "Philadelphia Police Department event security plan",
            "PGW and PECO utility access coordination",
            "L&I electrical permit (median hookup installation)",
        ],

        community_impact=(
            "North Philadelphia is one of the most economically distressed areas in the city, "
            "but it is also one of the most culturally rich. The Night Market is designed to "
            "convert cultural wealth into economic opportunity. Sixty vendor stalls at zero cost "
            "eliminate the barrier to entry for small food businesses and makers who cannot afford "
            "brick-and-mortar. The eight-week run provides a testing ground for business models — "
            "vendors learn pricing, customer service, inventory management, and marketing in a "
            "low-risk, high-traffic environment. Three vendors from the first season have since "
            "opened permanent locations on Broad Street.\n\n"
            "The market also addresses a more fundamental need: visibility. North Broad Street "
            "between Temple and Center City is perceived as a gap — something you drive through, "
            "not a destination. The Night Market inverts that perception. It draws visitors from "
            "every part of the city into a neighborhood they may never have visited, and it shows "
            "them what has been here all along: extraordinary food, music, and community. The "
            "economic impact during the eight-week run is estimated at $180,000 in direct vendor "
            "revenue, with additional multiplier effects on surrounding businesses."
        ),

        jobs_created=45,
        people_served=40000,

        color_palette=["#F97316", "#FB923C", "#7C2D12", "#FED7AA"],
        atmosphere=(
            "Saturday night, 9 PM. The air is warm and thick with competing aromas: jollof rice, "
            "carnitas, pho, jerk chicken, fried plantains, fresh-squeezed lemonade, charcoal "
            "smoke. Broad Street is a river of people moving in both directions, lit by string "
            "lights overhead and the glow of vendor stalls on both sides. Three different bands "
            "are playing — you can hear the R&B from the south end, the Afrobeat from the middle, "
            "and the hip-hop from the north, and in the transition zones the music blends into "
            "something new and accidental and perfect. Steam rises from food carts and catches "
            "the light. Children weave between legs. Vendors shout specials. Someone is laughing "
            "so hard they've stopped walking. It is loud and hot and crowded and alive and it is "
            "exactly what this street was built for."
        ),
        ambient_sounds=[
            "Overlapping live music from three stages",
            "Sizzling oil and clanging wok from food stalls",
            "Crowd noise — conversations in six languages",
            "A vendor calling out 'Jollof! Fresh jollof!'",
            "Children's laughter weaving through the crowd",
            "The pop and hiss of a cold drink being opened",
        ],
    ),

    # ======================================================================
    # EPISODE 8 — PLAZA: "The Winter Village"
    # ======================================================================
    Episode(
        id=8,
        slug="winter-village",
        title="The Winter Village",
        subtitle="The city gathers where the city governs",
        location="Dilworth Park, City Hall Courtyard",
        neighborhood="Center City",
        coordinates=Coordinates(lat=39.9524, lng=-75.1636),
        genre="Romance",
        genre_color="#448AFF",

        logline=(
            "The plaza surrounding City Hall becomes a Nordic-inspired winter village with "
            "ice skating, a makers market in wooden cabins, a hot chocolate bar, children's "
            "theater, and the building itself lit from below — a holiday gathering for the "
            "whole city in the shadow of the building that belongs to all of them."
        ),

        opening_text=(
            "City Hall is the largest municipal building in the United States. It took thirty "
            "years to build. It has 14.5 acres of floor space. William Penn stands on top, "
            "looking north, and on most winter nights he looks down on an empty plaza and "
            "a handful of people hurrying past. We think he deserves a better view."
        ),

        narrative_arc=(
            "The episode opens on November 1st. The plaza is gray and wind-swept. A few "
            "tourists photograph City Hall. Office workers cross with their heads down. The "
            "fountain is off for winter. Then a truck arrives. And another. And we know what's "
            "coming, even if the city doesn't yet.\n\n"
            "The build-out is told as a family story. The production designer is a Norwegian-American "
            "architect from Fishtown whose grandmother described the Christmas markets of Bergen. "
            "She has designed twenty wooden cabins — small, peaked-roof structures modeled on "
            "Nordic market stalls, each one assembled on-site from prefabricated panels. We watch "
            "her direct the construction while her daughter, age 7, 'supervises' from a folding "
            "chair. The ice rink is laid on the west side of the plaza. The children's theater — "
            "a puppet stage inside a heated tent — is assembled on the east. Lights are strung from "
            "every surface. City Hall's base is fitted with uplighting that turns the limestone "
            "walls into a glowing beacon visible from blocks away.\n\n"
            "The final act is opening weekend. The first snow of the season falls on cue — "
            "Hollywood couldn't script it better. The village is magical: warm light spilling from "
            "cabin windows, the sound of skates on ice, children pressed against the puppet theater's "
            "windows, the smell of hot chocolate and cinnamon. The architect's daughter skates for "
            "the first time, holding her mother's hand, and falls, and gets up, and falls, and "
            "gets up, and finally glides three feet on her own, and her face — her face is the "
            "reason we build things."
        ),

        the_moment=(
            "It is snowing. The village is full. The camera finds a man sitting alone on a bench "
            "near the ice rink, watching the skaters. He is holding a cup of hot chocolate. He is "
            "not skating. He is not shopping. He is just sitting. A child falls on the ice in front "
            "of him and he laughs — a real, surprised laugh — and the child looks up at him and "
            "laughs too, and they are strangers sharing a moment in the snow in front of City Hall, "
            "and the man takes a sip of his chocolate and closes his eyes and the camera holds on "
            "his face and we see something that looks like peace. Later, he tells the camera: 'I "
            "lost my wife in March. I haven't been to Center City since. I don't know why I came "
            "tonight. I think I just needed to be around people.' He looks at the village — the "
            "lights, the cabins, the skaters — and says, 'She would have loved this.' And then he "
            "smiles. And it is enough."
        ),

        current_state=(
            "Dilworth Park is the western plaza of Philadelphia City Hall, renovated in 2014 with "
            "a fountain, cafe, and seasonal programming. The space is well-maintained but underused "
            "in winter — the fountain is shut down from November through March, the cafe operates "
            "reduced hours, and the plaza's open design offers no shelter from wind. The existing "
            "seasonal ice rink (operated by a concessionaire) occupies a portion of the west plaza "
            "but leaves the majority of the space empty. The City Hall courtyard — the interior "
            "passage through the building — funnels cold wind. Evening foot traffic drops "
            "significantly in winter months. The infrastructure is excellent (embedded electrical, "
            "drainage, hardscape), but the programming doesn't match the space's potential or its "
            "symbolic importance as the civic center of Philadelphia."
        ),

        activation_concept="Nordic-inspired winter village with ice skating, makers market, children's theater, and architectural lighting",

        activation_description=(
            "Twenty prefabricated wooden market cabins are arranged in a U-shape around the "
            "Dilworth Park fountain (winterized, drained). Each cabin is 8x10 feet, peaked roof, "
            "tongue-and-groove pine construction, with a hinged front wall that opens to create a "
            "vendor counter. Cabins are wired for electricity and fitted with small electric heaters. "
            "Vendor selection prioritizes local makers: ceramicists, woodworkers, textile artists, "
            "candlemakers, bakers, and specialty food producers. A central cabin serves as the hot "
            "chocolate bar — five varieties, all sourced from Philadelphia chocolate makers.\n\n"
            "The existing seasonal ice rink is expanded and enhanced with better lighting and a "
            "sound system playing curated playlists. A children's theater tent (heated, 60-seat "
            "capacity) is erected on the east plaza, hosting free puppet shows and storytelling "
            "sessions on weekends. City Hall's base is fitted with 48 architectural uplights — "
            "LED fixtures in the ground plane aimed up at the limestone facade, programmable to "
            "shift color through the evening. The courtyard passageway is lined with evergreen "
            "garlands and warm white string lights. Heated bench pads are installed on existing "
            "seating. The overall effect is a warm, glowing village nested at the foot of a "
            "glowing civic monument — intimate and monumental at once."
        ),

        permanent_elements=[
            "Improved drainage systems for seasonal installations",
            "Embedded electrical infrastructure (48 ground-level junction boxes)",
            "Permanent pavilion anchor points in plaza hardscape",
            "Enhanced architectural lighting for City Hall base (48 LED uplights)",
            "Heated bench pad electrical connections",
            "Winterized water connections for future vendor use",
        ],

        permanence_percentage=25,

        permanence_narrative=(
            "The cabins are stored for next year — flat-packed in a city warehouse, ready to "
            "reassemble. The children's theater tent is donated to a community center in West "
            "Philly. But the lighting remains. City Hall glows every night now — the uplights "
            "run year-round, cycling through seasonal color programs. The embedded electrical "
            "infrastructure makes future seasonal installations faster and cheaper. The city's "
            "programming office, having seen what the plaza can be in winter, has committed to "
            "an annual Winter Village season running November through February. The man who sat "
            "alone on the bench comes back every Saturday. He has started bringing his "
            "granddaughter. She is learning to skate. He holds her hand the way his wife held "
            "his, and the village glows around them, and the city is a little less cold."
        ),

        estimated_cost=EstimatedCost(low=350000, high=600000),
        timeline_weeks=10,
        permits_needed=[
            "Philadelphia Department of Public Property plaza use permit",
            "Center City District partnership agreement",
            "Philadelphia Fire Department assembly permit",
            "Health Department food service permits (vendors)",
            "L&I temporary structure permits (20 cabins, theater tent)",
            "PECO electrical service upgrade coordination",
            "Streets Department loading zone permits (construction)",
            "Philadelphia Art Commission review (architectural lighting)",
        ],

        community_impact=(
            "Dilworth Park is the civic heart of Philadelphia — the front yard of City Hall, the "
            "crossroads of transit lines, the place where the city literally gathers. But in "
            "winter, it empties. The Winter Village fills it — not with commerce alone but with "
            "the warmth of presence. The makers market provides 20 local artisans with peak-season "
            "retail exposure at no stall cost, directly supporting Philadelphia's creative economy. "
            "The free children's theater serves families who cannot afford ticketed holiday "
            "entertainment. The ice rink expansion increases capacity by 40%.\n\n"
            "The deeper impact is symbolic. A winter village at City Hall says: this building "
            "belongs to you. Come here. Be warm. Be together. The architectural lighting transforms "
            "City Hall from a dark monolith after business hours into a glowing civic landmark "
            "visible from every approach. The permanent electrical infrastructure reduces the cost "
            "of future seasonal programming by an estimated 60%, making annual repetition "
            "financially sustainable. And the man on the bench — the man who came because he "
            "needed to be near people — he is not the only one. The Winter Village's deepest "
            "impact is the one that doesn't fit in a spreadsheet: the cure for urban loneliness "
            "is a warm place to sit and watch the world go by."
        ),

        jobs_created=55,
        people_served=75000,

        color_palette=["#06B6D4", "#67E8F9", "#164E63", "#ECFEFF"],
        atmosphere=(
            "Twilight in December. Fresh snow on the ground — just an inch, enough to soften "
            "every edge and muffle every sound. The sky is the color of a bruise, purple and gray, "
            "and against it City Hall glows warm gold from the uplights, the limestone facade "
            "turned into a lantern. The wooden cabins are lit from within — warm yellow light "
            "spilling through their windows and open counters. The ice rink is a circle of light "
            "and motion, skaters tracing arcs, blades hissing on ice. String lights overhead create "
            "a canopy of warm white stars. The air smells like pine garland and hot chocolate and "
            "cold stone. Children's laughter echoes off the courtyard walls. Somewhere a speaker "
            "plays something acoustic and gentle. The snow is still falling. The village is full. "
            "The city is home."
        ),
        ambient_sounds=[
            "Ice skates hissing and scraping on the rink",
            "Children laughing and calling out to parents",
            "The murmur of the crowd — warm, conversational",
            "A busker playing acoustic guitar near the cabins",
            "The clink of ceramic mugs at the hot chocolate bar",
            "Wind swirling through the City Hall courtyard",
        ],
    ),

    # ======================================================================
    # EPISODE 9 — CORRIDOR: "The Glow"
    # ======================================================================
    Episode(
        id=9,
        slug="glow-corridor",
        title="The Glow Corridor",
        subtitle="The river shows the way",
        location="Schuylkill Banks Trail, Center City to Grays Ferry",
        neighborhood="Center City / Grays Ferry",
        coordinates=Coordinates(lat=39.9417, lng=-75.1830),
        genre="Thriller",
        genre_color="#FF6E40",

        logline=(
            "A two-mile stretch of the Schuylkill River trail becomes an illuminated fitness "
            "corridor where LED light ribbons line the path, fitness stations glow every quarter "
            "mile, night runners chase their own reflections in the river, and a city learns "
            "that the path forward is sometimes the one that's lit."
        ),

        opening_text=(
            "The Schuylkill Banks trail runs along the west side of the river like a seam "
            "between the city and the water. In daylight, it's packed — runners, cyclists, "
            "dog walkers, rowers. But at dusk it empties. The lights end. The path goes dark. "
            "And two miles of riverfront become invisible. We are going to make them glow."
        ),

        narrative_arc=(
            "The episode is structured as a sports drama — the story of a run, told in real "
            "time, intercut with the story of how the path got its light. We open on a runner "
            "at the northern trailhead at dusk. She stretches. She checks her watch. She looks "
            "down the path into the gathering dark. And she goes.\n\n"
            "As she runs, we intercut with the installation story: weeks of work stringing "
            "waterproof LED strip lights along both edges of the two-mile path — 21,000 feet "
            "of light in total. The strips are embedded in aluminum channels bolted to the path's "
            "concrete edge, glowing different colors by section: blue for the first half mile, "
            "purple for the second, teal for the third, green for the fourth. Eight fitness "
            "stations are installed at quarter-mile intervals — pull-up bars, parallel bars, "
            "balance beams, stretching rails — each one lit by its own color-matched LED ring. "
            "We meet the installation crew: electricians, trail workers, a lighting designer who "
            "has only ever worked in theaters and is now working on a two-mile stage. We meet the "
            "runner's story too: she used to run this path every evening, but stopped when the "
            "days got shorter because the dark made her afraid. She hasn't run in four months.\n\n"
            "The final act is the night the lights come on. The runner is at the trailhead. She "
            "doesn't know the installation is complete — she's been invited by a friend who told "
            "her 'just come to the trail at 7.' She arrives. The path is dark. She's about to "
            "leave. And then the lights activate — all 21,000 feet at once, a ribbon of blue "
            "and purple and teal and green stretching along the river into the distance, reflected "
            "in the water, turning the Schuylkill into a mirror of light. She stares. She "
            "starts running. And the camera follows her for two unbroken miles as the city "
            "glows on one side and the river glows on the other and she is running, finally "
            "running, in the light."
        ),

        the_moment=(
            "Mile marker 1.5. The runner has been going for twelve minutes. Her breath is "
            "visible — the air is cold and the LED light catches the vapor, turning each exhale "
            "into a small blue cloud. She is in the teal section now. The river beside her is a "
            "sheet of teal light. Her reflection runs beside her in the water — a shadow-twin "
            "keeping pace. She looks over at it. She smiles. She accelerates. The camera drops "
            "low, running-level, and we see her feet striking the lit path, each footfall landing "
            "between the two glowing edges. Ahead, the path curves and the light curves with it, "
            "tracing the river's bend, and for a moment the illuminated trail looks like it goes "
            "on forever — an infinite ribbon of light following the water into the distance. She "
            "rounds the curve. A fitness station appears, glowing teal, and two other runners "
            "are there, stretching, laughing. She waves. She doesn't stop. She keeps going. The "
            "path keeps glowing. The river keeps reflecting. And she is not afraid."
        ),

        current_state=(
            "The Schuylkill Banks trail is a multi-use path running along the east bank of the "
            "Schuylkill River from Locust Street south to the Grays Ferry Crescent. The northern "
            "section (Locust to South Street) is well-lit, well-maintained, and heavily used. South "
            "of South Street, the path continues but conditions deteriorate: lighting is sparse, "
            "the surface is inconsistent (concrete gives way to gravel in sections), and amenities "
            "are minimal. The two-mile stretch from South Street to Grays Ferry is functionally "
            "unusable after dark — no continuous lighting, no emergency call stations, no "
            "programming. Usage drops to near zero after sunset, despite the path's proximity to "
            "dense residential neighborhoods in Graduate Hospital, Point Breeze, and Grays Ferry. "
            "The river itself is beautiful along this stretch, with mature tree cover and views "
            "of the west bank."
        ),

        activation_concept="LED-illuminated fitness corridor with color-coded sections and lighted exercise stations",

        activation_description=(
            "21,000 feet of waterproof LED strip lighting is installed along both edges of the "
            "two-mile path, embedded in extruded aluminum channels that are bolted to the "
            "existing concrete path edge or to new concrete curbing where the path transitions "
            "to gravel. The LED strips are RGBW (color-changing), controlled by a central system "
            "that maintains color zones: cool blue (0-0.5 mi), deep purple (0.5-1.0 mi), teal "
            "(1.0-1.5 mi), and emerald green (1.5-2.0 mi). The system is programmable for "
            "special events and holidays.\n\n"
            "Eight fitness stations are installed at quarter-mile intervals, each occupying a "
            "15x15-foot concrete pad adjacent to the path. Equipment includes pull-up bars, "
            "parallel bars, a balance beam, and stretching rails — all stainless steel, "
            "commercial-grade outdoor fitness equipment. Each station is lit by a ring of "
            "ground-level LED fixtures matching the section color, creating a glowing island "
            "effect. Wayfinding signage (distance markers, emergency information, QR codes "
            "linking to workout routines) is installed at each station. Four rest stations with "
            "benches, water fountains, and bike repair stands are positioned at half-mile "
            "intervals. Path surface is repaired and standardized to concrete throughout."
        ),

        permanent_elements=[
            "21,000 ft LED path lighting system (both edges, full length)",
            "8 outdoor fitness stations with commercial-grade equipment",
            "Wayfinding and distance marker signage system",
            "4 rest stations with benches, water fountains, and bike repair",
            "Repaired and standardized concrete path surface",
            "Central lighting control system with event programming",
            "Emergency call stations (4 locations)",
            "Stormwater drainage improvements along path edge",
        ],

        permanence_percentage=90,

        permanence_narrative=(
            "A year later, the Glow is one of the most popular running routes on the East Coast. "
            "Running magazines have featured it. Instagram is full of it — the glowing path, the "
            "river reflections, the before-and-after. Usage data from the trail counters shows a "
            "340% increase in evening and nighttime traffic. The fitness stations are in constant "
            "use — a personal trainer has started offering free group sessions at the purple station "
            "on Tuesday nights. The lighting system has been reprogrammed for holidays: red and "
            "green for Christmas, orange for Halloween, rainbow for Pride. A 5K race series uses "
            "the corridor quarterly, with registration proceeds funding maintenance. The runner "
            "from the episode runs here every night now. She's training for a marathon. She "
            "tells people: 'I got my path back.' But it's bigger than that. A city got its "
            "river back. Two miles of waterfront that disappeared every evening now glows until "
            "midnight, and the darkness that kept people away has been replaced by a ribbon of "
            "light that pulls them in."
        ),

        estimated_cost=EstimatedCost(low=280000, high=500000),
        timeline_weeks=12,
        permits_needed=[
            "Schuylkill River Development Corporation trail use agreement",
            "Philadelphia Parks & Recreation installation permit",
            "Philadelphia Water Department river setback review",
            "L&I electrical permits (lighting system, fitness stations)",
            "PennDOT coordination (trail sections near highway ramps)",
            "ADA compliance review (path surface, fitness stations)",
            "Philadelphia Art Commission review (lighting design)",
        ],

        community_impact=(
            "The Schuylkill River trail is Philadelphia's most important linear park, but its "
            "benefits have been unevenly distributed. The well-lit, well-maintained northern "
            "section serves Center City and University City — affluent, high-traffic neighborhoods. "
            "The southern section, serving Graduate Hospital, Point Breeze, and Grays Ferry — "
            "lower-income neighborhoods with less green space access — goes dark at sunset. The "
            "Glow corrects this inequity with permanent infrastructure that extends the trail's "
            "usability to all hours for all two miles.\n\n"
            "The health impact is direct and measurable. The fitness stations provide free outdoor "
            "gym equipment to neighborhoods where gym memberships are a luxury. The lighting "
            "enables safe evening exercise for shift workers and parents who can only find time "
            "after dark. The emergency call stations address the safety concerns that kept women "
            "and elderly residents off the path after sunset. An initial study by the Schuylkill "
            "River Development Corporation estimated 500 additional daily users in the first six "
            "months, representing approximately 2.5 million additional minutes of physical activity "
            "per year. The economic ripple includes increased property values along the trail "
            "corridor and new business activity at the Grays Ferry Crescent trailhead."
        ),

        jobs_created=28,
        people_served=50000,

        color_palette=["#3B82F6", "#8B5CF6", "#14B8A6", "#10B981"],
        atmosphere=(
            "Dusk turning to night. The sky is deep navy in the east, still faintly orange in "
            "the west. The river is dark and glassy, reflecting the last light. And then the "
            "LEDs come on — not all at once but in a slow cascade from north to south, like a "
            "fuse burning along the path's edge. Blue first, then purple, then teal, then green, "
            "each section igniting in sequence until the full two miles are lit. The river doubles "
            "everything — two ribbons of light, one on the path and one on the water. The air is "
            "cool and smells like river water and fallen leaves. Runners appear, their breath "
            "visible, their footfalls rhythmic on the concrete. The fitness stations glow like "
            "campfires along the trail. The city is a wall of warm light to the east. The river "
            "is a mirror to the west. And between them, the path glows, and the people run."
        ),
        ambient_sounds=[
            "Running shoes on concrete — a steady, rhythmic beat",
            "Breath — visible and audible in the cold air",
            "The Schuylkill River lapping against the bank",
            "Distant traffic from the expressway, muffled by trees",
            "A cyclist's bell as they pass",
            "The low hum of the LED lighting system's transformer",
        ],
    ),

    # ======================================================================
    # EPISODE 10 — GARDEN: "The Quiet Place"
    # ======================================================================
    Episode(
        id=10,
        slug="quiet-garden",
        title="The Recovery Garden",
        subtitle="The space between the noise",
        location="52nd and Larchwood, West Philadelphia",
        neighborhood="West Philadelphia",
        coordinates=Coordinates(lat=39.9540, lng=-75.2277),
        genre="Quiet Drama",
        genre_color="#FFAB40",

        logline=(
            "An entire vacant block in West Philadelphia becomes a contemplative garden with "
            "outdoor counseling spaces, a labyrinth walking path, meditation areas, a water "
            "feature, and a community gathering circle — designed with mental health professionals, "
            "built by the neighborhood, and left behind entirely. One hundred percent permanence. "
            "The garden is the point."
        ),

        opening_text=(
            "There is a block on Larchwood Avenue where five houses used to stand. They were "
            "demolished eight years ago. Since then, the block has held: nothing. Weeds. Quiet. "
            "The neighbors walk past it every day. They have stopped seeing it. We are going to "
            "make them stop and look."
        ),

        narrative_arc=(
            "The episode opens in silence. True silence — no music, no voiceover, no ambient "
            "score. Just the sound of the block: wind through weeds, a car passing, a bird. "
            "The camera sits at the center of the vacant lot and doesn't move for sixty seconds. "
            "It is the longest sixty seconds in the series. It is the most important.\n\n"
            "The middle act is a departure from every other episode. There is no single dramatic "
            "build, no climactic event. Instead, the camera documents a slow, communal "
            "transformation over twelve weeks. A landscape architect and a clinical psychologist "
            "co-design the garden in public workshops held on the lot itself — neighbors sit on "
            "folding chairs in the weeds and draw their vision. An elderly man asks for 'somewhere "
            "quiet to sit.' A mother asks for 'a place where I can cry and no one will look at me.' "
            "A teenager asks for 'a labyrinth, like the ones in the old churches.' A veteran asks "
            "for 'water. Moving water. It helps.' Every request is honored. The design emerges "
            "from the community. The construction is done by the community — neighbors with "
            "shovels, professionals with guidance, the landscape architect on her knees in the "
            "dirt beside the grandmother who asked for the crying place.\n\n"
            "The final act is not an opening night. There is no event. The garden simply becomes "
            "available, one morning in early autumn, without announcement. The gates are unlocked. "
            "The paths are swept. The water feature is running. And people come, one by one, "
            "because they can feel it. The elderly man sits on his bench. The mother finds her "
            "alcove. The teenager walks the labyrinth. The veteran stands by the water and "
            "closes his eyes. There is no audience. There is no performance. There is only a "
            "garden, and the people who needed it, and the profound, revolutionary act of "
            "building something quiet in a loud world."
        ),

        the_moment=(
            "Early morning. The garden has been open for three days. The camera finds a woman "
            "sitting alone in the small enclosed alcove that the community designed as the "
            "crying place — a curved stone bench surrounded by tall ornamental grasses that "
            "create a soft, rustling privacy screen. She is crying. Quietly, privately, with "
            "the particular release of someone who has been holding it for a long time. The "
            "grasses move around her. The water feature is audible but not visible — a gentle "
            "sound that fills the silence without breaking it. She cries for two minutes. Then "
            "she stops. She wipes her eyes. She takes a breath. She stands up. She walks out "
            "of the alcove and into the garden and the morning light hits her face and she "
            "looks — not happy, not healed, but lighter. She looks lighter. The camera holds "
            "on the empty alcove. The grasses sway. The water runs. The space holds what she "
            "left behind. That is what gardens do."
        ),

        current_state=(
            "The block at 52nd and Larchwood is approximately 12,000 square feet — the combined "
            "footprint of five demolished rowhomes. The lot is owned by the Philadelphia Land "
            "Bank. It is unfenced and unmaintained. The surface is a mix of old foundation "
            "rubble, compacted soil, and dense weed growth. There are several mature trees along "
            "the rear property line — sycamores and a large black walnut — that provide shade "
            "and vertical structure. The surrounding block is residential: occupied rowhomes on "
            "both sides, a church at the corner, a laundromat across the street. The neighborhood "
            "is predominantly African American, working-class, and significantly underserved in "
            "green space and mental health resources. There is no public park within a quarter "
            "mile. There is no mental health facility within a half mile. This block has both "
            "the need and the bones."
        ),

        activation_concept="Contemplative community garden with mental health integration, labyrinth, water feature, and gathering spaces",

        activation_description=(
            "The lot is cleared of rubble and the soil is tested, remediated where needed, and "
            "amended with compost and topsoil. The design, developed through community workshops, "
            "divides the space into five zones. The Labyrinth: a 30-foot-diameter walking labyrinth "
            "in the center of the garden, laid in local fieldstone set in gravel, based on the "
            "classical seven-circuit pattern. The Water Court: a small recirculating water feature "
            "in the northeast corner — water flowing over stacked stone into a shallow basin, "
            "creating constant gentle sound. The Alcoves: three curved stone benches with "
            "ornamental grass privacy screens, designed for individual contemplation and informal "
            "counseling sessions. The Gathering Circle: a 20-foot-diameter ring of stone seating "
            "in the southeast corner for community meetings, group sessions, and storytelling. "
            "The Growing Place: four raised garden beds along the western edge for community "
            "food production.\n\n"
            "Pathways connecting all zones are crushed stone with timber edging, fully ADA-accessible. "
            "Plantings are native and low-maintenance: ornamental grasses, shade-tolerant perennials "
            "under the existing trees, flowering shrubs along the property lines for screening. "
            "Lighting is minimal and warm — low path lights only, preserving the sense of quiet "
            "enclosure. A small equipment shed in the northwest corner holds maintenance tools. "
            "The garden is designed to be maintained by the community with quarterly professional "
            "support funded by an endowment established during production. A partnership with a "
            "local community mental health organization provides trained counselors who hold "
            "drop-in sessions in the garden on weekday mornings."
        ),

        permanent_elements=[
            "Fieldstone labyrinth (30 ft diameter, seven-circuit pattern)",
            "Recirculating water feature (stacked stone, solar pump)",
            "3 contemplation alcoves with stone benches and grass screens",
            "Community gathering circle (stone seating, 20 ft diameter)",
            "4 raised garden beds for food production",
            "Crushed stone accessible pathways throughout",
            "Native plantings and ornamental grasses",
            "Low-level path lighting (solar-powered)",
            "Equipment and maintenance shed",
            "Maintenance endowment fund",
            "Partnership agreement with community mental health provider",
        ],

        permanence_percentage=100,

        permanence_narrative=(
            "A year later, the garden is indistinguishable from something that has always been "
            "here. The plantings have filled in — the grasses are tall and feathery, the "
            "perennials bloom in succession from spring through fall, the black walnut drops its "
            "nuts in October and the children collect them. The labyrinth's stones are smooth "
            "from walking. The water feature has developed a soft green patina. The garden beds "
            "are in their second season, producing tomatoes, peppers, collard greens, and herbs "
            "that are shared among the neighbors who tend them.\n\n"
            "The counseling sessions have become a fixture — three mornings a week, a therapist "
            "from the partner organization sits in one of the alcoves and anyone can come. No "
            "appointment. No paperwork. Just a conversation in a garden. The veteran comes every "
            "Tuesday. He doesn't always talk to the counselor. Sometimes he just sits by the "
            "water. The teenager who asked for the labyrinth walks it before school. She says it "
            "helps her think. The elderly man has claimed the bench nearest the gathering circle. "
            "His neighbors know to find him there.\n\n"
            "A developer has not made an offer on this block. The land is no longer vacant. "
            "It is full — full of stone and water and growing things and the quiet, stubborn "
            "insistence that a neighborhood deserves a place to breathe. The garden is not "
            "temporary. The garden was never temporary. The garden is the point."
        ),

        estimated_cost=EstimatedCost(low=95000, high=220000),
        timeline_weeks=16,
        permits_needed=[
            "Philadelphia Land Bank long-term use agreement (10-year minimum)",
            "L&I zoning use permit (community garden / public space)",
            "Philadelphia Water Department stormwater management review",
            "ADA compliance review (pathways, gathering areas)",
            "Philadelphia Health Department soil testing clearance",
            "Underground utility locate and clearance",
        ],

        community_impact=(
            "West Philadelphia west of 50th Street is a neighborhood defined by what it lacks: "
            "green space, mental health services, safe gathering places, investment. The Quiet "
            "Place addresses all four with a single, permanent intervention. The garden provides "
            "12,000 square feet of new public green space in a neighborhood where the nearest "
            "park is a 15-minute walk. The counseling partnership provides free, accessible "
            "mental health support in a community where the average wait for an appointment is "
            "six weeks. The gathering circle provides a venue for community meetings that "
            "currently happen in living rooms and church basements. The garden beds provide "
            "fresh food in a USDA-designated food desert.\n\n"
            "But the deepest impact is the one the community designed for itself: the right to "
            "quiet. In a neighborhood stressed by poverty, gun violence, overwork, and neglect, "
            "the garden is a deliberate, designed silence. The labyrinth forces you to slow down. "
            "The water feature masks the traffic. The alcoves give you permission to feel. No "
            "other episode in the series achieves 100% permanence because no other episode needs "
            "to. The Winter Village can come and go. The Night Market can be monthly. But a garden "
            "that heals has to stay. It has to be there every morning when you need it. It has to "
            "be as permanent as the need itself."
        ),

        jobs_created=10,
        people_served=5000,

        color_palette=["#10B981", "#6EE7B7", "#064E3B", "#D1FAE5"],
        atmosphere=(
            "Early morning, first light. The sky is pewter. The air is cool and damp — it rained "
            "overnight and everything is washed clean. Mist sits low in the garden, threading "
            "between the grasses and pooling in the labyrinth's stone channels. The water feature "
            "is the only sound — a gentle, continuous pour over stone, steady as breath. Dew "
            "covers every surface: the bench stone, the grass blades, the labyrinth path. A "
            "single bird begins to sing — a wood thrush, impossibly rich and layered, the most "
            "beautiful birdsong in North America, coming from the black walnut tree. The light "
            "is gray and soft and even, with no shadows yet. The garden is empty of people but "
            "full of presence. It is waiting, the way a held breath waits. It is the quietest "
            "place in Philadelphia."
        ),
        ambient_sounds=[
            "Water flowing over stone — continuous, gentle, steady",
            "A wood thrush singing from the black walnut tree",
            "Wind through ornamental grasses — a soft, papery rustle",
            "Footsteps on crushed stone, slow and deliberate",
            "A distant church bell marking the hour",
            "Silence. Deep, held, intentional silence.",
        ],
    ),
]


# ---------------------------------------------------------------------------
# Data Access Functions
# ---------------------------------------------------------------------------

def get_all_episodes() -> list[Episode]:
    """Return all 10 episodes."""
    return EPISODES


def get_episode_summaries() -> list[EpisodeSummary]:
    """Return summary view of all episodes."""
    return [
        EpisodeSummary(
            id=ep.id,
            slug=ep.slug,
            title=ep.title,
            subtitle=ep.subtitle,
            location=ep.location,
            neighborhood=ep.neighborhood,
            genre=ep.genre,
            genre_color=ep.genre_color,
            color_palette=ep.color_palette,
            estimated_cost=ep.estimated_cost,
            permanence_percentage=ep.permanence_percentage,
        )
        for ep in EPISODES
    ]


def get_episode_by_slug(slug: str) -> Episode | None:
    """Return a single episode by slug, or None if not found."""
    for ep in EPISODES:
        if ep.slug == slug:
            return ep
    return None


def get_episode_stats() -> EpisodeStats:
    """Return aggregate statistics across all episodes."""
    return EpisodeStats(
        total_episodes=len(EPISODES),
        total_cost_low=sum(ep.estimated_cost.low for ep in EPISODES),
        total_cost_high=sum(ep.estimated_cost.high for ep in EPISODES),
        total_jobs_created=sum(ep.jobs_created for ep in EPISODES),
        total_people_served=sum(ep.people_served for ep in EPISODES),
        average_permanence=round(
            sum(ep.permanence_percentage for ep in EPISODES) / len(EPISODES), 1
        ),
        neighborhoods=list(dict.fromkeys(ep.neighborhood for ep in EPISODES)),
        genres=list(dict.fromkeys(ep.genre for ep in EPISODES)),
    )
