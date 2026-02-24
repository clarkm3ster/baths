"""
Chron Talent Agent — Game Orchestrator

Runs a complete DOMES or SPHERES production end-to-end:
  1. Take a project brief (character or parcel)
  2. Assign a principal
  3. Assemble a team via resonance matching
  4. Execute all 5 stages: Development → Distribution
  5. Score across all dimensions (Cosm 6 / Chron 5)
  6. Return complete production output with all deliverables,
     IP log, dimension scores, and citation sources.

The output is everything needed to declare the production complete.
"""

from typing import Dict, List, Optional
from datetime import datetime

from models import (
    TalentProfile, Principal, ProjectBrief, IPItem,
    TeamRecommendation, GameType, ProductionStage, ProjectStatus,
    Availability,
)
from assembly import assemble_team, recommend_principal
from production import execute_stage, get_prior_art
from scoring import score_stage_live, COSM_DIMENSIONS, CHRON_DIMENSIONS


STAGE_ORDER = [
    ProductionStage.DEVELOPMENT,
    ProductionStage.PRE_PRODUCTION,
    ProductionStage.PRODUCTION,
    ProductionStage.POST_PRODUCTION,
    ProductionStage.DISTRIBUTION,
]


def play_full_game(
    project: ProjectBrief,
    talent_roster: Dict[str, TalentProfile],
    principals: Dict[str, Principal],
    ip_store: Dict[str, IPItem],
    teams_store: Dict[str, TeamRecommendation],
    principal_id: Optional[str] = None,
    team_size: int = 6,
) -> Dict:
    """
    Play a complete game — all 5 stages — and return the full production output.
    This is the one-call version of the game pipeline.
    """

    # 1. Assign principal
    if principal_id and principal_id in principals:
        principal = principals[principal_id]
    else:
        principal = recommend_principal(project, list(principals.values()))
        if not principal:
            return {"error": "No available principals for this game type"}

    # 2. Assemble team
    roster_list = list(talent_roster.values())
    team = assemble_team(project, principal, roster_list, team_size)
    teams_store[project.project_id] = team

    # 3. Update project state
    project.principal_id = principal.principal_id
    project.team_ids = [m.talent_id for m in team.members]
    project.status = ProjectStatus.IN_PRODUCTION
    project.current_stage = ProductionStage.DEVELOPMENT
    project.started_at = datetime.utcnow()
    project.stage_log = []
    project.cosm_score = 0.0
    project.chron_score = 0.0

    # Mark talent as on_production
    for tid in project.team_ids:
        if tid in talent_roster:
            talent_roster[tid].availability = Availability.ON_PRODUCTION

    # 4. Execute all 5 stages
    stage_outputs = []
    dimension_snapshots = []

    for stage in STAGE_ORDER:
        project.current_stage = stage
        stage_output = execute_stage(
            project, principal, team, talent_roster,
            stage, ip_store,
            production_number=project.production_number,
        )
        project.stage_log.append(stage_output)
        project.cosm_score += stage_output.get("cosm_delta", 0)
        project.chron_score += stage_output.get("chron_delta", 0)
        stage_outputs.append(stage_output)

        # Live dimension scoring after each stage
        dim_snapshot = score_stage_live(project.game_type, project.stage_log)
        dimension_snapshots.append(dim_snapshot)

    # 5. Complete the production
    project.status = ProjectStatus.COMPLETED
    project.completed_at = datetime.utcnow()

    # Release talent
    for tid in project.team_ids:
        if tid in talent_roster:
            talent_roster[tid].availability = Availability.AVAILABLE
            talent_roster[tid].productions_completed.append(project.project_id)

    # Update principal
    if project.principal_id in principals:
        principals[project.principal_id].productions_led.append(project.project_id)

    # Distribute scores to talent
    for tid in project.team_ids:
        if tid in talent_roster:
            share = 1.0 / max(len(project.team_ids), 1)
            talent_roster[tid].total_cosm += project.cosm_score * share
            talent_roster[tid].total_chron += project.chron_score * share

    # Update principal scores
    if project.principal_id in principals:
        principals[project.principal_id].total_cosm += project.cosm_score
        principals[project.principal_id].total_chron += project.chron_score

    # 6. Final dimension scoring
    final_scores = score_stage_live(project.game_type, project.stage_log)

    # 7. Collect all IP generated
    project_ip = [
        ip for ip in ip_store.values()
        if ip.project_id == project.project_id
    ]

    # 8. Collect all sources cited
    sources = _collect_sources(project, stage_outputs)

    # 9. Build complete output
    return {
        "status": "completed",
        "project": project.model_dump(),
        "principal": {
            "id": principal.principal_id,
            "name": principal.name,
            "vision": principal.vision,
            "signature_style": principal.signature_style,
        },
        "team": {
            "members": [
                {
                    "talent_id": m.talent_id,
                    "talent_name": m.talent_name,
                    "resonance_score": m.resonance_score,
                    "reasoning": m.reasoning,
                    "capabilities_matched": m.capabilities_matched,
                    "unlikely_value": m.unlikely_value,
                }
                for m in team.members
            ],
            "team_strength": team.team_strength,
            "unlikely_collisions": team.unlikely_collisions,
            "capabilities_coverage": team.capabilities_coverage,
            "ip_surface_area": team.ip_surface_area,
        },
        "stages": stage_outputs,
        "dimension_progression": [s for s in dimension_snapshots],
        "final_scores": final_scores,
        "ip_log": [
            {
                "ip_id": ip.ip_id,
                "domain": ip.domain.value,
                "title": ip.title,
                "description": ip.description[:200],
                "format": ip.format,
                "practitioner_name": ip.practitioner_name,
                "practice": ip.practice,
                "stage": ip.stage_originated.value,
            }
            for ip in project_ip
        ],
        "sources_cited": sources,
        "summary": _build_summary(project, principal, team, final_scores, project_ip),
    }


def _collect_sources(project: ProjectBrief, stage_outputs: List[Dict]) -> List[Dict]:
    """Collect all real sources cited in the production."""
    sources = []
    seen = set()

    # Source: the character or parcel brief itself
    if project.game_type == GameType.DOMES and project.character:
        c = project.character
        key = f"source:{c.source}"
        if key not in seen:
            seen.add(key)
            sources.append({
                "type": "primary_source",
                "title": c.source,
                "citation": c.source_citation,
                "used_for": "Character brief — the person whose dome is being built",
            })

    if project.game_type == GameType.SPHERES and project.parcel:
        p = project.parcel
        sources.append({
            "type": "primary_source",
            "title": f"OpenDataPhilly: {p.address}",
            "citation": f"Philadelphia Office of Property Assessment via OpenDataPhilly. Parcel: {p.address}, {p.neighborhood}. Zoning: {p.zoning}. Lot: {p.lot_size_sqft:,.0f} sqft.",
            "used_for": "Parcel data — the site being activated",
        })
        sources.append({
            "type": "data_source",
            "title": "Philadelphia Land Bank Inventory",
            "citation": "Philadelphia Land Bank. Inventory of publicly-held vacant land. https://www.philadelphialandbank.org/",
            "used_for": "Vacancy status and ownership data",
        })

    # Source: government systems data (for DOMES)
    if project.game_type == GameType.DOMES and project.character:
        for sys_name in project.character.key_systems:
            key = f"system:{sys_name}"
            if key not in seen:
                seen.add(key)
                sources.append({
                    "type": "government_system",
                    "title": sys_name,
                    "citation": _system_citation(sys_name),
                    "used_for": f"System analysis — {sys_name} interactions with {project.character.name}",
                })

    # Source: practitioner body of work referenced in deliverables
    for stage_out in stage_outputs:
        for d in stage_out.get("deliverables", []):
            for w in d.get("work_referenced", []):
                key = f"work:{w['title']}"
                if key not in seen:
                    seen.add(key)
                    sources.append({
                        "type": "practitioner_work",
                        "title": w["title"],
                        "citation": f"{w['title']}. {w.get('description', '')} ({w.get('medium', 'work')}{', ' + str(w['year']) if w.get('year') else ''}).",
                        "used_for": f"Practitioner body of work — applied to {d.get('capability', 'production')}",
                    })

    return sources


def _system_citation(system_name: str) -> str:
    """Generate a citation for a government system based on known data."""
    citations = {
        "housing court": "Local Housing Court docket records. Privacy: state landlord-tenant law, court records.",
        "rental assistance": "Emergency Rental Assistance Program (ERAP). U.S. Treasury, 42 USC §3201.",
        "public housing": "Public Housing Authority (PHA). 24 CFR Part 960. Privacy: Privacy Act of 1974.",
        "TANF": "Temporary Assistance for Needy Families. 45 CFR Parts 260-265. Privacy: 42 USC §602.",
        "Medicaid": "Medicaid Management Information System (MMIS). Privacy: HIPAA, 42 CFR Part 431.",
        "public schools": "State Department of Education student records. Privacy: FERPA, 20 USC §1232g.",
        "employment services": "State Workforce Development system. Wagner-Peyser Act, WIOA.",
        "homeless shelter system": "Homeless Management Information System (HMIS). Privacy: HUD CoC Standards, VAWA.",
        "child welfare": "State Automated Child Welfare Information System (SACWIS). Privacy: CAPTA, state child welfare law.",
        "family court": "Family Court case management system. Privacy: state family law, sealed records.",
        "SNAP": "Supplemental Nutrition Assistance Program. 7 CFR Part 273. Privacy: 7 USC §2020(e)(8).",
        "juvenile justice": "Juvenile Justice Information System. Privacy: JJDPA, state juvenile records law.",
        "substance abuse treatment": "Behavioral Health Authority system. Privacy: 42 CFR Part 2, HIPAA.",
        "workforce development": "WIOA system. Workforce Innovation and Opportunity Act, 29 USC §3101.",
        "EITC": "Earned Income Tax Credit. IRS 26 USC §32. Privacy: IRC §6103.",
        "Medicaid expansion": "Medicaid Expansion under ACA. 42 USC §1396a(a)(10)(A)(i)(VIII). Privacy: HIPAA.",
        "Section 8": "Housing Choice Voucher Program. 24 CFR Part 982. Privacy: Privacy Act of 1974.",
        "CHIP": "Children's Health Insurance Program. 42 USC §1397aa. Privacy: HIPAA.",
        "transportation": "Transit benefit programs. State/local transit authority.",
        "childcare subsidies": "Child Care and Development Fund (CCDF). 45 CFR Parts 98-99.",
        "homelessness prevention": "HUD Continuum of Care, ESG programs. 24 CFR Part 576.",
        "public education": "State Department of Education. Privacy: FERPA, 20 USC §1232g.",
        "housing assistance": "HUD housing assistance programs. 24 CFR Parts 5, 982.",
    }
    return citations.get(system_name, f"{system_name}. Federal/state program records.")


def _build_summary(
    project: ProjectBrief,
    principal: Principal,
    team: TeamRecommendation,
    scores: Dict,
    ip_items: list,
) -> str:
    """Build the production summary narrative."""
    game = "dome" if project.game_type == GameType.DOMES else "sphere"
    score_name = "Cosm" if project.game_type == GameType.DOMES else "Chron"

    if project.game_type == GameType.DOMES and project.character:
        subject = project.character.name
        subject_detail = f"sourced from {project.character.source}"
    elif project.game_type == GameType.SPHERES and project.parcel:
        subject = project.parcel.address
        subject_detail = f"{project.parcel.neighborhood}, {project.parcel.city}"
    else:
        subject = project.title
        subject_detail = ""

    dims = scores.get("dimensions", {})
    total = scores.get("total", 0)
    weakest = scores.get("weakest", "unknown")
    strongest = scores.get("strongest", "unknown")
    dim_details = scores.get("dimension_details", {})

    parts = []
    parts.append(f"# {project.title}")
    parts.append(f"**{game.upper()}** production — {subject} ({subject_detail})")
    parts.append(f"Principal: **{principal.name}**")
    parts.append(f"Team: {len(team.members)} practitioners")
    parts.append("")

    parts.append(f"## Final {score_name} Score: {total}")
    parts.append(f"The {game} is only as strong as its weakest dimension.")
    parts.append("")

    for dim_key, dim_score in sorted(dims.items(), key=lambda x: x[1], reverse=True):
        detail = dim_details.get(dim_key, {})
        label = detail.get("label", dim_key)
        marker = " ← weakest" if dim_key == weakest else ""
        marker = " ← strongest" if dim_key == strongest else marker
        parts.append(f"  {label}: **{dim_score}**{marker}")

    parts.append("")
    parts.append(f"## IP Generated: {len(ip_items)} items")

    domain_counts = {}
    for ip in ip_items:
        d = ip.domain.value
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        parts.append(f"  {domain.replace('_', ' ').title()}: {count}")

    parts.append("")
    if team.unlikely_collisions:
        parts.append(f"## Unlikely Collisions: {len(team.unlikely_collisions)}")
        for uc in team.unlikely_collisions:
            parts.append(f"  - {uc}")

    return "\n".join(parts)
