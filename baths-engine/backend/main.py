"""
BATHS Game Engine - Main API
Unified game engine for DOMES + SPHERES
Now with elite data engines that get smarter over time.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
import json
import uuid
from datetime import datetime
import os
import logging

from models import (
    Player, ProductionState, StageAction, StageResult,
    GameType, ProductionStage, CompletedProduction,
    CosmDimensions, ChronDimensions
)
from pipeline import PipelineDirector
from data import initialize, scrape_all, scrape_engine, get_stats, start_scheduler, stop_scheduler
from pathlib import Path as _Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("baths.main")

# Fragment/Cosm data directory (repo root /data/)
FRAG_DATA = _Path(__file__).resolve().parent.parent.parent / "data"

def _read_json(path):
    """Read a JSON file, return None on failure."""
    try:
        return json.loads(path.read_text())
    except Exception:
        return None

# In-memory storage
players: Dict[str, Player] = {}
productions: Dict[str, ProductionState] = {}

# Load API registry
registry_path = os.path.join(os.path.dirname(__file__), "../../api-registry.json")
if os.path.exists(registry_path):
    with open(registry_path, "r") as f:
        API_REGISTRY = json.load(f)
else:
    API_REGISTRY = {"domes": {}, "spheres": {}}

pipeline_director: Optional[PipelineDirector] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize data engines and pipeline director on startup."""
    global pipeline_director

    # Initialize data engines — seed all engines with real data
    logger.info("Initializing BATHS data engines...")
    stats = initialize()
    logger.info(f"Data engines ready: {stats}")

    # Start background scrape scheduler
    start_scheduler()

    # Initialize pipeline director
    pipeline_director = PipelineDirector(API_REGISTRY)

    yield

    # Cleanup
    stop_scheduler()
    await pipeline_director.client.aclose()


app = FastAPI(
    title="BATHS Game Engine",
    description="Unified game engine for DOMES + SPHERES with elite data engines",
    version="0.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== PLAYER MANAGEMENT ==========

@app.post("/api/players", response_model=Player)
def create_player(name: str):
    """Create a new player"""
    player_id = str(uuid.uuid4())
    player = Player(player_id=player_id, name=name)
    players[player_id] = player
    return player


@app.get("/api/players/{player_id}", response_model=Player)
def get_player(player_id: str):
    """Get player state"""
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")
    return players[player_id]


@app.get("/api/players", response_model=list[Player])
def list_players():
    """List all players"""
    return list(players.values())


# ========== PRODUCTION MANAGEMENT ==========

@app.post("/api/productions/start", response_model=ProductionState)
def start_production(player_id: str, game_type: GameType, subject: str):
    """Start a new production"""
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")

    player = players[player_id]

    if player.active_production:
        raise HTTPException(status_code=400, detail="Player already has active production")

    production_id = str(uuid.uuid4())
    production = ProductionState(
        production_id=production_id,
        game_type=game_type,
        subject=subject,
        stage=ProductionStage.DEVELOPMENT,
        progress=0.0
    )

    productions[production_id] = production
    player.active_production = production
    player.current_game = game_type

    return production


@app.get("/api/productions/{production_id}", response_model=ProductionState)
def get_production(production_id: str):
    """Get production state"""
    if production_id not in productions:
        raise HTTPException(status_code=404, detail="Production not found")
    return productions[production_id]


@app.post("/api/productions/{production_id}/advance", response_model=StageResult)
async def advance_production(production_id: str, action: StageAction):
    """Advance production to next stage"""
    if production_id not in productions:
        raise HTTPException(status_code=404, detail="Production not found")

    production = productions[production_id]

    result = await pipeline_director.advance_stage(production, action.data)

    if result.success:
        production.progress = result.progress
        production.updated_at = datetime.utcnow()

        stage_key = production.stage.value
        production.stage_data[stage_key] = result.data

        if result.new_stage:
            production.stage = result.new_stage
        elif result.progress >= 100.0:
            await _complete_production(production)

    return result


async def _complete_production(production: ProductionState):
    """Move completed production to player portfolio"""
    player = None
    for p in players.values():
        if p.active_production and p.active_production.production_id == production.production_id:
            player = p
            break

    if not player:
        return

    completed = CompletedProduction(
        production_id=production.production_id,
        game_type=production.game_type,
        subject=production.subject
    )

    dist_data = production.stage_data.get("distribution", {})

    if production.game_type == GameType.DOMES:
        cosm_data = dist_data.get("cosm", {})
        completed.cosm = CosmDimensions(**cosm_data) if cosm_data else None
        completed.ip_created = dist_data.get("ip", [])
        completed.industries_changed = dist_data.get("industries_changed", [])

        player.portfolio.domes_completed.append(completed)
        if completed.cosm:
            player.portfolio.total_cosm.legal += completed.cosm.legal
            player.portfolio.total_cosm.data += completed.cosm.data
            player.portfolio.total_cosm.fiscal += completed.cosm.fiscal
            player.portfolio.total_cosm.coordination += completed.cosm.coordination
            player.portfolio.total_cosm.flourishing += completed.cosm.flourishing
            player.portfolio.total_cosm.narrative += completed.cosm.narrative

    elif production.game_type == GameType.SPHERES:
        chron_data = dist_data.get("chron", {})
        completed.chron = ChronDimensions(**chron_data) if chron_data else None

        player.portfolio.spheres_completed.append(completed)
        if completed.chron:
            player.portfolio.total_chron.unlock += completed.chron.unlock
            player.portfolio.total_chron.access += completed.chron.access
            player.portfolio.total_chron.permanence += completed.chron.permanence
            player.portfolio.total_chron.catalyst += completed.chron.catalyst
            player.portfolio.total_chron.policy += completed.chron.policy

    innovations = dist_data.get("innovations", [])
    completed.innovations = innovations
    player.portfolio.innovations.extend(innovations)

    player.active_production = None
    player.updated_at = datetime.utcnow()


# ========== PORTFOLIO ==========

@app.get("/api/players/{player_id}/portfolio")
def get_portfolio(player_id: str):
    """Get player portfolio"""
    if player_id not in players:
        raise HTTPException(status_code=404, detail="Player not found")

    player = players[player_id]
    return {
        "player": player.name,
        "portfolio": player.portfolio,
        "flourishing": player.portfolio.total_cosm.total * player.portfolio.total_chron.total
    }


# ========== DATA ENGINE ENDPOINTS ==========

@app.get("/api/data/stats")
def data_stats():
    """Get current data engine statistics — how much intelligence has accumulated."""
    return get_stats()


@app.post("/api/data/scrape")
async def trigger_scrape(engine: Optional[str] = None):
    """Trigger a scrape cycle. Optionally specify engine: legal, costs, systems, parcels."""
    if engine:
        results = await scrape_engine(engine)
    else:
        results = await scrape_all()
    return {"status": "completed", "results": results}


@app.get("/api/data/provisions")
def get_provisions(dimension: Optional[str] = None, limit: int = 50):
    """Get legal provisions from the data engine."""
    from data.store import get_store
    store = get_store()
    return {"provisions": store.get_provisions(dome_dimension=dimension, limit=limit)}


@app.get("/api/data/costs")
def get_costs(category: Optional[str] = None, limit: int = 50):
    """Get cost data points from the data engine."""
    from data.store import get_store
    store = get_store()
    return {"costs": store.get_costs(category=category, limit=limit)}


@app.get("/api/data/systems")
def get_systems(domain: Optional[str] = None):
    """Get government systems from the data engine."""
    from data.store import get_store
    store = get_store()
    return {
        "systems": store.get_systems(domain=domain),
        "links": store.get_system_links(),
    }


@app.get("/api/data/parcels")
def get_parcels(neighborhood: Optional[str] = None, vacant: Optional[bool] = None, limit: int = 50):
    """Get Philadelphia parcels from the data engine."""
    from data.store import get_store
    store = get_store()
    return {"parcels": store.get_parcels(neighborhood=neighborhood, vacant=vacant, limit=limit)}


@app.get("/api/data/enrichments")
def get_enrichments(enrichment_type: Optional[str] = None, limit: int = 50):
    """Get enrichment insights — cross-references, conflicts, opportunities."""
    from data.store import get_store
    store = get_store()
    return {"enrichments": store.get_enrichments(enrichment_type=enrichment_type, limit=limit)}


@app.get("/api/data/scrape-history")
def scrape_history(engine: Optional[str] = None, limit: int = 20):
    """View scrape run history."""
    from data.store import get_store
    store = get_store()
    return {"history": store.get_scrape_history(engine=engine, limit=limit)}


# ========== FRAGMENT / COSM AGENT DATA ==========

@app.get("/api/fragment/stats")
def fragment_stats():
    """Coverage and fragment counts from the Fragment scraper agent."""
    coverage = _read_json(FRAG_DATA / "meta" / "coverage.json")
    gaps = _read_json(FRAG_DATA / "meta" / "gaps.json")
    sources = _read_json(FRAG_DATA / "meta" / "sources.json")
    return {
        "coverage": coverage,
        "gaps": gaps,
        "sources": sources,
    }


@app.get("/api/fragment/county/{fips}")
def fragment_county(fips: str):
    """All scraped fragments for a given county FIPS code."""
    fragments_dir = FRAG_DATA / "fragments"
    result = {}
    if fragments_dir.exists():
        for source_dir in sorted(fragments_dir.iterdir()):
            if source_dir.is_dir():
                frag_file = source_dir / f"{fips}.json"
                data = _read_json(frag_file)
                if data:
                    result[source_dir.name] = data
    return {"fips": fips, "fragment_count": len(result), "fragments": result}


@app.get("/api/cosm/state")
def cosm_state():
    """The evolving Cosm currency state — total domes, savings, maturity."""
    state = _read_json(FRAG_DATA / "cosm.json")
    return state or {"total_domes": 0, "maturity": {"level": "seed"}}


@app.get("/api/cosm/domes/{fips}")
def cosm_domes(fips: str):
    """All assembled domes for a county."""
    domes_dir = FRAG_DATA / "domes" / fips
    result = {}
    if domes_dir.exists():
        for f in sorted(domes_dir.iterdir()):
            if f.suffix == ".json":
                data = _read_json(f)
                if data:
                    result[f.stem] = data
    return {"fips": fips, "dome_count": len(result), "domes": result}


@app.get("/api/cosm/dome/{fips}/{archetype}")
def cosm_dome(fips: str, archetype: str):
    """A specific dome for a county + archetype."""
    dome = _read_json(FRAG_DATA / "domes" / fips / f"{archetype}.json")
    if not dome:
        raise HTTPException(status_code=404, detail=f"No dome for {fips}/{archetype}")
    return dome


@app.get("/api/cosm/patterns")
def cosm_patterns():
    """Latest cross-dome patterns."""
    patterns_dir = FRAG_DATA / "patterns"
    if not patterns_dir.exists():
        return {"patterns": None}
    files = sorted(patterns_dir.glob("patterns-*.json"), reverse=True)
    if not files:
        return {"patterns": None}
    return {"patterns": _read_json(files[0])}


# ========== GAME INFO ==========

@app.get("/api/games")
def list_games():
    """List available games"""
    return {
        "games": [
            {
                "type": "domes",
                "name": "DOMES",
                "description": "Build a dome around one person using the entire US government",
                "currency": "Cosm",
                "dimensions": ["legal", "data", "fiscal", "coordination", "flourishing", "narrative"]
            },
            {
                "type": "spheres",
                "name": "SPHERES",
                "description": "Activate public spaces in cities",
                "currency": "Chron",
                "dimensions": ["unlock", "access", "permanence", "catalyst", "policy"]
            }
        ],
        "equation": "Cosm × Chron = Flourishing",
        "data_engines": get_stats(),
        "cosm_state": _read_json(FRAG_DATA / "cosm.json") or {"total_domes": 0},
        "fragment_coverage": _read_json(FRAG_DATA / "meta" / "coverage.json"),
    }


@app.get("/api/health")
def health():
    """Health check with data engine status"""
    stats = get_stats()
    return {
        "status": "ok",
        "engine": "BATHS Game Engine",
        "version": "0.2.0",
        "players": len(players),
        "active_productions": len([p for p in players.values() if p.active_production]),
        "data_engines": stats,
    }


# ========== SERVE FRONTEND ==========

if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes"""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
