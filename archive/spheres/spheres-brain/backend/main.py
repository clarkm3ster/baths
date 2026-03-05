"""
SPHERES Brain — API Gateway & Orchestrator
===========================================

The central nervous system of the SPHERES ecosystem.  This FastAPI
application runs on port **8009** and provides:

- **Unified parcel queries** that fan out to all four SPHERES micro-services
  (assets, legal, studio, viz) and merge the results.
- **Service registry** with health probes for every registered service.
- **Activity feed** spanning the entire ecosystem, seeded with 35+
  realistic Philadelphia events.
- **Webhook subscriptions** for real-time event forwarding.
- **Discovery scanner** that surfaces new parcels, policy changes,
  comparable-city innovations, and media mentions.
- **Ecosystem metrics** computed from the activity stream.

Launch
------
    cd spheres-brain/backend
    uvicorn main:app --host 0.0.0.0 --port 8009 --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.orchestrator import router as orchestrator_router
from routes.health import router as health_router
from routes.discovery import router as discovery_router


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown events
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: log a banner, initialise shared state.
    Shutdown: clean up (nothing to release for now).
    """
    print("=" * 60)
    print("  SPHERES Brain — API Gateway & Orchestrator")
    print("  Port 8009 | Philadelphia Public Space Activation")
    print("=" * 60)
    print()
    print("  Registered services:")
    from models.registry import SPHERES_SERVICES
    for svc in SPHERES_SERVICES:
        print(f"    - {svc.name:20s}  {svc.url}")
    print()
    print("  Activity tracker seeded with 35 events (past 7 days)")
    print("  Discovery scanner ready (parcels, policies, media, infra)")
    print("  All routes mounted. Ready to serve.")
    print("=" * 60)

    yield  # Application runs here

    print("SPHERES Brain shutting down.")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SPHERES Brain",
    description=(
        "API Gateway and Orchestrator for the SPHERES ecosystem — "
        "Philadelphia's platform for activating vacant public spaces. "
        "Unifies parcel data, legal pathways, community designs, and "
        "cinematic storytelling into a single intelligent API."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# CORS — allow frontends on any SPHERES port to reach the brain
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React / Next.js dev servers
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:5173",   # Vite dev servers
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://localhost:8006",   # spheres-assets
        "http://localhost:8007",   # spheres-studio
        "http://localhost:8008",   # spheres-viz
        "http://localhost:8009",   # spheres-brain (self)
        "http://localhost:8010",   # future services
        "*",                       # allow all in dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Mount routers
# ---------------------------------------------------------------------------

app.include_router(orchestrator_router, tags=["orchestrator"])
app.include_router(health_router, tags=["health"])
app.include_router(discovery_router, tags=["discovery"])


# ---------------------------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    """Landing page with API overview."""
    return {
        "service": "spheres-brain",
        "version": "0.1.0",
        "description": (
            "SPHERES Brain — API Gateway & Orchestrator for "
            "Philadelphia public space activation"
        ),
        "endpoints": {
            "query": "POST /api/query",
            "services": "GET /api/services",
            "activity": "GET /api/activity",
            "subscribe": "POST /api/subscribe",
            "metrics": "GET /api/metrics",
            "health": "GET /api/health",
            "health_service": "GET /api/health/{service}",
            "discovery_parcels": "GET /api/discovery/parcels",
            "discovery_policies": "GET /api/discovery/policies",
            "discovery_comparables": "GET /api/discovery/comparables",
            "discovery_media": "GET /api/discovery/media",
            "discovery_infrastructure": "GET /api/discovery/infrastructure",
            "discovery_scan": "GET /api/discovery/scan",
            "discovery_all": "GET /api/discovery/all",
            "docs": "GET /docs",
        },
        "port": 8009,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8009,
        reload=True,
    )
