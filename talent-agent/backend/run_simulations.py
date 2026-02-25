#!/usr/bin/env python3
"""
Run full end-to-end simulated productions:
  1. DOMES — The Dasani Production (project-001)
  2. SPHERES — The North Philadelphia Activation (project-009)

Captures all output: deliverables, IP logs, scorecards, sources, JSON data.
Publishes to production_files/ for portfolio display.
"""

import sys
import os
import json
import copy
from datetime import datetime

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from models import (
    TalentProfile, Principal, ProjectBrief, IPItem,
    TeamRecommendation, GameType, ProjectStatus,
)
from games import play_full_game
from files import generate_production_files
from seed import SEED_TALENT, SEED_PRINCIPALS, SEED_PROJECTS


def init_stores():
    """Initialize in-memory stores from seed data."""
    talent_roster = {}
    for t in SEED_TALENT:
        talent_roster[t.talent_id] = copy.deepcopy(t)

    principals_store = {}
    for p in SEED_PRINCIPALS:
        principals_store[p.principal_id] = copy.deepcopy(p)

    projects_store = {}
    for proj in SEED_PROJECTS:
        projects_store[proj.project_id] = copy.deepcopy(proj)

    ip_store = {}
    teams_store = {}

    return talent_roster, principals_store, projects_store, ip_store, teams_store


def run_production(project_id, principal_id=None, team_size=6):
    """Run a full production end-to-end and generate all output files."""
    talent_roster, principals, projects, ip_store, teams_store = init_stores()

    project = projects.get(project_id)
    if not project:
        print(f"ERROR: Project {project_id} not found in seed data")
        return None

    game_type = "DOMES" if project.game_type == GameType.DOMES else "SPHERES"
    print(f"\n{'='*70}")
    print(f"  RUNNING: {project.title}")
    print(f"  Game: {game_type}")
    if project.character:
        print(f"  Character: {project.character.name}")
        print(f"  Source: {project.character.source}")
        print(f"  Systems: {', '.join(project.character.key_systems)}")
    elif project.parcel:
        print(f"  Parcel: {project.parcel.address}")
        print(f"  Neighborhood: {project.parcel.neighborhood}")
        print(f"  Zoning: {project.parcel.zoning}")
        print(f"  Lot: {project.parcel.lot_size_sqft:,.0f} sqft")
    print(f"{'='*70}\n")

    # Run the full game
    print("Starting production...")
    game_output = play_full_game(
        project=project,
        talent_roster=talent_roster,
        principals=principals,
        ip_store=ip_store,
        teams_store=teams_store,
        principal_id=principal_id,
        team_size=team_size,
    )

    if "error" in game_output:
        print(f"ERROR: {game_output['error']}")
        return None

    # Print production summary
    print_production_summary(game_output)

    # Generate all output files
    print("\nGenerating production files...")
    files = generate_production_files(game_output)
    print(f"Generated {len(files)} files:")
    for name, path in files.items():
        size = os.path.getsize(path)
        print(f"  {name}: {path} ({size:,} bytes)")

    return game_output, files


def print_production_summary(output):
    """Print a detailed summary of the production."""
    project = output.get("project", {})
    principal = output.get("principal", {})
    team = output.get("team", {})
    stages = output.get("stages", [])
    scores = output.get("final_scores", {})
    ip_log = output.get("ip_log", [])
    sources = output.get("sources_cited", [])

    game_type = project.get("game_type", "")
    score_name = "Cosm" if game_type == "domes" else "Chron"

    print(f"\n--- PRINCIPAL ---")
    print(f"  {principal.get('name', 'Unknown')}")
    print(f"  Vision: {principal.get('vision', '')[:120]}...")

    print(f"\n--- TEAM ({len(team.get('members', []))} practitioners) ---")
    print(f"  Strength: {team.get('team_strength', '')[:150]}...")
    for m in team.get("members", []):
        caps = ", ".join(m.get("capabilities_matched", []))
        print(f"  - {m['talent_name']} (resonance: {m['resonance_score']:.0f}) — {caps}")

    if team.get("unlikely_collisions"):
        print(f"\n  Unlikely Collisions:")
        for uc in team["unlikely_collisions"]:
            print(f"    - {uc[:120]}")

    print(f"\n--- STAGE PROGRESSION ---")
    progression = output.get("dimension_progression", [])
    for i, stage_out in enumerate(stages):
        stage_name = stage_out.get("stage_name", f"Stage {i+1}")
        deliverable_count = len(stage_out.get("deliverables", []))
        ip_count = stage_out.get("ip_count", 0)
        unlikely_count = stage_out.get("unlikely_count", 0)

        snap = progression[i] if i < len(progression) else {}
        total = snap.get("total", 0)

        print(f"\n  {stage_name}:")
        print(f"    Focus: {stage_out.get('focus', '')[:100]}")
        print(f"    Deliverables: {deliverable_count} | IP Items: {ip_count} | Unlikely: {unlikely_count}")
        print(f"    {score_name} after stage: {total}")

        # Print deliverable titles
        for d in stage_out.get("deliverables", []):
            unlikely_tag = " [UNLIKELY]" if d.get("is_unlikely") else ""
            print(f"      > {d.get('title', '')} — {d.get('talent_name', '')}{unlikely_tag}")

    print(f"\n--- FINAL {score_name.upper()} SCORES ---")
    print(f"  Total: {scores.get('total', 0)}")
    print(f"  Weakest: {scores.get('weakest', 'N/A')}")
    print(f"  Strongest: {scores.get('strongest', 'N/A')}")
    dims = scores.get("dimensions", {})
    dim_details = scores.get("dimension_details", {})
    for dk in sorted(dims.keys(), key=lambda k: dims[k], reverse=True):
        det = dim_details.get(dk, {})
        print(f"    {det.get('label', dk)}: {dims[dk]}")

    print(f"\n--- IP LOG ({len(ip_log)} items) ---")
    domain_counts = {}
    for ip in ip_log:
        d = ip.get("domain", "other")
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    {domain.replace('_', ' ').title()}: {count}")

    print(f"\n--- SOURCES ({len(sources)} cited) ---")
    for s in sources[:5]:
        print(f"    {s.get('type', '')}: {s.get('title', '')}")
    if len(sources) > 5:
        print(f"    ... and {len(sources) - 5} more")

    print(f"\n--- PRODUCTION SUMMARY ---")
    print(output.get("summary", "No summary generated"))


if __name__ == "__main__":
    print("=" * 70)
    print("  BATHS PRODUCTION SIMULATOR")
    print(f"  {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)

    # ── PRODUCTION 1: Dasani (DOMES) ──────────────────────────────
    # Ava DuVernay directs — her vision centers the person's experience
    # of being inside the system looking out
    print("\n\n>>> PRODUCTION 1: THE DASANI PRODUCTION (DOMES)")
    dasani_result = run_production(
        project_id="project-001",
        principal_id="principal-003",  # Ava DuVernay
        team_size=6,
    )

    # ── PRODUCTION 2: North Philadelphia Parcel (SPHERES) ─────────
    # James Corner / Field Operations directs — infrastructure into
    # public life, long-term ecological thinking
    print("\n\n>>> PRODUCTION 2: THE NORTH PHILADELPHIA ACTIVATION (SPHERES)")
    philly_result = run_production(
        project_id="project-009",
        principal_id="principal-009",  # James Corner / Field Operations
        team_size=6,
    )

    print("\n\n" + "=" * 70)
    print("  SIMULATION COMPLETE")
    print("=" * 70)

    if dasani_result:
        dasani_output, dasani_files = dasani_result
        print(f"\n  Dasani Production: {dasani_output.get('final_scores', {}).get('total', 0)} Cosm")
        print(f"  Files: {len(dasani_files)}")

    if philly_result:
        philly_output, philly_files = philly_result
        print(f"\n  North Philly Activation: {philly_output.get('final_scores', {}).get('total', 0)} Chron")
        print(f"  Files: {len(philly_files)}")

    print("\n  All production files in: talent-agent/backend/production_files/")
    print("=" * 70)
