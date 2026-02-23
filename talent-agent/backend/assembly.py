"""
Chron Talent Agent — Team Assembly Engine
Resonance-based matching, not role-filling.
The question is: what does this person's body of work bring to THIS production?
"""

from typing import List, Dict, Optional
from models import (
    TalentProfile, Principal, ProjectBrief, TeamRecommendation,
    ResonanceMatch, GameType, Availability
)
import random


# Capabilities required by game type (team must collectively cover these)
DOMES_CAPABILITIES = {
    "legal_navigation": "Someone who can navigate the legal entitlement landscape",
    "data_systems": "Someone who can work with data systems and cost modeling",
    "narrative": "Someone who can tell the story",
    "flourishing_design": "Someone who can design what flourishing looks like for this specific person",
}

SPHERES_CAPABILITIES = {
    "spatial_legal": "Someone who can read the parcel, zoning, and permit landscape",
    "activation_design": "Someone who can design the activation",
    "economics": "Someone who can model the economics",
    "narrative": "Someone who can document and tell the story",
}

# Resonance tag mappings to capabilities
TAG_TO_DOMES_CAPABILITY = {
    "law": "legal_navigation", "rights": "legal_navigation", "legal": "legal_navigation",
    "entitlement": "legal_navigation", "constitution": "legal_navigation",
    "data": "data_systems", "systems": "data_systems", "modeling": "data_systems",
    "cost": "data_systems", "software": "data_systems", "API": "data_systems",
    "technology": "data_systems", "government": "data_systems",
    "narrative": "narrative", "storytelling": "narrative", "film": "narrative",
    "documentary": "narrative", "illustration": "narrative", "voice": "narrative",
    "graphic-novel": "narrative", "visualization": "narrative",
    "housing": "flourishing_design", "care": "flourishing_design",
    "dignity": "flourishing_design", "wellbeing": "flourishing_design",
    "community": "flourishing_design", "food": "flourishing_design",
    "health": "flourishing_design", "healthcare": "flourishing_design",
    "body": "flourishing_design", "environment": "flourishing_design",
    "autonomy": "flourishing_design", "healing": "flourishing_design",
}

TAG_TO_SPHERES_CAPABILITY = {
    "law": "spatial_legal", "legal": "spatial_legal", "rights": "spatial_legal",
    "landscape": "spatial_legal", "soil": "spatial_legal", "brownfield": "spatial_legal",
    "land": "spatial_legal",
    "art": "activation_design", "mural": "activation_design",
    "public-space": "activation_design", "space": "activation_design",
    "community": "activation_design", "sound": "activation_design",
    "music": "activation_design", "gathering": "activation_design",
    "transformation": "activation_design", "craft": "activation_design",
    "public-art": "activation_design", "expression": "activation_design",
    "finance": "economics", "bonds": "economics", "impact": "economics",
    "microfinance": "economics", "value": "economics",
    "narrative": "narrative", "storytelling": "narrative", "film": "narrative",
    "documentary": "narrative", "illustration": "narrative",
    "graphic-novel": "narrative", "visualization": "narrative",
}


def _compute_resonance(talent: TalentProfile, project: ProjectBrief) -> ResonanceMatch:
    """Compute how a talent's practice resonates with a specific project."""
    score = 0.0
    reasons = []
    caps_matched = []
    unlikely = ""

    # Extract project keywords based on type
    if project.game_type == GameType.DOMES and project.character:
        char = project.character
        project_tags = set()
        for dim in char.flourishing_dimensions:
            project_tags.add(dim.lower())
        for sys in char.key_systems:
            for word in sys.lower().split():
                project_tags.add(word)
        # Add words from situation and challenge
        for word in char.production_challenge.lower().split():
            if len(word) > 4:
                project_tags.add(word)
        tag_cap_map = TAG_TO_DOMES_CAPABILITY
    elif project.game_type == GameType.SPHERES and project.parcel:
        parcel = project.parcel
        project_tags = set()
        for word in parcel.opportunity.lower().split():
            if len(word) > 4:
                project_tags.add(word)
        for word in parcel.community_context.lower().split():
            if len(word) > 4:
                project_tags.add(word)
        for c in parcel.constraints:
            for word in c.lower().split():
                if len(word) > 4:
                    project_tags.add(word)
        tag_cap_map = TAG_TO_SPHERES_CAPABILITY
    else:
        return ResonanceMatch(
            talent_id=talent.talent_id,
            talent_name=talent.name,
            resonance_score=0,
            reasoning="Project brief incomplete",
        )

    # Score based on tag overlap
    talent_tags = set(t.lower() for t in talent.resonance_tags)
    overlap = talent_tags & project_tags
    tag_score = min(len(overlap) * 8, 30)
    score += tag_score

    # Score based on domain overlap with project flourishing dimensions
    domain_tags = set(d.lower() for d in talent.domains_of_practice)
    domain_overlap = 0
    for domain in domain_tags:
        for ptag in project_tags:
            if ptag in domain or domain in ptag:
                domain_overlap += 1
    domain_score = min(domain_overlap * 5, 25)
    score += domain_score

    # Score based on capabilities matched
    for tag in talent_tags:
        cap = tag_cap_map.get(tag)
        if cap and cap not in caps_matched:
            caps_matched.append(cap)
            score += 10

    # Cap capability score contribution
    cap_score = min(len(caps_matched) * 10, 25)
    score = score - (len(caps_matched) * 10) + cap_score

    # Body of work relevance
    work_score = 0
    for work in talent.body_of_work:
        work_text = (work.title + " " + work.description).lower()
        work_relevance = sum(1 for ptag in project_tags if ptag in work_text)
        work_score += work_relevance * 3
    work_score = min(work_score, 20)
    score += work_score

    # Clamp
    score = min(score, 100)

    # Build reasoning
    if overlap:
        reasons.append(f"Direct practice overlap: {', '.join(list(overlap)[:4])}")
    if domain_overlap > 0:
        reasons.append(f"Domain expertise intersects with {domain_overlap} project dimensions")
    if work_score > 5:
        reasons.append(f"Body of work directly relevant to this production")

    # Generate reasoning about what their practice brings
    practice_desc = talent.approach[:120] if talent.approach else talent.bio[:120]
    reasons.append(f"Brings: {practice_desc}")

    # Unlikely value — the most interesting thing they bring
    if score < 40 and score > 15:
        unlikely = f"Unexpected perspective: {talent.domains_of_practice[0] if talent.domains_of_practice else 'unique practice'} applied to {'dome construction' if project.game_type == GameType.DOMES else 'space activation'}"
    elif any(tag in talent_tags for tag in ["perfume", "scent", "blacksmith", "forge", "midwife", "dance", "choreography"]):
        unlikely = f"Unlikely collision: {talent.name}'s practice in {talent.domains_of_practice[0]} reframes how the team thinks about {'human flourishing' if project.game_type == GameType.DOMES else 'space activation'}"

    return ResonanceMatch(
        talent_id=talent.talent_id,
        talent_name=talent.name,
        resonance_score=round(score, 1),
        reasoning=" | ".join(reasons),
        capabilities_matched=caps_matched,
        unlikely_value=unlikely,
    )


def recommend_principal(
    project: ProjectBrief,
    principals: List[Principal],
) -> Optional[Principal]:
    """Recommend a principal for a project based on game type and vision alignment."""
    matching = [p for p in principals
                if p.game_type == project.game_type
                and p.availability != Availability.UNAVAILABLE]
    if not matching:
        matching = [p for p in principals if p.game_type is None]
    if not matching:
        return None
    # For now: weighted random selection favoring available principals
    available = [p for p in matching if p.availability == Availability.AVAILABLE]
    return random.choice(available) if available else random.choice(matching)


def assemble_team(
    project: ProjectBrief,
    principal: Principal,
    roster: List[TalentProfile],
    team_size: int = 6,
) -> TeamRecommendation:
    """
    Assemble a team based on resonance between each person's practice
    and the specific production challenge. Not role-filling — genuine matchmaking.
    """
    # Score every available talent
    available = [t for t in roster if t.availability != Availability.UNAVAILABLE]
    scored = [(t, _compute_resonance(t, project)) for t in available]
    scored.sort(key=lambda x: x[1].resonance_score, reverse=True)

    # Select team: take top resonators but ensure capability coverage
    required_caps = (DOMES_CAPABILITIES if project.game_type == GameType.DOMES
                     else SPHERES_CAPABILITIES)
    covered = set()
    selected: List[ResonanceMatch] = []
    unlikely_collisions = []

    # First pass: top resonators
    for talent, match in scored:
        if len(selected) >= team_size:
            break
        selected.append(match)
        covered.update(match.capabilities_matched)
        if match.unlikely_value:
            unlikely_collisions.append(match.unlikely_value)

    # Second pass: fill capability gaps if needed
    if len(covered) < len(required_caps):
        missing = set(required_caps.keys()) - covered
        for talent, match in scored:
            if match.talent_id in [s.talent_id for s in selected]:
                continue
            if any(cap in missing for cap in match.capabilities_matched):
                if len(selected) < team_size + 2:  # Allow slight oversize for gaps
                    selected.append(match)
                    covered.update(match.capabilities_matched)
                    missing = set(required_caps.keys()) - covered
                    if not missing:
                        break

    # Build capabilities coverage
    cap_coverage = {cap: cap in covered for cap in required_caps}

    # Determine expected IP domains
    ip_domains = set()
    for match in selected:
        for tag in [m.talent_name for m in selected]:
            pass  # IP domains come from the diversity of practices
    # Map practices to IP domains
    practice_to_ip = {
        "film": "entertainment", "documentary": "entertainment", "narrative": "entertainment",
        "software": "technology", "data": "technology", "API": "technology",
        "finance": "financial_product", "bonds": "financial_product",
        "law": "policy", "legal": "policy", "rights": "policy",
        "housing": "housing", "shelter": "housing",
        "healthcare": "healthcare", "care": "healthcare",
        "architecture": "architectural", "design": "urban_design",
        "fashion": "fashion", "food": "culinary",
        "performance": "performance", "dance": "performance",
    }
    for match in selected:
        # Find the talent to get their tags
        talent = next((t for t in roster if t.talent_id == match.talent_id), None)
        if talent:
            for tag in talent.resonance_tags:
                domain = practice_to_ip.get(tag)
                if domain:
                    ip_domains.add(domain)

    # Team strength narrative
    practice_names = []
    for match in selected:
        talent = next((t for t in roster if t.talent_id == match.talent_id), None)
        if talent and talent.domains_of_practice:
            practice_names.append(talent.domains_of_practice[0])
    strength = f"This team combines {', '.join(practice_names[:4])} — practices that don't normally sit at the same table. "
    if unlikely_collisions:
        strength += f"The unlikely pairings ({len(unlikely_collisions)}) will generate IP in domains nobody anticipated."
    else:
        strength += "Deep resonance across multiple dimensions of this production challenge."

    return TeamRecommendation(
        project_id=project.project_id,
        principal_id=principal.principal_id,
        principal_name=principal.name,
        members=selected,
        team_strength=strength,
        unlikely_collisions=unlikely_collisions,
        capabilities_coverage=cap_coverage,
        ip_surface_area=sorted(ip_domains),
    )
