"""
BATHS Intelligence — Frontier AI Research Tracker

This is the ongoing frontier AI researcher. It maintains a living map
of every capability that matters to BATHS — from robotics to world models
to agent networks to things that border on science fiction but are in
the realm of what's being built right now.

Each capability is mapped to specific BATHS layers and production capabilities.
Maturity is tracked honestly: theoretical, lab, pilot, production, frontier.

The system doesn't just list capabilities — it identifies CONVERGENCE ZONES
where multiple research threads are converging toward BATHS-relevant
breakthroughs, and PARADIGM SHIFTS that fundamentally change what's possible.

This is not aspirational. This is a research tracking system that tells
principals and practitioners: here's what's real, here's what's coming,
and here's what it means for your next dome or sphere.
"""

from typing import List, Dict, Optional
from datetime import datetime

from intelligence.models import (
    FrontierCapability, ResearchFrontier, ResearchMaturity,
)


# ── The Living Frontier Map ─────────────────────────────────────
# This is initialized with real capabilities. The researcher agent
# updates these as the field advances.

def build_initial_frontier() -> ResearchFrontier:
    """
    Build the initial frontier map from current AI research landscape.

    Every entry here is REAL research. Papers cited are real papers.
    Labs cited are real labs. The maturity assessments are honest.
    """

    capabilities = []

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: AGENT NETWORKS & MULTI-AGENT SYSTEMS
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Multi-Agent Task Decomposition",
        description=(
            "Systems where multiple AI agents decompose complex tasks, "
            "distribute subtasks, and synthesize results. Directly applicable "
            "to BATHS production stages where legal, financial, narrative, "
            "and design work happens in parallel."
        ),
        category="agent_networks",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_dome=[2, 3, 4, 5, 6],
        applicable_layers_sphere=[2, 3, 4, 5],
        applicable_capabilities=[
            "legal_navigation", "data_systems", "narrative",
            "flourishing_design", "activation_design", "economics",
        ],
        key_papers=[
            "AutoGen: Enabling Next-Gen LLM Applications (Microsoft, 2023)",
            "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework (2023)",
            "CrewAI: Framework for orchestrating role-playing autonomous AI agents (2024)",
        ],
        key_labs=["Microsoft Research", "DeepMind", "Anthropic", "OpenAI"],
        key_benchmarks=["SWE-bench", "GAIA", "AgentBench"],
        integration_path=(
            "Replace template-based production.py with agent-orchestrated production "
            "where specialist agents handle legal navigation, cost modeling, narrative "
            "generation, and design work. Each agent has access to the memory system "
            "and world models."
        ),
        dependencies=["LLM API access", "Tool-use frameworks"],
        estimated_timeline="Available now for integration",
    ))

    capabilities.append(FrontierCapability(
        name="Agent-to-Agent Communication Protocols",
        description=(
            "Structured protocols for AI agents to share findings, negotiate "
            "approaches, and build on each other's work within a production. "
            "Critical for dome/sphere productions where legal findings inform "
            "financial models which inform design which informs narrative."
        ),
        category="agent_networks",
        maturity=ResearchMaturity.LAB,
        applicable_layers_dome=[3, 4, 5, 6],
        applicable_layers_sphere=[3, 4, 5],
        applicable_capabilities=[
            "legal_navigation", "data_systems", "narrative",
            "flourishing_design",
        ],
        key_papers=[
            "Communicative Agents for Software Development (ChatDev, 2023)",
            "AgentVerse: Facilitating Multi-Agent Collaboration (2023)",
        ],
        key_labs=["Tsinghua University", "Microsoft Research"],
        integration_path=(
            "Implement inter-agent messaging in the production pipeline so that "
            "a legal navigator agent's findings are automatically available to "
            "the cost modeling agent, which feeds the design agent."
        ),
        dependencies=["Multi-Agent Task Decomposition", "Shared memory"],
        estimated_timeline="6-12 months for robust implementation",
    ))

    capabilities.append(FrontierCapability(
        name="Swarm Intelligence for Team Assembly",
        description=(
            "Using collective intelligence patterns to optimize team composition. "
            "Instead of tag-matching, the system simulates multiple team configurations "
            "and predicts which combinations will produce the most unexpected IP. "
            "The 'unlikely collision' becomes predictable."
        ),
        category="agent_networks",
        maturity=ResearchMaturity.LAB,
        applicable_layers_dome=[3],
        applicable_layers_sphere=[3],
        applicable_capabilities=["team_assembly", "resonance_matching"],
        key_papers=[
            "Emergent Tool Use From Multi-Agent Interaction (DeepMind, 2019)",
            "Quality-Diversity Optimization (Mouret & Clune, 2015)",
        ],
        key_labs=["DeepMind", "MIT CSAIL"],
        integration_path=(
            "Replace formula-based assembly.py resonance scoring with a system that "
            "simulates 100+ team configurations using the memory system's data on "
            "what team compositions historically produced the highest cosm/chron."
        ),
        dependencies=["Memory system with sufficient project history"],
        estimated_timeline="12-18 months (needs data accumulation)",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: WORLD MODELS
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Government System Simulation",
        description=(
            "World models that simulate how government systems actually behave — "
            "not how they're designed to behave. Includes processing times, "
            "bureaucratic friction, caseworker discretion, inter-system conflicts, "
            "and cascade failures. Critical for dome accuracy."
        ),
        category="world_models",
        maturity=ResearchMaturity.THEORETICAL,
        applicable_layers_dome=[1, 2, 3, 4, 5, 6],
        applicable_capabilities=["legal_navigation", "data_systems"],
        key_papers=[
            "World Models (Ha & Schmidhuber, 2018)",
            "Genie: Generative Interactive Environments (DeepMind, 2024)",
            "Dreamer V3: Mastering Diverse Domains (Hafner et al., 2023)",
        ],
        key_labs=["DeepMind", "UC Berkeley", "Meta FAIR"],
        integration_path=(
            "Build a government system simulator trained on real bureaucratic "
            "timelines, failure modes, and interaction patterns. Feed it case data "
            "from completed domes. The simulator predicts where coordination will "
            "break and what it will cost."
        ),
        dependencies=["Real case data", "Government system APIs"],
        estimated_timeline="18-36 months for useful accuracy",
    ))

    capabilities.append(FrontierCapability(
        name="Urban Digital Twins",
        description=(
            "High-fidelity digital models of physical places that simulate "
            "foot traffic, community dynamics, environmental conditions, "
            "and activation effects over time. Critical for sphere accuracy."
        ),
        category="world_models",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_sphere=[1, 2, 3, 4, 5, 6, 7],
        applicable_capabilities=[
            "spatial_legal", "activation_design", "economics",
        ],
        key_papers=[
            "CityDreamer: Compositional Generative Model of Unbounded 3D Cities (2024)",
            "Urban Computing (Zheng et al., 2014)",
            "Digital Twin Cities: Frameworks and Applications (2023)",
        ],
        key_labs=["MIT Senseable City Lab", "Google Research", "Sidewalk Labs"],
        key_benchmarks=["UrbanBench"],
        integration_path=(
            "For each sphere project, generate a digital twin of the parcel and "
            "surrounding blocks. Simulate activation scenarios: foot traffic patterns, "
            "noise propagation, sightlines, seasonal light, community gathering dynamics. "
            "The twin evolves as the sphere is built."
        ),
        dependencies=["3D city data", "Traffic/pedestrian models", "GIS data"],
        estimated_timeline="12-24 months for basic implementation",
    ))

    capabilities.append(FrontierCapability(
        name="Flourishing Prediction Models",
        description=(
            "ML models that predict flourishing outcomes based on system "
            "coordination levels, resource access, and individual circumstances. "
            "Not a single 'wellness score' but a multi-dimensional model that "
            "tracks stability, health, education, employment, community connection, "
            "and self-determination independently."
        ),
        category="world_models",
        maturity=ResearchMaturity.THEORETICAL,
        applicable_layers_dome=[5, 6, 7, 8],
        applicable_capabilities=["flourishing_design", "data_systems"],
        key_papers=[
            "Measuring Human Flourishing (VanderWeele, 2017)",
            "Causal Inference for Statistics (Imbens & Rubin, 2015)",
        ],
        key_labs=["Harvard Human Flourishing Program", "Stanford SPARQ"],
        integration_path=(
            "Build a multi-dimensional flourishing model trained on dome project "
            "outcomes. Given a person's circumstances and system access, predict "
            "which dimensions of flourishing will improve under coordination and "
            "which are structurally blocked."
        ),
        dependencies=["Longitudinal outcome data from completed domes"],
        estimated_timeline="24-48 months (data-dependent)",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: ROBOTICS & EMBODIED AI
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Drone-Based Site Survey and 3D Mapping",
        description=(
            "Autonomous drones that survey parcels, generate 3D point clouds, "
            "assess structural conditions, map vegetation, and produce "
            "photogrammetric models. Directly replaces manual site assessment "
            "for sphere projects."
        ),
        category="robotics",
        maturity=ResearchMaturity.PRODUCTION,
        applicable_layers_sphere=[1, 2, 3],
        applicable_capabilities=["spatial_legal", "activation_design"],
        key_papers=[
            "NeRF: Representing Scenes as Neural Radiance Fields (2020)",
            "3D Gaussian Splatting for Real-Time Radiance Field Rendering (2023)",
        ],
        key_labs=["DJI", "Skydio", "Pix4D", "NVIDIA"],
        integration_path=(
            "Integrate drone survey data into sphere development stage. "
            "3D models feed directly into activation design. Environmental "
            "assessment data (soil, vegetation, hydrology) feeds the ecology layer."
        ),
        dependencies=["FAA Part 107 certification", "Drone hardware", "Processing pipeline"],
        estimated_timeline="Available now — integration is engineering",
    ))

    capabilities.append(FrontierCapability(
        name="Embodied Agents for Accessibility Assessment",
        description=(
            "Robotic systems that physically traverse spaces to assess "
            "accessibility — wheelchair clearances, sensory environments, "
            "navigation difficulty. Produces quantitative accessibility maps "
            "that inform both dome (housing) and sphere (public space) design."
        ),
        category="robotics",
        maturity=ResearchMaturity.LAB,
        applicable_layers_dome=[6, 7],
        applicable_layers_sphere=[4, 5, 6],
        applicable_capabilities=["flourishing_design", "activation_design"],
        key_papers=[
            "RT-2: Vision-Language-Action Models (Google DeepMind, 2023)",
            "Mobile ALOHA: Learning Bimanual Mobile Manipulation (2024)",
        ],
        key_labs=["Google DeepMind", "Stanford", "CMU Robotics Institute"],
        integration_path=(
            "Deploy accessibility assessment robots in sphere sites during "
            "post-production. Feed data back into the world model to improve "
            "activation design for future spheres."
        ),
        dependencies=["Robot hardware", "Navigation training data"],
        estimated_timeline="24-36 months for useful deployment",
    ))

    capabilities.append(FrontierCapability(
        name="Construction Robotics for Space Activation",
        description=(
            "Robotic systems that assist in physical construction of sphere "
            "activations — soil remediation, planting, modular structure assembly, "
            "sensor installation. Reduces activation cost and increases precision."
        ),
        category="robotics",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_sphere=[4, 5],
        applicable_capabilities=["activation_design"],
        key_papers=[
            "Digital Construction Platform: Autonomous Building Construction (MIT, 2017)",
            "Robotic Fabrication in Architecture (Gramazio & Kohler, 2014)",
        ],
        key_labs=["MIT Media Lab", "ETH Zurich", "Boston Dynamics"],
        integration_path=(
            "During sphere production stage, deploy construction robots for "
            "soil remediation, precision planting, and modular structure placement. "
            "Robot telemetry feeds into the digital twin."
        ),
        dependencies=["Robot fleet", "Site preparation", "Safety protocols"],
        estimated_timeline="18-36 months for pilot deployment",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: SENSING & MEASUREMENT
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Awe Measurement Systems",
        description=(
            "Multi-modal sensing systems that measure awe responses in real time: "
            "facial expression analysis, physiological monitoring (HRV, GSR, "
            "cortisol), behavioral observation (dwell time, gaze patterns, "
            "prosocial behavior), and self-report collection. Validates whether "
            "awe design actually produces awe."
        ),
        category="sensing",
        maturity=ResearchMaturity.LAB,
        applicable_layers_sphere=[5, 6, 7, 8, 9],
        applicable_layers_dome=[7, 8],
        applicable_capabilities=["activation_design", "flourishing_design"],
        key_papers=[
            "The Science of Awe (Keltner & Haidt, 2003)",
            "Awe, the Small Self, and Prosocial Behavior (Piff et al., 2015)",
            "The Awe Experience Scale (Yaden et al., 2019)",
            "Physiological Correlates of Awe (Chirico et al., 2017)",
        ],
        key_labs=[
            "UC Berkeley Greater Good Science Center",
            "University of Pennsylvania Positive Psychology",
            "Università Cattolica del Sacro Cuore",
        ],
        integration_path=(
            "Deploy sensor arrays in sphere installations during post-production. "
            "Collect AWE-S survey data at exit points. Integrate wearable HRV data "
            "from opt-in participants. Feed all data back into the world model "
            "to calibrate awe trigger effectiveness scores."
        ),
        dependencies=["Sensor hardware", "IRB approval", "Privacy protocols"],
        estimated_timeline="12-18 months for pilot measurement",
    ))

    capabilities.append(FrontierCapability(
        name="Environmental Intelligence Sensors",
        description=(
            "IoT sensor networks that continuously monitor sphere environments: "
            "air quality, soil health, noise levels, temperature, light quality, "
            "biodiversity (acoustic ecology). Produces real-time data on how "
            "the activated space actually performs."
        ),
        category="sensing",
        maturity=ResearchMaturity.PRODUCTION,
        applicable_layers_sphere=[3, 4, 5, 6],
        applicable_capabilities=["activation_design", "economics"],
        key_papers=[
            "Array of Things: A Scientific Instrument for the City (Catlett et al., 2017)",
            "Urban Sensing: Progress, Prospects, and Challenges (2020)",
        ],
        key_labs=["Argonne National Lab", "MIT Senseable City Lab"],
        integration_path=(
            "Deploy sensor grids during sphere production. Real-time data feeds "
            "into the digital twin and the place world model. Environmental "
            "quality improvements are quantified and fed into economic models."
        ),
        dependencies=["Sensor hardware", "LoRaWAN/cellular infrastructure", "Data pipeline"],
        estimated_timeline="Available now — commercial IoT platforms exist",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: COMPUTER USE & AUTONOMOUS NAVIGATION
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Autonomous Legal Database Navigation",
        description=(
            "AI agents that navigate government portals, legal databases "
            "(Westlaw, LexisNexis, state benefit systems), and permit systems "
            "autonomously. Can research eligibility, file applications, track "
            "status, and identify conflicts between systems."
        ),
        category="computer_use",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_dome=[1, 2, 3],
        applicable_layers_sphere=[1, 2],
        applicable_capabilities=["legal_navigation", "spatial_legal"],
        key_papers=[
            "Computer Use by Claude (Anthropic, 2024)",
            "WebArena: A Realistic Web Environment for Building Autonomous Agents (2023)",
            "Mind2Web: A Generalist Agent for the Web (2023)",
        ],
        key_labs=["Anthropic", "CMU", "Google DeepMind"],
        key_benchmarks=["WebArena", "Mind2Web", "OSWorld"],
        integration_path=(
            "Deploy computer-use agents to autonomously navigate government "
            "benefit portals, research eligibility criteria, and map application "
            "pathways for dome characters. For spheres, navigate permit databases, "
            "zoning ordinances, and L&I systems."
        ),
        dependencies=["Computer use API", "Portal access credentials", "Compliance review"],
        estimated_timeline="6-12 months for supervised deployment",
    ))

    capabilities.append(FrontierCapability(
        name="Autonomous Permit Filing",
        description=(
            "Computer-use agents that can actually file permit applications, "
            "upload documents, track approval status, and respond to requests "
            "for additional information on government portals."
        ),
        category="computer_use",
        maturity=ResearchMaturity.LAB,
        applicable_layers_dome=[2, 3, 4],
        applicable_layers_sphere=[2, 3, 4],
        applicable_capabilities=["legal_navigation", "spatial_legal"],
        key_papers=[
            "Computer Use by Claude (Anthropic, 2024)",
        ],
        key_labs=["Anthropic"],
        integration_path=(
            "Beyond navigation: agents that can fill out forms, upload documents, "
            "and file applications. Requires careful human-in-the-loop approval "
            "before any filing action."
        ),
        dependencies=[
            "Computer use API", "Human approval workflow",
            "Legal review of agent-filed documents",
        ],
        estimated_timeline="12-24 months (legal/compliance barriers)",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: GENERATIVE AI & CREATIVE
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Architectural Visualization from Briefs",
        description=(
            "Generate photorealistic renderings of dome environments and "
            "sphere activations directly from project briefs. Not concept art — "
            "accurate spatial visualizations that show what the dome/sphere "
            "would actually look like, informed by real site data."
        ),
        category="generative",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_dome=[5, 6, 7],
        applicable_layers_sphere=[3, 4, 5, 6],
        applicable_capabilities=["flourishing_design", "activation_design"],
        key_papers=[
            "Stable Diffusion 3 (Stability AI, 2024)",
            "DALL-E 3 (OpenAI, 2023)",
            "ControlNet (Zhang et al., 2023)",
        ],
        key_labs=["Stability AI", "OpenAI", "Midjourney", "NVIDIA"],
        integration_path=(
            "During pre-production and production, generate visual renderings "
            "of the dome/sphere design. Constrained by real site dimensions, "
            "zoning setbacks, and community character. Used for stakeholder "
            "communication and awe design validation."
        ),
        dependencies=["Image generation API", "Site constraint data", "Style guidelines"],
        estimated_timeline="Available now with human curation",
    ))

    capabilities.append(FrontierCapability(
        name="Documentary Pre-Visualization",
        description=(
            "AI-generated storyboards, shot lists, and narrative structures "
            "for dome/sphere documentaries. Informed by the project brief, "
            "the team's body of work, and the production pipeline."
        ),
        category="generative",
        maturity=ResearchMaturity.PILOT,
        applicable_layers_dome=[4, 5, 6],
        applicable_layers_sphere=[4, 5, 6],
        applicable_capabilities=["narrative"],
        key_papers=[
            "Sora: Creating video from text (OpenAI, 2024)",
            "VideoPoet: A Large Language Model for Video Generation (Google, 2024)",
        ],
        key_labs=["OpenAI", "Google DeepMind", "Runway"],
        integration_path=(
            "Generate pre-visualization sequences for the dome/sphere documentary "
            "based on the narrative framework. Show the principal and team what the "
            "story could look like before cameras roll."
        ),
        dependencies=["Video generation API", "Narrative framework"],
        estimated_timeline="12-18 months for useful quality",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: FINANCIAL AI
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Coordination Bond Structuring",
        description=(
            "AI systems that structure financial instruments from dome/sphere "
            "data — coordination bonds that convert fragmentation savings to "
            "returns, community investment vehicles, social impact bonds with "
            "real outcome metrics. Not templates — live financial models."
        ),
        category="financial_ai",
        maturity=ResearchMaturity.THEORETICAL,
        applicable_layers_dome=[3, 4, 5, 10],
        applicable_layers_sphere=[3, 4, 5, 8],
        applicable_capabilities=["data_systems", "economics"],
        key_papers=[
            "FinGPT: Open-Source Financial Large Language Models (2023)",
            "BloombergGPT: A Large Language Model for Finance (2023)",
        ],
        key_labs=["Bloomberg", "JPMorgan AI Research", "Ant Group"],
        integration_path=(
            "During production stage, generate actual bond structures and "
            "investment models from the dome/sphere's cost data. The financial "
            "instrument is a production deliverable, not a concept."
        ),
        dependencies=["Financial modeling framework", "Regulatory compliance", "Actuarial data"],
        estimated_timeline="24-36 months (regulatory barriers)",
    ))

    # ═══════════════════════════════════════════════════════════════
    # CATEGORY: SCIENCE FICTION ADJACENT (IN THE REALM OF CAPABILITY)
    # ═══════════════════════════════════════════════════════════════

    capabilities.append(FrontierCapability(
        name="Whole-Person Digital Companion",
        description=(
            "A persistent AI companion that understands a dome resident's "
            "complete situation — every system they interact with, every "
            "deadline, every entitlement, every appointment — and proactively "
            "coordinates on their behalf. Not a chatbot. A navigator that "
            "never forgets, never misses a deadline, and sees all systems "
            "simultaneously."
        ),
        category="frontier_systems",
        maturity=ResearchMaturity.FRONTIER,
        applicable_layers_dome=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        applicable_capabilities=[
            "legal_navigation", "data_systems", "flourishing_design",
        ],
        key_papers=[
            "Personal LLM Agents (Stanford HAI, 2024)",
            "Constitutional AI (Anthropic, 2022)",
        ],
        key_labs=["Anthropic", "Stanford HAI", "Google DeepMind"],
        integration_path=(
            "The ultimate dome capability: a digital companion that acts as "
            "the permanent coordination layer between all systems. It doesn't "
            "replace human navigators — it ensures that no entitlement is "
            "missed, no deadline passes, no system drops a person."
        ),
        dependencies=[
            "Government API access", "Privacy/consent framework",
            "Long-context memory", "Constitutional AI safety",
        ],
        estimated_timeline="36-60 months (technical + political barriers)",
    ))

    capabilities.append(FrontierCapability(
        name="Neighborhood-Scale Collective Intelligence",
        description=(
            "A system where every activated sphere in a neighborhood forms "
            "a network — sharing environmental data, community patterns, "
            "economic effects, and activation learnings in real time. The "
            "neighborhood itself becomes intelligent. Adjacent spheres "
            "coordinate their programming. The network predicts which "
            "vacant lot to activate next for maximum catalyst effect."
        ),
        category="frontier_systems",
        maturity=ResearchMaturity.FRONTIER,
        applicable_layers_sphere=[6, 7, 8, 9, 10],
        applicable_capabilities=["activation_design", "economics"],
        key_papers=[
            "Collective Intelligence (Woolley et al., 2010)",
            "Smart Cities: Foundations, Principles, and Applications (2017)",
        ],
        key_labs=["MIT Media Lab", "Santa Fe Institute"],
        integration_path=(
            "As multiple spheres are activated in a corridor, link their "
            "sensor networks, programming calendars, and economic data. "
            "The collective intelligence of the network recommends optimal "
            "activation sequences, programming synergies, and resource sharing."
        ),
        dependencies=["Multiple activated spheres", "Sensor networks", "City data APIs"],
        estimated_timeline="48-72 months (requires sphere portfolio)",
    ))

    capabilities.append(FrontierCapability(
        name="Awe Engineering at Scale",
        description=(
            "Moving beyond individual awe triggers to designing entire "
            "corridors and neighborhoods for sustained, daily awe. Using "
            "accumulated data from sphere awe measurements to engineer "
            "urban environments where awe is not occasional but ambient — "
            "a persistent low-level sense that your neighborhood was "
            "designed for your transcendence."
        ),
        category="frontier_systems",
        maturity=ResearchMaturity.FRONTIER,
        applicable_layers_sphere=[7, 8, 9, 10],
        applicable_capabilities=["activation_design"],
        key_papers=[
            "Awe: The Transformative Power of Everyday Wonder (Keltner, 2023)",
            "The Overview Effect (White, 2014)",
            "Biophilic Design: The Theory, Science and Practice (Kellert, 2008)",
        ],
        key_labs=["UC Berkeley GGSC", "Harvard Design School"],
        integration_path=(
            "Use accumulated awe measurement data from the sphere portfolio "
            "to move from trigger-by-trigger design to environmental awe "
            "engineering. The design vocabulary expands from 'install an awe "
            "trigger here' to 'this entire corridor produces ambient awe.'"
        ),
        dependencies=["Large sphere portfolio", "Longitudinal awe data", "Urban planning authority"],
        estimated_timeline="60+ months (requires portfolio + political will)",
    ))

    capabilities.append(FrontierCapability(
        name="Interspecies Intelligence Integration",
        description=(
            "Incorporating non-human intelligence into sphere design — "
            "pollinator behavior patterns, bird migration routes, mycorrhizal "
            "network activity, soil microbiome health — as design inputs, "
            "not afterthoughts. The sphere doesn't just accommodate ecology. "
            "It listens to it."
        ),
        category="frontier_systems",
        maturity=ResearchMaturity.THEORETICAL,
        applicable_layers_sphere=[5, 6, 7],
        applicable_capabilities=["activation_design"],
        key_papers=[
            "The Hidden Life of Trees (Wohlleben, 2015)",
            "Bioacoustics for Ecosystem Monitoring (Sueur & Farina, 2015)",
            "Machine Learning for Ecological Monitoring (2023)",
        ],
        key_labs=["Cornell Lab of Ornithology", "ETH Zurich Plant Science"],
        integration_path=(
            "Deploy acoustic ecology sensors in sphere sites. Use ML to identify "
            "species, track biodiversity changes, and correlate with activation "
            "design choices. Feed ecological intelligence into the place world model."
        ),
        dependencies=["Bioacoustic sensors", "Species classification models", "Ecological baseline data"],
        estimated_timeline="18-24 months for basic biodiversity monitoring",
    ))

    # ── Convergence Zones ───────────────────────────────────────

    convergence_zones = [
        {
            "name": "The Autonomous Navigator",
            "converging_capabilities": [
                "Autonomous Legal Database Navigation",
                "Whole-Person Digital Companion",
                "Multi-Agent Task Decomposition",
                "Government System Simulation",
            ],
            "description": (
                "Computer use + multi-agent systems + government world models "
                "are converging toward an autonomous navigator that can "
                "actually DO the coordination work that domes describe. "
                "Not 'here's what you should file' but 'I've filed it, "
                "here's the confirmation, and the next deadline is March 15.'"
            ),
            "estimated_convergence": "2027-2028",
            "baths_impact": "Transforms domes from design documents to live coordination systems",
        },
        {
            "name": "The Living Sphere",
            "converging_capabilities": [
                "Urban Digital Twins",
                "Environmental Intelligence Sensors",
                "Awe Measurement Systems",
                "Neighborhood-Scale Collective Intelligence",
            ],
            "description": (
                "Digital twins + IoT sensors + awe measurement are converging "
                "toward spheres that are genuinely alive — responsive environments "
                "that adapt their programming, adjust their awe triggers, and "
                "optimize their community impact based on real-time data."
            ),
            "estimated_convergence": "2028-2030",
            "baths_impact": "Spheres become self-optimizing community infrastructure",
        },
        {
            "name": "The IP Factory",
            "converging_capabilities": [
                "Multi-Agent Task Decomposition",
                "Coordination Bond Structuring",
                "Architectural Visualization from Briefs",
                "Documentary Pre-Visualization",
            ],
            "description": (
                "Multi-agent production + generative AI + financial AI are "
                "converging toward productions that generate real IP at every "
                "stage — actual policy briefs, actual financial instruments, "
                "actual visualizations, actual documentaries. The production "
                "pipeline becomes a genuine IP factory."
            ),
            "estimated_convergence": "2026-2027",
            "baths_impact": "Productions generate investable IP, not just design documents",
        },
    ]

    # ── Paradigm Shifts ─────────────────────────────────────────

    paradigm_shifts = [
        (
            "FROM simulation TO execution: The BATHS production pipeline moves "
            "from simulating what practitioners would produce to actually producing "
            "it. AI agents don't describe a legal landscape map — they build one."
        ),
        (
            "FROM individual TO collective intelligence: As the sphere portfolio "
            "grows, the intelligence of each sphere is not individual but collective. "
            "Every new sphere starts with the knowledge of all prior spheres."
        ),
        (
            "FROM designed awe TO engineered awe: Awe moves from a design aspiration "
            "to an engineered outcome with measurement, feedback, and optimization. "
            "Awe becomes a public health intervention with evidence."
        ),
        (
            "FROM coordination as concept TO coordination as infrastructure: "
            "Government system coordination moves from something domes propose "
            "to something domes build — persistent digital infrastructure that "
            "coordinates on behalf of residents."
        ),
        (
            "FROM human-centered design TO human-centered systems: The dome "
            "doesn't just design FOR a person — it operates FOR them. The system "
            "is the dome. The dome is alive."
        ),
    ]

    return ResearchFrontier(
        capabilities=capabilities,
        convergence_zones=convergence_zones,
        paradigm_shifts=paradigm_shifts,
    )


class FrontierTracker:
    """
    Maintains and queries the frontier research map.
    Used by the researcher agent and by production pipelines
    to understand what capabilities are available or emerging.
    """

    def __init__(self):
        self.frontier = build_initial_frontier()

    def get_capabilities_for_layer(
        self,
        game_type: str,
        layer: int,
    ) -> List[FrontierCapability]:
        """Get all tracked capabilities relevant to a specific layer."""
        results = []
        for cap in self.frontier.capabilities:
            if game_type == "domes" and layer in cap.applicable_layers_dome:
                results.append(cap)
            elif game_type == "spheres" and layer in cap.applicable_layers_sphere:
                results.append(cap)
        return results

    def get_capabilities_for_production(
        self,
        capability: str,
    ) -> List[FrontierCapability]:
        """Get frontier capabilities relevant to a production capability."""
        return [
            cap for cap in self.frontier.capabilities
            if capability in cap.applicable_capabilities
        ]

    def get_production_ready(self) -> List[FrontierCapability]:
        """Get capabilities that are ready for integration now."""
        return [
            cap for cap in self.frontier.capabilities
            if cap.maturity in (ResearchMaturity.PRODUCTION, ResearchMaturity.PILOT)
        ]

    def get_by_category(self, category: str) -> List[FrontierCapability]:
        """Get all capabilities in a research category."""
        return [
            cap for cap in self.frontier.capabilities
            if cap.category == category
        ]

    def get_convergence_zones(self) -> List[Dict]:
        """Get active convergence zones."""
        return self.frontier.convergence_zones

    def get_maturity_summary(self) -> Dict[str, int]:
        """Count capabilities by maturity level."""
        summary = {}
        for cap in self.frontier.capabilities:
            level = cap.maturity.value
            summary[level] = summary.get(level, 0) + 1
        return summary

    def update_capability_maturity(
        self,
        capability_name: str,
        new_maturity: ResearchMaturity,
        note: str = "",
    ) -> bool:
        """
        Update a capability's maturity level.
        Called by the researcher agent when the field advances.
        """
        for cap in self.frontier.capabilities:
            if cap.name == capability_name:
                cap.maturity_history.append({
                    "date": datetime.utcnow().isoformat(),
                    "from": cap.maturity.value,
                    "to": new_maturity.value,
                    "note": note,
                })
                cap.maturity = new_maturity
                cap.last_reviewed = datetime.utcnow()
                return True
        return False

    def add_capability(self, capability: FrontierCapability) -> None:
        """Add a newly discovered capability to the frontier map."""
        self.frontier.capabilities.append(capability)
        self.frontier.last_updated = datetime.utcnow()

    def intelligence_brief(self) -> Dict:
        """
        Produce a concise intelligence brief on the current state of
        the frontier, suitable for principals and practitioners.
        """
        maturity = self.get_maturity_summary()
        production_ready = self.get_production_ready()

        return {
            "total_capabilities_tracked": len(self.frontier.capabilities),
            "maturity_breakdown": maturity,
            "production_ready_count": len(production_ready),
            "production_ready": [
                {
                    "name": c.name,
                    "category": c.category,
                    "maturity": c.maturity.value,
                    "integration_path": c.integration_path,
                }
                for c in production_ready
            ],
            "convergence_zones": len(self.frontier.convergence_zones),
            "paradigm_shifts": len(self.frontier.paradigm_shifts),
            "categories": list(set(c.category for c in self.frontier.capabilities)),
            "last_updated": self.frontier.last_updated.isoformat(),
        }
