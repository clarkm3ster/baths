"""
BATHS Game Engine - Main API
Unified game engine for DOMES + SPHERES
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

from models import (
    Player, ProductionState, StageAction, StageResult,
    GameType, ProductionStage, CompletedProduction,
    CosmDimensions, ChronDimensions
)
from pipeline import PipelineDirector

# In-memory storage (TODO: replace with SQLite)
players: Dict[str, Player] = {}
productions: Dict[str, ProductionState] = {}

# Load API registry
with open("../../api-registry.json", "r") as f:
    API_REGISTRY = json.load(f)

pipeline_director: Optional[PipelineDirector] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize pipeline director on startup"""
    global pipeline_director
    pipeline_director = PipelineDirector(API_REGISTRY)
    yield
    # Cleanup
    await pipeline_director.client.aclose()


app = FastAPI(
    title="BATHS Game Engine",
    description="Unified game engine for DOMES + SPHERES production games",
    version="0.1.0",
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
    
    # Check if player already has active production
    if player.active_production:
        raise HTTPException(status_code=400, detail="Player already has active production")
    
    # Create production
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
    
    # Call pipeline director
    result = await pipeline_director.advance_stage(production, action.data)
    
    # Update production state
    if result.success:
        production.progress = result.progress
        production.updated_at = datetime.utcnow()
        
        # Merge result data into stage_data
        stage_key = production.stage.value
        production.stage_data[stage_key] = result.data
        
        # Advance to next stage if specified
        if result.new_stage:
            production.stage = result.new_stage
        elif result.progress >= 100.0:
            # Production complete — move to portfolio
            await _complete_production(production)
    
    return result


async def _complete_production(production: ProductionState):
    """Move completed production to player portfolio"""
    # Find player
    player = None
    for p in players.values():
        if p.active_production and p.active_production.production_id == production.production_id:
            player = p
            break
    
    if not player:
        return
    
    # Create completed production record
    completed = CompletedProduction(
        production_id=production.production_id,
        game_type=production.game_type,
        subject=production.subject
    )
    
    # Extract final scores from distribution stage
    dist_data = production.stage_data.get("distribution", {})
    
    if production.game_type == GameType.DOMES:
        cosm_data = dist_data.get("cosm", {})
        completed.cosm = CosmDimensions(**cosm_data) if cosm_data else None
        completed.ip_created = dist_data.get("ip", [])
        completed.industries_changed = dist_data.get("industries_changed", [])
        
        # Add to portfolio
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
        
        # Add to portfolio
        player.portfolio.spheres_completed.append(completed)
        if completed.chron:
            player.portfolio.total_chron.unlock += completed.chron.unlock
            player.portfolio.total_chron.access += completed.chron.access
            player.portfolio.total_chron.permanence += completed.chron.permanence
            player.portfolio.total_chron.catalyst += completed.chron.catalyst
            player.portfolio.total_chron.policy += completed.chron.policy
    
    # Merge innovations
    innovations = dist_data.get("innovations", [])
    completed.innovations = innovations
    player.portfolio.innovations.extend(innovations)
    
    # Clear active production
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
        "equation": "Cosm × Chron = Flourishing"
    }


@app.get("/api/health")
def health():
    """Health check"""
    return {
        "status": "ok",
        "engine": "BATHS Game Engine",
        "version": "0.1.0",
        "players": len(players),
        "active_productions": len([p for p in players.values() if p.active_production])
    }


# ========== SERVE FRONTEND ==========

# Mount static files if they exist
if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend for all non-API routes"""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Serve index.html for all routes (SPA)
        return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
