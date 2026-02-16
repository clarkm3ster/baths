"""
SPHERES Innovation Laboratory — FastAPI Application Entry Point.
Port 8010 | Philadelphia Public Space Activation Innovation Engine.
"""

import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, SessionLocal, engine
from models import Innovation, Teammate
from routes import router
from teammates import TEAMMATE_REGISTRY, seed_teammates


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("  SPHERES Innovation Laboratory")
    print("  Port 8010 | Public Space Activation R&D")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_teammates(db)
        seed_innovations(db)
    finally:
        db.close()

    print(f"  {len(TEAMMATE_REGISTRY)} teammates loaded")
    print("  Ready.\n")
    yield
    print("SPHERES Lab shutting down.")


def seed_innovations(db):
    """Idempotent: insert seed innovations if table is empty."""
    if db.query(Innovation).count() > 0:
        return

    from innovations import SEED_INNOVATIONS

    base_time = datetime.now(timezone.utc) - timedelta(days=30)
    counter = 0

    for slug, innovations in SEED_INNOVATIONS.items():
        teammate = db.query(Teammate).filter_by(slug=slug).first()
        if not teammate:
            continue
        for innov in innovations:
            counter += 1
            created = base_time + timedelta(hours=counter * 3)
            db.add(Innovation(
                teammate_id=teammate.id,
                title=innov["title"],
                summary=innov["summary"],
                domain=teammate.domain,
                category=innov.get("category", "general"),
                impact_level=innov.get("impact_level", 3),
                feasibility=innov.get("feasibility", 3),
                novelty=innov.get("novelty", 3),
                time_horizon=innov.get("time_horizon", "medium"),
                status=innov.get("status", "draft"),
                details=json.dumps(innov.get("details", {})),
                tags=",".join(innov.get("tags", [])),
                created_at=created,
                updated_at=created,
            ))
    db.commit()
    print(f"  Seeded {counter} innovations")


app = FastAPI(
    title="SPHERES Innovation Laboratory",
    description="Innovation laboratory for public space activation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "spheres-lab", "port": 8010}


app.include_router(router)


@app.get("/")
def root():
    return {
        "app": "SPHERES Innovation Laboratory",
        "version": "1.0.0",
        "port": 8010,
        "endpoints": "/api/teammates, /api/innovations, /api/stats, /api/collaborations, /api/sessions",
    }
