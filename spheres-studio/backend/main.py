"""
SPHERES Studio — FastAPI Application Entry Point

Mounts all route modules and configures CORS for the React frontend.
Run with: uvicorn main:app --host 0.0.0.0 --port 8007 --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown hooks
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    print("SPHERES Studio API starting up ...")
    yield
    # Shutdown
    print("SPHERES Studio API shutting down ...")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SPHERES Studio API",
    description="Backend services for the SPHERES activation design studio.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow the Vite dev server and production front-end
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5190",   # Vite dev server
        "http://127.0.0.1:5190",
        "http://localhost:3000",
        "*",                       # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Import and mount route modules
# ---------------------------------------------------------------------------

from routes.designs import router as designs_router       # noqa: E402
from routes.costs import router as costs_router           # noqa: E402
from routes.timeline import router as timeline_router     # noqa: E402
from routes.collaboration import router as collab_router  # noqa: E402
from routes.world import router as world_router           # noqa: E402

app.include_router(designs_router)
app.include_router(costs_router)
app.include_router(timeline_router)
app.include_router(collab_router)
app.include_router(world_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["system"])
def health_check():
    """Lightweight health probe for load balancers and readiness checks."""
    return {
        "status": "ok",
        "service": "spheres-studio",
        "version": "1.0.0",
    }


# ---------------------------------------------------------------------------
# Run directly with `python main.py`
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        log_level="info",
    )
