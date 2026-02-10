from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, SessionLocal
from app.models import Parcel
from app.ingest import ingest_parcels
from app.routes import parcels, stats, value

app = FastAPI(title="Spheres Assets API", version="1.0.0")

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
            print("No parcels found. Ingesting from OpenDataPhilly...")
            ingested = ingest_parcels(db)
            print(f"Done. Ingested {ingested} parcels.")
        else:
            print(f"Database has {count} parcels. Skipping ingestion.")
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}
