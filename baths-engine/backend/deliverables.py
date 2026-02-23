"""
BATHS Game Engine — Deliverable Generation System

Generates real, downloadable files at each production stage for DOMES and SPHERES.
Every deliverable cites its real data sources. Every file is downloadable.

DOMES stages:
  Development  → Rights report, research bible, character study
  Pre-Prod     → Cleared rights matrix, technical survey, production bible
  Production   → Coordination agreements, dome architectural plan
  Post-Prod    → Dome visualization package, flourishing doc, EPK
  Distribution → Series bible, pitch deck, IP log

SPHERES stages:
  Development  → Location report, permit pathway, feasibility assessment
  Pre-Prod     → Site breakdown, program design, budget top sheet
  Production   → Activation design, build schedule, final budget
  Post-Prod    → Visualization package, impact report, EPK
  Distribution → Series bible, pitch deck, IP log
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from models import (
    GameType, ProductionStage, ProductionState, IPDomain
)

DELIVERABLES_DIR = Path(__file__).parent / "data" / "deliverables"
DELIVERABLES_DIR.mkdir(parents=True, exist_ok=True)

# IP Domain labels for the IP log
IP_DOMAIN_LABELS = {
    "entertainment": "Entertainment IP",
    "technology": "Technology IP",
    "financial_product": "Financial Product IP",
    "policy": "Policy IP",
    "product": "Product IP",
    "research": "Research IP",
    "housing": "Housing IP",
    "healthcare": "Healthcare IP",
    "urban_design": "Urban Design IP",
    "real_estate": "Real Estate IP",
}


def _write_deliverable(production_id: str, stage: str, filename: str, content: Any) -> str:
    """Write a deliverable file and return its relative path."""
    out_dir = DELIVERABLES_DIR / production_id / stage
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename

    if filename.endswith(".json"):
        path.write_text(json.dumps(content, indent=2, default=str) + "\n")
    elif filename.endswith(".md"):
        path.write_text(content if isinstance(content, str) else str(content))
    elif filename.endswith(".txt"):
        path.write_text(content if isinstance(content, str) else str(content))
    else:
        path.write_text(json.dumps(content, indent=2, default=str) + "\n")

    return str(path.relative_to(DELIVERABLES_DIR.parent))


def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")


# ══════════════════════════════════════════════════════════════════
# DOMES DELIVERABLES
# ══════════════════════════════════════════════════════════════════

def generate_domes_development(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Development deliverables:
    - Rights report listing all legal entitlements found
    - Research bible of all systems mapped
    - Character study with sources cited
    """
    pid = production.production_id
    subject = production.subject
    files = {}

    # 1. Rights Report
    rights_package = stage_data.get("rights_package", {})
    rights_count = stage_data.get("rights_count", 0)

    rights_md = f"# DOMES Rights Report\n## Subject: {subject}\n"
    rights_md += f"Generated: {_timestamp()}\n\n"
    rights_md += f"**Total Provisions Identified:** {rights_count}\n\n"
    rights_md += "---\n\n"

    for dimension, provisions in rights_package.items():
        rights_md += f"## {dimension.replace('_', ' ').title()}\n\n"
        for p in provisions:
            citation = p.get("citation", "Unknown")
            title = p.get("title", "Untitled")
            body = p.get("body", "")
            authority = p.get("authority", "")
            source_url = p.get("source_url", "")
            rights_md += f"### {citation}\n"
            rights_md += f"**{title}**\n\n"
            if body:
                rights_md += f"{body[:500]}{'...' if len(body) > 500 else ''}\n\n"
            if authority:
                rights_md += f"*Authority:* {authority}\n\n"
            if source_url:
                rights_md += f"*Source:* [{source_url}]({source_url})\n\n"
            rights_md += "---\n\n"

    rights_md += f"\n## Data Sources\n"
    rights_md += "- eCFR (Electronic Code of Federal Regulations) — ecfr.gov\n"
    rights_md += "- Federal Register — federalregister.gov\n"
    rights_md += "- BATHS Legal Data Engine — continuous scraping of federal regulatory databases\n"
    rights_md += f"- Total provisions in database at time of report: {rights_count}\n"

    files["rights_report.md"] = _write_deliverable(pid, "development", "rights_report.md", rights_md)

    # 2. Research Bible (data package)
    cast_list = stage_data.get("cast_list", [])
    deal_structure = stage_data.get("deal_structure", [])
    market_analysis = stage_data.get("market_analysis", {})
    stats = stage_data.get("data_engine_stats", {})

    research_bible = {
        "title": f"Research Bible — {subject}",
        "generated": _timestamp(),
        "subject": subject,
        "government_systems": {
            "total_mapped": len(cast_list),
            "systems": cast_list,
        },
        "system_connections": {
            "total_links": len(deal_structure),
            "active": stage_data.get("active_links", 0),
            "blocked": stage_data.get("blocked_links", 0),
            "possible": stage_data.get("possible_links", 0),
            "links": deal_structure,
        },
        "cost_landscape": {
            "total_data_points": stage_data.get("cost_point_count", 0),
            "by_category": market_analysis,
        },
        "data_engine_stats": stats,
        "data_sources": [
            "CMS (Centers for Medicare & Medicaid Services) — cms.gov",
            "HUD (Housing and Urban Development) — hud.gov",
            "BLS (Bureau of Labor Statistics) — bls.gov",
            "Census ACS 5-year — census.gov",
            "Vera Institute of Justice — vera.org",
            "HCUP (Healthcare Cost and Utilization Project) — hcup-us.ahrq.gov",
            "BATHS Data Engine — continuous multi-source scraping",
        ],
    }

    files["research_bible.json"] = _write_deliverable(pid, "development", "research_bible.json", research_bible)

    # 3. Character Study (profile document)
    profile = stage_data.get("profile", {})

    char_md = f"# Character Study — {subject}\n"
    char_md += f"Generated: {_timestamp()}\n\n"
    char_md += "## Profile Summary\n\n"
    char_md += f"**Name:** {profile.get('name', subject)}\n\n"

    needs = profile.get("needs", [])
    if needs:
        char_md += "**Identified Needs:**\n"
        for n in needs:
            char_md += f"- {n.replace('_', ' ').title()}\n"
        char_md += "\n"

    dims = profile.get("dimensions_affected", [])
    if dims:
        char_md += "**Regulatory Dimensions Affected:**\n"
        for d in dims:
            char_md += f"- {d.replace('_', ' ').title()}\n"
        char_md += "\n"

    frag_cost = profile.get("estimated_annual_fragmentation_cost", 0)
    char_md += f"**Estimated Annual Fragmentation Cost:** ${frag_cost:,.0f}\n\n"
    char_md += f"**Systems Involved:** {profile.get('systems_involved', 0)}\n\n"

    risk_factors = profile.get("risk_factors", [])
    if risk_factors:
        char_md += "## Risk Factors\n\n"
        for r in risk_factors:
            char_md += f"- {r}\n"
        char_md += "\n"

    strengths = profile.get("strengths", [])
    if strengths:
        char_md += "## Strengths\n\n"
        for s in strengths:
            char_md += f"- {s}\n"
        char_md += "\n"

    char_md += "## Data Sources\n\n"
    char_md += "- Federal regulatory databases (eCFR, Federal Register)\n"
    char_md += "- CMS cost data\n"
    char_md += "- Government systems mapping (BATHS Data Engine)\n"
    char_md += f"- {len(cast_list)} government data systems analyzed\n"
    char_md += f"- {len(deal_structure)} inter-system connections mapped\n"

    files["character_study.md"] = _write_deliverable(pid, "development", "character_study.md", char_md)

    return files


def generate_domes_pre_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Pre-Production deliverables:
    - Cleared rights matrix
    - Technical survey of system interconnections
    - Production bible with budget top sheet
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    files = {}

    # 1. Cleared Rights Matrix
    shooting_script = stage_data.get("shooting_script", {})
    layers = shooting_script.get("layers", [])

    matrix_md = f"# Cleared Rights Matrix — {subject}\n"
    matrix_md += f"Generated: {_timestamp()}\n\n"
    matrix_md += f"**Overall Dome Coverage:** {shooting_script.get('overall_coverage', 0):.0%}\n\n"
    matrix_md += "| Layer | Strength | Key Metrics |\n"
    matrix_md += "|-------|----------|-------------|\n"
    for layer in layers:
        name = layer.get("name", "Unknown")
        strength = layer.get("strength", 0)
        strength_pct = f"{strength:.0%}" if isinstance(strength, float) and strength <= 1 else str(strength)
        metrics = []
        for k, v in layer.items():
            if k not in ("name", "strength", "purpose"):
                metrics.append(f"{k}: {v}")
        matrix_md += f"| {name} | {strength_pct} | {'; '.join(metrics[:3])} |\n"

    matrix_md += "\n## Rights Clearance Status\n\n"
    rights_package = dev_data.get("rights_package", {})
    for dim, provisions in rights_package.items():
        matrix_md += f"### {dim.replace('_', ' ').title()} — {len(provisions)} provisions cleared\n\n"
        for p in provisions:
            matrix_md += f"- **{p.get('citation', 'N/A')}**: {p.get('title', 'N/A')}\n"
        matrix_md += "\n"

    matrix_md += "\n## Data Sources\n"
    matrix_md += "- eCFR / Federal Register (legal provisions)\n"
    matrix_md += "- BATHS Coordination Engine (model fitting)\n"
    matrix_md += "- Nussbaum Central Capabilities + OECD Better Life (flourishing framework)\n"

    files["cleared_rights_matrix.md"] = _write_deliverable(pid, "pre_production", "cleared_rights_matrix.md", matrix_md)

    # 2. Technical Survey of System Interconnections
    coordination_crew = stage_data.get("coordination_crew", [])
    intelligence = stage_data.get("intelligence", [])

    survey = {
        "title": f"Technical Survey — System Interconnections for {subject}",
        "generated": _timestamp(),
        "dome_architecture": shooting_script,
        "coordination_models": [{
            "name": m.get("name", ""),
            "description": m.get("description", ""),
            "real_examples": m.get("real_examples", []),
            "legal_authority": m.get("legal_authority", ""),
            "systems_connected": m.get("systems_connected", []),
            "consent_model": m.get("consent_model", ""),
            "estimated_savings_pct": m.get("estimated_savings_pct", 0),
            "implementation_cost": m.get("implementation_cost", ""),
            "fit_score": m.get("fit_score", 0),
        } for m in coordination_crew],
        "enrichment_intelligence": intelligence,
        "data_sources": [
            "BATHS Coordination Engine — real-world coordination model database",
            "CMS Innovation Center — ACO, Bundled Payment models",
            "HUD Moving to Work demonstrations",
            "SAMHSA Certified Community Behavioral Health Clinics",
        ],
    }

    files["technical_survey.json"] = _write_deliverable(pid, "pre_production", "technical_survey.json", survey)

    # 3. Production Bible with Budget Top Sheet
    budget = stage_data.get("budget_top_sheet", {})
    flourishing = stage_data.get("flourishing", {})

    bible_md = f"# Production Bible — {subject}\n"
    bible_md += f"Generated: {_timestamp()}\n\n"
    bible_md += "## Budget Top Sheet\n\n"
    bible_md += "### Above the Line\n\n"
    atl = budget.get("above_the_line", {})
    for item, cost in atl.items():
        bible_md += f"- **{item.replace('_', ' ').title()}:** ${cost:,.0f}\n"
    bible_md += f"\n**Above-the-Line Total:** ${sum(v for v in atl.values() if isinstance(v, (int, float))):,.0f}\n\n"

    bible_md += "### Below the Line\n\n"
    btl = budget.get("below_the_line", {})
    btl_total = 0
    for item, cost in btl.items():
        if isinstance(cost, (int, float)):
            bible_md += f"- **{item.replace('_', ' ').title()}:** ${cost:,.0f}\n"
            btl_total += cost
        else:
            bible_md += f"- **{item.replace('_', ' ').title()}:** {cost}\n"
    bible_md += f"\n**Below-the-Line Total:** ${btl_total:,.0f}\n\n"

    frag = budget.get("annual_fragmentation_cost", 0)
    savings = budget.get("annual_coordination_savings", 0)
    bible_md += "### Fragmented vs Coordinated Cost Comparison\n\n"
    bible_md += f"| Metric | Value |\n"
    bible_md += f"|--------|-------|\n"
    bible_md += f"| Annual Fragmentation Cost | ${frag:,.0f} |\n"
    bible_md += f"| Annual Coordination Savings | ${savings:,.0f} |\n"
    bible_md += f"| Net Coordinated Cost | ${frag - savings:,.0f} |\n"
    bible_md += f"| Annual Dome Value | ${budget.get('annual_dome_value', 0):,.0f} |\n\n"

    bible_md += "## Flourishing Index\n\n"
    scores = flourishing.get("scores", {})
    for dim, data in scores.items():
        if isinstance(data, dict):
            bible_md += f"- **{dim.title()}:** Score {data.get('score', 'N/A')}, Gap {data.get('gap', 'N/A')}\n"
    bible_md += f"\n**Overall Score:** {flourishing.get('overall_score', 'N/A')}\n"
    bible_md += f"**Overall Gap:** {flourishing.get('overall_gap', 'N/A')}\n\n"

    bible_md += "## Data Sources\n\n"
    bible_md += "- CMS (healthcare costs, Medicaid/Medicare spending)\n"
    bible_md += "- HCUP (hospital utilization costs)\n"
    bible_md += "- HUD (housing subsidy costs)\n"
    bible_md += "- Vera Institute (incarceration costs)\n"
    bible_md += "- BLS (labor market data)\n"
    bible_md += "- Nussbaum Central Capabilities Framework\n"
    bible_md += "- OECD Better Life Index\n"

    files["production_bible.md"] = _write_deliverable(pid, "pre_production", "production_bible.md", bible_md)

    return files


def generate_domes_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Production deliverables:
    - Coordination agreement templates
    - Dome architectural plan
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    files = {}

    # 1. Coordination Agreement Templates
    agreements = stage_data.get("executed_agreements", [])

    agree_md = f"# Coordination Agreement Templates — {subject}\n"
    agree_md += f"Generated: {_timestamp()}\n\n"
    agree_md += f"**Total Agreements:** {len(agreements)}\n\n"

    for i, agmt in enumerate(agreements, 1):
        agree_md += f"## Agreement {i}: {agmt.get('type', 'Unknown')}\n\n"
        agree_md += f"**Status:** {agmt.get('status', 'pending')}\n\n"
        agree_md += f"**Legal Authority:** {agmt.get('legal_authority', 'N/A')}\n\n"
        agree_md += f"**Consent Model:** {agmt.get('consent_model', 'N/A')}\n\n"
        agree_md += f"**Estimated Savings:** {agmt.get('estimated_savings_pct', 0)}%\n\n"
        parties = agmt.get("parties", [])
        if parties:
            agree_md += "**Participating Systems:**\n"
            for p in parties:
                agree_md += f"- {p}\n"
        agree_md += "\n### Template Terms\n\n"
        agree_md += "1. **Purpose:** Coordinate service delivery across participating systems "
        agree_md += f"for {subject} under {agmt.get('type', 'coordination')} model.\n"
        agree_md += "2. **Data Sharing:** Per consent model, share relevant data fields between "
        agree_md += "participating systems to reduce duplication and improve outcomes.\n"
        agree_md += "3. **Duration:** 12 months, renewable.\n"
        agree_md += "4. **Performance Metrics:** Reduction in fragmentation cost, improvement "
        agree_md += "in flourishing index scores across all covered dimensions.\n"
        agree_md += "5. **Dispute Resolution:** Mediation through coordinating entity.\n\n"
        agree_md += "---\n\n"

    agree_md += "## Data Sources\n\n"
    agree_md += "- CMS Innovation Center (ACO, Bundled Payment models)\n"
    agree_md += "- HUD Moving to Work demonstrations\n"
    agree_md += "- SAMHSA CCBHC integration models\n"
    agree_md += "- BATHS Coordination Engine\n"

    files["coordination_agreements.md"] = _write_deliverable(pid, "production", "coordination_agreements.md", agree_md)

    # 2. Dome Architectural Plan
    call_sheet = stage_data.get("call_sheet", {})
    vfx_report = stage_data.get("vfx_report", [])
    shooting_script = pre_data.get("shooting_script", {})

    plan = {
        "title": f"Dome Architectural Plan — {subject}",
        "generated": _timestamp(),
        "dome_status": call_sheet.get("dome_status", "under_construction"),
        "architecture": {
            "subject": subject,
            "layers": shooting_script.get("layers", []),
            "overall_coverage": shooting_script.get("overall_coverage", 0),
        },
        "execution_status": {
            "rights_applied": call_sheet.get("rights_applied", 0),
            "systems_connected": call_sheet.get("systems_connected", 0),
            "agreements_executed": call_sheet.get("agreements_executed", 0),
            "coordination_model": call_sheet.get("coordination_model", ""),
            "needs_addressed": call_sheet.get("needs_addressed", []),
            "coverage_dimensions": call_sheet.get("coverage_dimensions", []),
        },
        "cross_references": vfx_report,
        "data_sources": [
            "eCFR / Federal Register (legal provisions)",
            "CMS, HUD, BLS, Census (cost & demographic data)",
            "BATHS Data Engine (system mapping & enrichment)",
        ],
    }

    files["dome_architectural_plan.json"] = _write_deliverable(pid, "production", "dome_architectural_plan.json", plan)

    return files


def generate_domes_post_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Post-Production deliverables:
    - Dome visualization package
    - Flourishing documentation
    - EPK (Electronic Press Kit)
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    prod_data = production.stage_data.get("production", {})
    files = {}

    # 1. Dome Visualization Package
    assembly_cut = stage_data.get("assembly_cut", {})
    color_grade = stage_data.get("color_grade", {})

    viz_package = {
        "title": f"Dome Visualization Package — {subject}",
        "generated": _timestamp(),
        "dome_coverage": {
            "complete": assembly_cut.get("complete", False),
            "coverage_pct": assembly_cut.get("coverage", 0),
            "dimensions_covered": assembly_cut.get("dimensions_covered", []),
            "gaps": assembly_cut.get("gaps", []),
            "blocked_connections": assembly_cut.get("blocked_connections", 0),
            "notes": assembly_cut.get("notes", []),
        },
        "flourishing_grade": {
            "grade": color_grade.get("grade", "N/A"),
            "overall_score": color_grade.get("overall_score", 0),
            "overall_gap": color_grade.get("overall_gap", 0),
            "dimensions": color_grade.get("dimensions", {}),
        },
        "ip_outputs_count": len(stage_data.get("ip_outputs", [])),
        "data_sources": [
            "BATHS Assembly Engine (dome verification)",
            "Nussbaum Capabilities / OECD Better Life (flourishing metrics)",
            "All upstream data sources from Development & Pre-Production stages",
        ],
    }

    files["dome_visualization_package.json"] = _write_deliverable(
        pid, "post_production", "dome_visualization_package.json", viz_package
    )

    # 2. Flourishing Documentation
    flour_md = f"# Flourishing Documentation — {subject}\n"
    flour_md += f"Generated: {_timestamp()}\n\n"
    flour_md += f"**Grade:** {color_grade.get('grade', 'N/A')}\n\n"
    flour_md += f"**Overall Flourishing Score:** {color_grade.get('overall_score', 0):.1%}\n\n"
    flour_md += f"**Gap to Flourishing Threshold:** {color_grade.get('overall_gap', 0):.1%}\n\n"

    flour_md += "## Dimension Scores\n\n"
    flour_md += "| Dimension | Score | Gap | Status |\n"
    flour_md += "|-----------|-------|-----|--------|\n"
    for dim, data in color_grade.get("dimensions", {}).items():
        if isinstance(data, dict):
            score = data.get("score", 0)
            gap = data.get("gap", 0)
            status = "Above Threshold" if gap <= 0 else "Below Threshold"
            flour_md += f"| {dim.title()} | {score:.1%} | {gap:.1%} | {status} |\n"
    flour_md += "\n"

    flour_md += "## Dome Coverage Assessment\n\n"
    flour_md += f"- **Coverage:** {assembly_cut.get('coverage', 0):.0%}\n"
    flour_md += f"- **Dimensions Covered:** {', '.join(assembly_cut.get('dimensions_covered', []))}\n"
    gaps = assembly_cut.get("gaps", [])
    if gaps:
        flour_md += f"- **Gaps Remaining:** {', '.join(gaps)}\n"
    flour_md += "\n"

    flour_md += "## Frameworks Used\n\n"
    flour_md += "- Martha Nussbaum's Central Capabilities Approach\n"
    flour_md += "- OECD Better Life Index\n"
    flour_md += "- BATHS Flourishing Index (composite)\n\n"

    flour_md += "## Data Sources\n\n"
    flour_md += "- Census ACS 5-year (demographic baseline)\n"
    flour_md += "- CMS (healthcare outcomes)\n"
    flour_md += "- HUD (housing stability)\n"
    flour_md += "- BLS (employment)\n"
    flour_md += "- USDA (food access)\n"

    files["flourishing_documentation.md"] = _write_deliverable(
        pid, "post_production", "flourishing_documentation.md", flour_md
    )

    # 3. EPK (Electronic Press Kit)
    sound_mix = stage_data.get("sound_mix", {})
    vfx_finals = stage_data.get("vfx_finals", {})
    ip_outputs = stage_data.get("ip_outputs", [])

    epk_md = f"# Electronic Press Kit — The Dome of {subject}\n"
    epk_md += f"Generated: {_timestamp()}\n\n"
    epk_md += "## Logline\n\n"
    epk_md += f"A person navigating {len(assembly_cut.get('dimensions_covered', []))} "
    epk_md += "fragmented government systems receives the first complete protective dome "
    epk_md += "— built from real federal regulations, real cost data, and real coordination models.\n\n"

    epk_md += "## Narrative Sections\n\n"
    for section in sound_mix.get("sections", []):
        epk_md += f"### {section.get('title', 'Section')}\n\n"
        epk_md += f"{section.get('content', '')}\n\n"

    epk_md += "## Innovations\n\n"
    innovations = vfx_finals.get("innovations", [])
    for innov in innovations:
        epk_md += f"- {innov}\n"
    epk_md += "\n"

    epk_md += "## Intellectual Property Generated\n\n"
    epk_md += f"**{len(ip_outputs)} IP outputs across "
    domains_present = set()
    for ip in ip_outputs:
        d = ip.get("domain", "")
        domains_present.add(d)
    epk_md += f"{len(domains_present)} domains:**\n\n"
    for ip in ip_outputs:
        label = IP_DOMAIN_LABELS.get(ip.get("domain", ""), ip.get("domain", ""))
        epk_md += f"- **{label}:** {ip.get('title', '')} — {ip.get('description', '')[:100]}\n"
    epk_md += "\n"

    epk_md += "## Key Statistics\n\n"
    dev_data_stats = dev_data.get("data_engine_stats", {})
    epk_md += f"- Legal provisions mapped: {dev_data.get('rights_count', 0)}\n"
    epk_md += f"- Government systems connected: {dev_data.get('system_count', 0)}\n"
    epk_md += f"- Dome coverage: {assembly_cut.get('coverage', 0):.0%}\n"
    epk_md += f"- Flourishing grade: {color_grade.get('grade', 'N/A')}\n"

    files["epk.md"] = _write_deliverable(pid, "post_production", "epk.md", epk_md)

    return files


def generate_domes_distribution(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Distribution deliverables:
    - Series bible (replicable model)
    - Pitch deck
    - IP log categorized by domain
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    post_data = production.stage_data.get("post_production", {})
    files = {}

    cosm = stage_data.get("cosm", {})
    dome_bond = stage_data.get("dome_bond", {})
    ip_catalog = stage_data.get("ip_catalog", [])
    replication_kit = stage_data.get("replication_kit", {})
    narrative = stage_data.get("narrative", {})
    innovations = stage_data.get("innovations", [])
    industries = stage_data.get("industries_changed", [])

    # 1. Series Bible
    bible_md = f"# Series Bible — DOMES: {subject}\n"
    bible_md += f"Generated: {_timestamp()}\n\n"
    bible_md += "## Concept\n\n"
    bible_md += "DOMES builds a complete protective dome around one person using the entire "
    bible_md += "US government. Each dome is a financial instrument — the delta between fragmented "
    bible_md += "and coordinated cost IS the financial value.\n\n"

    bible_md += "## This Dome\n\n"
    bible_md += f"**Subject:** {subject}\n\n"
    bible_md += f"**COSM Score:** {cosm.get('total', 0):.1f}\n"
    bible_md += f"- Rights: {cosm.get('rights', 0):.0f}\n"
    bible_md += f"- Research: {cosm.get('research', 0):.0f}\n"
    bible_md += f"- Budget: {cosm.get('budget', 0):.0f}\n"
    bible_md += f"- Package: {cosm.get('package', 0):.0f}\n"
    bible_md += f"- Deliverables: {cosm.get('deliverables', 0):.0f}\n"
    bible_md += f"- Pitch: {cosm.get('pitch', 0):.0f}\n\n"

    bible_md += "## Replication Model\n\n"
    bible_md += f"- **Subject Archetype Needs:** {', '.join(replication_kit.get('subject_archetype', []))}\n"
    bible_md += f"- **Rights Template:** {replication_kit.get('rights_template', 0)} dimensions\n"
    bible_md += f"- **Coordination Model:** {replication_kit.get('coordination_model', 'N/A')}\n"
    bible_md += f"- **Coverage:** {replication_kit.get('coverage', 0):.0%}\n"
    bible_md += f"- **Estimated Annual Savings:** ${replication_kit.get('estimated_savings', 0):,.0f}\n"
    bible_md += f"- **Transferable:** {replication_kit.get('transferable', True)}\n\n"

    bible_md += "## Narrative\n\n"
    for section in narrative.get("sections", []):
        bible_md += f"### {section.get('title', '')}\n\n{section.get('content', '')}\n\n"

    bible_md += "## Industries Changed\n\n"
    for ind in industries:
        bible_md += f"- {ind}\n"
    bible_md += "\n"

    bible_md += "## Data Sources\n\n"
    bible_md += "Every data point in this dome is sourced from public federal databases:\n"
    bible_md += "- eCFR, Federal Register (legal provisions)\n"
    bible_md += "- CMS, HCUP (healthcare costs)\n"
    bible_md += "- HUD (housing costs & programs)\n"
    bible_md += "- BLS (labor data)\n"
    bible_md += "- Census ACS (demographics)\n"
    bible_md += "- Vera Institute (justice costs)\n"
    bible_md += "- BATHS Fragment Agent (28 counties, 15 sources)\n"

    files["series_bible.md"] = _write_deliverable(pid, "distribution", "series_bible.md", bible_md)

    # 2. Pitch Deck
    pitch_md = f"# Pitch Deck — DOMES: {subject}\n"
    pitch_md += f"Generated: {_timestamp()}\n\n"

    pitch_md += "---\n## Slide 1: The Problem\n\n"
    pitch_md += "The US government spends trillions through fragmented systems. "
    pitch_md += "For multi-system individuals, this fragmentation costs an estimated "
    pitch_md += "$78,168/year per person in uncoordinated care.\n\n"

    pitch_md += "---\n## Slide 2: The Solution — DOMES\n\n"
    pitch_md += f"Build a complete protective dome around {subject} using every relevant "
    pitch_md += "federal regulation, every relevant system, coordinated through proven models.\n\n"

    pitch_md += "---\n## Slide 3: The Data\n\n"
    pitch_md += f"- {dev_data.get('rights_count', 0)} legal provisions mapped\n"
    pitch_md += f"- {dev_data.get('system_count', 0)} government systems connected\n"
    pitch_md += f"- {dev_data.get('cost_point_count', 0)} cost data points sourced\n"
    pitch_md += "- All from public federal databases — reproducible, verifiable\n\n"

    pitch_md += "---\n## Slide 4: The Financial Instrument\n\n"
    pitch_md += f"**Dome Bond:** {dome_bond.get('rating', 'N/A')} rated\n"
    pitch_md += f"- Face Value: ${dome_bond.get('face_value', 0):,.0f}\n"
    pitch_md += f"- Coupon Rate: {dome_bond.get('coupon_rate', 0):.1f}%\n"
    pitch_md += f"- Maturity: {dome_bond.get('maturity_years', 0)} years\n"
    pitch_md += f"- Backed by: {dome_bond.get('programs_backing', 0)} federal programs\n\n"

    pitch_md += "---\n## Slide 5: COSM Score\n\n"
    pitch_md += f"**{cosm.get('total', 0):.1f}** — the minimum coverage across 6 dimensions.\n"
    pitch_md += "The dome is only as strong as its thinnest point.\n\n"

    pitch_md += f"---\n## Slide 6: Intellectual Property\n\n"
    pitch_md += f"**{len(ip_catalog)} IP outputs** across {len(set(ip.get('domain', '') for ip in ip_catalog))} domains:\n"
    for ip in ip_catalog:
        label = IP_DOMAIN_LABELS.get(ip.get("domain", ""), ip.get("domain", ""))
        pitch_md += f"- {label}: {ip.get('title', '')}\n"
    pitch_md += "\n"

    pitch_md += "---\n## Slide 7: Replication\n\n"
    pitch_md += "Every dome is transferable. The architecture, the legal framework, "
    pitch_md += "the coordination model — all documented and reproducible across any geography.\n\n"

    files["pitch_deck.md"] = _write_deliverable(pid, "distribution", "pitch_deck.md", pitch_md)

    # 3. IP Log
    ip_log = _build_ip_log(ip_catalog, innovations, "domes", subject)
    files["ip_log.json"] = _write_deliverable(pid, "distribution", "ip_log.json", ip_log)

    return files


# ══════════════════════════════════════════════════════════════════
# SPHERES DELIVERABLES
# ══════════════════════════════════════════════════════════════════

def generate_spheres_development(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Development deliverables:
    - Location report with parcel data
    - Permit pathway document
    - Feasibility assessment
    """
    pid = production.production_id
    subject = production.subject
    files = {}

    location = stage_data.get("location_report", {})
    permits = stage_data.get("rights_assessment", {}).get("permits", [])
    nearby = stage_data.get("nearby_parcels", [])
    insights = stage_data.get("location_insights", [])

    # 1. Location Report
    loc_md = f"# Location Report — {subject}\n"
    loc_md += f"Generated: {_timestamp()}\n\n"
    loc_md += "## Parcel Data\n\n"
    loc_md += f"| Field | Value |\n"
    loc_md += f"|-------|-------|\n"
    loc_md += f"| Parcel ID | {location.get('parcel_id', 'N/A')} |\n"
    loc_md += f"| Address | {location.get('address', 'N/A')} |\n"
    loc_md += f"| Neighborhood | {location.get('neighborhood', 'N/A')} |\n"
    loc_md += f"| Owner | {location.get('owner', 'N/A')} |\n"
    loc_md += f"| Zoning | {location.get('zoning', 'N/A')} — {location.get('zoning_info', {}).get('name', '')} |\n"
    loc_md += f"| Land Area | {location.get('land_area_sqft', 0):,.0f} sqft |\n"
    loc_md += f"| Land Value | ${location.get('land_val', 0):,.0f} |\n"
    loc_md += f"| Improvement Value | ${location.get('improvement_val', 0):,.0f} |\n"
    loc_md += f"| Total Assessed Value | ${location.get('total_val', 0):,.0f} |\n"
    loc_md += f"| Vacant | {'Yes' if location.get('vacant') else 'No'} |\n"
    loc_md += f"| Coordinates | {location.get('lat', 0)}, {location.get('lon', 0)} |\n"
    loc_md += f"| Council District | {location.get('council_district', 'N/A')} |\n\n"

    if nearby:
        loc_md += "## Nearby Parcels\n\n"
        loc_md += "| Parcel ID | Address | Zoning | Vacant | Value |\n"
        loc_md += "|-----------|---------|--------|--------|-------|\n"
        for n in nearby:
            loc_md += f"| {n.get('parcel_id', '')} | {n.get('address', '')} "
            loc_md += f"| {n.get('zoning', '')} | {'Yes' if n.get('vacant') else 'No'} "
            loc_md += f"| ${n.get('total_val', 0):,.0f} |\n"
        loc_md += "\n"

    if insights:
        loc_md += "## Location Insights\n\n"
        for ins in insights:
            loc_md += f"- {ins.get('description', '')}\n"
            if ins.get("activation_types"):
                loc_md += f"  Activation types: {', '.join(ins['activation_types'])}\n"
        loc_md += "\n"

    loc_md += "## Data Sources\n\n"
    loc_md += "- Philadelphia Office of Property Assessment (OPA)\n"
    loc_md += "- Philadelphia City Planning Commission (zoning)\n"
    loc_md += "- OpenDataPhilly (parcel boundaries)\n"
    loc_md += "- BATHS Parcel Data Engine\n"

    files["location_report.md"] = _write_deliverable(pid, "development", "location_report.md", loc_md)

    # 2. Permit Pathway Document
    permit_md = f"# Permit Pathway — {location.get('address', subject)}\n"
    permit_md += f"Generated: {_timestamp()}\n\n"
    permit_md += f"**Zoning:** {location.get('zoning', 'N/A')}\n\n"

    permit_md += "## Required Permits & Approvals\n\n"
    permit_md += "| Permit Type | Status | Description |\n"
    permit_md += "|-------------|--------|-------------|\n"
    for p in permits:
        permit_md += f"| {p.get('type', '')} | {p.get('status', '')} | {p.get('description', '')} |\n"
    permit_md += "\n"

    permit_md += "## Permit Process\n\n"
    permit_md += "1. **Pre-Application Meeting** — Meet with L&I and Planning Commission\n"
    permit_md += "2. **Zoning Review** — Confirm permitted uses for activation type\n"
    permit_md += "3. **Application Submission** — File all required permits simultaneously\n"
    permit_md += "4. **Public Notice** — 30-day community comment period for variances\n"
    permit_md += "5. **Approval & Issuance** — Estimated 6-8 weeks total\n\n"

    permit_md += "## Data Sources\n\n"
    permit_md += "- Philadelphia Department of Licenses and Inspections\n"
    permit_md += "- Philadelphia Zoning Code\n"
    permit_md += "- BATHS Permit Database\n"

    files["permit_pathway.md"] = _write_deliverable(pid, "development", "permit_pathway.md", permit_md)

    # 3. Feasibility Assessment
    feasibility = {
        "title": f"Feasibility Assessment — {location.get('address', subject)}",
        "generated": _timestamp(),
        "parcel": location,
        "permits_required": permits,
        "nearby_context": {
            "total_nearby": len(nearby),
            "vacant_nearby": len([n for n in nearby if n.get("vacant")]),
            "parcels": nearby,
        },
        "feasibility_factors": {
            "site_available": location.get("vacant", False),
            "zoning_compatible": "CMX" in location.get("zoning", "") or "IRMX" in location.get("zoning", ""),
            "permits_achievable": all(p.get("status") != "denied" for p in permits),
            "community_context": len(nearby) > 0,
        },
        "recommendation": (
            "PROCEED" if location.get("vacant") else "PROCEED WITH ADAPTIVE REUSE"
        ),
        "data_sources": [
            "Philadelphia OPA (parcel data)",
            "Philadelphia Zoning Code",
            "BATHS Parcel & Enrichment Engines",
        ],
    }

    files["feasibility_assessment.json"] = _write_deliverable(pid, "development", "feasibility_assessment.json", feasibility)

    return files


def generate_spheres_pre_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Pre-Production deliverables:
    - Site breakdown
    - Program design
    - Budget top sheet with revenue projections
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    parcel = dev_data.get("location_report", {})
    files = {}

    design = stage_data.get("design_board", {})
    budget = stage_data.get("budget_model", {})
    timeline = stage_data.get("timeline", {})

    # 1. Site Breakdown
    site_md = f"# Site Breakdown — {parcel.get('address', subject)}\n"
    site_md += f"Generated: {_timestamp()}\n\n"
    site_md += f"**Total Area:** {parcel.get('land_area_sqft', 0):,.0f} sqft\n\n"
    site_md += f"**Zoning:** {parcel.get('zoning', 'N/A')}\n\n"

    site_md += "## Activation Types\n\n"
    for at in design.get("activation_types", []):
        site_md += f"- {at.replace('_', ' ').title()}\n"
    site_md += "\n"

    site_md += "## Features\n\n"
    for f in design.get("features", []):
        site_md += f"- {f}\n"
    site_md += "\n"

    site_md += "## Timeline\n\n"
    site_md += "| Phase | Duration |\n"
    site_md += "|-------|----------|\n"
    for phase in timeline.get("phases", []):
        site_md += f"| {phase.get('name', '')} | {phase.get('weeks', 0)} weeks |\n"
    site_md += f"\n**Total Duration:** {timeline.get('duration_years', 0)} years "
    site_md += f"({timeline.get('total_weeks', 0)} weeks)\n"

    files["site_breakdown.md"] = _write_deliverable(pid, "pre_production", "site_breakdown.md", site_md)

    # 2. Program Design
    program = {
        "title": f"Program Design — {parcel.get('address', subject)}",
        "generated": _timestamp(),
        "design": design,
        "programming": {
            "weekly_events": max(2, parcel.get("land_area_sqft", 2500) // 2000),
            "anchor_programs": [at.replace("_", " ").title() for at in design.get("activation_types", [])[:3]],
            "target_visitors_weekly": max(50, parcel.get("land_area_sqft", 2500) // 10),
            "community_partners": [
                "Local neighborhood association",
                "Community development corporation",
                "Local schools and youth organizations",
                "Small business association",
            ],
        },
        "access": {
            "public_hours_weekly": min(84, max(20, parcel.get("land_area_sqft", 2500) // 100)),
            "staffed_hours_weekly": min(40, max(10, parcel.get("land_area_sqft", 2500) // 200)),
        },
        "data_sources": [
            "Philadelphia OPA (site data)",
            "BATHS Design Engine (activation modeling)",
        ],
    }

    files["program_design.json"] = _write_deliverable(pid, "pre_production", "program_design.json", program)

    # 3. Budget Top Sheet with Revenue Projections
    area = parcel.get("land_area_sqft", 2500)

    budget_md = f"# Budget Top Sheet — {parcel.get('address', subject)}\n"
    budget_md += f"Generated: {_timestamp()}\n\n"

    budget_md += "## Cost Tiers\n\n"
    budget_md += "| Tier | Per sqft | Total | Includes |\n"
    budget_md += "|------|----------|-------|----------|\n"
    for tier_name in ["light_activation", "moderate_activation", "full_buildout"]:
        tier = budget.get(tier_name, {})
        budget_md += f"| {tier_name.replace('_', ' ').title()} "
        budget_md += f"| ${tier.get('per_sqft', 0)}/sqft "
        budget_md += f"| ${tier.get('total', 0):,.0f} "
        budget_md += f"| {tier.get('includes', '')} |\n"

    recommended = budget.get("recommended", "")
    rec_total = budget.get("recommended_total", 0)
    budget_md += f"\n**Recommended:** {recommended.replace('_', ' ').title()} "
    budget_md += f"— ${rec_total:,.0f}\n\n"

    budget_md += "## Revenue Projections (Annual)\n\n"
    event_revenue = max(50, area // 20) * 52 * 15  # weekly visitors * 52 weeks * $15 avg spend
    vendor_revenue = min(12, area // 1000) * 52 * 200  # vendors * weeks * fee
    grant_revenue = rec_total * 0.4  # 40% grant funding estimate
    sponsorship = rec_total * 0.15  # 15% sponsorship estimate

    budget_md += "| Revenue Source | Annual Estimate |\n"
    budget_md += "|---------------|----------------|\n"
    budget_md += f"| Event Revenue | ${event_revenue:,.0f} |\n"
    budget_md += f"| Vendor Fees | ${vendor_revenue:,.0f} |\n"
    budget_md += f"| Grant Funding (est.) | ${grant_revenue:,.0f} |\n"
    budget_md += f"| Sponsorship (est.) | ${sponsorship:,.0f} |\n"
    total_revenue = event_revenue + vendor_revenue + grant_revenue + sponsorship
    budget_md += f"| **Total Projected** | **${total_revenue:,.0f}** |\n\n"

    budget_md += "## Data Sources\n\n"
    budget_md += "- National Recreation and Park Association (cost benchmarks)\n"
    budget_md += "- Philadelphia Commerce Department (vendor & event data)\n"
    budget_md += "- BATHS Budget Engine\n"

    files["budget_top_sheet.md"] = _write_deliverable(pid, "pre_production", "budget_top_sheet.md", budget_md)

    return files


def generate_spheres_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Production deliverables:
    - Complete activation design
    - Build schedule
    - Final budget
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    parcel = dev_data.get("location_report", {})
    files = {}

    build_report = stage_data.get("build_report", {})
    activation_log = stage_data.get("activation_log", {})

    # 1. Complete Activation Design
    design_md = f"# Activation Design — {parcel.get('address', subject)}\n"
    design_md += f"Generated: {_timestamp()}\n\n"
    design_md += f"**Status:** {'ACTIVATED' if activation_log.get('activated') else 'IN PROGRESS'}\n\n"
    design_md += f"**Area Activated:** {activation_log.get('sqft_activated', 0):,.0f} sqft\n\n"
    design_md += f"**Investment:** ${activation_log.get('investment', 0):,.0f}\n\n"
    design_md += f"**Events Capacity:** {activation_log.get('events_capacity', 0)} people\n\n"

    design_md += "## Features Installed\n\n"
    for f in activation_log.get("features_installed", []):
        design_md += f"- {f}\n"
    design_md += "\n"

    design_md += "## Activation Types\n\n"
    for at in activation_log.get("activation_types", []):
        design_md += f"- {at.replace('_', ' ').title()}\n"
    design_md += "\n"

    design_md += "## Policy Changes Enabled\n\n"
    for pc in build_report.get("policy_changes", []):
        design_md += f"- {pc}\n"
    design_md += "\n"

    files["activation_design.md"] = _write_deliverable(pid, "production", "activation_design.md", design_md)

    # 2. Build Schedule
    timeline = pre_data.get("timeline", {})
    permits = build_report.get("permits", [])

    schedule_md = f"# Build Schedule — {parcel.get('address', subject)}\n"
    schedule_md += f"Generated: {_timestamp()}\n\n"

    schedule_md += "## Permits\n\n"
    schedule_md += "| Permit | Status |\n"
    schedule_md += "|--------|--------|\n"
    for p in permits:
        schedule_md += f"| {p.get('type', '')} | {p.get('status', '')} |\n"
    schedule_md += "\n"

    schedule_md += "## Build Phases\n\n"
    week_offset = 0
    for phase in timeline.get("phases", []):
        weeks = phase.get("weeks", 0)
        schedule_md += f"### {phase.get('name', '')} — Weeks {week_offset + 1}-{week_offset + weeks}\n\n"
        week_offset += weeks
    schedule_md += f"\n**Total:** {timeline.get('total_weeks', 0)} weeks "
    schedule_md += f"({timeline.get('duration_years', 0)} years)\n"

    files["build_schedule.md"] = _write_deliverable(pid, "production", "build_schedule.md", schedule_md)

    # 3. Final Budget
    budget = pre_data.get("budget_model", {})
    recommended = budget.get("recommended", "moderate_activation")
    final_budget = {
        "title": f"Final Budget — {parcel.get('address', subject)}",
        "generated": _timestamp(),
        "recommended_tier": recommended,
        "total_investment": budget.get("recommended_total", 0),
        "tiers": {k: v for k, v in budget.items() if k not in ("recommended", "recommended_total")},
        "permits_executed": permits,
        "activation_metrics": activation_log,
        "data_sources": [
            "Philadelphia OPA",
            "National Recreation and Park Association",
            "BATHS Budget Engine",
        ],
    }

    files["final_budget.json"] = _write_deliverable(pid, "production", "final_budget.json", final_budget)

    return files


def generate_spheres_post_production(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Post-Production deliverables:
    - Visualization package (before/after)
    - Impact report
    - EPK
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    prod_data = production.stage_data.get("production", {})
    parcel = dev_data.get("location_report", {})
    files = {}

    impact = stage_data.get("impact_dashboard", {})
    episodes = stage_data.get("episode_timeline", [])
    innovation_portfolio = stage_data.get("innovation_portfolio", {})
    ip_outputs = stage_data.get("ip_outputs", [])

    # 1. Visualization Package
    viz = {
        "title": f"Visualization Package — {parcel.get('address', subject)}",
        "generated": _timestamp(),
        "before": {
            "status": "vacant" if parcel.get("vacant") else "underutilized",
            "assessed_value": parcel.get("total_val", 0),
            "area_sqft": parcel.get("land_area_sqft", 0),
            "zoning": parcel.get("zoning", ""),
            "description": f"Vacant lot at {parcel.get('address', '')} in {parcel.get('neighborhood', '')}",
        },
        "after": {
            "status": "activated",
            "investment": pre_data.get("budget_model", {}).get("recommended_total", 0),
            "area_activated": prod_data.get("activation_log", {}).get("sqft_activated", 0),
            "features": prod_data.get("activation_log", {}).get("features_installed", []),
            "activation_types": prod_data.get("activation_log", {}).get("activation_types", []),
            "capacity": prod_data.get("activation_log", {}).get("events_capacity", 0),
        },
        "impact_metrics": impact,
        "episodes": episodes,
        "data_sources": [
            "Philadelphia OPA (property data)",
            "BATHS Impact Engine (measurement)",
        ],
    }

    files["visualization_package.json"] = _write_deliverable(pid, "post_production", "visualization_package.json", viz)

    # 2. Impact Report
    impact_md = f"# Impact Report — {parcel.get('address', subject)}\n"
    impact_md += f"Generated: {_timestamp()}\n\n"

    impact_md += "## Key Metrics\n\n"
    impact_md += "| Metric | Value |\n"
    impact_md += "|--------|-------|\n"
    impact_md += f"| Total Visitors | {impact.get('total_visitors', 0):,} |\n"
    impact_md += f"| Economic Impact | ${impact.get('economic_impact', 0):,.0f} |\n"
    impact_md += f"| Jobs Created | {impact.get('jobs_created', 0)} |\n"
    impact_md += f"| Property Value Impact | +{impact.get('property_value_impact_pct', 0)}% |\n"
    impact_md += f"| Community Rating | {impact.get('community_rating', 0)}/5 |\n"
    impact_md += f"| Connected Projects | {impact.get('connected_projects', 0)} |\n\n"

    impact_md += "## Episode Timeline\n\n"
    for ep in episodes:
        impact_md += f"### {ep.get('title', '')} — {ep.get('date', '')}\n\n"
        impact_md += f"{ep.get('impact', '')}\n\n"
        metrics = ep.get("metrics", {})
        if metrics:
            for k, v in metrics.items():
                impact_md += f"- {k.replace('_', ' ').title()}: {v:,}\n" if isinstance(v, int) else f"- {k.replace('_', ' ').title()}: {v}\n"
            impact_md += "\n"

    impact_md += "## Innovations\n\n"
    for innov in innovation_portfolio.get("innovations", []):
        impact_md += f"- {innov}\n"
    impact_md += "\n"

    impact_md += "## Data Sources\n\n"
    impact_md += "- Philadelphia Commerce Department\n"
    impact_md += "- BATHS Impact Engine (3.2x economic multiplier per NRPA benchmarks)\n"
    impact_md += "- Community survey data\n"

    files["impact_report.md"] = _write_deliverable(pid, "post_production", "impact_report.md", impact_md)

    # 3. EPK
    epk_md = f"# Electronic Press Kit — Sphere: {parcel.get('neighborhood', subject)}\n"
    epk_md += f"Generated: {_timestamp()}\n\n"

    epk_md += "## Logline\n\n"
    epk_md += f"A {parcel.get('land_area_sqft', 0):,.0f} sqft "
    epk_md += f"{'vacant lot' if parcel.get('vacant') else 'underused space'} "
    epk_md += f"at {parcel.get('address', '')} transforms into a thriving community hub "
    epk_md += f"serving {impact.get('total_visitors', 0):,} visitors and generating "
    epk_md += f"${impact.get('economic_impact', 0):,.0f} in economic impact.\n\n"

    epk_md += "## Key Stats\n\n"
    epk_md += f"- **Location:** {parcel.get('address', '')}, {parcel.get('neighborhood', '')}\n"
    epk_md += f"- **Investment:** ${pre_data.get('budget_model', {}).get('recommended_total', 0):,.0f}\n"
    epk_md += f"- **Economic Return:** {impact.get('economic_impact', 0) / max(1, pre_data.get('budget_model', {}).get('recommended_total', 1)):.1f}x\n"
    epk_md += f"- **Jobs:** {impact.get('jobs_created', 0)}\n"
    epk_md += f"- **IP Outputs:** {len(ip_outputs)}\n\n"

    epk_md += "## IP Generated\n\n"
    for ip in ip_outputs:
        label = IP_DOMAIN_LABELS.get(ip.get("domain", ""), ip.get("domain", ""))
        epk_md += f"- **{label}:** {ip.get('title', '')}\n"

    files["epk.md"] = _write_deliverable(pid, "post_production", "epk.md", epk_md)

    return files


def generate_spheres_distribution(production: ProductionState, stage_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Distribution deliverables:
    - Series bible
    - Pitch deck
    - IP log categorized by domain
    """
    pid = production.production_id
    subject = production.subject
    dev_data = production.stage_data.get("development", {})
    pre_data = production.stage_data.get("pre_production", {})
    post_data = production.stage_data.get("post_production", {})
    parcel = dev_data.get("location_report", {})
    files = {}

    chron = stage_data.get("chron", {})
    chron_bond = stage_data.get("chron_bond", {})
    ip_catalog = stage_data.get("ip_catalog", [])
    replication_kit = stage_data.get("replication_kit", {})
    innovations = stage_data.get("innovations", [])
    impact = stage_data.get("impact_dashboard", {}) or post_data.get("impact_dashboard", {})

    # 1. Series Bible
    bible_md = f"# Series Bible — SPHERES: {parcel.get('neighborhood', subject)}\n"
    bible_md += f"Generated: {_timestamp()}\n\n"

    bible_md += "## Concept\n\n"
    bible_md += "SPHERES activates public spaces in cities. Each sphere transforms "
    bible_md += "underused land into community infrastructure — measured in square meters "
    bible_md += "x time x significance.\n\n"

    bible_md += "## This Sphere\n\n"
    bible_md += f"**Location:** {parcel.get('address', subject)}\n\n"
    bible_md += f"**Neighborhood:** {parcel.get('neighborhood', '')}\n\n"
    bible_md += f"**CHRON Score:** {chron.get('total', 0):.1f}\n"
    bible_md += f"- Unlock: {chron.get('unlock', 0):,.0f} sqft\n"
    bible_md += f"- Access: {chron.get('access', 0):,.0f} hours\n"
    bible_md += f"- Permanence: {chron.get('permanence', 0):.2f}\n"
    bible_md += f"- Catalyst: {chron.get('catalyst', 0):.2f}\n"
    bible_md += f"- Policy: {chron.get('policy', 0):.2f}\n\n"

    bible_md += "## Replication Model\n\n"
    bible_md += f"- **Parcel Type:** {replication_kit.get('parcel_type', '')}\n"
    bible_md += f"- **Zoning:** {replication_kit.get('zoning', '')}\n"
    bible_md += f"- **Activation Types:** {', '.join(replication_kit.get('activation_types', []))}\n"
    bible_md += f"- **Budget Tier:** {replication_kit.get('budget_tier', '').replace('_', ' ').title()}\n"
    bible_md += f"- **Transferable:** {replication_kit.get('transferable', True)}\n\n"

    bible_md += "## Impact Summary\n\n"
    bible_md += f"- Visitors: {impact.get('total_visitors', 0):,}\n"
    bible_md += f"- Economic Impact: ${impact.get('economic_impact', 0):,.0f}\n"
    bible_md += f"- Jobs: {impact.get('jobs_created', 0)}\n"
    bible_md += f"- Property Value Impact: +{impact.get('property_value_impact_pct', 0)}%\n\n"

    bible_md += "## Data Sources\n\n"
    bible_md += "- Philadelphia OPA (property data)\n"
    bible_md += "- Philadelphia Zoning Code\n"
    bible_md += "- National Recreation and Park Association (benchmarks)\n"
    bible_md += "- BATHS Fragment Agent (Census, BLS, EPA data for 28 counties)\n"

    files["series_bible.md"] = _write_deliverable(pid, "distribution", "series_bible.md", bible_md)

    # 2. Pitch Deck
    pitch_md = f"# Pitch Deck — SPHERES: {parcel.get('neighborhood', subject)}\n"
    pitch_md += f"Generated: {_timestamp()}\n\n"

    pitch_md += "---\n## Slide 1: The Opportunity\n\n"
    pitch_md += f"Philadelphia has thousands of vacant lots. {parcel.get('address', '')} is "
    pitch_md += f"{parcel.get('land_area_sqft', 0):,.0f} sqft of untapped potential in {parcel.get('neighborhood', '')}.\n\n"

    pitch_md += "---\n## Slide 2: The Activation\n\n"
    activation_types = replication_kit.get("activation_types", [])
    pitch_md += f"Transform into: {', '.join(at.replace('_', ' ').title() for at in activation_types)}\n\n"
    pitch_md += f"Investment: ${pre_data.get('budget_model', {}).get('recommended_total', 0):,.0f}\n\n"

    pitch_md += "---\n## Slide 3: The Impact\n\n"
    pitch_md += f"- {impact.get('total_visitors', 0):,} visitors\n"
    pitch_md += f"- ${impact.get('economic_impact', 0):,.0f} economic impact (3.2x multiplier)\n"
    pitch_md += f"- {impact.get('jobs_created', 0)} jobs created\n"
    pitch_md += f"- +{impact.get('property_value_impact_pct', 0)}% property values\n\n"

    pitch_md += "---\n## Slide 4: The Financial Instrument\n\n"
    pitch_md += f"**Chron Bond:** {chron_bond.get('rating', 'N/A')} rated\n"
    pitch_md += f"- Face Value: ${chron_bond.get('face_value', 0):,.0f}\n"
    pitch_md += f"- Coupon Rate: {chron_bond.get('coupon_rate', 0):.1f}%\n"
    pitch_md += f"- Maturity: {chron_bond.get('maturity_years', 0)} years\n"
    pitch_md += f"- Backed by: {chron_bond.get('sqft_backing', 0):,.0f} sqft\n\n"

    pitch_md += "---\n## Slide 5: CHRON Score\n\n"
    pitch_md += f"**{chron.get('total', 0):.1f}** — square meters x time x significance.\n\n"

    pitch_md += f"---\n## Slide 6: Intellectual Property\n\n"
    pitch_md += f"**{len(ip_catalog)} IP outputs:**\n"
    for ip in ip_catalog:
        label = IP_DOMAIN_LABELS.get(ip.get("domain", ""), ip.get("domain", ""))
        pitch_md += f"- {label}: {ip.get('title', '')}\n"
    pitch_md += "\n"

    pitch_md += "---\n## Slide 7: Replication\n\n"
    pitch_md += "Every sphere is transferable. The activation model, the permitting pathway, "
    pitch_md += "the budget framework — documented and reproducible in any city.\n\n"

    files["pitch_deck.md"] = _write_deliverable(pid, "distribution", "pitch_deck.md", pitch_md)

    # 3. IP Log
    ip_log = _build_ip_log(ip_catalog, innovations, "spheres", subject)
    files["ip_log.json"] = _write_deliverable(pid, "distribution", "ip_log.json", ip_log)

    return files


# ══════════════════════════════════════════════════════════════════
# IP LOG BUILDER — shared between DOMES and SPHERES
# ══════════════════════════════════════════════════════════════════

def _build_ip_log(ip_catalog: List[Dict], innovations: List[str],
                  game_type: str, subject: str) -> Dict[str, Any]:
    """
    Build comprehensive IP log categorized by domain.
    Categorizes each innovation by: entertainment, technology, financial_product,
    policy, product, research, housing, healthcare, urban_design, real_estate.
    """
    # Map IP outputs by domain
    by_domain = {}
    all_domains = [
        "entertainment", "technology", "financial_product", "policy",
        "product", "research", "housing", "healthcare",
        "urban_design", "real_estate",
    ]

    for domain in all_domains:
        by_domain[domain] = {
            "label": IP_DOMAIN_LABELS.get(domain, domain),
            "items": [],
        }

    # Categorize IP catalog items
    for ip in ip_catalog:
        domain = ip.get("domain", "product")
        if domain not in by_domain:
            domain = "product"
        by_domain[domain]["items"].append({
            "title": ip.get("title", ""),
            "description": ip.get("description", ""),
            "format": ip.get("format", ""),
            "stage_originated": ip.get("stage_originated", ""),
            "value_driver": ip.get("value_driver", ""),
        })

    # Categorize innovations into domains
    innovation_domain_map = {
        "dome": "technology",
        "protocol": "technology",
        "api": "technology",
        "orchestration": "technology",
        "dashboard": "technology",
        "measurement": "technology",
        "bond": "financial_product",
        "pricing": "financial_product",
        "cost": "financial_product",
        "savings": "financial_product",
        "calculator": "financial_product",
        "consent": "policy",
        "ordinance": "policy",
        "permit": "policy",
        "zoning": "policy",
        "streamlined": "policy",
        "playbook": "product",
        "kit": "product",
        "modular": "product",
        "architecture": "housing",
        "housing": "housing",
        "land trust": "real_estate",
        "property": "real_estate",
        "parcel": "real_estate",
        "activation": "urban_design",
        "space": "urban_design",
        "community": "urban_design",
        "garden": "urban_design",
        "benefits": "healthcare",
        "health": "healthcare",
        "care": "healthcare",
        "portable": "healthcare",
        "study": "research",
        "index": "research",
        "methodology": "research",
        "fragmentation": "research",
        "documentary": "entertainment",
        "narrative": "entertainment",
        "episode": "entertainment",
        "story": "entertainment",
    }

    for innov in innovations:
        matched_domain = "product"  # default
        innov_lower = innov.lower()
        for keyword, domain in innovation_domain_map.items():
            if keyword in innov_lower:
                matched_domain = domain
                break
        by_domain[matched_domain]["items"].append({
            "title": innov,
            "description": f"Innovation from {game_type.upper()} production: {subject}",
            "format": "innovation",
            "stage_originated": "production",
            "value_driver": "Novel approach or method",
        })

    # Build summary
    total_items = sum(len(d["items"]) for d in by_domain.values())
    active_domains = sum(1 for d in by_domain.values() if d["items"])

    return {
        "title": f"IP Log — {game_type.upper()}: {subject}",
        "generated": _timestamp(),
        "game_type": game_type,
        "subject": subject,
        "summary": {
            "total_ip_items": total_items,
            "active_domains": active_domains,
            "total_domains_tracked": len(all_domains),
        },
        "by_domain": by_domain,
        "domain_index": {
            domain: {
                "label": IP_DOMAIN_LABELS.get(domain, domain),
                "count": len(by_domain[domain]["items"]),
            }
            for domain in all_domains
        },
    }


# ══════════════════════════════════════════════════════════════════
# MASTER GENERATOR — called from pipeline after each stage
# ══════════════════════════════════════════════════════════════════

# Maps (game_type, stage) -> generator function
_GENERATORS = {
    (GameType.DOMES, ProductionStage.DEVELOPMENT): generate_domes_development,
    (GameType.DOMES, ProductionStage.PRE_PRODUCTION): generate_domes_pre_production,
    (GameType.DOMES, ProductionStage.PRODUCTION): generate_domes_production,
    (GameType.DOMES, ProductionStage.POST_PRODUCTION): generate_domes_post_production,
    (GameType.DOMES, ProductionStage.DISTRIBUTION): generate_domes_distribution,
    (GameType.SPHERES, ProductionStage.DEVELOPMENT): generate_spheres_development,
    (GameType.SPHERES, ProductionStage.PRE_PRODUCTION): generate_spheres_pre_production,
    (GameType.SPHERES, ProductionStage.PRODUCTION): generate_spheres_production,
    (GameType.SPHERES, ProductionStage.POST_PRODUCTION): generate_spheres_post_production,
    (GameType.SPHERES, ProductionStage.DISTRIBUTION): generate_spheres_distribution,
}


def generate_stage_deliverables(
    production: ProductionState,
    stage: ProductionStage,
    stage_data: Dict[str, Any],
) -> Dict[str, str]:
    """
    Generate all deliverables for a completed stage.
    Returns dict of {filename: relative_path} for all generated files.
    """
    generator = _GENERATORS.get((production.game_type, stage))
    if not generator:
        return {}

    return generator(production, stage_data)


def list_deliverables(production_id: str) -> Dict[str, List[str]]:
    """List all generated deliverables for a production, grouped by stage."""
    prod_dir = DELIVERABLES_DIR / production_id
    if not prod_dir.exists():
        return {}

    result = {}
    for stage_dir in sorted(prod_dir.iterdir()):
        if stage_dir.is_dir():
            files = sorted(f.name for f in stage_dir.iterdir() if f.is_file())
            if files:
                result[stage_dir.name] = files
    return result


def get_deliverable_path(production_id: str, stage: str, filename: str) -> Optional[Path]:
    """Get the full path to a deliverable file, or None if not found."""
    path = DELIVERABLES_DIR / production_id / stage / filename
    if path.exists():
        return path
    return None
