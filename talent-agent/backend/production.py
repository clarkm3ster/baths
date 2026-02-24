"""
Chron Talent Agent — Production Engine
When a team plays a game, this is what happens at each stage.
Every stage generates deliverables, IP, scores, and a narrative.
The team's actual composition determines what gets produced.
Different teams on the same project produce different outputs.
Subsequent teams see what was already built and decide to use or diverge.
"""

from typing import List, Dict, Optional, Tuple
from models import (
    TalentProfile, Principal, ProjectBrief, TeamRecommendation,
    ResonanceMatch, IPItem, IPDomain, GameType, ProductionStage,
)
from datetime import datetime
import uuid
import hashlib


# ── Stage definitions: what each stage produces ──────────────────

DOMES_STAGES = {
    ProductionStage.DEVELOPMENT: {
        "name": "Development",
        "focus": "Map the legal landscape. Discover every entitlement. Model every system.",
        "deliverable_types": [
            ("legal_navigation", "policy", "Legal Landscape Map", "Comprehensive mapping of all legal entitlements, eligibility criteria, and application pathways for {character}"),
            ("data_systems", "technology", "Systems Fragmentation Model", "Data model showing how {system_count} government systems interact (or fail to) around {character}'s specific situation"),
            ("narrative", "entertainment", "Character Documentary Treatment", "Documentary treatment capturing {character}'s full landscape — not just their problems, but their intelligence, joy, and agency"),
            ("flourishing_design", "research", "Flourishing Dimensions Analysis", "Research framework mapping {character}'s {dimension_count} flourishing dimensions against current system coverage"),
        ],
    },
    ProductionStage.PRE_PRODUCTION: {
        "name": "Pre-Production",
        "focus": "Design the dome. Blueprint the coordination. Model the costs.",
        "deliverable_types": [
            ("legal_navigation", "policy", "Entitlement Coordination Blueprint", "Step-by-step coordination plan linking {system_count} systems into a single pathway for {character}"),
            ("data_systems", "financial_product", "Cost-of-Fragmentation Model", "Financial model showing the cost of non-coordination vs. coordination for {character}'s specific case"),
            ("narrative", "entertainment", "Production Narrative Framework", "Narrative architecture for the dome — how {character}'s story gets told through the production"),
            ("flourishing_design", "architectural", "Dome Architecture Concept", "Spatial and conceptual design for {character}'s dome — the environment for complete flourishing"),
        ],
    },
    ProductionStage.PRODUCTION: {
        "name": "Production",
        "focus": "Build the dome. Every discipline produces. The IP starts flowing.",
        "deliverable_types": [
            ("legal_navigation", "policy", "Policy Brief", "Actionable policy brief: how to replicate {character}'s dome coordination model at municipal scale"),
            ("data_systems", "financial_product", "Coordination Bond Structure", "Financial instrument that makes {character}'s dome investable — the coordination savings converted to returns"),
            ("narrative", "entertainment", "Documentary First Cut", "First cut of the dome documentary — {character}'s journey through the production pipeline"),
            ("flourishing_design", "housing", "Flourishing Design Package", "Complete design package for {character}'s dome — every system, every transition, every threshold designed for dignity"),
        ],
    },
    ProductionStage.POST_PRODUCTION: {
        "name": "Post-Production",
        "focus": "Stress-test the dome. Integrate the deliverables. Refine the IP.",
        "deliverable_types": [
            ("legal_navigation", "policy", "Stress Test: Legal Pathways", "Testing every legal pathway in {character}'s dome against real bureaucratic conditions — what holds, what breaks"),
            ("data_systems", "technology", "Dome Digital Twin", "Interactive simulation of {character}'s dome — 10-year trajectory modeling under different coordination scenarios"),
            ("narrative", "entertainment", "Documentary Final Cut", "Final documentary: {character}'s dome production from sourcing through completion"),
            ("flourishing_design", "research", "Flourishing Impact Assessment", "Quantified assessment: how {character}'s dome scores across all {dimension_count} flourishing dimensions"),
        ],
    },
    ProductionStage.DISTRIBUTION: {
        "name": "Distribution",
        "focus": "Publish to domes.cc. The IP enters the portfolio. The Cosm scores are final.",
        "deliverable_types": [
            ("legal_navigation", "policy", "Published Policy Portfolio", "All policy deliverables from {character}'s dome published and indexed on domes.cc"),
            ("data_systems", "technology", "Open-Source Coordination Model", "The dome's coordination model published as open-source infrastructure on domes.cc"),
            ("narrative", "entertainment", "Dome Premiere Package", "Complete documentary, narrative assets, and media kit for {character}'s dome premiere"),
            ("flourishing_design", "research", "Dome Portfolio Entry", "Full portfolio entry on domes.cc — the dome as a replicable model for human flourishing"),
        ],
    },
}

SPHERES_STAGES = {
    ProductionStage.DEVELOPMENT: {
        "name": "Development",
        "focus": "Read the parcel. Map the community. Understand the constraints.",
        "deliverable_types": [
            ("spatial_legal", "policy", "Parcel Legal Analysis", "Complete zoning, permit, and regulatory analysis for {address} — every constraint and opportunity in the code"),
            ("activation_design", "urban_design", "Site Assessment", "Physical and community assessment of {address} — what the space is, what the community needs, what's possible"),
            ("economics", "financial_product", "Activation Economics Baseline", "Economic model of the parcel's current cost to the city vs. projected value under activation at {address}"),
            ("narrative", "entertainment", "Community Story Archive", "Documented oral histories and community narratives connected to {address} and its {neighborhood} context"),
        ],
    },
    ProductionStage.PRE_PRODUCTION: {
        "name": "Pre-Production",
        "focus": "Design the activation. Model the economics. Plan the experience.",
        "deliverable_types": [
            ("spatial_legal", "policy", "Permit Pathway Map", "Step-by-step permit and regulatory pathway for activating {address} — every approval, every timeline, every fee"),
            ("activation_design", "architectural", "Activation Design Concept", "Full concept design for the sphere at {address} — spatial layout, experience flow, material palette"),
            ("economics", "financial_product", "Community Benefit Model", "Financial model quantifying community benefit of activation at {address} — jobs, foot traffic, property effects, social value"),
            ("narrative", "entertainment", "Activation Narrative Plan", "How the sphere at {address} tells {neighborhood}'s story — the experience architecture from arrival to departure"),
        ],
    },
    ProductionStage.PRODUCTION: {
        "name": "Production",
        "focus": "Activate the space. Every discipline produces. The parcel comes alive.",
        "deliverable_types": [
            ("spatial_legal", "real_estate", "Activation Implementation Plan", "Construction and implementation plan for the sphere at {address} — phasing, logistics, compliance"),
            ("activation_design", "performance", "Activation Program", "Full program for the sphere — every experience, every performance, every interaction designed and scheduled"),
            ("economics", "financial_product", "Sphere Investment Instrument", "Financial instrument making the sphere at {address} investable — community returns quantified and structured"),
            ("narrative", "entertainment", "Production Documentary", "Documentary capturing the activation of {address} — from vacant lot to living sphere"),
        ],
    },
    ProductionStage.POST_PRODUCTION: {
        "name": "Post-Production",
        "focus": "Document the impact. Measure the activation. Refine the model.",
        "deliverable_types": [
            ("spatial_legal", "policy", "Regulatory Lessons Learned", "What the permit process revealed about activating space at {address} — template for future spheres"),
            ("activation_design", "urban_design", "Activation Impact Assessment", "Measured impact: foot traffic, community usage, spatial transformation metrics for {address}"),
            ("economics", "research", "Economic Impact Report", "Full economic impact report: actual vs. projected returns from the sphere at {address}"),
            ("narrative", "entertainment", "Sphere Documentary Final", "Final documentary: the complete story of {address} from dormant parcel to activated sphere"),
        ],
    },
    ProductionStage.DISTRIBUTION: {
        "name": "Distribution",
        "focus": "Publish to spheres.land. The activation model enters the portfolio.",
        "deliverable_types": [
            ("spatial_legal", "policy", "Published Activation Template", "Replicable activation template from {address} published on spheres.land — permits, timelines, costs, lessons"),
            ("activation_design", "architectural", "Sphere Portfolio Entry", "Full portfolio entry on spheres.land — the sphere as a model for urban activation"),
            ("economics", "financial_product", "Open Investment Model", "The sphere's financial model published as an open template for community investment on spheres.land"),
            ("narrative", "entertainment", "Sphere Premiere Package", "Complete media package for the {neighborhood} sphere premiere — documentary, assets, impact data"),
        ],
    },
}


# ── Unlikely collision deliverables ──────────────────────────────

UNLIKELY_DELIVERABLE_TEMPLATES = {
    "fashion": ("fashion", "Adaptive {game} Garment Line", "Clothing designed for the specific physical and emotional conditions of {context} — the body as first architecture of {concept}"),
    "food": ("culinary", "{game} Nourishment Protocol", "Food and gathering design for {context} — nourishment as social infrastructure within the {concept}"),
    "sound": ("performance", "Sonic Environment Design", "Sound design for the {game} — the acoustic architecture of {context}, replacing institutional noise with healing frequencies"),
    "scent": ("product", "Olfactory Environment Protocol", "Scent design for the {game} — what safety smells like inside {context}"),
    "movement": ("performance", "Movement Autonomy Program", "Choreographic framework for {context} — how the body moves through the {game}, designed for agency not processing"),
    "blacksmith": ("product", "Permanent Making Installation", "Forged permanent objects for the {game} — material transformation as metaphor and function within {context}"),
    "midwife": ("research", "Transition Support Framework", "Transition accompaniment model for {context} — every system crossing in the {game} treated with the care of a birth"),
    "graffiti": ("performance", "Public Voice Installation", "Large-scale visual storytelling for the {game} — the walls of {context} speaking in the community's voice"),
    "mural": ("performance", "Community Documentation Mural", "Permanent visual documentation of the {game} production — {context} made visible at neighborhood scale"),
    "prosthetics": ("product", "Affordable Access Design", "Affordably designed access tools for {context} — constraint as design excellence within the {game}"),
    "game": ("technology", "Friction Audit Report", "Accessibility and friction audit of every system in the {game} — which barriers protect, which barriers exclude within {context}"),
    "perfume": ("product", "Sensory Safety Protocol", "Environmental sensory design for {context} — what the {game} smells like when it's working"),
    "graphic-novel": ("entertainment", "Visual Systems Narrative", "Graphic narrative of the {game} — {context} drawn at human height, in the emotional register of the people inside it"),
    "choreography": ("performance", "Embodied Experience Design", "Movement and spatial experience choreography for the {game} — how bodies navigate {context}"),
    "dance": ("performance", "Embodied Experience Design", "Movement and spatial experience choreography for the {game} — how bodies navigate {context}"),
}


# ── Practice-specific title modifiers ────────────────────────────
# When a specific practitioner produces a deliverable, their practice
# inflects the title to make it unique to THEIR perspective.
# This is why different teams produce different outputs.

PRACTICE_INFLECTIONS = {
    "transitional housing": ("through the lens of spatial dignity", "Every threshold designed as a dignity metric"),
    "adaptive fashion": ("through the body-as-system lens", "The garment as interface between person and environment"),
    "community nutrition": ("through the nourishment lens", "Food as social infrastructure, not caloric delivery"),
    "systems modeling": ("through cascade failure analysis", "Every system interaction mapped as a feedback loop"),
    "documentary poetry": ("through the voice of documentation", "The person inside the case number, the family inside the file"),
    "microfinance": ("through invisible value instruments", "Community value translated into financial terms without losing its meaning"),
    "movement as autonomy": ("through embodied autonomy", "The body's agency as the foundation of all other agency"),
    "accessibility design": ("through friction analysis", "Every barrier audited — which protect, which exclude"),
    "mobile healthcare": ("through proximity-as-care", "Healthcare as relationship, not building"),
    "brownfield remediation": ("through soil memory", "Understanding what happened here before building what comes next"),
    "affordable design": ("through the constraint lens", "Constraint as the space where real design happens"),
    "sound therapy": ("through sonic environment design", "The acoustic architecture of safety"),
    "disability rights": ("through rights architecture", "Every entitlement stress-tested as structural support"),
    "documentary filmmaking": ("from the defendant's chair", "The camera positioned where the system looks most broken"),
    "government technology": ("through the interface-as-policy lens", "Every dropdown menu as a civil rights decision"),
    "bureaucratic navigation": ("through the navigation tax lens", "The invisible labor of being inside the system"),
    "graphic narrative": ("through the child's eye-level", "The system drawn from the height of the person inside it"),
    "olfactory design": ("through the sensory safety lens", "What the environment tells your nervous system before your brain catches up"),
    "material transformation": ("through the forge", "Material honesty as the foundation for transformation"),
    "transition support": ("through the accompaniment lens", "Every system crossing treated with the care of a birth"),
    "public art": ("through the wall's voice", "The community speaking at the scale of the neighborhood"),
}


def _format_template(template: str, project: ProjectBrief) -> str:
    """Fill in template variables from project brief."""
    replacements = {}
    if project.game_type == GameType.DOMES and project.character:
        char = project.character
        replacements["character"] = char.name
        replacements["system_count"] = str(len(char.key_systems))
        replacements["dimension_count"] = str(len(char.flourishing_dimensions))
        replacements["situation"] = char.situation[:80]
        replacements["game"] = "dome"
        replacements["concept"] = "human flourishing"
        replacements["context"] = char.situation[:60]
    elif project.game_type == GameType.SPHERES and project.parcel:
        parcel = project.parcel
        replacements["address"] = parcel.address
        replacements["neighborhood"] = parcel.neighborhood
        replacements["city"] = parcel.city
        replacements["lot_size"] = str(parcel.lot_size_sqft)
        replacements["game"] = "sphere"
        replacements["concept"] = "space activation"
        replacements["context"] = f"{parcel.address}, {parcel.neighborhood}"

    result = template
    for key, val in replacements.items():
        result = result.replace("{" + key + "}", val)
    return result


def _find_capability_for_talent(
    talent: TalentProfile,
    project: ProjectBrief,
) -> Optional[str]:
    """Find which required capability this talent best covers."""
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


def _get_practice_inflection(talent: TalentProfile) -> Tuple[str, str]:
    """Get the practice-specific inflection for a talent's deliverables."""
    for domain in talent.domains_of_practice:
        key = domain.lower()
        if key in PRACTICE_INFLECTIONS:
            return PRACTICE_INFLECTIONS[key]
    # Fallback: use their approach
    if talent.approach:
        return (f"through {talent.domains_of_practice[0] if talent.domains_of_practice else 'their'} practice",
                talent.approach[:80])
    return ("", "")


def _get_unlikely_tag(talent: TalentProfile) -> Optional[str]:
    """Find if this talent has a practice that generates unlikely collisions."""
    unlikely_tags = set(UNLIKELY_DELIVERABLE_TEMPLATES.keys())
    for tag in talent.resonance_tags:
        if tag.lower() in unlikely_tags:
            return tag.lower()
    for domain in talent.domains_of_practice:
        for utag in unlikely_tags:
            if utag in domain.lower():
                return utag
    return None


def _compute_stage_scores(
    stage: ProductionStage,
    deliverable_count: int,
    team_size: int,
    unlikely_count: int,
    prior_art_used: int,
) -> Tuple[float, float]:
    """Compute Cosm and Chron score increments for a stage."""
    stage_weights = {
        ProductionStage.DEVELOPMENT: (8, 6),
        ProductionStage.PRE_PRODUCTION: (10, 8),
        ProductionStage.PRODUCTION: (15, 12),
        ProductionStage.POST_PRODUCTION: (10, 10),
        ProductionStage.DISTRIBUTION: (7, 14),
    }
    base_cosm, base_chron = stage_weights.get(stage, (5, 5))

    cosm_bonus = deliverable_count * 1.5
    chron_bonus = deliverable_count * 1.0

    # Unlikely collision bonus
    unlikely_bonus = unlikely_count * 4.0

    # Building on prior art bonus — learning accelerates production
    prior_art_bonus = prior_art_used * 2.0

    cosm = round(base_cosm + cosm_bonus + unlikely_bonus + prior_art_bonus, 1)
    chron = round(base_chron + chron_bonus + (unlikely_bonus * 0.5) + (prior_art_bonus * 1.5), 1)

    return cosm, chron


def _ip_format_for_domain(domain: str) -> str:
    """Map IP domain to typical format."""
    formats = {
        "policy": "policy brief",
        "technology": "software/data model",
        "financial_product": "financial instrument",
        "entertainment": "documentary/narrative",
        "research": "research paper",
        "housing": "design package",
        "healthcare": "care protocol",
        "urban_design": "urban design plan",
        "real_estate": "development plan",
        "fashion": "garment collection",
        "culinary": "food program",
        "architectural": "architectural concept",
        "performance": "performance/installation",
        "product": "product design",
    }
    return formats.get(domain, "deliverable")


# ── Prior Art System ─────────────────────────────────────────────

def get_prior_art(
    project: ProjectBrief,
    ip_store: Dict[str, IPItem],
    stage: ProductionStage,
    current_production_id: Optional[str] = None,
) -> List[Dict]:
    """
    Find prior art relevant to this project and stage.
    Prior art = IP already produced for the same project brief
    (by previous teams/productions) or the same character/parcel
    at any stage up to and including this one.

    Returns a list of prior art items the team can see and decide
    whether to build on or diverge from.
    """
    stage_order = [
        ProductionStage.DEVELOPMENT,
        ProductionStage.PRE_PRODUCTION,
        ProductionStage.PRODUCTION,
        ProductionStage.POST_PRODUCTION,
        ProductionStage.DISTRIBUTION,
    ]
    current_stage_idx = stage_order.index(stage)

    prior = []
    for ip in ip_store.values():
        # Same project, earlier or current stage, from a different production run
        if ip.project_id == project.project_id:
            ip_stage_idx = stage_order.index(ip.stage_originated)
            # Include prior art from the same stage or earlier
            if ip_stage_idx <= current_stage_idx:
                prior.append({
                    "ip_id": ip.ip_id,
                    "title": ip.title,
                    "description": ip.description,
                    "domain": ip.domain.value,
                    "format": ip.format,
                    "practitioner_name": ip.practitioner_name,
                    "practice": ip.practice,
                    "stage": ip.stage_originated.value,
                    "production_title": ip.production_title,
                })

    return prior


# ── Main Production Engine ───────────────────────────────────────

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

    Different teams produce different outputs because:
    1. Each talent's practice inflects the deliverable title and approach
    2. Unlikely collisions depend on who's on the team
    3. Prior art from previous productions is visible — the team decides
       to build on it (bonus scores) or diverge (new IP)

    Returns a StageOutput dict with:
    - deliverables: what each team member produced
    - ip_generated: new IP items created
    - prior_art: what was already built by previous teams
    - prior_art_referenced: which prior art this team built on
    - cosm_delta / chron_delta: score changes
    - narrative: what happened at this stage
    - unlikely_outputs: unexpected IP from unlikely collisions
    """
    stage_defs = (DOMES_STAGES if project.game_type == GameType.DOMES
                  else SPHERES_STAGES)
    stage_def = stage_defs.get(stage)
    if not stage_def:
        return {"error": "Unknown stage"}

    # Phase 0: Gather prior art — what previous teams already built
    prior_art = get_prior_art(project, ip_store, stage)

    deliverables = []
    ip_generated = []
    unlikely_outputs = []
    prior_art_referenced = []
    capability_producers = {}

    # Phase 1: Required capability deliverables
    # Each talent's practice inflects what they produce
    for member in team.members:
        talent = roster.get(member.talent_id)
        if not talent:
            continue

        cap = _find_capability_for_talent(talent, project)
        if not cap:
            continue

        for (req_cap, ip_domain, title_template, desc_template) in stage_def["deliverable_types"]:
            if req_cap == cap and cap not in capability_producers:
                capability_producers[cap] = talent

                title = _format_template(title_template, project)
                desc = _format_template(desc_template, project)

                # Practice-specific inflection — THIS is why different teams
                # produce different outputs on the same project
                inflection, inflection_detail = _get_practice_inflection(talent)
                if inflection:
                    title = f"{title} ({inflection})"
                    desc = f"{desc}. {inflection_detail}"

                # Check if prior art exists for this capability
                # If so, this team is building on what came before
                relevant_prior = [
                    p for p in prior_art
                    if p["domain"] == ip_domain
                    and p["stage"] == stage.value
                ]
                built_on = None
                if relevant_prior:
                    built_on = relevant_prior[0]
                    prior_art_referenced.append(built_on)
                    desc = f"{desc}. Builds on prior work: \"{built_on['title']}\" by {built_on['practitioner_name']}"

                # Production number differentiator
                prod_label = f"[Production #{production_number}]" if production_number > 1 else ""
                if prod_label:
                    title = f"{title} {prod_label}"

                deliverable = {
                    "talent_id": talent.talent_id,
                    "talent_name": talent.name,
                    "practice": talent.domains_of_practice[0] if talent.domains_of_practice else "general",
                    "capability": cap,
                    "title": title,
                    "description": desc,
                    "ip_domain": ip_domain,
                    "stage": stage.value,
                    "is_unlikely": False,
                    "built_on": built_on["ip_id"] if built_on else None,
                }
                deliverables.append(deliverable)

                ip_item = IPItem(
                    ip_id=str(uuid.uuid4()),
                    domain=IPDomain(ip_domain),
                    title=f"{title} — {talent.name}",
                    description=desc,
                    format=_ip_format_for_domain(ip_domain),
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
                break

    # Phase 2: Unlikely collision deliverables
    for member in team.members:
        talent = roster.get(member.talent_id)
        if not talent:
            continue

        if talent.talent_id in [d["talent_id"] for d in deliverables]:
            continue

        unlikely_tag = _get_unlikely_tag(talent)
        if unlikely_tag and unlikely_tag in UNLIKELY_DELIVERABLE_TEMPLATES:
            ip_domain_str, title_template, desc_template = UNLIKELY_DELIVERABLE_TEMPLATES[unlikely_tag]

            title = _format_template(title_template, project)
            desc = _format_template(desc_template, project)

            # Practice inflection on unlikely too
            inflection, inflection_detail = _get_practice_inflection(talent)
            if inflection_detail:
                desc = f"{desc}. {inflection_detail}"

            if production_number > 1:
                title = f"{title} [Production #{production_number}]"

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
            }
            deliverables.append(deliverable)
            unlikely_outputs.append(deliverable)

            ip_item = IPItem(
                ip_id=str(uuid.uuid4()),
                domain=IPDomain(ip_domain_str),
                title=f"{title} — {talent.name}",
                description=desc,
                format=_ip_format_for_domain(ip_domain_str),
                project_id=project.project_id,
                production_title=f"{project.title} (#{production_number})" if production_number > 1 else project.title,
                practitioner_id=talent.talent_id,
                practitioner_name=talent.name,
                practice=talent.domains_of_practice[0] if talent.domains_of_practice else "general",
                stage_originated=stage,
                value_driver=f"Unlikely collision: {talent.name}'s {unlikely_tag} practice generates unexpected IP in {project.title}",
            )
            ip_generated.append(ip_item)
            ip_store[ip_item.ip_id] = ip_item

    # Phase 3: Score computation
    cosm_delta, chron_delta = _compute_stage_scores(
        stage, len(deliverables), len(team.members),
        len(unlikely_outputs), len(prior_art_referenced)
    )

    # Phase 4: Build narrative
    narrative = _build_stage_narrative(
        stage, stage_def, project, principal, deliverables,
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
                "ip_id": ip.ip_id,
                "domain": ip.domain.value,
                "title": ip.title,
                "description": ip.description,
                "format": ip.format,
                "practitioner_name": ip.practitioner_name,
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
    }


def _build_stage_narrative(
    stage: ProductionStage,
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
    game = "dome" if project.game_type == GameType.DOMES else "sphere"
    subject = ""
    if project.game_type == GameType.DOMES and project.character:
        subject = project.character.name
    elif project.game_type == GameType.SPHERES and project.parcel:
        subject = f"{project.parcel.address}, {project.parcel.neighborhood}"

    parts = []
    parts.append(f"**{stage_def['name']}** — {stage_def['focus']}")
    parts.append("")

    if production_number > 1:
        parts.append(f"*Production #{production_number}* — a new team brings a different perspective to {subject}.")
        parts.append("")

    # Prior art awareness
    if prior_art:
        parts.append(f"The team reviewed **{len(prior_art)} prior deliverables** already produced for this project.")
        if prior_art_referenced:
            parts.append(f"They chose to build on **{len(prior_art_referenced)}** of them, accelerating production:")
            for pa in prior_art_referenced:
                parts.append(f"  - Built on: *{pa['title']}* ({pa['practitioner_name']})")
        else:
            parts.append("They chose to diverge from all prior work — fresh perspective, new IP.")
        parts.append("")

    parts.append(f"Under {principal.name}'s direction, the team produced {len(deliverables)} deliverables for {subject}.")

    # Required deliverables
    required = [d for d in deliverables if not d["is_unlikely"]]
    if required:
        parts.append("")
        for d in required:
            parts.append(f"- **{d['talent_name']}** ({d['practice']}): *{d['title']}*")
            parts.append(f"  {d['description'][:150]}")

    # Unlikely collisions
    if unlikely_outputs:
        parts.append("")
        parts.append(f"**Unlikely collisions** ({len(unlikely_outputs)}):")
        for d in unlikely_outputs:
            parts.append(f"- **{d['talent_name']}** ({d['practice']}): *{d['title']}*")
            parts.append(f"  Nobody expected this. {d['description'][:120]}")

    # Scores
    parts.append("")
    score_note = f"Stage scores: **+{cosm_delta} Cosm**, **+{chron_delta} Chron**"
    if prior_art_referenced:
        score_note += f" (includes prior art bonus from {len(prior_art_referenced)} references)"
    parts.append(score_note)

    return "\n".join(parts)
