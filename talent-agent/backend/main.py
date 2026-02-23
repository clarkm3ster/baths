"""
Chron Talent Agent — Main API
talent.baths.cc
Roster, principals, project sourcing, team assembly, IP tracking, leaderboard
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import Optional, Dict, List, Any
import uuid
import os
import logging

from models import (
    TalentProfile, Principal, ProjectBrief, IPItem,
    TeamRecommendation, ResonanceMatch, LeaderboardEntry,
    GameType, ProductionStage, ProjectStatus, Availability, IPDomain,
    WorkItem, CharacterBrief, ParcelBrief,
)
from assembly import assemble_team, recommend_principal, _compute_resonance
from seed import SEED_TALENT, SEED_PRINCIPALS, SEED_PROJECTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("talent-agent")


# ── In-memory storage ────────────────────────────────────────────

talent_roster: Dict[str, TalentProfile] = {}
principals: Dict[str, Principal] = {}
projects: Dict[str, ProjectBrief] = {}
ip_items: Dict[str, IPItem] = {}
teams: Dict[str, TeamRecommendation] = {}  # keyed by project_id


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Seed data on startup."""
    logger.info("Initializing Chron Talent Agent...")

    # Seed roster
    for t in SEED_TALENT:
        talent_roster[t.talent_id] = t
    logger.info(f"Roster: {len(talent_roster)} practitioners")

    # Seed principals
    for p in SEED_PRINCIPALS:
        principals[p.principal_id] = p
    logger.info(f"Principals: {len(principals)} production leaders")

    # Seed projects
    for proj in SEED_PROJECTS:
        projects[proj.project_id] = proj
    logger.info(f"Projects: {len(projects)} briefs sourced")

    yield


app = FastAPI(
    title="Chron Talent Agent",
    description="Recruits talent, assembles multi-disciplinary production teams, assigns projects, tracks productions",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════════════════
# ROSTER — every person profiled by practice
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/roster")
def list_roster(
    domain: Optional[str] = None,
    availability: Optional[str] = None,
    search: Optional[str] = None,
):
    """List all talent on the roster, optionally filtered."""
    results = list(talent_roster.values())

    if domain:
        results = [t for t in results
                   if any(domain.lower() in d.lower() for d in t.domains_of_practice)]
    if availability:
        results = [t for t in results if t.availability.value == availability]
    if search:
        q = search.lower()
        results = [t for t in results
                   if q in t.name.lower()
                   or q in t.bio.lower()
                   or any(q in d.lower() for d in t.domains_of_practice)
                   or any(q in tag.lower() for tag in t.resonance_tags)]

    return {"roster": results, "total": len(results)}


@app.get("/api/roster/{talent_id}")
def get_talent(talent_id: str):
    """Get a talent profile by ID."""
    if talent_id not in talent_roster:
        raise HTTPException(status_code=404, detail="Talent not found")
    return talent_roster[talent_id]


@app.post("/api/roster")
def add_talent(talent: TalentProfile):
    """Add a new person to the roster."""
    if not talent.talent_id:
        talent.talent_id = str(uuid.uuid4())
    talent_roster[talent.talent_id] = talent
    return talent


@app.get("/api/roster/{talent_id}/resonance/{project_id}")
def talent_project_resonance(talent_id: str, project_id: str):
    """See how a specific talent resonates with a specific project."""
    if talent_id not in talent_roster:
        raise HTTPException(status_code=404, detail="Talent not found")
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    match = _compute_resonance(talent_roster[talent_id], projects[project_id])
    return match


# ═══════════════════════════════════════════════════════════════════
# PRINCIPALS — top-tier production leaders
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/principals")
def list_principals(game_type: Optional[str] = None):
    """List all principals, optionally filtered by game type."""
    results = list(principals.values())
    if game_type:
        results = [p for p in results
                   if p.game_type is None or p.game_type.value == game_type]
    return {"principals": results, "total": len(results)}


@app.get("/api/principals/{principal_id}")
def get_principal(principal_id: str):
    """Get a principal by ID."""
    if principal_id not in principals:
        raise HTTPException(status_code=404, detail="Principal not found")
    return principals[principal_id]


# ═══════════════════════════════════════════════════════════════════
# PROJECTS — sourced characters and parcels
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/projects")
def list_projects(
    game_type: Optional[str] = None,
    status: Optional[str] = None,
):
    """List all projects, optionally filtered."""
    results = list(projects.values())
    if game_type:
        results = [p for p in results if p.game_type.value == game_type]
    if status:
        results = [p for p in results if p.status.value == status]
    return {"projects": results, "total": len(results)}


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    """Get a project brief by ID."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    project = projects[project_id]
    # Include team if assembled
    team = teams.get(project_id)
    return {"project": project, "team": team}


@app.post("/api/projects")
def create_project(project: ProjectBrief):
    """Create a new project brief."""
    if not project.project_id:
        project.project_id = str(uuid.uuid4())
    projects[project.project_id] = project
    return project


# ═══════════════════════════════════════════════════════════════════
# TEAM ASSEMBLY — resonance-based matching
# ═══════════════════════════════════════════════════════════════════

@app.post("/api/projects/{project_id}/assemble")
def assemble_project_team(
    project_id: str,
    principal_id: Optional[str] = None,
    team_size: int = 6,
):
    """Assemble a team for a project. The agent recommends based on resonance."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]

    # Select or assign principal
    if principal_id:
        if principal_id not in principals:
            raise HTTPException(status_code=404, detail="Principal not found")
        principal = principals[principal_id]
    else:
        principal = recommend_principal(project, list(principals.values()))
        if not principal:
            raise HTTPException(status_code=400, detail="No available principals for this game type")

    # Assemble team
    roster = list(talent_roster.values())
    team = assemble_team(project, principal, roster, team_size)

    # Store
    teams[project_id] = team
    project.principal_id = principal.principal_id
    project.team_ids = [m.talent_id for m in team.members]
    project.status = ProjectStatus.ASSEMBLING

    return team


@app.get("/api/projects/{project_id}/team")
def get_project_team(project_id: str):
    """Get the assembled team for a project."""
    if project_id not in teams:
        raise HTTPException(status_code=404, detail="No team assembled for this project")
    return teams[project_id]


@app.post("/api/projects/{project_id}/start")
def start_project_production(project_id: str):
    """Start a project's production — move from assembling to in_production."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    if not project.principal_id or not project.team_ids:
        raise HTTPException(status_code=400, detail="Team not assembled yet")

    project.status = ProjectStatus.IN_PRODUCTION
    project.current_stage = ProductionStage.DEVELOPMENT
    from datetime import datetime
    project.started_at = datetime.utcnow()

    # Mark team members as on_production
    for tid in project.team_ids:
        if tid in talent_roster:
            talent_roster[tid].availability = Availability.ON_PRODUCTION

    return {"status": "started", "project": project}


@app.post("/api/projects/{project_id}/advance")
def advance_project_stage(project_id: str):
    """Advance a project to the next production stage."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    project = projects[project_id]
    if project.status != ProjectStatus.IN_PRODUCTION:
        raise HTTPException(status_code=400, detail="Project not in production")

    stage_order = [
        ProductionStage.DEVELOPMENT,
        ProductionStage.PRE_PRODUCTION,
        ProductionStage.PRODUCTION,
        ProductionStage.POST_PRODUCTION,
        ProductionStage.DISTRIBUTION,
    ]

    current_idx = stage_order.index(project.current_stage)
    if current_idx >= len(stage_order) - 1:
        # Complete the production
        project.status = ProjectStatus.COMPLETED
        from datetime import datetime
        project.completed_at = datetime.utcnow()

        # Release team members
        for tid in project.team_ids:
            if tid in talent_roster:
                talent_roster[tid].availability = Availability.AVAILABLE
                talent_roster[tid].productions_completed.append(project_id)

        # Update principal
        if project.principal_id in principals:
            principals[project.principal_id].productions_led.append(project_id)

        return {"status": "completed", "project": project}

    project.current_stage = stage_order[current_idx + 1]
    return {"status": "advanced", "stage": project.current_stage, "project": project}


# ═══════════════════════════════════════════════════════════════════
# IP TRACKING — every innovation categorized and attributed
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/ip")
def list_ip(
    domain: Optional[str] = None,
    project_id: Optional[str] = None,
    practitioner_id: Optional[str] = None,
    search: Optional[str] = None,
):
    """List all IP items, with filtering."""
    results = list(ip_items.values())
    if domain:
        results = [i for i in results if i.domain.value == domain]
    if project_id:
        results = [i for i in results if i.project_id == project_id]
    if practitioner_id:
        results = [i for i in results if i.practitioner_id == practitioner_id]
    if search:
        q = search.lower()
        results = [i for i in results
                   if q in i.title.lower() or q in i.description.lower()]

    # Aggregate by domain
    domain_counts = {}
    for item in list(ip_items.values()):
        d = item.domain.value
        domain_counts[d] = domain_counts.get(d, 0) + 1

    return {
        "ip_items": results,
        "total": len(results),
        "by_domain": domain_counts,
    }


@app.post("/api/ip")
def create_ip(item: IPItem):
    """Log a new IP item."""
    if not item.ip_id:
        item.ip_id = str(uuid.uuid4())
    ip_items[item.ip_id] = item
    return item


@app.get("/api/ip/domains")
def ip_domains():
    """Get all IP domains with counts."""
    counts = {}
    for item in ip_items.values():
        d = item.domain.value
        counts[d] = counts.get(d, 0) + 1
    return {
        "domains": [
            {"domain": d.value, "label": d.value.replace("_", " ").title(), "count": counts.get(d.value, 0)}
            for d in IPDomain
        ]
    }


# ═══════════════════════════════════════════════════════════════════
# LEADERBOARD — individuals and teams
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/leaderboard")
def get_leaderboard(sort_by: str = "flourishing"):
    """Get the leaderboard — talent and principals ranked."""
    entries = []

    # Talent entries
    for t in talent_roster.values():
        ip_count = len([i for i in ip_items.values() if i.practitioner_id == t.talent_id])
        ip_doms = list(set(i.domain.value for i in ip_items.values() if i.practitioner_id == t.talent_id))
        entries.append(LeaderboardEntry(
            id=t.talent_id,
            name=t.name,
            role="talent",
            productions_completed=len(t.productions_completed),
            total_cosm=t.total_cosm,
            total_chron=t.total_chron,
            flourishing=t.total_cosm * t.total_chron,
            ip_count=ip_count,
            ip_domains=ip_doms,
            domains_of_practice=t.domains_of_practice,
        ))

    # Principal entries
    for p in principals.values():
        entries.append(LeaderboardEntry(
            id=p.principal_id,
            name=p.name,
            role="principal",
            productions_completed=len(p.productions_led),
            total_cosm=p.total_cosm,
            total_chron=p.total_chron,
            flourishing=p.total_cosm * p.total_chron,
            ip_count=0,
            ip_domains=[],
            domains_of_practice=[],
        ))

    # Sort
    if sort_by == "cosm":
        entries.sort(key=lambda e: e.total_cosm, reverse=True)
    elif sort_by == "chron":
        entries.sort(key=lambda e: e.total_chron, reverse=True)
    elif sort_by == "ip":
        entries.sort(key=lambda e: e.ip_count, reverse=True)
    elif sort_by == "productions":
        entries.sort(key=lambda e: e.productions_completed, reverse=True)
    else:
        entries.sort(key=lambda e: e.flourishing, reverse=True)

    return {"leaderboard": entries, "total": len(entries)}


# ═══════════════════════════════════════════════════════════════════
# STATS & OVERVIEW
# ═══════════════════════════════════════════════════════════════════

@app.get("/api/stats")
def get_stats():
    """Overview stats for the talent agent dashboard."""
    active_productions = [p for p in projects.values() if p.status == ProjectStatus.IN_PRODUCTION]
    completed = [p for p in projects.values() if p.status in (ProjectStatus.COMPLETED, ProjectStatus.PUBLISHED)]
    sourced = [p for p in projects.values() if p.status == ProjectStatus.SOURCED]

    return {
        "roster_size": len(talent_roster),
        "principals_count": len(principals),
        "projects_sourced": len(sourced),
        "active_productions": len(active_productions),
        "completed_productions": len(completed),
        "total_ip": len(ip_items),
        "available_talent": len([t for t in talent_roster.values() if t.availability == Availability.AVAILABLE]),
        "domes_projects": len([p for p in projects.values() if p.game_type == GameType.DOMES]),
        "spheres_projects": len([p for p in projects.values() if p.game_type == GameType.SPHERES]),
    }


@app.get("/api/health")
def health():
    """Health check."""
    return {
        "status": "ok",
        "service": "Chron Talent Agent",
        "version": "1.0.0",
        "roster_size": len(talent_roster),
        "principals": len(principals),
        "projects": len(projects),
    }


# ═══════════════════════════════════════════════════════════════════
# SERVE FRONTEND
# ═══════════════════════════════════════════════════════════════════

if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes."""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
