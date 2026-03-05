"""
DOMES Profiles API - FastAPI application.

Main entry point with CORS, routers, lifespan, and root endpoint.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables, SessionLocal
from .seed import seed_profiles
from .routes.profiles import router as profiles_router
from .routes.costs import router as costs_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables and seed data. Shutdown: cleanup."""
    logger.info("Starting DOMES Profiles API...")
    create_tables()
    logger.info("Database tables created.")

    db = SessionLocal()
    try:
        seed_profiles(db)
    except Exception as exc:
        logger.error("Seed failed: %s", exc)
    finally:
        db.close()

    logger.info("DOMES Profiles API ready on port 8004.")
    yield
    logger.info("Shutting down DOMES Profiles API.")


app = FastAPI(
    title="DOMES Profiles API",
    description=(
        "Person profile system for the DOMES project. "
        "Generates composite profiles showing the cost of fragmented "
        "government data systems and the savings from coordination."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "domes-profiles", "port": 8004}


# Routers
app.include_router(profiles_router)
app.include_router(costs_router)


@app.get("/")
def root():
    """Root endpoint listing available APIs."""
    return {
        "service": "DOMES Profiles API",
        "version": "1.0.0",
        "description": (
            "Person profile system showing the cost of fragmented government "
            "data systems and the savings achievable through coordination."
        ),
        "endpoints": {
            "profiles": {
                "list": "GET /api/profiles",
                "get": "GET /api/profiles/{id}",
                "generate": "POST /api/profiles/generate",
                "update": "PUT /api/profiles/{id}",
                "delete": "DELETE /api/profiles/{id}",
                "dome": "GET /api/profiles/{id}/dome",
                "compare": "POST /api/profiles/compare",
                "versions": "GET /api/profiles/{id}/versions",
                "circumstances": "GET /api/profiles/circumstances",
            },
        },
        "sample_profiles": [
            "sample-marcus-thompson",
            "sample-sarah-chen",
            "sample-james-williams",
            "sample-maria-rodriguez",
            "sample-robert-jackson",
        ],
    }
