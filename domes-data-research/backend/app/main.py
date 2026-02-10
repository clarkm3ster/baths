from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, SessionLocal
from app.seed import seed_all
from app.routes import systems, gaps

app = FastAPI(title="DOMES Data Constellation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(systems.router)
app.include_router(gaps.router)


@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        result = seed_all(db)
        if result["systems"] > 0:
            print(f"Seeded {result['systems']} systems, {result['connections']} connections, {result['gaps']} gaps.")
        else:
            print("Database already seeded.")
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/constellation")
def get_constellation(profile: dict):
    """Return the full constellation for a person: systems, connections, gaps."""
    from app.database import SessionLocal
    from app.models import System, Connection, Gap
    import json

    db = SessionLocal()
    try:
        # Find matching systems
        all_systems = db.query(System).all()
        profile_values: set[str] = set()
        for key in ("insurance", "disabilities", "housing", "income", "system_involvement"):
            profile_values.update(profile.get(key, []))
        if profile.get("age_group"):
            profile_values.add(profile["age_group"])
        for bf in ("pregnant", "veteran", "dv_survivor", "immigrant", "lgbtq", "rural"):
            if profile.get(bf):
                profile_values.add(bf)

        matched_ids = set()
        matched_systems = []
        for s in all_systems:
            applies = json.loads(s.applies_when)
            if not applies or profile_values & set(applies):
                matched_ids.add(s.id)
                matched_systems.append({
                    "id": s.id, "name": s.name, "acronym": s.acronym,
                    "agency": s.agency, "domain": s.domain,
                    "description": s.description,
                    "data_standard": s.data_standard,
                    "data_held": json.loads(s.data_held),
                    "privacy_law": s.privacy_law,
                    "privacy_laws": json.loads(s.privacy_laws),
                })

        # Find connections between matched systems
        all_conns = db.query(Connection).all()
        matched_conns = []
        for c in all_conns:
            if c.source_id in matched_ids and c.target_id in matched_ids:
                matched_conns.append({
                    "id": c.id, "source_id": c.source_id, "target_id": c.target_id,
                    "direction": c.direction, "frequency": c.frequency,
                    "format": c.format, "data_shared": json.loads(c.data_shared),
                    "description": c.description, "reliability": c.reliability,
                })

        # Find gaps between matched systems
        all_gaps = db.query(Gap).all()
        matched_gaps = []
        for g in all_gaps:
            gap_applies = json.loads(g.applies_when)
            if (g.system_a_id in matched_ids and g.system_b_id in matched_ids and
                    (not gap_applies or profile_values & set(gap_applies))):
                matched_gaps.append({
                    "id": g.id, "system_a_id": g.system_a_id, "system_b_id": g.system_b_id,
                    "barrier_type": g.barrier_type, "barrier_law": g.barrier_law,
                    "barrier_description": g.barrier_description,
                    "impact": g.impact, "what_it_would_take": g.what_it_would_take,
                    "consent_closable": g.consent_closable,
                    "consent_mechanism": g.consent_mechanism,
                    "severity": g.severity,
                })

        connected_pairs = {(c["source_id"], c["target_id"]) for c in matched_conns}
        connected_pairs |= {(c["target_id"], c["source_id"]) for c in matched_conns}
        connected_count = len({frozenset((c["source_id"], c["target_id"])) for c in matched_conns})
        siloed_ids = matched_ids - {sid for pair in connected_pairs for sid in pair}

        return {
            "systems": matched_systems,
            "connections": matched_conns,
            "gaps": matched_gaps,
            "summary": {
                "total_systems": len(matched_systems),
                "connected": connected_count,
                "siloed": len(siloed_ids),
                "gaps": len(matched_gaps),
                "consent_closable": sum(1 for g in matched_gaps if g["consent_closable"]),
            },
        }
    finally:
        db.close()
