from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, SessionLocal
from app.models import Parcel
from app.ingest import ingest_parcels
from app.seed import seed_parcels
from app.routes import parcels, stats, value

app = FastAPI(title="Spheres Assets API", description="Philadelphia parcel and asset management", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parcels.router)
app.include_router(stats.router)
app.include_router(value.router)


@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        count = db.query(Parcel).count()
        if count == 0:
            print("No parcels found. Attempting live ingest from OpenDataPhilly...")
            try:
                ingested = ingest_parcels(db)
                if ingested > 0:
                    print(f"Done. Ingested {ingested} parcels from Carto API.")
                else:
                    raise RuntimeError("Carto returned 0 rows")
            except Exception as exc:
                print(f"Live ingest failed ({exc}). Loading offline seed data...")
                seeded = seed_parcels(db)
                print(f"Loaded {seeded} offline seed parcels.")
        else:
            print(f"Database has {count} parcels. Skipping ingestion.")
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}
