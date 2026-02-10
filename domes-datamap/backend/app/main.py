from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, SessionLocal, Base
from app.models import System, Connection, Gap, Bridge
from app.seed import seed_all
from app.routes import systems, connections, gaps, person_map, bridges


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seeded = seed_all(db)
        if seeded:
            print("Database seeded with 21 systems, 13 connections, 18 gaps, and bridges.")
        else:
            print("Database already contains data, skipping seed.")
    finally:
        db.close()
    yield


app = FastAPI(
    title="DOMES DataMap API",
    description="Government data systems registry, connectivity model, gap analysis, and bridge solutions for the DOMES project.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers
app.include_router(systems.router)
app.include_router(connections.router)
app.include_router(gaps.router)
app.include_router(person_map.router)
app.include_router(bridges.router)


@app.get("/")
def root():
    return {
        "name": "DOMES DataMap API",
        "version": "1.0.0",
        "endpoints": {
            "systems": "/api/systems",
            "system_detail": "/api/systems/{system_id}",
            "connections": "/api/connections",
            "connection_matrix": "/api/connections/matrix",
            "gaps": "/api/gaps",
            "gap_detail": "/api/gaps/{gap_id}",
            "person_map": "/api/person-map (POST)",
            "bridges": "/api/bridges",
            "bridge_priority": "/api/bridges/priority",
            "bridges_for_gap": "/api/bridges/{gap_id}",
            "consent_pathway": "/api/bridges/consent-pathway (POST)",
            "stats": "/api/stats",
        },
    }
