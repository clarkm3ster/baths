"""
Chron Talent Agent — Production Engine
When a team plays a game, this is what happens at each stage.
Every stage generates deliverables, IP, scores, and a narrative.

The team's actual composition determines what gets produced.
Each practitioner pulls from their real body of work.
Patricia Hawkins-Morrow's legal landscape map comes from
The Architecture of Rights and 23 landmark cases.
Dr. Kenji Nakamura's systems model extends his Fragmentation Index.
Different teams on the same project produce genuinely different outputs
because they're bringing different prior work to the table.

Subsequent teams see what was already built and decide to use or diverge.
"""

from typing import List, Dict, Optional, Tuple
from models import (
    TalentProfile, Principal, ProjectBrief, TeamRecommendation,
    ResonanceMatch, IPItem, IPDomain, GameType, ProductionStage,
    WorkItem,
)
from datetime import datetime
import uuid


# ── Stage definitions ────────────────────────────────────────────

DOMES_STAGES = {
    ProductionStage.DEVELOPMENT: {
        "name": "Development",
        "focus": "Map the legal landscape. Discover every entitlement. Model every system.",
        "capability_prompts": {
            "legal_navigation": {
                "title": "Legal Landscape Map",
                "ip_domain": "policy",
                "verb": "maps",
                "target": "all legal entitlements, eligibility criteria, and application pathways for {character}",
            },
            "data_systems": {
                "title": "Systems Fragmentation Model",
                "ip_domain": "technology",
                "verb": "models",
                "target": "how {system_count} government systems interact (or fail to) around {character}'s specific situation",
            },
            "narrative": {
                "title": "Character Documentary Treatment",
                "ip_domain": "entertainment",
                "verb": "captures",
                "target": "{character}'s full landscape — not just their problems, but their intelligence, joy, and agency",
            },
            "flourishing_design": {
                "title": "Flourishing Dimensions Analysis",
                "ip_domain": "research",
                "verb": "assesses",
                "target": "{character}'s {dimension_count} flourishing dimensions against current system coverage",
            },
        },
    },
    ProductionStage.PRE_PRODUCTION: {
        "name": "Pre-Production",
        "focus": "Design the dome. Blueprint the coordination. Model the costs.",
        "capability_prompts": {
            "legal_navigation": {
                "title": "Entitlement Coordination Blueprint",
                "ip_domain": "policy",
                "verb": "blueprints",
                "target": "a coordination plan linking {system_count} systems into a single pathway for {character}",
            },
            "data_systems": {
                "title": "Cost-of-Fragmentation Model",
                "ip_domain": "financial_product",
                "verb": "models",
                "target": "the cost of non-coordination vs. coordination for {character}'s specific case",
            },
            "narrative": {
                "title": "Production Narrative Framework",
                "ip_domain": "entertainment",
                "verb": "architects",
                "target": "how {character}'s story gets told through the production",
            },
            "flourishing_design": {
                "title": "Dome Architecture Concept",
                "ip_domain": "architectural",
                "verb": "designs",
                "target": "the spatial and conceptual environment for {character}'s complete flourishing",
            },
        },
    },
    ProductionStage.PRODUCTION: {
        "name": "Production",
        "focus": "Build the dome. Every discipline produces. The IP starts flowing.",
        "capability_prompts": {
            "legal_navigation": {
                "title": "Policy Brief",
                "ip_domain": "policy",
                "verb": "produces",
                "target": "an actionable policy brief: how to replicate {character}'s dome coordination model at municipal scale",
            },
            "data_systems": {
                "title": "Coordination Bond Structure",
                "ip_domain": "financial_product",
                "verb": "structures",
                "target": "a financial instrument that makes {character}'s dome investable — coordination savings converted to returns",
            },
            "narrative": {
                "title": "Documentary First Cut",
                "ip_domain": "entertainment",
                "verb": "produces",
                "target": "the first cut of the dome documentary — {character}'s journey through the production pipeline",
            },
            "flourishing_design": {
                "title": "Flourishing Design Package",
                "ip_domain": "housing",
                "verb": "delivers",
                "target": "the complete design package for {character}'s dome — every system, every transition, every threshold",
            },
        },
    },
    ProductionStage.POST_PRODUCTION: {
        "name": "Post-Production",
        "focus": "Stress-test the dome. Integrate the deliverables. Refine the IP.",
        "capability_prompts": {
            "legal_navigation": {
                "title": "Stress Test: Legal Pathways",
                "ip_domain": "policy",
                "verb": "stress-tests",
                "target": "every legal pathway in {character}'s dome against real bureaucratic conditions",
            },
            "data_systems": {
                "title": "Dome Digital Twin",
                "ip_domain": "technology",
                "verb": "builds",
                "target": "an interactive simulation of {character}'s dome — 10-year trajectory modeling under different coordination scenarios",
            },
            "narrative": {
                "title": "Documentary Final Cut",
                "ip_domain": "entertainment",
                "verb": "completes",
                "target": "the final documentary: {character}'s dome production from sourcing through completion",
            },
            "flourishing_design": {
                "title": "Flourishing Impact Assessment",
                "ip_domain": "research",
                "verb": "quantifies",
                "target": "how {character}'s dome scores across all {dimension_count} flourishing dimensions",
            },
        },
    },
    ProductionStage.DISTRIBUTION: {
        "name": "Distribution",
        "focus": "Publish to domes.cc. The IP enters the portfolio. The Cosm scores are final.",
        "capability_prompts": {
            "legal_navigation": {
                "title": "Published Policy Portfolio",
                "ip_domain": "policy",
                "verb": "publishes",
                "target": "all policy deliverables from {character}'s dome indexed on domes.cc",
            },
            "data_systems": {
                "title": "Open-Source Coordination Model",
                "ip_domain": "technology",
                "verb": "releases",
                "target": "the dome's coordination model as open-source infrastructure on domes.cc",
            },
            "narrative": {
                "title": "Dome Premiere Package",
                "ip_domain": "entertainment",
                "verb": "packages",
                "target": "the complete documentary, narrative assets, and media kit for {character}'s dome premiere",
            },
            "flourishing_design": {
                "title": "Dome Portfolio Entry",
                "ip_domain": "research",
                "verb": "publishes",
                "target": "the full portfolio entry on domes.cc — the dome as a replicable model",
            },
        },
    },
}

SPHERES_STAGES = {
    ProductionStage.DEVELOPMENT: {
        "name": "Development",
        "focus": "Read the parcel. Map the community. Understand the constraints. Identify awe potential.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Parcel Legal Analysis",
                "ip_domain": "policy",
                "verb": "maps",
                "target": "complete zoning, permit, and regulatory analysis for {address}",
            },
            "activation_design": {
                "title": "Site Awe Assessment",
                "ip_domain": "urban_design",
                "verb": "assesses",
                "target": "the awe potential of {address} — which of Keltner's 8 awe elicitors this site can deploy and why",
            },
            "economics": {
                "title": "Activation Economics Baseline",
                "ip_domain": "financial_product",
                "verb": "models",
                "target": "the parcel's current cost to the city vs. projected value under activation at {address}",
            },
            "narrative": {
                "title": "Community Story Archive",
                "ip_domain": "entertainment",
                "verb": "documents",
                "target": "oral histories and community narratives connected to {address} and {neighborhood}",
            },
        },
    },
    ProductionStage.PRE_PRODUCTION: {
        "name": "Pre-Production",
        "focus": "Design the activation. Deploy awe triggers. Model the economics. Plan the experience.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Permit Pathway Map",
                "ip_domain": "policy",
                "verb": "maps",
                "target": "the permit and regulatory pathway for activating {address}",
            },
            "activation_design": {
                "title": "Awe Design Framework",
                "ip_domain": "architectural",
                "verb": "designs",
                "target": "the full awe-designed concept for the sphere at {address} — every elicitor mapped to specific design elements with site rationale",
            },
            "economics": {
                "title": "Community Benefit Model",
                "ip_domain": "financial_product",
                "verb": "models",
                "target": "community benefit of activation at {address} — jobs, foot traffic, property effects, social value",
            },
            "narrative": {
                "title": "Activation Narrative Plan",
                "ip_domain": "entertainment",
                "verb": "plans",
                "target": "how the sphere at {address} tells {neighborhood}'s story",
            },
        },
    },
    ProductionStage.PRODUCTION: {
        "name": "Production",
        "focus": "Activate the space. Deploy awe triggers. Every discipline produces. The parcel comes alive.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Activation Implementation Plan",
                "ip_domain": "real_estate",
                "verb": "implements",
                "target": "the construction and implementation plan for the sphere at {address}",
            },
            "activation_design": {
                "title": "Awe Activation Program",
                "ip_domain": "performance",
                "verb": "programs",
                "target": "every awe-designed experience at {address} — triggers deployed, visitor journey, measurement protocol",
            },
            "economics": {
                "title": "Sphere Investment Instrument",
                "ip_domain": "financial_product",
                "verb": "structures",
                "target": "the financial instrument making the sphere at {address} investable",
            },
            "narrative": {
                "title": "Production Documentary",
                "ip_domain": "entertainment",
                "verb": "captures",
                "target": "the activation of {address} — from vacant lot to living sphere",
            },
        },
    },
    ProductionStage.POST_PRODUCTION: {
        "name": "Post-Production",
        "focus": "Measure awe outcomes. Document the impact. Validate the design. Refine the model.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Regulatory Lessons Learned",
                "ip_domain": "policy",
                "verb": "documents",
                "target": "what the permit process revealed about activating space at {address}",
            },
            "activation_design": {
                "title": "Awe Impact Assessment",
                "ip_domain": "urban_design",
                "verb": "measures",
                "target": "awe outcomes at {address} — AWE-S scores, prosocial behavior, time expansion, belonging, physiological markers",
            },
            "economics": {
                "title": "Economic Impact Report",
                "ip_domain": "research",
                "verb": "reports",
                "target": "actual vs. projected returns from the sphere at {address}",
            },
            "narrative": {
                "title": "Sphere Documentary Final",
                "ip_domain": "entertainment",
                "verb": "completes",
                "target": "the full story of {address} from dormant parcel to activated sphere",
            },
        },
    },
    ProductionStage.DISTRIBUTION: {
        "name": "Distribution",
        "focus": "Publish to spheres.land. The activation model enters the portfolio.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Published Activation Template",
                "ip_domain": "policy",
                "verb": "publishes",
                "target": "the replicable activation template from {address} on spheres.land",
            },
            "activation_design": {
                "title": "Sphere Awe Portfolio Entry",
                "ip_domain": "architectural",
                "verb": "publishes",
                "target": "the full awe-designed portfolio entry on spheres.land — replicable awe triggers, validated metrics, design guidance",
            },
            "economics": {
                "title": "Open Investment Model",
                "ip_domain": "financial_product",
                "verb": "releases",
                "target": "the sphere's financial model as open template for community investment on spheres.land",
            },
            "narrative": {
                "title": "Sphere Premiere Package",
                "ip_domain": "entertainment",
                "verb": "packages",
                "target": "complete media for the {neighborhood} sphere premiere",
            },
        },
    },
}


# ── Unlikely collision templates ─────────────────────────────────

UNLIKELY_TEMPLATES = {
    "fashion": ("fashion", "Adaptive {game} Garment Line"),
    "food": ("culinary", "{game} Nourishment Protocol"),
    "sound": ("performance", "Sonic Environment Design"),
    "scent": ("product", "Olfactory Environment Protocol"),
    "movement": ("performance", "Movement Autonomy Program"),
    "blacksmith": ("product", "Permanent Making Installation"),
    "midwife": ("research", "Transition Support Framework"),
    "graffiti": ("performance", "Public Voice Installation"),
    "mural": ("performance", "Community Documentation Mural"),
    "prosthetics": ("product", "Affordable Access Design"),
    "game": ("technology", "Friction Audit Report"),
    "perfume": ("product", "Sensory Safety Protocol"),
    "graphic-novel": ("entertainment", "Visual Systems Narrative"),
    "choreography": ("performance", "Embodied Experience Design"),
    "dance": ("performance", "Embodied Experience Design"),
}


# ── Template formatting ──────────────────────────────────────────

def _fill(template: str, project: ProjectBrief) -> str:
    """Fill {variables} from project brief."""
    r = {}
    if project.game_type == GameType.DOMES and project.character:
        c = project.character
        r = {
            "character": c.name,
            "system_count": str(len(c.key_systems)),
            "dimension_count": str(len(c.flourishing_dimensions)),
            "game": "dome", "concept": "human flourishing",
            "context": c.situation[:80],
        }
    elif project.game_type == GameType.SPHERES and project.parcel:
        p = project.parcel
        r = {
            "address": p.address, "neighborhood": p.neighborhood,
            "city": p.city, "lot_size": str(p.lot_size_sqft),
            "game": "sphere", "concept": "space activation",
            "context": f"{p.address}, {p.neighborhood}",
        }
    result = template
    for k, v in r.items():
        result = result.replace("{" + k + "}", v)
    return result


# ── Simulated production output ──────────────────────────────────
# This is the core simulation engine. Simulated versions of each
# practitioner play the games, pulling from their actual body of work
# and applying it to the specific project brief. The output is what
# their dome or sphere WOULD look like.

def _pick(items: list, seed_str: str, count: int = 2) -> list:
    """Deterministic selection from a list based on a seed string."""
    import hashlib
    h = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    if not items:
        return []
    picked = []
    for i in range(min(count, len(items))):
        idx = (h + i * 7) % len(items)
        if items[idx] not in picked:
            picked.append(items[idx])
    return picked


def _select_relevant_work(talent: TalentProfile, project: ProjectBrief, cap: str) -> List[WorkItem]:
    """Find the most relevant pieces from a talent's body of work."""
    if not talent.body_of_work:
        return []

    keywords = set()
    if project.game_type == GameType.DOMES and project.character:
        c = project.character
        for sys in c.key_systems:
            keywords.update(w.lower() for w in sys.split() if len(w) > 3)
        for dim in c.flourishing_dimensions:
            keywords.add(dim.lower())
        keywords.update(w.lower() for w in c.production_challenge.split() if len(w) > 4)
    elif project.game_type == GameType.SPHERES and project.parcel:
        p = project.parcel
        keywords.update(w.lower() for w in p.opportunity.split() if len(w) > 4)
        keywords.update(w.lower() for w in p.community_context.split() if len(w) > 4)

    cap_terms = cap.replace("_", " ").split()
    keywords.update(t.lower() for t in cap_terms)

    scored = []
    for work in talent.body_of_work:
        text = f"{work.title} {work.description}".lower()
        hits = sum(1 for kw in keywords if kw in text)
        scored.append((hits, work))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [w for _, w in scored[:2]]


def _simulate_dome_finding(
    talent: TalentProfile,
    project: ProjectBrief,
    cap: str,
    stage: ProductionStage,
    relevant_work: List[WorkItem],
) -> str:
    """
    Simulate what this practitioner would actually find/produce
    at THIS stage when applying their body of work to this character.
    The dome gets more concrete at each stage — from discovery through
    publication. The practitioner's work evolves through the pipeline.
    """
    char = project.character
    seed = f"{talent.talent_id}:{project.project_id}:{cap}:{stage.value}"
    name = talent.name
    work_anchor = relevant_work[0].title if relevant_work else "their practice"
    work_second = relevant_work[1].title if len(relevant_work) > 1 else None

    focus_systems = _pick(char.key_systems, seed, 3)
    focus_dims = _pick(char.flourishing_dimensions, seed, 2)
    sys0 = focus_systems[0] if focus_systems else "the primary system"
    sys1 = focus_systems[1] if len(focus_systems) > 1 else "adjacent systems"
    sys_list = ", ".join(focus_systems)
    dim0 = focus_dims[0] if focus_dims else "flourishing"
    dim1 = focus_dims[1] if len(focus_dims) > 1 else "stability"
    dim_list = " and ".join(focus_dims)
    all_dims = ", ".join(char.flourishing_dimensions)
    n_sys = len(char.key_systems)
    approach = talent.approach.split('.')[0].strip() if talent.approach else ""
    work_and_second = f' and "{work_second}"' if work_second else ""

    S = stage
    D = ProductionStage.DEVELOPMENT
    PP = ProductionStage.PRE_PRODUCTION
    P = ProductionStage.PRODUCTION
    PO = ProductionStage.POST_PRODUCTION
    DI = ProductionStage.DISTRIBUTION

    # ── legal_navigation ────────────────────────────────────
    if cap == "legal_navigation":
        if S == D:
            return (
                f"Applying \"{work_anchor}\" to {char.name}'s case, {name} identifies "
                f"that {char.name} intersects with {n_sys} systems simultaneously — "
                f"focusing first on {sys_list}. The gap analysis reveals that eligibility "
                f"exists on paper across all systems, but application timelines conflict "
                f"and documentation requirements between {sys0} and {sys1} duplicate effort "
                f"without sharing data. {approach}. The map exposes {n_sys} specific "
                f"coordination failures that, if resolved, would unlock {dim_list} simultaneously."
            )
        if S == PP:
            return (
                f"From the landscape map, {name} now blueprints the coordination: a "
                f"step-by-step pathway linking {sys0}, {sys1}, and {n_sys - 2} other systems "
                f"into a single application sequence for {char.name}. Extending \"{work_anchor}\", "
                f"the blueprint identifies which applications must file first, which deadlines "
                f"gate others, and where a single navigator could collapse {n_sys} separate "
                f"timelines into one. {approach}. The blueprint converts legal entitlements into "
                f"an operational choreography — {char.name} should never have to explain their "
                f"situation twice."
            )
        if S == P:
            return (
                f"The blueprint becomes policy. {name} produces an actionable brief showing "
                f"how {char.name}'s dome coordination model — {n_sys} systems linked through "
                f"a single navigator pathway — can replicate at municipal scale. Drawing on "
                f"\"{work_anchor}\"{work_and_second}, "
                f"the brief demonstrates that the coordination savings from {sys0} and {sys1} "
                f"alone would fund navigator positions for the next 50 cases. {approach}. "
                f"This is policy produced from inside a production, not a think tank."
            )
        if S == PO:
            return (
                f"{name} stress-tests every legal pathway in {char.name}'s dome against real "
                f"bureaucratic conditions. The {sys0} pathway holds under normal timelines but "
                f"breaks when recertification windows shift. The {sys1} pathway requires physical "
                f"presence at offices with conflicting hours. Using \"{work_anchor}\", {name} "
                f"identifies which pathways are structurally sound and which depend on individual "
                f"caseworker discretion — the difference between a right and a favor. {approach}."
            )
        # Distribution
        return (
            f"All policy deliverables from {char.name}'s dome — the landscape map, the "
            f"coordination blueprint, the municipal policy brief, the stress test results — "
            f"are published and indexed on domes.cc. {name}'s methodology from \"{work_anchor}\" "
            f"is now a replicable template: any navigator facing a {n_sys}-system coordination "
            f"challenge can start from this dome's legal architecture rather than zero. {approach}."
        )

    # ── data_systems ────────────────────────────────────────
    if cap == "data_systems":
        if S == D:
            return (
                f"Extending \"{work_anchor}\" to {char.name}'s situation, {name} models "
                f"the cascade: a single failure in {sys0} propagates through {sys_list}, "
                f"compounding costs at each handoff. The model quantifies the fragmentation "
                f"tax — the hours, the duplicate applications, the missed deadlines that "
                f"aren't bugs but features of systems designed to operate in isolation. "
                f"{approach}. The simulation shows that coordinating just {len(focus_systems)} "
                f"of {n_sys} systems would reduce the administrative burden on {char.name} "
                f"by the equivalent of a part-time job."
            )
        if S == PP:
            return (
                f"From the fragmentation model, {name} builds the cost comparison: what "
                f"{char.name}'s case costs under current fragmentation vs. what it would "
                f"cost under coordination. Extending \"{work_anchor}\", the model shows "
                f"that {sys0} and {sys1} alone generate duplicate administrative costs — "
                f"the same information collected twice, stored in incompatible formats, "
                f"verified by different standards. {approach}. The cost-of-fragmentation "
                f"model makes the invisible tax visible: {char.name} is paying for government's "
                f"failure to coordinate, in hours that could go toward {dim0}."
            )
        if S == P:
            return (
                f"The cost model becomes a financial instrument. {name} structures a "
                f"coordination bond: the savings from linking {n_sys} systems — reduced "
                f"duplicate processing, fewer missed appointments, lower emergency costs — "
                f"are quantified and converted into investable returns. Using "
                f"\"{work_anchor}\"{work_and_second}, "
                f"the bond structure shows that coordination pays for itself within 18 months "
                f"for cases like {char.name}'s. {approach}. This is a financial product "
                f"produced from inside a dome, not a spreadsheet."
            )
        if S == PO:
            return (
                f"{name} builds the digital twin: an interactive simulation of {char.name}'s "
                f"dome under different coordination scenarios over 10 years. What happens if "
                f"{sys0} coordination holds but {sys1} lapses? What if a policy change disrupts "
                f"the navigator pathway? Using \"{work_anchor}\", the simulation models "
                f"{n_sys} systems across 4 policy scenarios, showing which configurations "
                f"produce sustained {dim0} and which create new fragmentation. {approach}."
            )
        return (
            f"The dome's coordination model — {n_sys} systems, the fragmentation index, "
            f"the cost comparison, the bond structure, the 10-year simulation — is released "
            f"as open-source infrastructure on domes.cc. {name}'s methodology from "
            f"\"{work_anchor}\" is now a public tool: any city can model their own "
            f"fragmentation tax and build a coordination bond from the savings. {approach}."
        )

    # ── narrative ───────────────────────────────────────────
    if cap == "narrative":
        if S == D:
            return (
                f"Drawing on \"{work_anchor}\", {name} builds the documentary treatment "
                f"around {char.name}'s full landscape: {char.full_landscape[:120]}. "
                f"The treatment refuses to flatten {char.name} into a case study. {approach}. "
                f"The narrative structure mirrors the fragmentation — the audience experiences "
                f"the same disorientation of navigating {n_sys} disconnected systems, then "
                f"the relief when coordination begins to work."
            )
        if S == PP:
            return (
                f"From the treatment, {name} architects the production narrative: how "
                f"{char.name}'s story moves through the dome pipeline. Drawing on "
                f"\"{work_anchor}\", the framework structures the dome not as a rescue story "
                f"but as an engineering problem — {n_sys} systems that should work together "
                f"and don't, and what it takes to make them. {approach}. The narrative "
                f"architecture gives equal weight to {char.name}'s intelligence, humor, and "
                f"agency as it does to the systems that constrain them."
            )
        if S == P:
            return (
                f"The first cut. {name} produces the documentary capturing {char.name}'s "
                f"journey through the dome production. Using \"{work_anchor}\""
                f"{work_and_second}, the film positions "
                f"the camera where {char.name} stands — inside the systems, not above them. "
                f"The audience watches {sys0} and {sys1} from the applicant's chair. {approach}. "
                f"The first cut runs 47 minutes. The coordination sequence — when {n_sys} "
                f"systems finally link — is the structural climax."
            )
        if S == PO:
            return (
                f"Final cut. {name} refines the documentary from first cut through three "
                f"rounds of editing, using \"{work_anchor}\" as the aesthetic standard. The "
                f"final version runs 38 minutes. Every frame earns its place. {char.name}'s "
                f"dome production — from mapping through coordination through the systems "
                f"finally working — is documented with the rigor of evidence and the care "
                f"of portraiture. {approach}."
            )
        return (
            f"The complete documentary, narrative assets, and media kit for {char.name}'s "
            f"dome premiere are packaged for distribution. {name}'s film — produced through "
            f"\"{work_anchor}\" — becomes the portfolio's primary narrative vehicle. The "
            f"dome is not explained. It is shown. Audiences see what {n_sys} systems look "
            f"like when they work, and what {dim0} looks like when it's real. {approach}."
        )

    # ── flourishing_design ──────────────────────────────────
    if cap == "flourishing_design":
        if S == D:
            return (
                f"Using \"{work_anchor}\" as foundation, {name} maps {char.name}'s "
                f"specific flourishing dimensions: {all_dims}. Starting with {dim_list}, "
                f"the analysis asks: what does {dim0} actually look like for {char.name} — "
                f"not in the abstract, but on a Tuesday morning? {approach}. The framework "
                f"maps each dimension against current system coverage and finds that {sys0} "
                f"addresses {dim0} partially but ignores {dim1} entirely.\n\n"
                f"AWE POTENTIAL ASSESSMENT: A person inside a complete dome — where all {n_sys} "
                f"systems coordinate — should experience awe at the wholeness of their own life. "
                f"The awe triggers identified for {char.name}'s dome:\n"
                f"- VASTNESS: seeing all {n_sys} systems, all {len(char.flourishing_dimensions)} "
                f"dimensions, all resources orbiting one person simultaneously\n"
                f"- ACCOMMODATION: realizing this coordination IS possible but doesn't currently "
                f"exist — the mind restructures around what could be\n"
                f"- MORAL BEAUTY: an entire team designed this for {char.name}'s flourishing\n"
                f"- EPIPHANY: fragmented cost vs. coordinated cost, understood for the first time"
            )
        if S == PP:
            return (
                f"From the dimensions analysis, {name} designs the dome's architecture: "
                f"a spatial and conceptual environment where {char.name}'s "
                f"{len(char.flourishing_dimensions)} flourishing dimensions are structurally "
                f"supported. Drawing on \"{work_anchor}\", the concept treats every transition "
                f"between {sys0} and {sys1} as a design problem — not a bureaucratic one.\n\n"
                f"AWE DESIGN FOR {char.name.upper()}'S DOME:\n\n"
                f"VASTNESS: The dome visualization renders all {n_sys} systems as orbital layers "
                f"around {char.name} — {sys_list}. Each system visible, each connection mapped, "
                f"each entitlement glowing. The scale of what exists for one person, made visible "
                f"for the first time. Not a chart. An environment you can stand inside.\n\n"
                f"ACCOMMODATION: Two renderings side by side — fragmented (current reality: {n_sys} "
                f"disconnected systems, {char.name} navigating alone) and coordinated (the dome: "
                f"same systems, linked, working). The gap between them IS the accommodation trigger. "
                f"Your mental model of 'how systems work' must expand.\n\n"
                f"MORAL BEAUTY: The dome credits every contributor — every practitioner who mapped, "
                f"modeled, designed, and built. The viewer sees that real people applied their life's "
                f"work to one person's wholeness. The team is visible inside the dome.\n\n"
                f"EPIPHANY: The cost visualization — what fragmentation costs vs. what coordination "
                f"saves. The moment when the audience sees the number and understands: we are paying "
                f"MORE for {char.name}'s suffering than her flourishing would cost.\n\n"
                f"{approach}. The dome's architecture ensures that pursuing {dim0} never requires "
                f"sacrificing {dim1}. A dome that documents everything but moves no one is incomplete."
            )
        if S == P:
            return (
                f"The concept becomes a complete design package. {name} delivers {char.name}'s "
                f"dome — every system, every transition, every threshold designed for dignity. "
                f"Using \"{work_anchor}\"{work_and_second}, "
                f"the package specifies how {sys0} connects to {sys1} without requiring "
                f"{char.name} to re-prove eligibility. How the physical environment supports "
                f"{dim0}. How the schedule respects {dim1}.\n\n"
                f"The dome visualization is designed for awe. When {char.name} — or anyone "
                f"watching — sees the complete dome for the first time, the vastness of "
                f"coordinated support, the moral beauty of a team building this, and the "
                f"epiphany of fragmented vs. coordinated cost should produce a measurable "
                f"awe response (target AWE-S 4.0+). {approach}. This is the dome. "
                f"Not a concept — a deliverable that produces transcendence."
            )
        if S == PO:
            return (
                f"{name} quantifies the dome's impact across all "
                f"{len(char.flourishing_dimensions)} flourishing dimensions and its awe "
                f"design effectiveness. Using \"{work_anchor}\", the assessment scores "
                f"{char.name}'s dome on each dimension — {all_dims} — comparing baseline "
                f"(fragmented systems) to coordinated (the dome). {dim0} improves when "
                f"{sys0} and {sys1} share data. {dim1} improves when navigation burden drops.\n\n"
                f"AWE ASSESSMENT: Does the dome produce awe?\n"
                f"- Vastness: Viewers report feeling 'the scope of what's possible' when seeing "
                f"all {n_sys} systems coordinated. AWE-S vastness subscale: 4.3/5.0.\n"
                f"- Accommodation: 82% of viewers report their understanding of government "
                f"coordination changed after seeing the dome. Mental frameworks expanded.\n"
                f"- Moral beauty: The team credits produce elevation response (Haidt, 2000) — "
                f"viewers express desire to contribute after seeing what the team built.\n"
                f"- Epiphany: The cost comparison is the single most cited moment — viewers "
                f"understand for the first time what fragmentation actually costs.\n\n"
                f"{approach}. The assessment is evidence, not aspiration."
            )
        return (
            f"The full portfolio entry on domes.cc: {char.name}'s dome as a replicable "
            f"model for human flourishing that produces awe. {name}'s methodology from "
            f"\"{work_anchor}\" is published alongside the dome's dimensions ({all_dims}), "
            f"the coordination architecture, the impact scores, and the awe design framework.\n\n"
            f"PUBLISHED AWE DESIGN GUIDANCE FOR DOMES:\n"
            f"The portfolio entry documents how the dome visualization triggers:\n"
            f"- Vastness through rendering all systems as orbital layers\n"
            f"- Accommodation through fragmented vs. coordinated comparison\n"
            f"- Moral beauty through visible team contribution\n"
            f"- Epiphany through cost comparison revelation\n"
            f"- Projected AWE-S scores for dome viewers\n\n"
            f"{approach}. Any practitioner designing a dome can start from this awe "
            f"framework — not just the flourishing dimensions but the experience design "
            f"that makes seeing the dome transcendent."
        )

    # Fallback for any unmapped capability
    return (
        f"{name} applies \"{work_anchor}\" to {char.name}'s situation. {approach}."
    )


def _simulate_sphere_finding(
    talent: TalentProfile,
    project: ProjectBrief,
    cap: str,
    stage: ProductionStage,
    relevant_work: List[WorkItem],
) -> str:
    """
    Simulate what this practitioner would actually find/produce
    at THIS stage when applying their body of work to this parcel.
    The sphere gets more concrete at each stage — from reading the site
    through activation through publication.
    """
    parcel = project.parcel
    seed = f"{talent.talent_id}:{project.project_id}:{cap}:{stage.value}"
    name = talent.name
    work_anchor = relevant_work[0].title if relevant_work else "their practice"
    work_second = relevant_work[1].title if len(relevant_work) > 1 else None
    addr = parcel.address
    hood = parcel.neighborhood
    sqft = f"{parcel.lot_size_sqft:,.0f}"

    focus_constraints = _pick(parcel.constraints, seed, 2)
    con0 = focus_constraints[0] if focus_constraints else "regulatory constraints"
    con1 = focus_constraints[1] if len(focus_constraints) > 1 else "site conditions"
    approach = talent.approach.split('.')[0].strip() if talent.approach else ""
    work_and_second = f' and "{work_second}"' if work_second else ""

    S = stage
    D = ProductionStage.DEVELOPMENT
    PP = ProductionStage.PRE_PRODUCTION
    P = ProductionStage.PRODUCTION
    PO = ProductionStage.POST_PRODUCTION
    DI = ProductionStage.DISTRIBUTION

    # ── spatial_legal ───────────────────────────────────────
    if cap == "spatial_legal":
        if S == D:
            return (
                f"Applying \"{work_anchor}\" to {addr}, {name} reads the {parcel.zoning} "
                f"zoning code as a design document — what it permits, what it prohibits, "
                f"and the variance pathways between. The {sqft} sqft lot in {hood} has a "
                f"regulatory landscape shaped by its history: {parcel.history[:80]}. "
                f"Key constraint: {con0}. {approach}. The analysis maps every permit pathway "
                f"and identifies 3 activation scenarios within the current code."
            )
        if S == PP:
            return (
                f"From the legal analysis, {name} now maps the permit pathway: every "
                f"approval, timeline, and fee required to activate {addr}. Drawing on "
                f"\"{work_anchor}\", the map shows that {con0} can be addressed through "
                f"a variance process, while {con1} requires a phased approach. {approach}. "
                f"The pathway identifies the critical-path approvals — which permits gate "
                f"others, and where parallel applications can save months."
            )
        if S == P:
            return (
                f"The permit pathway becomes an implementation plan. {name} produces the "
                f"construction and compliance blueprint for the sphere at {addr} — phasing, "
                f"logistics, inspection schedules. Using \"{work_anchor}\""
                f"{work_and_second}, the plan navigates "
                f"{con0} through the variance obtained in pre-production and stages "
                f"construction to maintain community access throughout. {approach}. "
                f"The implementation plan is a legal instrument, not just a construction schedule."
            )
        if S == PO:
            return (
                f"{name} documents what the permit process actually revealed about activating "
                f"space at {addr}. Using \"{work_anchor}\", the lessons learned identify "
                f"which approvals took longer than projected, which variance arguments "
                f"succeeded, and where {con0} created unexpected opportunities. {approach}. "
                f"This is the template for the next sphere — every delay explained, every "
                f"shortcut mapped, every fee itemized."
            )
        return (
            f"The replicable activation template from {addr} is published on spheres.land. "
            f"{name}'s methodology from \"{work_anchor}\" — the legal analysis, the permit "
            f"pathway, the implementation plan, the lessons learned — becomes a public "
            f"resource. Any neighborhood facing {parcel.zoning} zoning and similar constraints "
            f"can start from this template. {approach}."
        )

    # ── activation_design ───────────────────────────────────
    if cap == "activation_design":
        if S == D:
            return (
                f"Drawing on \"{work_anchor}\", {name} reads {addr} as an awe site — assessing "
                f"which of Keltner's 8 awe elicitors this specific parcel can deploy and why.\n\n"
                f"AWE TRIGGERS ASSESSED:\n"
                f"1. VASTNESS — The {sqft} sqft lot at {addr} has open sky access from the "
                f"cleared site. The scale contrast between the vacant lot and surrounding "
                f"institutional buildings creates perceived vastness through negative space — "
                f"the absence IS the vastness. Vertical elements (trees, light structures) can "
                f"amplify this without institutional monumentalism. DEPLOYABLE: high potential.\n"
                f"2. ACCOMMODATION — {parcel.history[:60]}. The transformation from dead space "
                f"to living sphere IS the accommodation trigger. Before/after made physically "
                f"walkable. Visitors' mental models of 'vacant lot' must expand. DEPLOYABLE: peak.\n"
                f"3. COLLECTIVE EFFERVESCENCE — The site's position in {hood} near transit and "
                f"foot traffic creates natural gathering potential. Shared movement paths, "
                f"communal making, participatory installations can synchronize visitors. "
                f"DEPLOYABLE: high.\n"
                f"4. MORAL BEAUTY — {parcel.community_context[:80]}. The community's resilience "
                f"IS the moral beauty. The design surfaces it, doesn't manufacture it. "
                f"DEPLOYABLE: high.\n"
                f"5. NATURE — Currently zero tree canopy, zero permeable surface. Introducing "
                f"living systems (native plantings, water, soil, canopy) into dead urban space "
                f"creates the sharpest nature-awe contrast. DEPLOYABLE: peak.\n"
                f"6. MUSIC/SOUND — Current sonic environment: traffic, urban noise. Designed "
                f"soundscape replacing institutional noise with intentional sound — aeolian "
                f"instruments, water, curated silence zones. DEPLOYABLE: high.\n"
                f"7. VISUAL ART — Site-specific installations responding to the parcel's history "
                f"and {hood}'s built environment. Material transformation of industrial remnants. "
                f"DEPLOYABLE: high.\n"
                f"8. EPIPHANY — The sphere's own data made walkable: the lot's vacancy cost vs. "
                f"activation value, the neighborhood's invisible assets revealed, the moment when "
                f"fragmented space becomes legible as connected system. DEPLOYABLE: peak.\n\n"
                f"{approach}. This is not a park assessment. It's an awe audit — mapping what this "
                f"specific site can make people feel, grounded in Keltner's research."
            )
        if S == PP:
            return (
                f"From the awe assessment, {name} designs the activation with every trigger mapped "
                f"to specific design elements. Using \"{work_anchor}\", the framework specifies:\n\n"
                f"AWE DESIGN FRAMEWORK FOR {addr.upper()}:\n\n"
                f"VASTNESS: 40-foot native canopy trees at lot corners creating a green ceiling "
                f"over open ground. The sky becomes visible through the canopy — perceived height "
                f"exceeds physical height. Sight lines from {hood}'s streets draw the eye through "
                f"the space to a horizon point. No walls above 4 feet. The space breathes.\n\n"
                f"ACCOMMODATION: The lot's history ({parcel.history[:50]}) is embedded in the ground "
                f"plane — old footprints traced in contrasting material. Visitors walk on the before "
                f"while standing in the after. The juxtaposition forces accommodation: this WAS dead. "
                f"It IS alive. Your framework for 'vacant lot' no longer holds.\n\n"
                f"COLLECTIVE EFFERVESCENCE: A central gathering circle with acoustic design — sound "
                f"carries inward, creating intimacy at scale. Weekly communal meals. Monthly "
                f"collective making sessions. The rhythm synchronizes the neighborhood. Shared "
                f"movement paths converge at the circle.\n\n"
                f"MORAL BEAUTY: Community history wall built BY residents — oral histories, "
                f"photos, objects. The neighborhood's resilience made physically present. Every "
                f"visit reveals another story of human goodness that was always here but invisible.\n\n"
                f"NATURE: Bioswale water management visible as design element — rain becomes a "
                f"show. Native pollinator garden. Living walls on any retained structure. Soil "
                f"exposed — the ground itself is alive, not sealed.\n\n"
                f"MUSIC/SOUND: Aeolian sound sculptures responding to wind. Water features tuned "
                f"to mask traffic. Acoustic zones: a loud zone for gathering, a quiet zone for "
                f"reflection. The sphere has a sound signature unique to this site.\n\n"
                f"VISUAL ART: Site-specific installation using materials from {hood}'s industrial "
                f"history. Forced perspective piece visible from the street that resolves only when "
                f"you enter the sphere. Light art activating the space after dark.\n\n"
                f"EPIPHANY: A data walk — the sphere's own metrics embedded in the ground: vacancy "
                f"cost per day, activation value per visit, the number of people who walked past "
                f"when this was nothing. The reveal moment: you realize you're standing on the proof.\n\n"
                f"{approach}. The material palette pulls from {hood}'s built environment. "
                f"Every element has a measurable awe target. This sphere looks like it belongs "
                f"here because it's made of here."
            )
        if S == P:
            return (
                f"The awe framework becomes a live program. {name} delivers the full activation "
                f"at {addr} with every trigger deployed and measured. Using "
                f"\"{work_anchor}\"{work_and_second}:\n\n"
                f"AWE ACTIVATION PROGRAM:\n\n"
                f"ARRIVAL SEQUENCE (Vastness + Accommodation): Visitors approach from the street "
                f"through a threshold — the transition from sidewalk to sphere. The canopy opens "
                f"overhead. The ground plane shifts from concrete to living material. The "
                f"accommodation hits: this was a vacant lot. The mental model breaks.\n\n"
                f"GATHERING RHYTHM (Collective Effervescence): Morning: neighborhood walkers. "
                f"Midday: workers from adjacent blocks. Afternoon: school-age children. Evening: "
                f"communal dinner every Thursday. Weekend: maker markets, live music. The rhythm "
                f"creates synchrony — people who came alone leave as a collective.\n\n"
                f"LIVING SYSTEMS (Nature): The bioswale activates in rain — water flows visibly "
                f"through the garden. Pollinator counts tracked and displayed. Seasonal plantings "
                f"change the sphere's character quarterly. The soil program invites community "
                f"participation: the ground improves because people tend it.\n\n"
                f"SONIC ENVIRONMENT (Music/Sound): Aeolian sculptures active whenever wind exceeds "
                f"5mph — {hood} has a sound. Curated silence in the reflection zone. Live music "
                f"Fridays — local artists. The acoustic circle amplifies without electronics.\n\n"
                f"ART PROGRAM (Visual Art + Moral Beauty): Community history wall grows weekly — "
                f"new stories, new photos, new objects. The forced perspective piece draws people "
                f"in from 2 blocks away. Evening light installation transforms the sphere at dusk.\n\n"
                f"REVELATION (Epiphany): The data walk updates live — today's visitor count, this "
                f"week's community hours, this month's adjacent activation. Visitors walk on "
                f"real-time proof that their presence creates value.\n\n"
                f"AWE MEASUREMENT PROTOCOL:\n"
                f"- AWE-S surveys (Yaden et al.) at exit: target 4.2/5.0\n"
                f"- Prosocial behavior: community signup rate >15% of visitors\n"
                f"- Time expansion: 70% of visitors underestimate time spent by >20%\n"
                f"- HRV monitoring (opt-in wearables): vagal tone increase during gathering events\n"
                f"- Return visit rate: target 40% within 30 days\n\n"
                f"{approach}. The {sqft} sqft becomes a room the neighborhood didn't know it had. "
                f"Not an event space — a place that produces awe as reliably as it produces shade."
            )
        if S == PO:
            return (
                f"{name} measures awe outcomes at {addr} against every projected target. Using "
                f"\"{work_anchor}\", the assessment validates which triggers produced measurable awe "
                f"and which need refinement.\n\n"
                f"AWE METRICS RESULTS:\n\n"
                f"Self-reported awe (AWE-S): 4.4/5.0 (target: 4.2) — exceeded. Strongest on "
                f"'connection to something larger' subscale. Accommodation and collective "
                f"effervescence scored highest among the 8 triggers.\n\n"
                f"Prosocial behavior: 18% community signup rate (target: 15%) — exceeded. "
                f"Volunteers for the community history wall: 34 in first month. Dictator game "
                f"variant shows 23% increase in generosity post-visit vs. control.\n\n"
                f"Time expansion: 74% of surveyed visitors underestimated time spent by >20% "
                f"(target: 70%) — exceeded. Average visit duration: 47 minutes. Average "
                f"estimated duration: 25 minutes. The sphere bends time.\n\n"
                f"Sense of belonging (SCI-2): Significant increase in 'community connection' "
                f"subscale among visitors from {hood}. New residents report 2.3x higher "
                f"neighborhood identification after repeated visits.\n\n"
                f"Small self: Reduced self-focus confirmed via implicit measures — visitors "
                f"use more collective pronouns ('we', 'our neighborhood') in post-visit "
                f"interviews. The sphere makes people feel part of something.\n\n"
                f"Physiological (opt-in, N=89): HRV increased 12% during communal dinner "
                f"events — vagal tone responding to collective effervescence. Cortisol "
                f"synchronization detected in groups >8. Piloerection reported by 31% during "
                f"first canopy walk.\n\n"
                f"Community impact: 3 adjacent parcels activated within 6 months. Foot traffic "
                f"on {hood} corridor up 45%. Return visit rate: 52% (target: 40%). 6 new "
                f"community initiatives launched by sphere visitors.\n\n"
                f"TRIGGER EFFECTIVENESS RANKING:\n"
                f"1. Collective Effervescence (communal dinners, maker markets) — highest AWE-S\n"
                f"2. Nature (canopy, bioswale, living walls) — highest physiological response\n"
                f"3. Accommodation (before/after ground plane) — highest first-visit impact\n"
                f"4. Epiphany (data walk) — highest return-visit driver\n"
                f"5. Moral Beauty (community history wall) — highest prosocial behavior trigger\n\n"
                f"{approach}. This is not a satisfaction survey. It's awe science applied to "
                f"public space — validated, measured, replicable."
            )
        return (
            f"The complete awe-designed portfolio entry on spheres.land: the sphere at {addr} "
            f"as a model for awe-based urban activation. {name}'s methodology from "
            f"\"{work_anchor}\" — awe assessment, 8-trigger design framework, activation "
            f"program, validated metrics — is published as the definitive case study.\n\n"
            f"PUBLISHED AWE DESIGN GUIDANCE:\n"
            f"For any principal designing a sphere, this entry documents:\n"
            f"- Which of Keltner's 8 elicitors work best for lots of this size ({sqft} sqft)\n"
            f"- Which triggers have the strongest site-specific rationale in neighborhoods "
            f"like {hood}\n"
            f"- Validated AWE-S scores and prosocial outcomes from actual visitors\n"
            f"- Physiological data confirming awe responses (HRV, cortisol sync)\n"
            f"- The awe-to-action pipeline: how measured awe converts to community impact\n\n"
            f"This is what separates a sphere from a park renovation. A park gives people grass. "
            f"A sphere gives people awe — and awe makes them show up again, bring their "
            f"neighbors, start something new, and believe the next lot can be activated too.\n\n"
            f"{approach}."
        )

    # ── economics ───────────────────────────────────────────
    if cap == "economics":
        if S == D:
            return (
                f"Extending \"{work_anchor}\" to {addr}, {name} models the economic gap: "
                f"a {sqft} sqft vacant lot in {hood} currently costs the city in maintenance, "
                f"lost tax revenue, and neighborhood depression effects. Under activation: "
                f"{parcel.opportunity[:60]}. {approach}. The model quantifies the community "
                f"benefit — not just property values but foot traffic, social cohesion, and "
                f"the economic multiplier when a dead corner becomes a living one."
            )
        if S == PP:
            return (
                f"From the baseline, {name} builds the community benefit model: every "
                f"projected return from activating {addr} — jobs, foot traffic, property "
                f"effects, social value. Using \"{work_anchor}\", the model shows that "
                f"activation produces returns in categories that traditional real estate "
                f"economics doesn't measure: the value of a gathering place, the economic "
                f"ripple of foot traffic, the property effects on adjacent blocks. {approach}. "
                f"The benefit model makes the invisible value of {hood}'s activated space legible "
                f"to investors."
            )
        if S == P:
            return (
                f"The benefit model becomes a financial instrument. {name} structures the "
                f"community investment vehicle for the sphere at {addr}: returns quantified "
                f"and structured so that neighborhood value becomes investable. Using "
                f"\"{work_anchor}\"{work_and_second}, the "
                f"instrument converts foot traffic data, community usage, and property effects "
                f"into a return profile. {approach}. This is a financial product that rewards "
                f"community activation, not displacement."
            )
        if S == PO:
            return (
                f"{name} produces the full economic impact report: actual vs. projected returns "
                f"from the sphere at {addr}. Using \"{work_anchor}\", the report shows which "
                f"projections held, which exceeded expectations, and where the model needs "
                f"recalibration. {approach}. The report is honest — it shows both the economic "
                f"wins and the costs that weren't in the original model. This is data for the "
                f"next sphere, not a success narrative."
            )
        return (
            f"The sphere's financial model is published as an open template for community "
            f"investment on spheres.land. {name}'s methodology from \"{work_anchor}\" — the "
            f"baseline model, the benefit projections, the investment instrument, the actual "
            f"impact data — becomes a public resource. {approach}. Any neighborhood building "
            f"a sphere can use this model as a starting point for their own investment case."
        )

    # ── narrative ───────────────────────────────────────────
    if cap == "narrative":
        if S == D:
            return (
                f"Using \"{work_anchor}\", {name} documents the stories that live at "
                f"{addr}: {parcel.community_context[:100]}. {approach}. The archive captures "
                f"what {hood} remembers about this space, what it needs now, and what it "
                f"imagines. The story of {hood} is told by the people who walk past this "
                f"lot every day."
            )
        if S == PP:
            return (
                f"From the story archive, {name} plans the activation narrative: how the "
                f"sphere at {addr} tells {hood}'s story. Drawing on \"{work_anchor}\", the "
                f"plan structures the experience architecture from arrival to departure — "
                f"what you see first, what you hear, what the space tells you about where "
                f"you are. {approach}. The narrative isn't about the sphere. It's about "
                f"{hood}. The sphere is just the container."
            )
        if S == P:
            return (
                f"The documentary captures the activation of {addr} — from vacant lot to "
                f"living sphere. {name} produces the film using \"{work_anchor}\""
                f"{work_and_second}, positioning the "
                f"camera at street level in {hood}. The community isn't the subject — "
                f"they're the directors. {approach}. The documentary runs in real time "
                f"during key sequences: the audience waits the actual minutes it takes "
                f"for a space to come alive."
            )
        if S == PO:
            return (
                f"Final cut. {name} completes the documentary of {addr}'s transformation. "
                f"Using \"{work_anchor}\", the film moves from the first site visit through "
                f"the full activation. {approach}. The final version is tight — every frame "
                f"earned. The before/after isn't sentimental. It's architectural. You see "
                f"what a {sqft} sqft lot in {hood} can become when someone decides to "
                f"activate it."
            )
        return (
            f"Complete media for the {hood} sphere premiere — documentary, narrative "
            f"assets, impact data, and media kit. {name}'s film from \"{work_anchor}\" "
            f"is the portfolio's primary narrative vehicle. {approach}. The premiere "
            f"package positions {addr} not as a one-off but as proof: vacant lots are "
            f"design problems, not permanent conditions."
        )

    # Fallback
    return (
        f"{name} applies \"{work_anchor}\" to {addr}. {approach}."
    )


def _generate_deliverable(
    talent: TalentProfile,
    principal: Principal,
    project: ProjectBrief,
    cap: str,
    prompt: Dict,
    stage: ProductionStage,
) -> Tuple[str, str]:
    """
    Generate a simulated deliverable. This practitioner's actual body
    of work meets this specific project's details. The output is what
    their dome or sphere contribution WOULD look like.
    """
    base_title = _fill(prompt["title"], project)
    relevant_work = _select_relevant_work(talent, project, cap)

    # Title: deliverable name + practitioner
    title = f"{base_title}: {talent.name}"

    # Description: the simulated output
    if project.game_type == GameType.DOMES and project.character:
        finding = _simulate_dome_finding(talent, project, cap, stage, relevant_work)
    elif project.game_type == GameType.SPHERES and project.parcel:
        finding = _simulate_sphere_finding(talent, project, cap, stage, relevant_work)
    else:
        target = _fill(prompt["target"], project)
        finding = f"{talent.name} {prompt['verb']} {target}."

    # Add principal's directorial signature
    if principal.signature_style:
        style = principal.signature_style.split('.')[0].strip()
        finding += f" [{principal.name}'s direction: {style}.]"

    return title, finding


def _generate_unlikely_deliverable(
    talent: TalentProfile,
    principal: Principal,
    project: ProjectBrief,
    unlikely_tag: str,
) -> Tuple[str, str, str]:
    """
    Simulate the unlikely collision. This practitioner's practice
    was never on the production plan, but they bring their actual
    body of work to a domain nobody expected.
    """
    ip_domain, title_template = UNLIKELY_TEMPLATES[unlikely_tag]
    base_title = _fill(title_template, project)
    title = f"{base_title}: {talent.name}"

    practice = talent.domains_of_practice[0] if talent.domains_of_practice else unlikely_tag
    game = "dome" if project.game_type == GameType.DOMES else "sphere"

    # Build the simulated unlikely finding from their actual work
    parts = []
    parts.append(f"Nobody put {practice} on the production plan for this {game}.")

    if talent.body_of_work:
        anchor = talent.body_of_work[0]
        parts.append(
            f"But {talent.name} brings \"{anchor.title}\" — "
            f"{anchor.description}"
        )

    # Cross their approach with the specific project
    if project.game_type == GameType.DOMES and project.character:
        char = project.character
        dims = _pick(char.flourishing_dimensions, f"{talent.talent_id}:unlikely", 2)
        parts.append(
            f"Applied to {char.name}'s {game}, their practice reframes "
            f"{dims[0] if dims else 'flourishing'} as something the other "
            f"disciplines couldn't see. {talent.approach.split('.')[0] if talent.approach else ''}"
        )
        if len(talent.body_of_work) > 1:
            second = talent.body_of_work[1]
            parts.append(
                f"Their methodology from \"{second.title}\" — {second.description[:80]} — "
                f"produces an entirely new category of output for {char.name}'s dome"
            )
    elif project.game_type == GameType.SPHERES and project.parcel:
        parcel = project.parcel
        parts.append(
            f"Applied to {parcel.address} in {parcel.neighborhood}, their practice "
            f"transforms how the team thinks about the activation. "
            f"{talent.approach.split('.')[0] if talent.approach else ''}"
        )
        if len(talent.body_of_work) > 1:
            second = talent.body_of_work[1]
            parts.append(
                f"Their methodology from \"{second.title}\" — {second.description[:80]} — "
                f"generates IP in a domain the sphere was never designed to enter"
            )

    parts.append(f"This is the collision that makes the portfolio undeniable.")

    desc = ". ".join(parts)
    return title, desc, ip_domain


# ── Capability matching ──────────────────────────────────────────

def _find_capability(talent: TalentProfile, project: ProjectBrief) -> Optional[str]:
    """Find which required capability this talent covers."""
    if project.game_type == GameType.DOMES:
        from assembly import TAG_TO_DOMES_CAPABILITY
        tag_map = TAG_TO_DOMES_CAPABILITY
    else:
        from assembly import TAG_TO_SPHERES_CAPABILITY
        tag_map = TAG_TO_SPHERES_CAPABILITY

    for tag in talent.resonance_tags:
        cap = tag_map.get(tag.lower())
        if cap:
            return cap
    return None


def _get_unlikely_tag(talent: TalentProfile) -> Optional[str]:
    """Find if this talent's practice generates unlikely collisions."""
    utags = set(UNLIKELY_TEMPLATES.keys())
    for tag in talent.resonance_tags:
        if tag.lower() in utags:
            return tag.lower()
    for domain in talent.domains_of_practice:
        for ut in utags:
            if ut in domain.lower():
                return ut
    return None


# ── Scoring ──────────────────────────────────────────────────────

def _compute_scores(
    stage: ProductionStage,
    deliverable_count: int,
    unlikely_count: int,
    prior_art_used: int,
    work_refs_count: int,
) -> Tuple[float, float]:
    """Compute Cosm and Chron score increments."""
    weights = {
        ProductionStage.DEVELOPMENT: (8, 6),
        ProductionStage.PRE_PRODUCTION: (10, 8),
        ProductionStage.PRODUCTION: (15, 12),
        ProductionStage.POST_PRODUCTION: (10, 10),
        ProductionStage.DISTRIBUTION: (7, 14),
    }
    base_cosm, base_chron = weights.get(stage, (5, 5))

    cosm = base_cosm + (deliverable_count * 1.5) + (unlikely_count * 4.0) + (prior_art_used * 2.0) + (work_refs_count * 1.0)
    chron = base_chron + (deliverable_count * 1.0) + (unlikely_count * 2.0) + (prior_art_used * 3.0) + (work_refs_count * 0.5)

    return round(cosm, 1), round(chron, 1)


def _ip_format(domain: str) -> str:
    return {
        "policy": "policy brief", "technology": "software/data model",
        "financial_product": "financial instrument", "entertainment": "documentary/narrative",
        "research": "research paper", "housing": "design package",
        "healthcare": "care protocol", "urban_design": "urban design plan",
        "real_estate": "development plan", "fashion": "garment collection",
        "culinary": "food program", "architectural": "architectural concept",
        "performance": "performance/installation", "product": "product design",
    }.get(domain, "deliverable")


# ── Prior Art ────────────────────────────────────────────────────

def get_prior_art(
    project: ProjectBrief,
    ip_store: Dict[str, IPItem],
    stage: ProductionStage,
    current_production_id: Optional[str] = None,
) -> List[Dict]:
    """Find IP already produced for this project by previous teams."""
    stage_order = [
        ProductionStage.DEVELOPMENT, ProductionStage.PRE_PRODUCTION,
        ProductionStage.PRODUCTION, ProductionStage.POST_PRODUCTION,
        ProductionStage.DISTRIBUTION,
    ]
    idx = stage_order.index(stage)

    prior = []
    for ip in ip_store.values():
        if ip.project_id == project.project_id:
            ip_idx = stage_order.index(ip.stage_originated)
            if ip_idx <= idx:
                prior.append({
                    "ip_id": ip.ip_id, "title": ip.title,
                    "description": ip.description, "domain": ip.domain.value,
                    "format": ip.format, "practitioner_name": ip.practitioner_name,
                    "practice": ip.practice, "stage": ip.stage_originated.value,
                    "production_title": ip.production_title,
                })
    return prior


# ── Main Engine ──────────────────────────────────────────────────

def execute_stage(
    project: ProjectBrief,
    principal: Principal,
    team: TeamRecommendation,
    roster: Dict[str, TalentProfile],
    stage: ProductionStage,
    ip_store: Dict[str, IPItem],
    production_number: int = 1,
    intelligence_context: Optional[Dict] = None,
) -> Dict:
    """
    Execute a production stage. This is the gameplay.

    Each practitioner pulls from their body of work.
    The principal's vision shapes the direction.
    Different teams produce different outputs because they
    bring different prior work to the same production challenge.

    If intelligence_context is provided (from the memory system),
    deliverables are enriched with cross-project insights.
    """
    stage_defs = (DOMES_STAGES if project.game_type == GameType.DOMES
                  else SPHERES_STAGES)
    stage_def = stage_defs.get(stage)
    if not stage_def:
        return {"error": "Unknown stage"}

    # Phase 0: Prior art from previous productions
    prior_art = get_prior_art(project, ip_store, stage)

    deliverables = []
    ip_generated = []
    unlikely_outputs = []
    prior_art_referenced = []
    capability_producers = {}
    total_work_refs = 0

    # Phase 1: Required capability deliverables
    for member in team.members:
        talent = roster.get(member.talent_id)
        if not talent:
            continue

        cap = _find_capability(talent, project)
        if not cap or cap not in stage_def["capability_prompts"]:
            continue
        if cap in capability_producers:
            continue

        capability_producers[cap] = talent
        prompt = stage_def["capability_prompts"][cap]

        # Generate deliverable from this practitioner's actual body of work
        title, desc = _generate_deliverable(
            talent, principal, project, cap, prompt, stage
        )

        # Count work references for scoring
        relevant = _select_relevant_work(talent, project, cap)
        total_work_refs += len(relevant)

        # Add work references to deliverable data
        work_refs = []
        for w in relevant:
            work_refs.append({
                "title": w.title, "description": w.description,
                "medium": w.medium, "year": w.year,
            })

        # Check for prior art to build on
        relevant_prior = [
            p for p in prior_art
            if p["domain"] == prompt["ip_domain"]
            and p["stage"] == stage.value
        ]
        built_on = None
        if relevant_prior:
            built_on = relevant_prior[0]
            prior_art_referenced.append(built_on)
            desc += f" Builds on prior work: \"{built_on['title']}\" by {built_on['practitioner_name']}."

        if production_number > 1:
            title += f" [#{production_number}]"

        deliverable = {
            "talent_id": talent.talent_id,
            "talent_name": talent.name,
            "practice": talent.domains_of_practice[0] if talent.domains_of_practice else "general",
            "capability": cap,
            "title": title,
            "description": desc,
            "ip_domain": prompt["ip_domain"],
            "stage": stage.value,
            "is_unlikely": False,
            "built_on": built_on["ip_id"] if built_on else None,
            "work_referenced": work_refs,
        }
        deliverables.append(deliverable)

        ip_item = IPItem(
            ip_id=str(uuid.uuid4()),
            domain=IPDomain(prompt["ip_domain"]),
            title=title,
            description=desc,
            format=_ip_format(prompt["ip_domain"]),
            project_id=project.project_id,
            production_title=f"{project.title} (#{production_number})" if production_number > 1 else project.title,
            practitioner_id=talent.talent_id,
            practitioner_name=talent.name,
            practice=talent.domains_of_practice[0] if talent.domains_of_practice else "general",
            stage_originated=stage,
            value_driver=f"{talent.name}'s {cap.replace('_', ' ')} practice applied to {project.title}",
        )
        ip_generated.append(ip_item)
        ip_store[ip_item.ip_id] = ip_item

    # Phase 2: Unlikely collisions
    for member in team.members:
        talent = roster.get(member.talent_id)
        if not talent:
            continue
        if talent.talent_id in [d["talent_id"] for d in deliverables]:
            continue

        unlikely_tag = _get_unlikely_tag(talent)
        if not unlikely_tag or unlikely_tag not in UNLIKELY_TEMPLATES:
            continue

        title, desc, ip_domain_str = _generate_unlikely_deliverable(
            talent, principal, project, unlikely_tag
        )

        if production_number > 1:
            title += f" [#{production_number}]"

        work_refs = []
        for w in talent.body_of_work[:2]:
            work_refs.append({
                "title": w.title, "description": w.description,
                "medium": w.medium, "year": w.year,
            })
        total_work_refs += len(work_refs)

        deliverable = {
            "talent_id": talent.talent_id,
            "talent_name": talent.name,
            "practice": talent.domains_of_practice[0] if talent.domains_of_practice else "general",
            "capability": f"unlikely:{unlikely_tag}",
            "title": title,
            "description": desc,
            "ip_domain": ip_domain_str,
            "stage": stage.value,
            "is_unlikely": True,
            "built_on": None,
            "work_referenced": work_refs,
        }
        deliverables.append(deliverable)
        unlikely_outputs.append(deliverable)

        ip_item = IPItem(
            ip_id=str(uuid.uuid4()),
            domain=IPDomain(ip_domain_str),
            title=title,
            description=desc,
            format=_ip_format(ip_domain_str),
            project_id=project.project_id,
            production_title=f"{project.title} (#{production_number})" if production_number > 1 else project.title,
            practitioner_id=talent.talent_id,
            practitioner_name=talent.name,
            practice=talent.domains_of_practice[0] if talent.domains_of_practice else "general",
            stage_originated=stage,
            value_driver=f"Unlikely collision: {talent.name}'s {unlikely_tag} practice in {project.title}",
        )
        ip_generated.append(ip_item)
        ip_store[ip_item.ip_id] = ip_item

    # Phase 2.5: Intelligence enrichment
    # If cross-project intelligence is available, annotate deliverables
    # with insights from prior projects. This is where the system
    # demonstrates that it's learning.
    intelligence_annotations = []
    if intelligence_context and intelligence_context.get("prior_insights"):
        for deliverable in deliverables:
            cap = deliverable.get("capability", "")
            relevant_insights = [
                ins for ins in intelligence_context["prior_insights"]
                if ins.get("capability") == cap or ins.get("type") in ("pattern", "method")
            ]
            if relevant_insights:
                # Add cross-project intelligence to the deliverable
                best_insight = relevant_insights[0]
                cross_ref = (
                    f" [Cross-project intelligence: {best_insight['source']} "
                    f"({best_insight['type']}, reliability {best_insight['reliability']}) — "
                    f"{best_insight['insight'][:150]}]"
                )
                deliverable["description"] += cross_ref
                deliverable["cross_project_source"] = best_insight["source"]
                intelligence_annotations.append({
                    "deliverable": deliverable["title"],
                    "insight_source": best_insight["source"],
                    "insight_type": best_insight["type"],
                    "reliability": best_insight["reliability"],
                })

    # Phase 3: Scores
    cosm_delta, chron_delta = _compute_scores(
        stage, len(deliverables), len(unlikely_outputs),
        len(prior_art_referenced), total_work_refs
    )

    # Intelligence bonus: cross-project learning adds score
    if intelligence_annotations:
        intel_bonus = min(len(intelligence_annotations) * 1.5, 6.0)
        cosm_delta = round(cosm_delta + intel_bonus, 1)
        chron_delta = round(chron_delta + intel_bonus * 0.5, 1)

    # Phase 4: Narrative
    narrative = _build_narrative(
        stage_def, project, principal, deliverables,
        unlikely_outputs, prior_art, prior_art_referenced,
        cosm_delta, chron_delta, production_number
    )

    result = {
        "stage": stage.value,
        "stage_name": stage_def["name"],
        "focus": stage_def["focus"],
        "production_number": production_number,
        "deliverables": deliverables,
        "ip_generated": [
            {
                "ip_id": ip.ip_id, "domain": ip.domain.value,
                "title": ip.title, "description": ip.description,
                "format": ip.format, "practitioner_name": ip.practitioner_name,
                "practice": ip.practice,
            }
            for ip in ip_generated
        ],
        "prior_art": prior_art,
        "prior_art_referenced": prior_art_referenced,
        "unlikely_outputs": unlikely_outputs,
        "cosm_delta": cosm_delta,
        "chron_delta": chron_delta,
        "narrative": narrative,
        "deliverable_count": len(deliverables),
        "ip_count": len(ip_generated),
        "unlikely_count": len(unlikely_outputs),
        "prior_art_count": len(prior_art),
        "prior_art_used": len(prior_art_referenced),
        "work_refs_count": total_work_refs,
    }

    # Add intelligence annotations if present
    if intelligence_annotations:
        result["intelligence_annotations"] = intelligence_annotations
        result["cross_project_insights_used"] = len(intelligence_annotations)

    return result


def _build_narrative(
    stage_def: Dict,
    project: ProjectBrief,
    principal: Principal,
    deliverables: List[Dict],
    unlikely_outputs: List[Dict],
    prior_art: List[Dict],
    prior_art_referenced: List[Dict],
    cosm_delta: float,
    chron_delta: float,
    production_number: int,
) -> str:
    """Build a narrative of what happened at this stage."""
    subject = ""
    if project.game_type == GameType.DOMES and project.character:
        subject = project.character.name
    elif project.game_type == GameType.SPHERES and project.parcel:
        subject = f"{project.parcel.address}, {project.parcel.neighborhood}"

    parts = []
    parts.append(f"**{stage_def['name']}** — {stage_def['focus']}")
    parts.append("")

    if production_number > 1:
        parts.append(f"*Production #{production_number}* — a new team, new perspectives, same brief.")
        parts.append("")

    if prior_art:
        parts.append(f"The team reviewed **{len(prior_art)} prior deliverables** from previous productions.")
        if prior_art_referenced:
            parts.append(f"They chose to build on **{len(prior_art_referenced)}**:")
            for pa in prior_art_referenced:
                parts.append(f"  \u21aa *{pa['title']}* ({pa['practitioner_name']})")
        else:
            parts.append("They chose to diverge — fresh perspective, new IP.")
        parts.append("")

    # Principal's vision
    if principal.vision:
        vision_fragment = principal.vision.split('.')[0].strip()
        parts.append(f"**{principal.name}** directs: {vision_fragment}.")
        parts.append("")

    parts.append(f"The team produced **{len(deliverables)} deliverables** for {subject}:")
    parts.append("")

    for d in deliverables:
        unlikely_marker = " \u2728 *unlikely collision*" if d["is_unlikely"] else ""
        parts.append(f"**{d['talent_name']}** ({d['practice']}){unlikely_marker}")
        parts.append(f"*{d['title']}*")

        # Show what prior work they drew from
        if d.get("work_referenced"):
            refs = ", ".join(f'"{w["title"]}"' for w in d["work_referenced"])
            parts.append(f"Drawing on: {refs}")

        # First ~150 chars of description
        desc_preview = d["description"][:180]
        if len(d["description"]) > 180:
            desc_preview += "..."
        parts.append(desc_preview)
        parts.append("")

    score_note = f"**+{cosm_delta} Cosm**, **+{chron_delta} Chron**"
    if prior_art_referenced:
        score_note += f" (prior art bonus from {len(prior_art_referenced)} refs)"
    parts.append(score_note)

    return "\n".join(parts)
