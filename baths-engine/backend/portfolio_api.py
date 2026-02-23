"""
BATHS Portfolio API — Public-facing endpoints for completed productions.

Serves data for domes.cc and spheres.land portfolio sites.
Every completed production becomes a publicly viewable page.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
from pathlib import Path

from models import (
    GameType, CompletedProduction, CosmDimensions, ChronDimensions,
    ProductionStage
)
from deliverables import list_deliverables, DELIVERABLES_DIR

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

# Published productions store — populated when productions complete
# In production this would be a database; here we use in-memory with JSON backup
_published: Dict[str, Dict[str, Any]] = {}

PUBLISH_DIR = Path(__file__).parent / "data" / "published"
PUBLISH_DIR.mkdir(parents=True, exist_ok=True)


def _load_published():
    """Load published productions from disk on startup."""
    for f in PUBLISH_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            _published[data["production_id"]] = data
        except Exception:
            pass


def publish_production(production_state, player_name: str = "Producer"):
    """
    Called when a production completes.  Snapshots the full production
    state into the published store so portfolio pages can serve it.
    """
    pid = production_state.production_id
    game_type = production_state.game_type.value if hasattr(production_state.game_type, 'value') else production_state.game_type

    # Build the full published record
    stage_data = production_state.stage_data or {}
    dist_data = stage_data.get("distribution", {})

    record = {
        "production_id": pid,
        "game_type": game_type,
        "subject": production_state.subject,
        "player_name": player_name,
        "completed_at": datetime.utcnow().isoformat(),
        "stage_data": stage_data,
        "deliverables": list_deliverables(pid),
    }

    # Extract scoring
    if game_type == "domes":
        cosm = dist_data.get("cosm", {})
        record["cosm"] = cosm
        dims = [cosm.get("rights", 0), cosm.get("research", 0), cosm.get("budget", 0),
                cosm.get("package", 0), cosm.get("deliverables", 0), cosm.get("pitch", 0)]
        record["cosm_total"] = min(dims) if dims and any(d > 0 for d in dims) else 0
        record["dome_bond"] = dist_data.get("dome_bond", {})
        record["ip_catalog"] = dist_data.get("ip_catalog", [])
        record["innovations"] = dist_data.get("innovations", [])
        record["industries_changed"] = dist_data.get("industries_changed", [])
        record["replication_kit"] = dist_data.get("replication_kit", {})
        record["narrative"] = dist_data.get("narrative", {})
        record["data_engine_stats"] = stage_data.get("development", {}).get("data_engine_stats", {})
    elif game_type == "spheres":
        chron = dist_data.get("chron", {})
        record["chron"] = chron
        base = chron.get("unlock", 0) * chron.get("access", 0)
        sig = (chron.get("permanence", 0) + chron.get("catalyst", 0) + chron.get("policy", 0)) / 3
        record["chron_total"] = base * (1 + sig)
        record["chron_bond"] = dist_data.get("chron_bond", {})
        record["ip_catalog"] = dist_data.get("ip_catalog", [])
        record["innovations"] = dist_data.get("innovations", [])
        record["replication_kit"] = dist_data.get("replication_kit", {})
        record["impact_dashboard"] = dist_data.get("impact_dashboard", {}) or stage_data.get("post_production", {}).get("impact_dashboard", {})
        record["data_engine_stats"] = stage_data.get("development", {}).get("data_engine_stats", {})

    _published[pid] = record

    # Persist to disk
    try:
        out = PUBLISH_DIR / f"{pid}.json"
        out.write_text(json.dumps(record, indent=2, default=str) + "\n")
    except Exception:
        pass

    return record


# ── Public API Endpoints ─────────────────────────────────────────────

@router.get("/domes")
def list_domes(sort: str = "date", order: str = "desc"):
    """List all completed dome productions for the domes.cc index."""
    domes = [p for p in _published.values() if p.get("game_type") == "domes"]

    if sort == "cosm":
        domes.sort(key=lambda d: d.get("cosm_total", 0), reverse=(order == "desc"))
    elif sort == "subject":
        domes.sort(key=lambda d: d.get("subject", ""), reverse=(order == "desc"))
    else:
        domes.sort(key=lambda d: d.get("completed_at", ""), reverse=(order == "desc"))

    # Return summary cards (not full stage data)
    cards = []
    for d in domes:
        dev_data = d.get("stage_data", {}).get("development", {})
        cards.append({
            "production_id": d["production_id"],
            "subject": d["subject"],
            "player_name": d.get("player_name", "Producer"),
            "completed_at": d.get("completed_at"),
            "cosm": d.get("cosm", {}),
            "cosm_total": d.get("cosm_total", 0),
            "dome_bond": d.get("dome_bond", {}),
            "rights_count": dev_data.get("rights_count", 0),
            "system_count": dev_data.get("system_count", 0),
            "cost_point_count": dev_data.get("cost_point_count", 0),
            "ip_count": len(d.get("ip_catalog", [])),
            "industries_changed": d.get("industries_changed", []),
        })

    return {"count": len(cards), "productions": cards}


@router.get("/spheres")
def list_spheres(sort: str = "date", order: str = "desc"):
    """List all completed sphere productions for the spheres.land index."""
    spheres = [p for p in _published.values() if p.get("game_type") == "spheres"]

    if sort == "chron":
        spheres.sort(key=lambda d: d.get("chron_total", 0), reverse=(order == "desc"))
    elif sort == "subject":
        spheres.sort(key=lambda d: d.get("subject", ""), reverse=(order == "desc"))
    else:
        spheres.sort(key=lambda d: d.get("completed_at", ""), reverse=(order == "desc"))

    cards = []
    for s in spheres:
        dev_data = s.get("stage_data", {}).get("development", {})
        location = dev_data.get("location_report", {})
        cards.append({
            "production_id": s["production_id"],
            "subject": s["subject"],
            "player_name": s.get("player_name", "Producer"),
            "completed_at": s.get("completed_at"),
            "chron": s.get("chron", {}),
            "chron_total": s.get("chron_total", 0),
            "chron_bond": s.get("chron_bond", {}),
            "location": {
                "address": location.get("address", ""),
                "neighborhood": location.get("neighborhood", ""),
                "land_area_sqft": location.get("land_area_sqft", 0),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
            },
            "impact": s.get("impact_dashboard", {}),
            "ip_count": len(s.get("ip_catalog", [])),
        })

    return {"count": len(cards), "productions": cards}


@router.get("/productions/{production_id}")
def get_published_production(production_id: str):
    """Get full production data for a portfolio page."""
    if production_id not in _published:
        raise HTTPException(status_code=404, detail="Production not found")

    prod = _published[production_id]

    # Build deliverable download links
    deliverables = prod.get("deliverables", {})
    deliverable_links = {}
    for stage, files in deliverables.items():
        deliverable_links[stage] = {
            f: f"/api/deliverables/{production_id}/{stage}/{f}"
            for f in files
        }

    return {
        **prod,
        "deliverable_links": deliverable_links,
    }


# Load on import
_load_published()
