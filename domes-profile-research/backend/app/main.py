from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .seed import seed
from .routes import cases, profiles, costs, systems

app = FastAPI(title="DOMES Profile Research", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cases.router)
app.include_router(profiles.router)
app.include_router(costs.router)
app.include_router(systems.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)
    seed()


@app.get("/api/health")
def health():
    return {"status": "ok"}
