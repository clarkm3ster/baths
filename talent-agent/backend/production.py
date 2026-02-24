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
        "focus": "Read the parcel. Map the community. Understand the constraints.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Parcel Legal Analysis",
                "ip_domain": "policy",
                "verb": "maps",
                "target": "complete zoning, permit, and regulatory analysis for {address}",
            },
            "activation_design": {
                "title": "Site Assessment",
                "ip_domain": "urban_design",
                "verb": "assesses",
                "target": "the physical and community potential of {address} — what the space is, what's possible",
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
        "focus": "Design the activation. Model the economics. Plan the experience.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Permit Pathway Map",
                "ip_domain": "policy",
                "verb": "maps",
                "target": "the permit and regulatory pathway for activating {address}",
            },
            "activation_design": {
                "title": "Activation Design Concept",
                "ip_domain": "architectural",
                "verb": "designs",
                "target": "the full concept for the sphere at {address} — spatial layout, experience flow, material palette",
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
        "focus": "Activate the space. Every discipline produces. The parcel comes alive.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Activation Implementation Plan",
                "ip_domain": "real_estate",
                "verb": "implements",
                "target": "the construction and implementation plan for the sphere at {address}",
            },
            "activation_design": {
                "title": "Activation Program",
                "ip_domain": "performance",
                "verb": "programs",
                "target": "every experience, performance, and interaction for the sphere at {address}",
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
        "focus": "Document the impact. Measure the activation. Refine the model.",
        "capability_prompts": {
            "spatial_legal": {
                "title": "Regulatory Lessons Learned",
                "ip_domain": "policy",
                "verb": "documents",
                "target": "what the permit process revealed about activating space at {address}",
            },
            "activation_design": {
                "title": "Activation Impact Assessment",
                "ip_domain": "urban_design",
                "verb": "measures",
                "target": "foot traffic, community usage, spatial transformation at {address}",
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
                "title": "Sphere Portfolio Entry",
                "ip_domain": "architectural",
                "verb": "publishes",
                "target": "the full portfolio entry on spheres.land",
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
                f"addresses {dim0} partially but ignores {dim1} entirely."
            )
        if S == PP:
            return (
                f"From the dimensions analysis, {name} designs the dome's architecture: "
                f"a spatial and conceptual environment where {char.name}'s {len(char.flourishing_dimensions)} "
                f"flourishing dimensions are structurally supported. Drawing on \"{work_anchor}\", "
                f"the concept treats every transition between {sys0} and {sys1} as a design "
                f"problem — not a bureaucratic one. {approach}. The dome's architecture ensures "
                f"that pursuing {dim0} never requires sacrificing {dim1}. The systems serve "
                f"the person, not the other way around."
            )
        if S == P:
            return (
                f"The concept becomes a complete design package. {name} delivers {char.name}'s "
                f"dome — every system, every transition, every threshold designed for dignity. "
                f"Using \"{work_anchor}\"{work_and_second}, "
                f"the package specifies how {sys0} connects to {sys1} without requiring "
                f"{char.name} to re-prove eligibility. How the physical environment supports "
                f"{dim0}. How the schedule respects {dim1}. {approach}. This is the dome. "
                f"Not a concept — a deliverable."
            )
        if S == PO:
            return (
                f"{name} quantifies the dome's impact across all {len(char.flourishing_dimensions)} "
                f"flourishing dimensions. Using \"{work_anchor}\", the assessment scores "
                f"{char.name}'s dome on each dimension — {all_dims} — comparing baseline "
                f"(fragmented systems) to coordinated (the dome). {dim0} improves when {sys0} "
                f"and {sys1} share data. {dim1} improves when navigation burden drops. {approach}. "
                f"The assessment is evidence, not aspiration."
            )
        return (
            f"The full portfolio entry on domes.cc: {char.name}'s dome as a replicable "
            f"model for human flourishing. {name}'s methodology from \"{work_anchor}\" is "
            f"published alongside the dome's dimensions ({all_dims}), the coordination "
            f"architecture, and the impact scores. {approach}. Any practitioner designing "
            f"a dome for a similar case can start from this model — the flourishing "
            f"dimensions, the system linkages, the threshold designs — rather than zero."
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
                f"Drawing on \"{work_anchor}\", {name} reads {addr} as a site with memory: "
                f"{parcel.history[:80]}. The assessment maps what the community is already "
                f"doing with the space — {parcel.opportunity[:80]}. {approach}. The assessment "
                f"identifies the site's natural gathering patterns, acoustic properties, sight "
                f"lines from the street, and the threshold moments where public space becomes "
                f"activated space."
            )
        if S == PP:
            return (
                f"From the site assessment, {name} designs the activation concept: spatial "
                f"layout, experience flow, material palette for the sphere at {addr}. Using "
                f"\"{work_anchor}\", the concept responds to the community's existing use "
                f"patterns — what people already do here — and amplifies them. The design "
                f"works within {con0} rather than against it. {approach}. The material palette "
                f"pulls from {hood}'s built environment: this sphere looks like it belongs here "
                f"because it's made of here."
            )
        if S == P:
            return (
                f"The concept becomes a program. {name} delivers the full activation: every "
                f"experience, every performance, every interaction at {addr} designed and "
                f"scheduled. Using \"{work_anchor}\"{work_and_second}, "
                f"the program creates a rhythm — morning to night, weekday to weekend — that "
                f"serves {hood}'s actual community. {approach}. The {sqft} sqft becomes a "
                f"living room for the neighborhood. Not an event space. A place."
            )
        if S == PO:
            return (
                f"{name} measures the activation's impact at {addr}: foot traffic, community "
                f"usage patterns, spatial transformation metrics. Using \"{work_anchor}\", the "
                f"assessment compares what the site was (vacant, {parcel.history[:40]}) to what "
                f"it became. {approach}. The data shows which program elements drew the most "
                f"community engagement, which times of day activated the space most effectively, "
                f"and which design choices made the difference between a visited space and a "
                f"lived-in one."
            )
        return (
            f"The full portfolio entry on spheres.land: the sphere at {addr} as a model for "
            f"urban activation. {name}'s methodology from \"{work_anchor}\" — site reading, "
            f"concept design, programming, impact data — is published as a complete case study. "
            f"{approach}. Any neighborhood with a similar site can start from this sphere's "
            f"design principles rather than a blank lot."
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
) -> Dict:
    """
    Execute a production stage. This is the gameplay.

    Each practitioner pulls from their body of work.
    The principal's vision shapes the direction.
    Different teams produce different outputs because they
    bring different prior work to the same production challenge.
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

    # Phase 3: Scores
    cosm_delta, chron_delta = _compute_scores(
        stage, len(deliverables), len(unlikely_outputs),
        len(prior_art_referenced), total_work_refs
    )

    # Phase 4: Narrative
    narrative = _build_narrative(
        stage_def, project, principal, deliverables,
        unlikely_outputs, prior_art, prior_art_referenced,
        cosm_delta, chron_delta, production_number
    )

    return {
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
