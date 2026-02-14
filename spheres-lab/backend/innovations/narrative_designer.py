"""
SPHERES Innovation Laboratory — Narrative Designer seed innovations and templates.

Domain: narrative-design
Compelling narratives: documentary series, oral histories, data visualization
stories, community journalism platforms, social media campaigns.

Philadelphia context: PhillyCAM community media, WHYY/NPR, Mural Arts
storytelling tradition, neighborhood newspapers, vibrant social media culture
around community organizing, and a deep documentary film community.
"""

# ---------------------------------------------------------------------------
# Seed innovations — 6 approved concepts ready for activation
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    {
        "title": "\"The Lot Next Door\" Documentary Series",
        "summary": (
            "A 10-episode documentary series following the transformation of "
            "vacant lots across five Philadelphia neighborhoods, told entirely "
            "through the voices of the residents who live beside them."
        ),
        "category": "documentary",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "narrative_format": (
                "10 x 28-minute episodes; verite-style observational "
                "documentary with interstitial data animations showing lot "
                "metrics over time"
            ),
            "distribution_channels": [
                "WHYY/PBS local broadcast",
                "PhillyCAM community cable",
                "YouTube channel with weekly drops",
                "Pop-up screenings at activated lots",
                "Philadelphia Film Festival premiere",
            ],
            "production_timeline": (
                "18-month shoot across four seasons; 6-month post-production; "
                "rolling episode releases starting month 20"
            ),
            "community_voices_featured": (
                "Minimum 50 resident storytellers drawn from Kensington, "
                "Strawberry Mansion, Point Breeze, Mantua, and Nicetown; "
                "elder narrators paired with youth camera crews"
            ),
            "media_partnerships": [
                "WHYY/NPR Philadelphia",
                "PhillyCAM",
                "Scribe Video Center",
                "Mural Arts Philadelphia",
                "Philadelphia Inquirer documentary desk",
            ],
        },
        "tags": [
            "documentary",
            "community-voice",
            "long-form",
            "PBS",
            "neighborhood-stories",
        ],
    },
    {
        "title": "Vacant Memories Oral History Archive",
        "summary": (
            "A growing digital archive of elder-narrated oral histories "
            "capturing what Philadelphia's now-vacant lots once were — corner "
            "stores, dance halls, front stoops where neighbors gathered."
        ),
        "category": "oral-history",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "narrative_format": (
                "Audio recordings (5-20 minutes each) with geotagged "
                "transcripts, archival photo overlays, and hand-drawn memory "
                "maps created in collaboration with each storyteller"
            ),
            "distribution_channels": [
                "Searchable web archive with interactive map",
                "QR codes installed at lot locations for on-site listening",
                "WHYY podcast feed — weekly 'Memory Minute' segments",
                "Free Library of Philadelphia local history collection",
                "PhillyCAM radio broadcast rotation",
            ],
            "production_timeline": (
                "Rolling collection: 10 stories per month; archive launch at "
                "month 4 with 40 founding stories; ongoing in perpetuity"
            ),
            "community_voices_featured": (
                "Priority outreach to residents aged 60+ through senior "
                "centers, churches, barbershops, and block captains; bilingual "
                "recordings in English and Spanish"
            ),
            "storytelling_methodology": (
                "StoryCorps-inspired facilitated dialogue model; trained "
                "community interviewers from each neighborhood; consent-first "
                "protocol with storyteller editorial approval"
            ),
        },
        "tags": [
            "oral-history",
            "elder-wisdom",
            "archive",
            "geotagged",
            "bilingual",
        ],
    },
    {
        "title": "Data Story Engine",
        "summary": (
            "An automated visual narrative system that transforms real-time "
            "lot activation metrics into compelling infographic stories, "
            "published weekly to keep communities informed and engaged."
        ),
        "category": "data-visualization",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "narrative_format": (
                "Automated weekly data stories combining sensor data, event "
                "attendance, and community sentiment into scrollytelling web "
                "pages, social media card decks, and printable one-pagers"
            ),
            "distribution_channels": [
                "SPHERES platform embedded story feed",
                "Instagram carousel auto-generated posts",
                "Neighborhood newspaper insert (print-ready PDF)",
                "City Council briefing dashboard",
                "Community meeting slide decks",
            ],
            "production_timeline": (
                "Engine development: 3 months; beta with 5 pilot lots: "
                "month 4; full network rollout: month 6; weekly cadence "
                "thereafter"
            ),
            "audience_reach_target": (
                "5,000 unique readers per weekly story by month 8; 20,000 "
                "social media impressions per story by month 12"
            ),
            "storytelling_methodology": (
                "Narrative arc templates: 'The Turnaround' (declining lot "
                "revived), 'The Gathering Place' (event-driven activation), "
                "'The Quiet Shift' (gradual neighborhood change); each "
                "template pairs quantitative data with a resident quote"
            ),
        },
        "tags": [
            "data-viz",
            "automation",
            "scrollytelling",
            "metrics",
            "weekly-cadence",
        ],
    },
    {
        "title": "Block Beat Community Journalism Platform",
        "summary": (
            "A hyperlocal journalism platform training and equipping "
            "neighborhood correspondents to cover lot activations, turning "
            "residents into the reporters of their own transformation stories."
        ),
        "category": "community-journalism",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "narrative_format": (
                "Short-form reported articles (400-800 words), photo essays, "
                "60-second video dispatches, and monthly long-form features; "
                "all published on a shared community news site with "
                "neighborhood edition pages"
            ),
            "distribution_channels": [
                "BlockBeat.philly website with neighborhood editions",
                "Weekly email newsletter per neighborhood",
                "PhillyCAM television segment compilation",
                "Cross-publication syndication with Billy Penn and Kensington Voice",
                "Printed broadsheet distributed at corner stores and laundromats",
            ],
            "production_timeline": (
                "Correspondent recruitment and training: months 1-3; soft "
                "launch with 3 neighborhoods: month 4; city-wide expansion: "
                "month 9; sustainable independent operation by month 18"
            ),
            "community_voices_featured": (
                "Cohort of 30 paid neighborhood correspondents — minimum 50% "
                "residents of color, 25% youth (16-24), 25% bilingual — each "
                "covering a 10-block radius around activated lots"
            ),
            "media_partnerships": [
                "Resolve Philadelphia (collaborative journalism network)",
                "Temple University Klein College of Media",
                "Billy Penn / The Philadelphia Inquirer",
                "Kensington Voice",
                "AL DIA News",
            ],
        },
        "tags": [
            "journalism",
            "hyperlocal",
            "paid-correspondents",
            "neighborhood-news",
            "syndication",
        ],
    },
    {
        "title": "#MyPhillyLot Social Media Campaign",
        "summary": (
            "A viral storytelling initiative inviting Philadelphians to share "
            "memories, dreams, and transformation stories about the lots in "
            "their neighborhoods through a unified social media campaign."
        ),
        "category": "social-media",
        "impact_level": 4,
        "feasibility": 5,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "narrative_format": (
                "User-generated short videos (15-90 seconds), photo + caption "
                "posts, Instagram Reels, TikTok duets, and Twitter/X threads; "
                "curated weekly highlight reels and monthly 'Best Of' "
                "compilations"
            ),
            "distribution_channels": [
                "Instagram (@MyPhillyLot)",
                "TikTok (@MyPhillyLot)",
                "Twitter/X (#MyPhillyLot)",
                "Facebook community groups per neighborhood",
                "SPHERES platform social wall embed",
            ],
            "production_timeline": (
                "Campaign identity and launch: 6 weeks; influencer seeding: "
                "weeks 4-8; sustained community posting: ongoing; quarterly "
                "themed challenges to reignite engagement"
            ),
            "audience_reach_target": (
                "10,000 posts using #MyPhillyLot in year one; 500,000 total "
                "impressions per month by month 6; 50 neighborhood influencer "
                "ambassadors recruited"
            ),
            "storytelling_methodology": (
                "Prompt-driven storytelling: weekly prompts ('What did this "
                "lot look like when you were 10?', 'Film your favorite moment "
                "at a lot event', 'Show us your lot dream'); ambassador kit "
                "with tripod, ring light, and story prompt cards"
            ),
        },
        "tags": [
            "social-media",
            "viral",
            "user-generated",
            "hashtag-campaign",
            "influencer",
        ],
    },
    {
        "title": "Before/After Time-Lapse Network",
        "summary": (
            "A network of 100 solar-powered cameras installed on vacant lots "
            "across Philadelphia, capturing daily time-lapse imagery that "
            "documents two years of transformation into cinematic narratives."
        ),
        "category": "documentary",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "far",
        "status": "approved",
        "details": {
            "narrative_format": (
                "Daily still frames composited into season-by-season "
                "time-lapse sequences; 4-minute cinematic compilation per lot "
                "with original score; live-updating web viewer showing "
                "real-time vs. day-one comparison slider"
            ),
            "distribution_channels": [
                "Interactive web gallery with comparison slider per lot",
                "Annual 'Year in Transformation' feature film (festival circuit)",
                "Social media daily GIF drops — 'Lot of the Day'",
                "Philadelphia Museum of Art installation partnership",
                "City planning department evidence library",
            ],
            "production_timeline": (
                "Hardware procurement and installation: months 1-6; first "
                "seasonal compilation at month 6; continuous capture for 24 "
                "months; feature film edit in month 28; gallery exhibition "
                "month 30"
            ),
            "community_voices_featured": (
                "Each camera site paired with a 'Lot Guardian' — a resident "
                "volunteer who provides monthly audio commentary overlaid on "
                "the time-lapse, narrating changes as they witness them"
            ),
            "media_partnerships": [
                "Philadelphia Museum of Art — media installation",
                "Comcast NBCUniversal — broadcast segments",
                "Google Arts & Culture — online exhibition",
                "National Geographic Short Film Showcase",
                "University of Pennsylvania Weitzman School — research data",
            ],
        },
        "tags": [
            "time-lapse",
            "camera-network",
            "cinematic",
            "long-term",
            "visual-evidence",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator templates — 8 templates for procedural innovation generation
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    {
        "title": "Neighborhood Audio Walking Tour",
        "summary": (
            "A GPS-triggered audio experience guiding walkers through "
            "activated lots with layered storytelling — oral history, live "
            "data sonification, and ambient soundscapes recorded on site."
        ),
        "category": "audio-experience",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 5],
        "details": {
            "narrative_format": (
                "30-45 minute GPS-triggered audio walk; chapters unlock at "
                "each lot location; layered tracks for history, data, and "
                "ambient sound"
            ),
            "distribution_channels": [
                "Mobile app with GPS triggers",
                "Downloadable MP3 for offline use",
                "Free Library of Philadelphia lending kits",
            ],
            "storytelling_methodology": (
                "Immersive audio layering: resident narration over field "
                "recordings; data sonification translates lot metrics into "
                "musical tones the listener hears in real time"
            ),
        },
        "tags": ["audio", "walking-tour", "GPS", "immersive", "sonification"],
    },
    {
        "title": "Youth Documentary Fellowship",
        "summary": (
            "A paid 12-week fellowship placing Philadelphia teens behind the "
            "camera to produce short documentaries about lot activations in "
            "their own neighborhoods."
        ),
        "category": "documentary",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 4],
        "details": {
            "narrative_format": (
                "5-10 minute short documentary per fellow; cohort screening "
                "event; compilation reel for broadcast"
            ),
            "community_voices_featured": (
                "20 fellows per cohort aged 16-22; recruitment through school "
                "district, YouthBuild, and community centers"
            ),
            "media_partnerships": [
                "Scribe Video Center — mentorship",
                "PhillyCAM — broadcast",
                "Temple University Klein College — equipment and facilities",
            ],
            "production_timeline": (
                "Recruitment month 1; training weeks 1-4; production weeks "
                "5-10; post-production and screening weeks 11-12"
            ),
        },
        "tags": [
            "youth",
            "fellowship",
            "documentary",
            "paid-opportunity",
            "mentorship",
        ],
    },
    {
        "title": "Multilingual Story Booth",
        "summary": (
            "Solar-powered recording booths placed at activated lots where "
            "residents can record stories in any language, building a "
            "multilingual narrative tapestry of Philadelphia's communities."
        ),
        "category": "oral-history",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "narrative_format": (
                "Self-guided 3-minute audio recordings; automated "
                "transcription and translation; published to searchable web "
                "archive with language filters"
            ),
            "distribution_channels": [
                "On-site playback kiosk",
                "Web archive with 20+ language filters",
                "WHYY multilingual podcast channel",
            ],
            "community_voices_featured": (
                "Prompts available in 12 languages reflecting neighborhood "
                "demographics; partnership with immigrant service "
                "organizations for outreach"
            ),
        },
        "tags": [
            "multilingual",
            "oral-history",
            "booth",
            "solar-powered",
            "translation",
        ],
    },
    {
        "title": "Lot Transformation Data Dashboard",
        "summary": (
            "A public-facing interactive dashboard narrating the quantitative "
            "story of every activated lot — foot traffic, events hosted, green "
            "cover change, and community sentiment over time."
        ),
        "category": "data-visualization",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 4],
        "details": {
            "narrative_format": (
                "Interactive web dashboard with animated timeline, drill-down "
                "per lot, comparative neighborhood view, and exportable "
                "reports for community meetings"
            ),
            "audience_reach_target": (
                "2,000 monthly active users by month 6; adopted by 5 City "
                "Council offices for district reporting"
            ),
            "storytelling_methodology": (
                "Data-as-narrative: each metric presented with contextual "
                "sentence explaining what the number means for residents; "
                "annotations from community correspondents"
            ),
        },
        "tags": [
            "dashboard",
            "data-viz",
            "public-data",
            "interactive",
            "civic-tech",
        ],
    },
    {
        "title": "Mural Story Map",
        "summary": (
            "An augmented-reality layer over Mural Arts murals near activated "
            "lots, letting viewers scan murals with their phones to hear the "
            "artist and community narrate the story behind each piece."
        ),
        "category": "augmented-reality",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "narrative_format": (
                "AR overlay triggered by phone camera; 90-second artist "
                "narration with animation; links to full documentary episode "
                "if available"
            ),
            "media_partnerships": [
                "Mural Arts Philadelphia — content and access",
                "Snap Inc. — AR lens development",
                "Visit Philadelphia — tourism integration",
            ],
            "distribution_channels": [
                "Snapchat AR lens",
                "Dedicated SPHERES AR viewer (web-based)",
                "Printed postcards with QR fallback for non-AR users",
            ],
        },
        "tags": [
            "augmented-reality",
            "murals",
            "Mural-Arts",
            "interactive",
            "tourism",
        ],
    },
    {
        "title": "Seasonal Neighborhood Zine",
        "summary": (
            "A quarterly print zine produced by residents of each activated "
            "neighborhood, combining photography, poetry, data snapshots, and "
            "hand-drawn maps into a collectible record of change."
        ),
        "category": "print-media",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [3, 4],
        "details": {
            "narrative_format": (
                "16-page risograph-printed zine; bilingual English/Spanish; "
                "mix of resident essays, photo essays, data infographics, and "
                "youth artwork"
            ),
            "production_timeline": (
                "Quarterly cadence; 6-week production cycle per issue; "
                "community editorial board selects content"
            ),
            "distribution_channels": [
                "Free at corner stores, laundromats, and libraries",
                "Mailed to 500 subscribers",
                "Digital PDF on SPHERES platform",
                "Archived at Free Library of Philadelphia",
            ],
        },
        "tags": ["zine", "print", "quarterly", "risograph", "bilingual"],
    },
    {
        "title": "Live Storytelling Night Series",
        "summary": (
            "Monthly open-mic storytelling events held on activated lots where "
            "residents perform true personal stories about place, memory, and "
            "neighborhood change — recorded for podcast distribution."
        ),
        "category": "live-performance",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [4, 5],
        "novelty_range": [3, 4],
        "details": {
            "narrative_format": (
                "6-8 live performers per event; 5-minute true personal "
                "stories; theme per month (e.g., 'First Home', 'The Corner', "
                "'What We Built'); recorded and edited for podcast"
            ),
            "audience_reach_target": (
                "150 in-person attendees per event; 3,000 podcast downloads "
                "per episode by month 6"
            ),
            "community_voices_featured": (
                "Open call with reserved slots for first-time storytellers; "
                "story coaching workshops offered two weeks before each event"
            ),
        },
        "tags": [
            "live-event",
            "storytelling",
            "open-mic",
            "podcast",
            "monthly",
        ],
    },
    {
        "title": "Counter-Narrative Research Collaborative",
        "summary": (
            "A resident-scholar partnership producing rigorous counter-"
            "narratives that challenge deficit framing of vacant lots and "
            "their neighborhoods, published as accessible multimedia reports."
        ),
        "category": "community-journalism",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "narrative_format": (
                "Annual multimedia report combining academic research, "
                "resident testimony, data analysis, and short film; executive "
                "summary designed for policy audiences; full report designed "
                "for community reading"
            ),
            "media_partnerships": [
                "University of Pennsylvania urban studies program",
                "PolicyLink national network",
                "Philadelphia Inquirer opinion desk",
                "Resolve Philadelphia",
            ],
            "storytelling_methodology": (
                "Participatory action research: residents co-design research "
                "questions, conduct interviews, and co-author findings; "
                "counter-narrative framework foregrounds community assets "
                "over deficits"
            ),
        },
        "tags": [
            "counter-narrative",
            "research",
            "participatory",
            "policy",
            "multimedia-report",
        ],
    },
]
