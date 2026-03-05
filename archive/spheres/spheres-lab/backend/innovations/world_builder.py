"""
SPHERES Innovation Laboratory — World Builder seed innovations and generator templates.

Domain: immersive-worlds
Agent: World Builder — Immersive Experience Designer

Seed innovations and randomized templates for 3D visualization, AR/VR experiences,
WebGL installations, projection mapping, and virtual walkthroughs that let Philadelphia
communities see transformed spaces before they're built.
"""

# ---------------------------------------------------------------------------
# Seed innovations — 6 fully-specified immersive-world concepts
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # 1 — AR Lot Lens
    {
        "title": "AR Lot Lens",
        "summary": (
            "A mobile AR application that overlays proposed community designs onto "
            "Philadelphia's 40,000+ vacant lots in real-time through the phone camera, "
            "letting residents walk the site and see pocket parks, gardens, and micro-housing "
            "before a single shovel breaks ground."
        ),
        "category": "ar-overlay",
        "impact_level": 5,
        "feasibility": 4,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "ARKit/ARCore with custom Three.js fallback for web-AR; real-time "
                "ground-plane detection and light estimation for photorealistic "
                "compositing against live camera feed."
            ),
            "interaction_model": (
                "Point-and-view with tap-to-cycle design variants; pinch-to-scale "
                "elements; long-press to drop community comment pins geotagged to "
                "the parcel; swipe to toggle between proposal versions."
            ),
            "device_requirements": (
                "Any smartphone with ARCore 1.9+ or ARKit 3+; progressive web app "
                "fallback using WebXR for older devices; minimum 2 GB RAM; works "
                "offline with cached parcel geometry."
            ),
            "content_pipeline": (
                "Design proposals exported from Rhino/Grasshopper as glTF 2.0 "
                "compressed with Draco; automated LOD generation for near/mid/far "
                "viewing; community-submitted SketchUp models converted via "
                "server-side pipeline; PBR material library for consistent look."
            ),
            "accessibility_features": (
                "VoiceOver/TalkBack screen reader narration of design elements; "
                "high-contrast outline mode for low-vision users; haptic feedback "
                "on interactive hotspots; audio descriptions of each design variant "
                "triggered by spatial proximity."
            ),
        },
        "tags": ["ar", "mobile", "vacant-lots", "community-design", "webxr"],
    },

    # 2 — Neighborhood Time Machine
    {
        "title": "Neighborhood Time Machine",
        "summary": (
            "A browser-based WebGL experience that renders any Philadelphia block across "
            "three temporal layers — historical streetscape, present-day conditions, and "
            "speculative future activation — driven by archival photography, LiDAR scans, "
            "and community-sourced vision boards."
        ),
        "category": "webgl-experience",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "Custom Three.js scene graph with instanced mesh rendering; "
                "temporal interpolation shader for smooth cross-fade between past, "
                "present, and future geometry layers; post-processing bloom and "
                "film-grain for historical epochs."
            ),
            "interaction_model": (
                "Scroll-driven timeline scrubber that morphs geometry between eras; "
                "click-to-reveal oral history audio clips pinned to buildings; "
                "drag-orbit camera with cinematic ease curves; keyboard arrow "
                "navigation for accessibility."
            ),
            "device_requirements": (
                "Modern browser with WebGL 2.0 support; graceful degradation to "
                "static image sequences on low-end devices; recommended GPU with "
                "2 GB VRAM for full experience; touch support for tablets."
            ),
            "content_pipeline": (
                "Historical photos photogrammetrically reconstructed into 3D via "
                "NeRF; present-day geometry from City of Philadelphia LiDAR open "
                "data; future visions modeled by UPenn architecture students in "
                "Blender and exported as glTF; oral histories recorded at "
                "community design charrettes."
            ),
            "frame_rate_target": (
                "60 fps on desktop, 30 fps on mobile; dynamic LOD switching and "
                "texture streaming to maintain target; GPU-based occlusion culling "
                "for dense urban blocks."
            ),
        },
        "tags": ["webgl", "history", "temporal", "storytelling", "lidar", "threejs"],
    },

    # 3 — Community Design VR
    {
        "title": "Community Design VR",
        "summary": (
            "A multiplayer VR workshop environment where neighbors don headsets and "
            "collaboratively design space activations in real-time — dragging trees, "
            "benches, murals, and play structures onto a 1:1 scale digital twin of "
            "their neighborhood vacant lot."
        ),
        "category": "vr-workshop",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "WebXR-based renderer using Three.js with hand-tracking support; "
                "real-time collaborative state sync via WebRTC data channels; "
                "baked global illumination for stable lighting in co-design scenes; "
                "spatial audio for natural conversation between participants."
            ),
            "interaction_model": (
                "Grab-and-place asset palette with snapping grid; voice commands "
                "for undo/redo and material swaps; laser pointer for remote "
                "annotation; consensus voting system where each participant can "
                "upvote or flag placed elements; facilitator mode with broadcast "
                "camera for non-VR observers."
            ),
            "device_requirements": (
                "Meta Quest 3 or Quest Pro as primary target; PCVR fallback for "
                "Valve Index; WebXR spectator mode in browser for participants "
                "without headsets; portable VR kits deployed to rec centers and "
                "libraries for equitable access."
            ),
            "content_pipeline": (
                "Asset library of 200+ neighborhood-appropriate elements curated "
                "with community input — culturally specific murals, native plant "
                "species, ADA-compliant furniture; assets modeled in Blender at "
                "three LOD tiers; real-time physics for stacking and placement "
                "validation."
            ),
            "community_engagement_method": (
                "Pop-up VR design charrettes at rec centers, churches, and "
                "laundromats; bilingual facilitation in English and Spanish; "
                "session recordings exported as 360-degree video for asynchronous "
                "community review; final designs 3D-printed as physical scale "
                "models for city council presentations."
            ),
        },
        "tags": ["vr", "co-design", "multiplayer", "webxr", "charrette", "equity"],
    },

    # 4 — Projection Mapping Previews
    {
        "title": "Projection Mapping Previews",
        "summary": (
            "Nighttime projection events that beam proposed designs onto the walls and "
            "ground planes of vacant lots, transforming empty parcels into luminous "
            "previews of community-chosen futures — viewable without any device, "
            "democratizing access to spatial imagination."
        ),
        "category": "projection-mapping",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "TouchDesigner real-time rendering pipeline with custom GLSL "
                "shaders for surface-adaptive warping; dual 20K-lumen laser "
                "projectors with geometric correction for irregular building "
                "facades; Notch integration for particle effects."
            ),
            "interaction_model": (
                "Audience SMS voting to cycle between design proposals projected "
                "live; QR code links to AR Lot Lens for daytime revisiting; "
                "live DJ/musician collaboration where audio reactivity drives "
                "visual transitions between design concepts."
            ),
            "device_requirements": (
                "No audience device required — projections visible to naked eye; "
                "production rig: weatherproof projector enclosures, portable "
                "generator or street-power tap, laptop running TouchDesigner with "
                "RTX 4070 GPU; LiDAR scanner for pre-event surface calibration."
            ),
            "content_pipeline": (
                "Community design proposals rendered as animated sequences in "
                "Blender Cycles; perspective-corrected in MadMapper for each "
                "unique wall geometry; seasonal content rotations curated by "
                "neighborhood cultural councils; archival footage composited "
                "for historical context layers."
            ),
            "accessibility_features": (
                "Audio narration broadcast on low-power FM transmitter for "
                "visually impaired attendees; wheelchair-accessible viewing "
                "zones; ASL interpreter projected as picture-in-picture overlay; "
                "sensory-friendly quiet viewings scheduled monthly with reduced "
                "brightness and no audio reactivity."
            ),
        },
        "tags": [
            "projection-mapping", "public-art", "nighttime", "no-device",
            "community-voting", "touchdesigner",
        ],
    },

    # 5 — Interactive 3D Parcel Explorer
    {
        "title": "Interactive 3D Parcel Explorer",
        "summary": (
            "A browser-based 3D map of all 580,000 Philadelphia parcels — color-coded "
            "by vacancy status, zoning, activation potential, and community proposals — "
            "enabling anyone to fly through the city, click a lot, and see its data, "
            "history, and proposed transformations."
        ),
        "category": "3d-mapping",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "Deck.gl for geospatial tile rendering with Three.js overlay for "
                "3D building extrusions; Mapbox vector tiles as base layer; "
                "custom WebGL fragment shaders for parcel heat-mapping; "
                "GPU-accelerated picking for instant parcel identification on hover."
            ),
            "interaction_model": (
                "Fly-through navigation with WASD + mouse orbit; click parcel to "
                "open info drawer with ownership, zoning, soil data, and community "
                "proposals; filter toolbar for vacancy status, land bank parcels, "
                "and activation score; shareable deep links to specific parcels."
            ),
            "device_requirements": (
                "Any modern browser; progressive loading with 2D fallback for "
                "low-end devices; mobile-responsive with touch gestures; embeddable "
                "iframe widget for city agency dashboards and community org websites."
            ),
            "content_pipeline": (
                "Philadelphia Open Data parcel geometry updated nightly via ETL; "
                "building footprints extruded from city LiDAR height data; "
                "community proposals linked via SPHERES platform API; satellite "
                "imagery tiles from Mapbox for ground texture."
            ),
            "frame_rate_target": (
                "60 fps with up to 50,000 visible parcels using instanced rendering "
                "and frustum culling; level-of-detail transitions at camera distance "
                "thresholds; tile-based loading to keep memory under 512 MB."
            ),
        },
        "tags": [
            "3d-map", "geospatial", "open-data", "parcels", "deck-gl",
            "city-scale", "browser",
        ],
    },

    # 6 — Immersive Impact Theater
    {
        "title": "Immersive Impact Theater",
        "summary": (
            "A portable 360-degree projection dome that tells before-and-after "
            "transformation stories of Philadelphia lots — combining drone footage, "
            "resident interviews, 3D renders, and spatial audio into an emotionally "
            "compelling experience deployable at community events, city council "
            "hearings, and funder presentations."
        ),
        "category": "360-experience",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "rendering_engine": (
                "Unreal Engine 5 with Lumen global illumination for photorealistic "
                "before/after scenes; exported as equirectangular video at 8K "
                "resolution; real-time variant uses Three.js WebGL for browser-based "
                "flat-screen fallback."
            ),
            "interaction_model": (
                "Passive seated experience with facilitator-controlled chapter "
                "navigation; audience response clickers for live polling during "
                "intermissions; optional gaze-based hotspot exploration in VR "
                "headset version; post-show digital survey linked via QR code."
            ),
            "device_requirements": (
                "Inflatable 20-foot geodesic dome with 4x fisheye projectors and "
                "spatial audio array; portable in a cargo van; indoor fallback "
                "using curved screen and 2 projectors; browser version accessible "
                "on any device for remote audiences."
            ),
            "content_pipeline": (
                "Drone photogrammetry of existing lots; Unreal Engine cinematic "
                "sequences of proposed activations; resident video testimonials "
                "filmed in 180-degree stereo; ambisonic field recordings of "
                "neighborhood soundscapes; all stitched in DaVinci Resolve with "
                "custom spatial audio mix."
            ),
            "community_engagement_method": (
                "Traveling dome visits each council district quarterly; community "
                "members featured as narrators of their own block's story; youth "
                "media program trains teens to capture drone footage and conduct "
                "interviews; screening followed by facilitated design workshop."
            ),
        },
        "tags": [
            "360-video", "dome", "storytelling", "drone", "unreal-engine",
            "community-voice", "portable",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator templates — 8 randomized templates the generator can instantiate
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # T1 — AR Heritage Walk
    {
        "title": "AR Heritage Walk",
        "summary": (
            "A geolocated AR walking tour that resurrects demolished buildings and "
            "lost landmarks as ghostly 3D holograms, layering oral history audio "
            "over the present-day streetscape as visitors walk Philadelphia's "
            "historically significant corridors."
        ),
        "category": "ar-overlay",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 5],
        "details": {
            "rendering_engine": (
                "WebXR with 8th Wall integration for broad device support; "
                "ghostly transparency shader with bloom post-processing; "
                "GPS + visual-inertial odometry for sub-meter placement accuracy."
            ),
            "interaction_model": (
                "Walk-to-trigger waypoints; tap hologram to hear oral history "
                "clip; swipe timeline slider to see building at different decades; "
                "photo mode for sharing AR snapshots to social media."
            ),
            "device_requirements": (
                "Any smartphone with camera and GPS; progressive web app — no "
                "app store download required; works in daylight and dusk conditions."
            ),
            "content_pipeline": (
                "Historical photos reconstructed via photogrammetry; oral histories "
                "sourced from Temple University Urban Archives; 3D models optimized "
                "for mobile with Draco compression under 5 MB per landmark."
            ),
            "accessibility_features": (
                "Full audio description mode for visually impaired walkers; "
                "seated/stationary mode for mobility-impaired users viewing all "
                "stops from a single location; captions on all audio content."
            ),
        },
        "tags": ["ar", "heritage", "walking-tour", "oral-history", "webxr"],
    },

    # T2 — Lot-Scale Digital Twin
    {
        "title": "Lot-Scale Digital Twin",
        "summary": (
            "A high-fidelity digital twin of a single vacant parcel — capturing "
            "soil conditions, sun exposure, drainage patterns, and neighboring "
            "structures — enabling architects and community planners to test "
            "interventions in simulation before physical implementation."
        ),
        "category": "digital-twin",
        "time_horizon": "medium",
        "impact_range": [3, 4],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 4],
        "details": {
            "rendering_engine": (
                "Three.js with custom PBR soil material library; sun-path "
                "simulation via solar position algorithm; real-time shadow "
                "casting for time-of-day analysis; rain particle system for "
                "drainage visualization."
            ),
            "interaction_model": (
                "Drag-and-drop planting and structure placement; time-lapse "
                "slider showing seasonal growth simulation; split-screen "
                "compare mode for testing multiple design options side by side."
            ),
            "device_requirements": (
                "Browser-based with WebGL 2.0; exportable to VR for immersive "
                "site visits; print-ready orthographic views for permit "
                "applications."
            ),
            "content_pipeline": (
                "LiDAR point cloud capture; soil data from USDA Web Soil Survey "
                "API; solar irradiance from NREL PVWatts; neighboring structures "
                "from OpenStreetMap 3D buildings."
            ),
            "community_engagement_method": (
                "Digital twin stations at block captain meetings; residents test "
                "garden vs. playground vs. housing scenarios and vote on preferred "
                "outcome; results exported as formal proposal to Philadelphia "
                "Land Bank."
            ),
        },
        "tags": ["digital-twin", "simulation", "soil", "solar", "planning"],
    },

    # T3 — WebGL Mural Previewer
    {
        "title": "WebGL Mural Previewer",
        "summary": (
            "A browser tool that lets artists and community groups preview "
            "proposed murals on building facades using photogrammetric 3D scans "
            "of the wall surface, with accurate scale, lighting, and perspective "
            "distortion correction."
        ),
        "category": "webgl-experience",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "rendering_engine": (
                "Three.js with UV-projection shader mapping 2D artwork onto "
                "scanned 3D wall geometry; environment lighting matched to "
                "site photography via HDR environment map; paint material "
                "simulation for matte/gloss/metallic finishes."
            ),
            "interaction_model": (
                "Upload artwork image; drag to position on wall; adjust scale "
                "and rotation; toggle time-of-day lighting; generate shareable "
                "before/after comparison link."
            ),
            "device_requirements": (
                "Any browser; mobile-friendly touch interface; exports "
                "high-resolution renders for Mural Arts Philadelphia proposals."
            ),
            "content_pipeline": (
                "Photogrammetry scans of target walls captured via smartphone "
                "video processed in Meshroom; standard wall template library "
                "for common Philadelphia row house dimensions."
            ),
            "accessibility_features": (
                "Alt-text generation for mural preview images; keyboard-only "
                "navigation for all controls; high-contrast UI theme option."
            ),
        },
        "tags": ["webgl", "mural", "public-art", "mural-arts", "preview"],
    },

    # T4 — Soundscape Immersion Layer
    {
        "title": "Soundscape Immersion Layer",
        "summary": (
            "A spatial audio experience layered onto 3D visualizations that "
            "simulates the acoustic environment of a proposed activation — "
            "children playing, water features, birdsong from native plantings — "
            "giving communities an auditory preview alongside the visual one."
        ),
        "category": "spatial-audio",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [4, 5],
        "details": {
            "rendering_engine": (
                "Web Audio API with HRTF spatialization; Resonance Audio SDK "
                "for room acoustics simulation; custom reverb impulse responses "
                "captured from existing Philadelphia public spaces."
            ),
            "interaction_model": (
                "Navigate 3D scene and hear sounds shift spatially; toggle "
                "sound layers on/off (traffic, nature, people, water); A/B "
                "compare current ambient noise vs. proposed soundscape."
            ),
            "device_requirements": (
                "Headphones recommended for full spatialization; stereo speaker "
                "fallback with crossfeed; compatible with all SPHERES WebGL "
                "episodes as an add-on layer."
            ),
            "content_pipeline": (
                "Ambisonic field recordings from Philadelphia parks and plazas; "
                "procedural sound generation for water features and wind through "
                "foliage; community-recorded neighborhood sounds for authentic "
                "baseline."
            ),
            "community_engagement_method": (
                "Listening sessions where residents close their eyes and "
                "experience proposed soundscapes; feedback forms capture emotional "
                "responses; sound preferences inform design priorities."
            ),
        },
        "tags": ["spatial-audio", "soundscape", "web-audio", "immersion", "sensory"],
    },

    # T5 — Participatory Zoning Sandbox
    {
        "title": "Participatory Zoning Sandbox",
        "summary": (
            "A game-like 3D environment where residents manipulate zoning "
            "parameters — height limits, setbacks, use designations — and "
            "instantly see the resulting built form on their block, demystifying "
            "zoning code and empowering informed civic participation."
        ),
        "category": "interactive-simulation",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "rendering_engine": (
                "Three.js with procedural building generation from zoning "
                "parameters; real-time boolean geometry for setback visualization; "
                "shadow study renderer for solar access analysis; color-coded "
                "use-type overlays."
            ),
            "interaction_model": (
                "Slider controls for FAR, height, setback, and lot coverage; "
                "dropdown for use types; instant 3D regeneration on parameter "
                "change; save and compare up to four scenarios; export zoning "
                "proposal as formatted PDF."
            ),
            "device_requirements": (
                "Browser-based; responsive design for phone through desktop; "
                "real-time rendering requires WebGL 2.0 and 1 GB available RAM."
            ),
            "content_pipeline": (
                "Philadelphia zoning code parsed into parametric rules engine; "
                "existing building stock from OpenStreetMap 3D; procedural "
                "facade textures from Philadelphia architectural typology library."
            ),
            "community_engagement_method": (
                "Deployed at zoning board hearing prep sessions; community "
                "organizations use it to visualize impact of proposed variances; "
                "results submitted as public comment attachments."
            ),
        },
        "tags": ["zoning", "simulation", "civic", "parametric", "education"],
    },

    # T6 — Drone-to-WebGL Pipeline
    {
        "title": "Drone-to-WebGL Pipeline",
        "summary": (
            "An automated pipeline that transforms drone survey footage of a "
            "vacant lot into a navigable WebGL 3D scene within 24 hours, "
            "drastically reducing the cost and time of creating digital site "
            "models for community design processes."
        ),
        "category": "content-pipeline",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "rendering_engine": (
                "Three.js with potree-based point cloud renderer for raw scan "
                "display; meshed and textured model via OpenDroneMap; progressive "
                "mesh loading for bandwidth-constrained viewers."
            ),
            "interaction_model": (
                "Orbit navigation around reconstructed lot; measurement tool for "
                "distances and areas; annotation pins for noting features like "
                "existing trees, utilities, and access points."
            ),
            "device_requirements": (
                "DJI Mini 4 Pro or equivalent drone for capture; cloud processing "
                "server with OpenDroneMap; output viewable on any WebGL-capable "
                "browser."
            ),
            "content_pipeline": (
                "Automated flight plan generation from parcel polygon; drone "
                "captures 200+ overlapping photos; OpenDroneMap processes to "
                "point cloud and textured mesh; automated glTF optimization "
                "and upload to SPHERES CDN."
            ),
            "community_engagement_method": (
                "Youth drone pilot training program in partnership with Drexel "
                "engineering; teens survey their own neighborhood lots and "
                "present 3D models at community meetings."
            ),
        },
        "tags": ["drone", "photogrammetry", "pipeline", "automation", "youth"],
    },

    # T7 — Storefront Window Portal
    {
        "title": "Storefront Window Portal",
        "summary": (
            "Repurposing vacant storefront windows as transparent display "
            "surfaces showing real-time 3D visualizations of proposed lot "
            "activations visible to passersby 24/7 — turning blight into "
            "a billboard for community possibility."
        ),
        "category": "public-display",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [4, 5],
        "details": {
            "rendering_engine": (
                "Raspberry Pi 5 driving transparent OLED or rear-projection "
                "film on storefront glass; Chromium kiosk mode running Three.js "
                "scene; ambient light sensor adjusts brightness for day/night "
                "visibility."
            ),
            "interaction_model": (
                "Passerby detection via ultrasonic sensor triggers animation "
                "sequence; NFC tap point on window frame launches AR companion "
                "experience on phone; QR code for community feedback form; "
                "content rotates weekly based on community input."
            ),
            "device_requirements": (
                "Transparent display film or OLED panel; Raspberry Pi 5 with "
                "4 GB RAM; weatherproof enclosure; solar panel option for "
                "off-grid locations; cellular modem for remote content updates."
            ),
            "content_pipeline": (
                "Automated render-to-video from SPHERES 3D proposals; weekly "
                "content rotation managed via CMS dashboard; community-submitted "
                "artwork integrated via moderated upload portal."
            ),
            "accessibility_features": (
                "Audio description via directional speaker triggered by NFC; "
                "braille information placard adjacent to display; high-contrast "
                "rendering mode active during daylight hours."
            ),
        },
        "tags": [
            "public-display", "storefront", "transparent-display", "24-7",
            "street-level", "raspberry-pi",
        ],
    },

    # T8 — Collaborative World-Jam Sessions
    {
        "title": "Collaborative World-Jam Sessions",
        "summary": (
            "Live-streamed 3D world-building jam sessions where architects, "
            "artists, and community members simultaneously sculpt a shared "
            "WebGL scene representing a proposed lot activation — combining "
            "the energy of a hackathon with the creativity of a design charrette."
        ),
        "category": "collaborative-creation",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [3, 5],
        "details": {
            "rendering_engine": (
                "Three.js with operational transform sync layer for conflict-free "
                "concurrent editing; WebSocket server for real-time state "
                "broadcast; instanced rendering for participant cursors and "
                "avatars; snapshot system saving scene state every 30 seconds."
            ),
            "interaction_model": (
                "Browser-based 3D editor with simplified Blender-like controls; "
                "asset stamp tool for placing pre-made elements; freeform voxel "
                "sculpting for terrain; text chat and voice channels per team; "
                "facilitator can freeze scene for group discussion."
            ),
            "device_requirements": (
                "Browser with WebGL 2.0 and WebSocket support; recommended "
                "mouse + keyboard but touch-friendly mobile mode available; "
                "Twitch/YouTube stream embed for passive viewers."
            ),
            "content_pipeline": (
                "Shared asset library of Philadelphia-specific elements hosted "
                "on SPHERES CDN; participants can import custom glTF models "
                "under 10 MB; session recordings archived as replayable "
                "time-lapse animations."
            ),
            "community_engagement_method": (
                "Monthly jam sessions themed around specific neighborhoods; "
                "winning designs selected by community vote receive funding "
                "for physical prototyping; partnership with UPenn, Temple, "
                "and Drexel architecture programs for student participation."
            ),
        },
        "tags": [
            "collaborative", "live-stream", "jam-session", "hackathon",
            "architecture-schools", "websocket",
        ],
    },
]
