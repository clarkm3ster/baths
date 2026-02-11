from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.seed import seed_all
from app.routes.models import router as models_router
from app.routes.architectures import router as architectures_router

app = FastAPI(title="DOMES Architect", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(models_router)
app.include_router(architectures_router)


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
    return {"status": "ok", "service": "domes-architect"}
