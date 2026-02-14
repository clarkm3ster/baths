"""
SPHERES Innovation Laboratory — Culture Engineer seed data.

Cultural programming that transforms empty lots into community stages:
public art, performance, maker spaces, heritage celebrations, festivals.

Philadelphia context: Mural Arts Program (4,000+ murals), rich jazz/hip-hop/
spoken word tradition, strong Black and Latino cultural networks, community
theater tradition, block party culture, Philadelphia Flower Show, First Friday
events.
"""

# ---------------------------------------------------------------------------
# Seed innovations — 6 concrete proposals ready for activation
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # ------------------------------------------------------------------
    # 1. Lot Stage Network
    # ------------------------------------------------------------------
    {
        "title": "Lot Stage Network",
        "summary": (
            "A distributed network of open-air performance venues built on "
            "vacant lots, equipped with modular sound and lighting rigs that "
            "can be deployed in under two hours by trained neighborhood crews."
        ),
        "category": "performance-series",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "programming_format": (
                "Weekly rotating lineup: Monday open-mic spoken word, "
                "Wednesday jazz jam sessions, Friday DJ sets and MC battles, "
                "Saturday family matinee theater. Each lot hosts 2-3 events "
                "per week with curated local headliners."
            ),
            "audience_capacity": (
                "Modular seating for 80-200 depending on lot size. Standing "
                "room configurations expand to 400 for headline shows. ADA "
                "accessible ground-level viewing areas at every venue."
            ),
            "equipment_requirements": (
                "Weatherproof rolling sound cabinet (2x powered speakers, "
                "mixer, wireless mics), portable LED lighting truss, modular "
                "stage decking (8x12 ft sections), generator or grid tie-in, "
                "and a lockable storage container on each activated lot."
            ),
            "artist_stipend": (
                "Headliners receive $300-$500 per set. Emerging artists "
                "receive $150 plus mentorship pairing. Open-mic participants "
                "receive free studio recording time at partner facilities."
            ),
            "community_partners": [
                "Philadelphia Mural Arts Program",
                "Ars Nova Workshop (jazz)",
                "Illadelph Poetry collective",
                "Philadanco (dance)",
                "WRTI / WXPN community radio",
            ],
        },
        "tags": [
            "performance",
            "open-air",
            "jazz",
            "hip-hop",
            "spoken-word",
            "modular-infrastructure",
        ],
    },

    # ------------------------------------------------------------------
    # 2. Community Mural Garden
    # ------------------------------------------------------------------
    {
        "title": "Community Mural Garden",
        "summary": (
            "Combines Philadelphia's world-renowned Mural Arts tradition "
            "with food-growing infrastructure on party walls and adjacent "
            "vacant lots, creating edible landscapes framed by monumental art."
        ),
        "category": "public-art",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "programming_format": (
                "Each site pairs a lead muralist with a master gardener for "
                "a 10-week community co-design sprint. Residents vote on mural "
                "themes and crop selections. Monthly harvest festivals combine "
                "art tours with communal cooking using on-site produce."
            ),
            "seasonal_schedule": {
                "spring": (
                    "Mural design workshops and soil preparation. Seedling "
                    "starts distributed to participating households."
                ),
                "summer": (
                    "Mural painting in public sessions with live music. "
                    "Vertical trellis installation for climbing crops. "
                    "Weekly pick-your-own hours."
                ),
                "fall": (
                    "Harvest festival and mural unveiling celebration. "
                    "Canning and preservation workshops. Seed saving for "
                    "the following year."
                ),
                "winter": (
                    "Indoor gallery exhibitions documenting each site. "
                    "Planning charrettes for next season. Cold-frame greens "
                    "production continues on south-facing walls."
                ),
            },
            "artist_stipend": (
                "Lead muralists receive $5,000 per wall. Apprentice artists "
                "(prioritizing neighborhood youth) receive $1,500 stipends. "
                "Master gardeners receive seasonal contracts at $2,500."
            ),
            "cultural_traditions_honored": [
                "African American quilting patterns as mural geometry",
                "Puerto Rican casita garden tradition",
                "Italian Market row-house gardening heritage",
                "Southeast Asian refugee community crop knowledge",
                "Southern Black foodways and seed-keeping traditions",
            ],
            "community_partners": [
                "Philadelphia Mural Arts Program",
                "Pennsylvania Horticultural Society",
                "Soil Generation",
                "Las Parcelas / Norris Square Neighborhood Project",
                "Urban Creators (Life Do Grow Farm)",
            ],
        },
        "tags": [
            "mural-arts",
            "urban-agriculture",
            "food-justice",
            "public-art",
            "party-wall",
            "co-design",
        ],
    },

    # ------------------------------------------------------------------
    # 3. Maker Space Popup
    # ------------------------------------------------------------------
    {
        "title": "Maker Space Popup",
        "summary": (
            "Rotating fabrication and repair workshops deployed on activated "
            "parcels, bringing tool libraries, 3D printing, sewing machines, "
            "and bike repair stations directly to neighborhoods."
        ),
        "category": "maker-space",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "programming_format": (
                "Two-week residencies on each lot. Week 1: open workshop "
                "hours (10am-6pm) with drop-in repair cafe and tool lending. "
                "Week 2: structured skill-building classes (woodworking, "
                "screen printing, small electronics, bicycle mechanics). "
                "Each residency culminates in a community market where "
                "participants sell or trade what they have made."
            ),
            "audience_capacity": (
                "15-20 concurrent workstations per popup. Classes capped at "
                "12 for hands-on instruction. Open workshop hours serve "
                "40-60 visitors per day."
            ),
            "equipment_requirements": (
                "20-foot shipping container converted to mobile workshop: "
                "table saws, drill presses, sewing machines, 3D printer, "
                "soldering stations, hand tool library (200+ tools). "
                "Requires 30-amp electrical service or solar+battery trailer."
            ),
            "artist_stipend": (
                "Lead maker-instructors receive $400/day. Guest specialists "
                "(welders, upholsterers, luthiers) receive $250 per session. "
                "Youth apprentices receive $15/hour stipend."
            ),
            "community_partners": [
                "NextFab (makerspace network)",
                "The Free Library of Philadelphia tool lending",
                "Philly Bike Action",
                "Neighborhood Bike Works",
                "Philadelphia Sculptors",
            ],
        },
        "tags": [
            "maker",
            "repair-cafe",
            "tool-library",
            "fabrication",
            "skill-building",
            "circular-economy",
        ],
    },

    # ------------------------------------------------------------------
    # 4. Block Heritage Archive
    # ------------------------------------------------------------------
    {
        "title": "Block Heritage Archive",
        "summary": (
            "An oral history and augmented reality installation that preserves "
            "neighborhood memory, letting residents record stories tied to "
            "specific locations and view archival imagery overlaid on the "
            "present-day streetscape through their phones."
        ),
        "category": "heritage-archive",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "programming_format": (
                "StoryCorps-style recording booths on activated lots, open "
                "3 days per week. Trained neighborhood historians conduct "
                "interviews. Collected audio is geotagged and accessible via "
                "a free AR app. Physical listening posts (solar-powered, "
                "weather-resistant speakers with handsets) are installed at "
                "key story locations so residents without smartphones can "
                "participate."
            ),
            "audience_capacity": (
                "Recording booth serves 8-10 storytellers per day. AR "
                "experience is unlimited concurrent users. Listening posts "
                "serve 1 visitor at a time with 3-5 minute story loops."
            ),
            "equipment_requirements": (
                "Portable sound-isolation recording booth, broadcast-quality "
                "microphones, tablet-based AR kiosk, solar-powered listening "
                "post hardware, and a dedicated web server for the geotagged "
                "story database."
            ),
            "cultural_traditions_honored": [
                "Great Migration narratives and family origin stories",
                "Philadelphia jazz and R&B oral histories",
                "Puerto Rican and Dominican neighborhood founding stories",
                "Vietnamese and Cambodian refugee resettlement memories",
                "Italian, Irish, and Jewish immigrant block histories",
            ],
            "community_partners": [
                "Philadelphia Free Library Oral History Program",
                "Temple University Center for Public History",
                "PhillyHistory.org / PhillyGeoHistory",
                "Taller Puertorriqueno",
                "African American Museum in Philadelphia",
            ],
        },
        "tags": [
            "oral-history",
            "augmented-reality",
            "heritage",
            "storytelling",
            "geotagged",
            "intergenerational",
        ],
    },

    # ------------------------------------------------------------------
    # 5. Seasonal Festival Circuit
    # ------------------------------------------------------------------
    {
        "title": "Seasonal Festival Circuit",
        "summary": (
            "A four-season programming calendar that rotates cultural festivals "
            "across activated vacant lots, ensuring year-round vibrancy and "
            "giving every neighborhood a signature seasonal celebration."
        ),
        "category": "festival-series",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "programming_format": (
                "Each season anchors around a flagship weekend festival plus "
                "4-6 smaller satellite events. Flagship format: live music "
                "on two stages, food vendors (prioritizing neighborhood "
                "kitchens), artisan market, children's area, and a community "
                "art build. Satellite events include porch concerts, block "
                "party tie-ins, and cultural workshops."
            ),
            "seasonal_schedule": {
                "spring": (
                    "Bloom Festival — floral installations echoing the "
                    "Philadelphia Flower Show tradition, garden plot lottery, "
                    "seed swaps, and maypole dance performances."
                ),
                "summer": (
                    "Block Beat Festival — hip-hop, go-go, salsa, and "
                    "Afrobeat stages celebrating Philly's deep rhythmic "
                    "traditions. Water play zones for children. Evening "
                    "outdoor film screenings."
                ),
                "fall": (
                    "Harvest & Heritage Festival — storytelling circles, "
                    "community cook-offs, ancestor altars for Dia de los "
                    "Muertos, and a lantern parade connecting activated lots "
                    "across the neighborhood."
                ),
                "winter": (
                    "Light Up the Lot — solar-powered light art installations, "
                    "warming stations with hot cider, winter market for local "
                    "makers, and a New Year's community visioning ceremony."
                ),
            },
            "audience_capacity": (
                "Flagship festivals: 500-2,000 attendees. Satellite events: "
                "50-300. Annual circuit goal: 15,000 total unique participants "
                "across all seasons and neighborhoods."
            ),
            "artist_stipend": (
                "Flagship headliners: $1,000-$2,500. Supporting acts: $300-$600. "
                "Festival coordinators (neighborhood residents): $2,000 per "
                "season. Youth street team: $100 stipend per event."
            ),
            "community_partners": [
                "Philadelphia Folklore Project",
                "Odunde Festival organizers",
                "Feria del Barrio / Taller Puertorriqueno",
                "First Friday Philly network",
                "Philadelphia Parks & Recreation",
            ],
        },
        "tags": [
            "festival",
            "seasonal",
            "block-party",
            "multicultural",
            "food-culture",
            "lantern-parade",
        ],
    },

    # ------------------------------------------------------------------
    # 6. Youth Culture Lab
    # ------------------------------------------------------------------
    {
        "title": "Youth Culture Lab",
        "summary": (
            "Teen-led creative programming on neighborhood lots where young "
            "people aged 14-21 design, produce, and host their own cultural "
            "events with mentorship from professional artists and organizers."
        ),
        "category": "youth-program",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "programming_format": (
                "8-week cohort cycles. Weeks 1-2: visioning and skill "
                "workshops (event production, sound engineering, marketing, "
                "budgeting). Weeks 3-6: collaborative production of a youth-"
                "designed event. Week 7: public event execution. Week 8: "
                "reflection, documentation, and portfolio building. Each "
                "cohort of 15 youth is paired with 3 professional mentors."
            ),
            "audience_capacity": (
                "Cohort size: 15 youth per cycle, 4 cycles per year. "
                "Youth-produced events draw 100-500 attendees depending on "
                "format. Annual reach: 60 youth participants, 1,200+ event "
                "attendees."
            ),
            "equipment_requirements": (
                "Portable PA system, digital audio workstation laptops (5), "
                "DSLR cameras and tripods (3), screen printing setup, "
                "projection equipment for outdoor cinema, and a supply "
                "budget of $1,500 per cohort for materials."
            ),
            "artist_stipend": (
                "Youth participants receive $500 stipend per 8-week cycle. "
                "Professional mentors receive $2,000 per cycle. Guest "
                "workshop leaders receive $200 per session."
            ),
            "cultural_traditions_honored": [
                "Philadelphia hip-hop and battle rap legacy",
                "Black Arts Movement and spoken word tradition",
                "Latino mural and street art culture",
                "Philly ball culture and voguing",
                "DIY punk and zine-making tradition",
            ],
            "community_partners": [
                "The Colored Girls Museum",
                "Asian Arts Initiative",
                "Will Power Productions (youth theater)",
                "Amber Art & Design",
                "PhillyCAM (community media)",
            ],
        },
        "tags": [
            "youth",
            "teen-led",
            "mentorship",
            "event-production",
            "creative-workforce",
            "hip-hop",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator templates — 8 patterns for spawning new innovations
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # ------------------------------------------------------------------
    # 1. Pop-Up Performance Venue
    # ------------------------------------------------------------------
    {
        "title": "Pop-Up Performance Venue",
        "summary": (
            "Template for rapidly deploying a temporary performance venue "
            "on any activated vacant lot, complete with staging, sound, and "
            "community seating."
        ),
        "category": "performance-series",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "programming_format": (
                "Single-genre or mixed-bill live events: concerts, comedy "
                "nights, poetry slams, dance showcases, or theatrical "
                "readings. 2-4 hour runtime with intermission."
            ),
            "audience_capacity": "50-300 depending on lot footprint.",
            "equipment_requirements": (
                "Portable stage (8x12 ft minimum), PA system with mixer, "
                "4-channel LED wash lights, folding chairs or hay bales, "
                "and a permit from Streets Department."
            ),
            "artist_stipend": "$150-$500 per performer depending on draw.",
            "community_partners": [
                "Local block captain",
                "Neighborhood advisory committee",
                "Philadelphia Office of Arts, Culture and the Creative Economy",
            ],
        },
        "tags": ["performance", "live-music", "popup", "vacant-lot"],
    },

    # ------------------------------------------------------------------
    # 2. Mural + Growing Wall
    # ------------------------------------------------------------------
    {
        "title": "Mural + Growing Wall",
        "summary": (
            "Template for integrating vertical food production with a new "
            "or restored community mural on an exposed party wall."
        ),
        "category": "public-art",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "programming_format": (
                "Co-design charrette with neighbors, followed by a 6-8 week "
                "mural painting process with integrated trellis and planter "
                "installation. Ongoing monthly garden tending days."
            ),
            "seasonal_schedule": {
                "spring": "Design and prep. Soil testing and amendment.",
                "summer": "Mural painting and planter installation.",
                "fall": "Harvest celebration and mural dedication.",
                "winter": "Maintenance planning and next-wall scouting.",
            },
            "cultural_traditions_honored": [
                "Philadelphia Mural Arts legacy",
                "Community garden movement",
                "Neighborhood identity storytelling",
            ],
            "community_partners": [
                "Mural Arts Philadelphia",
                "Pennsylvania Horticultural Society",
                "Property owner or Land Bank",
            ],
        },
        "tags": ["mural", "urban-agriculture", "party-wall", "public-art"],
    },

    # ------------------------------------------------------------------
    # 3. Traveling Repair Cafe
    # ------------------------------------------------------------------
    {
        "title": "Traveling Repair Cafe",
        "summary": (
            "Template for a mobile repair and skill-sharing event that "
            "rotates through neighborhoods, reducing waste and building "
            "practical know-how."
        ),
        "category": "maker-space",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "programming_format": (
                "Half-day drop-in events (10am-3pm). Stations for clothing "
                "repair, small electronics, furniture, bicycles, and small "
                "appliances. Each station staffed by a skilled volunteer "
                "paired with a youth apprentice."
            ),
            "audience_capacity": "30-60 visitors per session.",
            "equipment_requirements": (
                "Folding tables, basic tool kits per station, sewing "
                "machines, soldering irons, bicycle stand, canopy tents "
                "for weather protection, signage, and intake/tracking forms."
            ),
            "artist_stipend": (
                "Lead repair volunteers: $100 honorarium. Youth apprentices: "
                "$50 stipend per event."
            ),
            "community_partners": [
                "Local repair and trade professionals",
                "High school shop and CTE programs",
                "Neighborhood civic associations",
            ],
        },
        "tags": ["repair", "skill-share", "circular-economy", "maker"],
    },

    # ------------------------------------------------------------------
    # 4. Neighborhood Story Booth
    # ------------------------------------------------------------------
    {
        "title": "Neighborhood Story Booth",
        "summary": (
            "Template for deploying a portable oral history recording "
            "station on a lot, collecting and archiving the lived "
            "experiences of long-time residents."
        ),
        "category": "heritage-archive",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 5],
        "details": {
            "programming_format": (
                "3-day popup: Day 1 community outreach and sign-ups, "
                "Days 2-3 recording sessions (30-minute slots). Interviews "
                "conducted by trained peer historians. Stories archived "
                "digitally and shared at a public listening party."
            ),
            "audience_capacity": (
                "8-12 storytellers per day. Listening party serves 50-100."
            ),
            "equipment_requirements": (
                "Portable sound booth or quiet tent, condenser microphones, "
                "digital recorder, noise-canceling headphones, tablet for "
                "consent forms, and archival storage service."
            ),
            "cultural_traditions_honored": [
                "Griot storytelling tradition",
                "StoryCorps-inspired peer interviewing",
                "Neighborhood memory and place attachment",
            ],
            "community_partners": [
                "Local library branch",
                "Senior center or aging-in-place organization",
                "University oral history program",
            ],
        },
        "tags": ["oral-history", "storytelling", "archive", "heritage"],
    },

    # ------------------------------------------------------------------
    # 5. Seasonal Block Celebration
    # ------------------------------------------------------------------
    {
        "title": "Seasonal Block Celebration",
        "summary": (
            "Template for a neighborhood-scale seasonal festival that "
            "activates one or more vacant lots with food, music, art, and "
            "community ritual."
        ),
        "category": "festival-series",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 4],
        "details": {
            "programming_format": (
                "Full-day event (11am-8pm): opening ceremony led by a "
                "community elder, live entertainment on one stage, food "
                "vendors in a curated row, children's activity zone, "
                "artisan market, and a closing community sing or ritual."
            ),
            "seasonal_schedule": {
                "spring": "Renewal themes, planting ceremonies, kite flying.",
                "summer": "Water play, dance battles, cookout competitions.",
                "fall": "Harvest feast, storytelling, ancestor remembrance.",
                "winter": "Light installations, warming stations, gift exchange.",
            },
            "audience_capacity": "200-1,500 depending on lot cluster size.",
            "artist_stipend": (
                "Musicians and performers: $200-$800. Emcee/host: $300. "
                "Children's activity leaders: $150 each."
            ),
            "community_partners": [
                "Block captain and civic association",
                "Neighborhood faith institutions",
                "Local business improvement district",
            ],
        },
        "tags": ["festival", "block-party", "seasonal", "community-ritual"],
    },

    # ------------------------------------------------------------------
    # 6. Youth Arts Residency
    # ------------------------------------------------------------------
    {
        "title": "Youth Arts Residency",
        "summary": (
            "Template for an intensive multi-week creative residency where "
            "teens collaborate with professional artists to produce original "
            "work showcased on a neighborhood lot."
        ),
        "category": "youth-program",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "programming_format": (
                "6-week residency: 3 afternoons per week (3-6pm). Focus on "
                "a single discipline (muralism, filmmaking, music production, "
                "fashion, or spoken word). Culminates in a public showcase "
                "event produced entirely by the youth cohort."
            ),
            "audience_capacity": (
                "Cohort: 10-15 youth. Showcase event: 100-300 attendees."
            ),
            "equipment_requirements": (
                "Discipline-specific supplies (paint, cameras, instruments, "
                "sewing machines, microphones), covered workspace or tent, "
                "storage for in-progress work, and showcase staging."
            ),
            "artist_stipend": (
                "Lead teaching artist: $3,000 per residency. Youth stipend: "
                "$300 per participant. Guest critics: $150 per visit."
            ),
            "cultural_traditions_honored": [
                "Apprenticeship and mentorship lineage",
                "Philadelphia's tradition of youth-led creative movements",
                "Intergenerational knowledge transfer",
            ],
            "community_partners": [
                "School district arts coordinators",
                "Youth-serving nonprofit in the neighborhood",
                "Professional artist or cultural institution",
            ],
        },
        "tags": ["youth", "residency", "arts-education", "mentorship"],
    },

    # ------------------------------------------------------------------
    # 7. Cultural Heritage Trail
    # ------------------------------------------------------------------
    {
        "title": "Cultural Heritage Trail",
        "summary": (
            "Template for linking multiple activated lots into a walkable "
            "cultural trail with interpretive signage, AR waypoints, and "
            "curated audio guides narrated by community members."
        ),
        "category": "heritage-archive",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "programming_format": (
                "Self-guided walking tour available year-round via app and "
                "physical signage. Monthly docent-led group walks with live "
                "narration. Quarterly trail expansion events where new "
                "stories and stops are added by the community."
            ),
            "audience_capacity": (
                "Self-guided: unlimited. Docent-led walks: 15-25 per group. "
                "Annual target: 5,000 trail users."
            ),
            "equipment_requirements": (
                "Weather-resistant interpretive signs with QR codes, AR "
                "content hosted on cloud platform, solar-powered audio "
                "posts at key stops, and printed trail maps."
            ),
            "cultural_traditions_honored": [
                "Walking as communal practice and protest tradition",
                "Place-based identity and belonging",
                "Multilingual neighborhood histories",
            ],
            "community_partners": [
                "Local historical society",
                "Preservation Alliance for Greater Philadelphia",
                "Walking tour operators and urban guides",
            ],
        },
        "tags": [
            "heritage-trail",
            "walking-tour",
            "augmented-reality",
            "interpretive-signage",
        ],
    },

    # ------------------------------------------------------------------
    # 8. Artist-in-Residence Lot Activation
    # ------------------------------------------------------------------
    {
        "title": "Artist-in-Residence Lot Activation",
        "summary": (
            "Template for granting a professional artist exclusive use of "
            "a vacant lot for 1-3 months to create a site-specific public "
            "artwork, with required community engagement hours."
        ),
        "category": "public-art",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "programming_format": (
                "Open call for proposals reviewed by a panel of neighbors "
                "and arts professionals. Selected artist receives lot access, "
                "a stipend, and a materials budget. Required: minimum 20 "
                "hours of public-facing process (open studios, workshops, "
                "conversations). Artwork remains on view for at least 6 "
                "months after completion."
            ),
            "audience_capacity": (
                "Open studio visits: 10-30 per session. Final unveiling "
                "event: 100-500. Ongoing public viewing: unlimited."
            ),
            "equipment_requirements": (
                "Varies by medium. Baseline: secured perimeter fencing, "
                "water access, electrical hookup or generator, portable "
                "toilet, and a weather shelter for the artist."
            ),
            "artist_stipend": (
                "Resident artist: $5,000-$10,000 depending on duration. "
                "Materials budget: $2,000-$5,000. Community engagement "
                "coordinator: $1,500."
            ),
            "cultural_traditions_honored": [
                "Site-specific and land-based art practices",
                "Philadelphia's legacy as a public art capital",
                "Neighborhood co-creation and participatory aesthetics",
            ],
            "community_partners": [
                "Philadelphia Office of Arts, Culture and the Creative Economy",
                "Neighborhood advisory committee",
                "Local gallery or cultural anchor institution",
            ],
        },
        "tags": [
            "artist-residency",
            "site-specific",
            "public-art",
            "community-engagement",
        ],
    },
]
