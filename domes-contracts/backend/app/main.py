from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.seed import seed_all
from app.routes.agreements import router as agreements_router
from app.routes.compliance import router as compliance_router
from app.routes.consent import router as consent_router

app = FastAPI(title="DOMES Contracts", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agreements_router)
app.include_router(compliance_router)
app.include_router(consent_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        result = seed_all(db)
        print(f"Seeded: {result}")
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "domes-contracts"}
