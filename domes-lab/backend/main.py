"""
DOMES Innovation Laboratory — FastAPI Application.

The DOMES Lab manages 12 innovation domain specialists (teammates) that
generate breakthrough innovations for person-centered government.

Port: 8007
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, SessionLocal, engine
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and seed data on startup."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed teammates first (innovations reference them)
        from teammates import seed_teammates
        created_teammates = seed_teammates(db)
        if created_teammates:
            print(f"[seed] Created {len(created_teammates)} teammates")

        # Seed innovations
        from innovations import seed_innovations
        created_innovations = seed_innovations(db)
        if created_innovations:
            print(f"[seed] Created {len(created_innovations)} innovations")
    finally:
        db.close()

    print("[domes-lab] Backend ready on port 8007")
    yield


app = FastAPI(
    title="DOMES Innovation Laboratory",
    description=(
        "Backend API for the DOMES Innovation Lab — managing 12 innovation "
        "domain specialists that generate breakthrough innovations for "
        "person-centered government."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5181",
        "http://127.0.0.1:5181",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "domes-lab", "port": 8007}


# ── Routes ──────────────────────────────────────────────────────────────────
app.include_router(router)


# ── Root ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {
        "name": "DOMES Innovation Laboratory",
        "version": "1.0.0",
        "status": "operational",
        "api": "/api",
        "docs": "/docs",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
