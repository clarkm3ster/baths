"""
Chron Talent Agent — Deliverable File Generator

Generates real downloadable files from completed productions:
  - Full production report (markdown)
  - Stage-by-stage deliverable files
  - IP log
  - Dimension scorecard
  - Sources cited

All files are markdown with real content — not templates.
"""

import os
import json
from typing import Dict, List
from datetime import datetime

from models import GameType


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "production_files")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_production_files(game_output: Dict) -> Dict[str, str]:
    """
    Generate all downloadable files from a completed game output.
    Returns a dict of filename → filepath.
    """
    ensure_output_dir()

    project = game_output.get("project", {})
    project_id = project.get("project_id", "unknown")
    prod_num = project.get("production_number", 1)
    title = project.get("title", "Production").replace(" ", "_")

    prefix = f"{title}_P{prod_num}"
    base = os.path.join(OUTPUT_DIR, project_id)
    os.makedirs(base, exist_ok=True)

    files = {}

    # 1. Full production report
    report_path = os.path.join(base, f"{prefix}_Full_Report.md")
    _write_full_report(report_path, game_output)
    files["full_report"] = report_path

    # 2. Stage deliverable files — one per stage
    for stage_out in game_output.get("stages", []):
        stage_name = stage_out.get("stage_name", stage_out.get("stage", "unknown"))
        safe_name = stage_name.replace(" ", "_").replace("-", "_")
        stage_path = os.path.join(base, f"{prefix}_{safe_name}_Deliverables.md")
        _write_stage_file(stage_path, stage_out, game_output)
        files[f"stage_{stage_out.get('stage', '')}"] = stage_path

    # 3. IP log
    ip_path = os.path.join(base, f"{prefix}_IP_Log.md")
    _write_ip_log(ip_path, game_output)
    files["ip_log"] = ip_path

    # 4. Dimension scorecard
    score_path = os.path.join(base, f"{prefix}_Scorecard.md")
    _write_scorecard(score_path, game_output)
    files["scorecard"] = score_path

    # 5. Sources cited
    sources_path = os.path.join(base, f"{prefix}_Sources.md")
    _write_sources(sources_path, game_output)
    files["sources"] = sources_path

    # 6. JSON data package
    json_path = os.path.join(base, f"{prefix}_Data.json")
    _write_json_package(json_path, game_output)
    files["data_package"] = json_path

    return files


def _write_full_report(path: str, game_output: Dict):
    project = game_output.get("project", {})
    principal = game_output.get("principal", {})
    team = game_output.get("team", {})
    scores = game_output.get("final_scores", {})
    sources = game_output.get("sources_cited", [])

    game_type = project.get("game_type", "")
    is_domes = game_type == "domes"
    score_name = "Cosm" if is_domes else "Chron"
    game_label = "DOMES" if is_domes else "SPHERES"

    # Subject info
    if is_domes and project.get("character"):
        char = project["character"]
        subject = char.get("name", "Unknown")
        subject_source = char.get("source_citation", char.get("source", ""))
        subject_situation = char.get("situation", "")
        subject_challenge = char.get("production_challenge", "")
    else:
        parcel = project.get("parcel", {})
        subject = parcel.get("address", "Unknown")
        subject_source = f"OpenDataPhilly. {parcel.get('neighborhood', '')}, {parcel.get('city', 'Philadelphia')}."
        subject_situation = parcel.get("history", "")
        subject_challenge = parcel.get("opportunity", "")

    with open(path, "w") as f:
        f.write(f"# {project.get('title', 'Production Report')}\n\n")
        f.write(f"**Game:** {game_label}  \n")
        f.write(f"**Subject:** {subject}  \n")
        f.write(f"**Source:** {subject_source}  \n")
        f.write(f"**Principal:** {principal.get('name', 'Unknown')}  \n")
        f.write(f"**Production #:** {project.get('production_number', 1)}  \n")
        f.write(f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}  \n\n")

        f.write("---\n\n")

        # Brief
        f.write("## Production Brief\n\n")
        f.write(f"**Situation:** {subject_situation}\n\n")
        f.write(f"**Challenge/Opportunity:** {subject_challenge}\n\n")

        if is_domes and project.get("character"):
            char = project["character"]
            f.write(f"**Key Systems:** {', '.join(char.get('key_systems', []))}\n\n")
            f.write(f"**Flourishing Dimensions:** {', '.join(char.get('flourishing_dimensions', []))}\n\n")
        elif project.get("parcel"):
            parcel = project["parcel"]
            f.write(f"**Zoning:** {parcel.get('zoning', '')}\n")
            f.write(f"**Lot Size:** {parcel.get('lot_size_sqft', 0):,.0f} sqft\n")
            f.write(f"**Constraints:** {', '.join(parcel.get('constraints', []))}\n\n")

        f.write("---\n\n")

        # Principal
        f.write("## Principal\n\n")
        f.write(f"**{principal.get('name', 'Unknown')}**\n\n")
        f.write(f"Vision: {principal.get('vision', '')}\n\n")
        f.write(f"Signature: {principal.get('signature_style', '')}\n\n")

        # Team
        f.write("## Team\n\n")
        f.write(f"{team.get('team_strength', '')}\n\n")
        for m in team.get("members", []):
            f.write(f"- **{m['talent_name']}** (resonance: {m['resonance_score']:.0f})")
            if m.get("capabilities_matched"):
                f.write(f" — {', '.join(m['capabilities_matched'])}")
            f.write("\n")
            f.write(f"  {m.get('reasoning', '').split('|')[0].strip()}\n")
        f.write("\n---\n\n")

        # Stage-by-stage
        f.write("## Production Stages\n\n")
        for i, stage_out in enumerate(game_output.get("stages", [])):
            f.write(f"### Stage {i+1}: {stage_out.get('stage_name', '')}\n\n")
            f.write(f"*{stage_out.get('focus', '')}*\n\n")

            for d in stage_out.get("deliverables", []):
                unlikely = " [UNLIKELY COLLISION]" if d.get("is_unlikely") else ""
                f.write(f"#### {d.get('title', '')}{unlikely}\n\n")
                f.write(f"**Practitioner:** {d.get('talent_name', '')} ({d.get('practice', '')})\n\n")

                if d.get("work_referenced"):
                    refs = ", ".join(f'"{w["title"]}"' for w in d["work_referenced"])
                    f.write(f"*Drawing on: {refs}*\n\n")

                f.write(f"{d.get('description', '')}\n\n")

                if d.get("built_on"):
                    f.write(f"*Builds on prior art*\n\n")

            # Stage scores
            dim_snap = game_output.get("dimension_progression", [])
            if i < len(dim_snap):
                snap = dim_snap[i]
                f.write(f"**After {stage_out.get('stage_name', '')}:** {score_name} = {snap.get('total', 0)}\n\n")
                deltas = snap.get("stage_deltas", {})
                for dk, dv in deltas.items():
                    if dv > 0:
                        det = snap.get("dimension_details", {}).get(dk, {})
                        f.write(f"  {det.get('label', dk)}: +{dv}\n")
                f.write("\n")

            f.write("---\n\n")

        # Final scores
        f.write("## Final Scores\n\n")
        dims = scores.get("dimensions", {})
        dim_details = scores.get("dimension_details", {})
        f.write(f"**Total {score_name}: {scores.get('total', 0)}**\n\n")
        f.write(f"Weakest dimension: {scores.get('weakest', 'N/A')}  \n")
        f.write(f"Strongest dimension: {scores.get('strongest', 'N/A')}\n\n")
        for dk in sorted(dims.keys(), key=lambda k: dims[k], reverse=True):
            det = dim_details.get(dk, {})
            f.write(f"| {det.get('label', dk)} | {dims[dk]} | {det.get('description', '')} |\n")
        f.write("\n---\n\n")

        # IP Log
        f.write("## IP Generated\n\n")
        for ip in game_output.get("ip_log", []):
            f.write(f"- **{ip['title']}** ({ip['domain'].replace('_', ' ')}) — {ip['practitioner_name']}, {ip['stage']}\n")
        f.write("\n---\n\n")

        # Sources
        f.write("## Sources Cited\n\n")
        for s in sources:
            f.write(f"- **{s['title']}** ({s['type'].replace('_', ' ')})\n")
            f.write(f"  {s['citation']}\n")
            f.write(f"  *Used for: {s['used_for']}*\n\n")


def _write_stage_file(path: str, stage_out: Dict, game_output: Dict):
    project = game_output.get("project", {})

    with open(path, "w") as f:
        f.write(f"# {stage_out.get('stage_name', '')} — {project.get('title', '')}\n\n")
        f.write(f"*{stage_out.get('focus', '')}*\n\n")
        f.write(f"Production #{stage_out.get('production_number', 1)}\n\n")
        f.write("---\n\n")

        for d in stage_out.get("deliverables", []):
            unlikely = " [UNLIKELY COLLISION]" if d.get("is_unlikely") else ""
            f.write(f"## {d.get('title', '')}{unlikely}\n\n")
            f.write(f"**Practitioner:** {d.get('talent_name', '')} ({d.get('practice', '')})  \n")
            f.write(f"**Capability:** {d.get('capability', '').replace('_', ' ')}  \n")
            f.write(f"**IP Domain:** {d.get('ip_domain', '').replace('_', ' ')}  \n\n")

            if d.get("work_referenced"):
                f.write("### Referenced Work\n\n")
                for w in d["work_referenced"]:
                    f.write(f"- \"{w['title']}\" — {w.get('description', '')} ({w.get('medium', '')}{', ' + str(w['year']) if w.get('year') else ''})\n")
                f.write("\n")

            f.write("### Deliverable\n\n")
            f.write(f"{d.get('description', '')}\n\n")
            f.write("---\n\n")

        # Score info
        f.write(f"**Stage Scores:** +{stage_out.get('cosm_delta', 0)} Cosm, +{stage_out.get('chron_delta', 0)} Chron\n")
        f.write(f"**Deliverables:** {stage_out.get('deliverable_count', 0)}  \n")
        f.write(f"**IP Items:** {stage_out.get('ip_count', 0)}  \n")
        if stage_out.get("unlikely_count", 0) > 0:
            f.write(f"**Unlikely Collisions:** {stage_out['unlikely_count']}\n")


def _write_ip_log(path: str, game_output: Dict):
    project = game_output.get("project", {})

    with open(path, "w") as f:
        f.write(f"# IP Log — {project.get('title', '')}\n\n")
        f.write(f"Production #{project.get('production_number', 1)}\n\n")

        # Group by domain
        by_domain = {}
        for ip in game_output.get("ip_log", []):
            d = ip.get("domain", "other")
            by_domain.setdefault(d, []).append(ip)

        for domain, items in sorted(by_domain.items()):
            f.write(f"## {domain.replace('_', ' ').title()} ({len(items)} items)\n\n")
            for ip in items:
                f.write(f"### {ip['title']}\n\n")
                f.write(f"**Practitioner:** {ip['practitioner_name']} ({ip.get('practice', '')})\n")
                f.write(f"**Format:** {ip.get('format', '')}  \n")
                f.write(f"**Stage:** {ip.get('stage', '').replace('_', ' ')}  \n\n")
                f.write(f"{ip.get('description', '')}\n\n")
                f.write("---\n\n")


def _write_scorecard(path: str, game_output: Dict):
    project = game_output.get("project", {})
    scores = game_output.get("final_scores", {})
    game_type = project.get("game_type", "")
    score_name = "Cosm" if game_type == "domes" else "Chron"

    with open(path, "w") as f:
        f.write(f"# {score_name} Scorecard — {project.get('title', '')}\n\n")
        f.write(f"Production #{project.get('production_number', 1)}\n\n")

        f.write(f"## Total {score_name}: {scores.get('total', 0)}\n\n")

        dims = scores.get("dimensions", {})
        dim_details = scores.get("dimension_details", {})

        f.write(f"The {'dome' if game_type == 'domes' else 'sphere'} is only as strong as its weakest dimension.\n\n")
        f.write(f"**Weakest:** {scores.get('weakest', 'N/A')}  \n")
        f.write(f"**Strongest:** {scores.get('strongest', 'N/A')}\n\n")

        f.write("## Dimensions\n\n")
        f.write("| Dimension | Score | Description |\n")
        f.write("|-----------|-------|-------------|\n")
        for dk in sorted(dims.keys(), key=lambda k: dims[k], reverse=True):
            det = dim_details.get(dk, {})
            f.write(f"| {det.get('label', dk)} | {dims[dk]} | {det.get('description', '')} |\n")
        f.write("\n")

        # Stage progression
        f.write("## Progression\n\n")
        progression = game_output.get("dimension_progression", [])
        stages = game_output.get("stages", [])
        for i, snap in enumerate(progression):
            stage_name = stages[i].get("stage_name", f"Stage {i+1}") if i < len(stages) else f"Stage {i+1}"
            f.write(f"### After {stage_name}\n\n")
            f.write(f"Total: {snap.get('total', 0)}\n\n")
            for dk, dv in snap.get("dimensions", {}).items():
                det = snap.get("dimension_details", {}).get(dk, {})
                delta = snap.get("stage_deltas", {}).get(dk, 0)
                delta_str = f" (+{delta})" if delta > 0 else ""
                f.write(f"  {det.get('label', dk)}: {dv}{delta_str}\n")
            f.write("\n")


def _write_sources(path: str, game_output: Dict):
    project = game_output.get("project", {})
    sources = game_output.get("sources_cited", [])

    with open(path, "w") as f:
        f.write(f"# Sources Cited — {project.get('title', '')}\n\n")
        f.write(f"Production #{project.get('production_number', 1)}\n\n")
        f.write(f"Total sources: {len(sources)}\n\n")

        # Group by type
        by_type = {}
        for s in sources:
            t = s.get("type", "other")
            by_type.setdefault(t, []).append(s)

        for stype, items in sorted(by_type.items()):
            f.write(f"## {stype.replace('_', ' ').title()} ({len(items)})\n\n")
            for s in items:
                f.write(f"### {s['title']}\n\n")
                f.write(f"{s['citation']}\n\n")
                f.write(f"*Used for: {s['used_for']}*\n\n")


def _write_json_package(path: str, game_output: Dict):
    """Write the complete game output as a JSON data package."""
    with open(path, "w") as f:
        json.dump(game_output, f, indent=2, default=str)
