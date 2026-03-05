"""
DOMES Legal -- Structured Legal Ingestion Engine

Takes discoveries from domes-legal-research and structures them into
a searchable, queryable, machine-readable legal database.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .seed import seed

app = FastAPI(title="DOMES Legal Engine", description="Legal provisions database and search", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "domes-legal", "port": 8003}


@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    seed()


# Routes are imported and included by each team member
# Legal-parser: /api/ingest, /api/provisions/updates
# Taxonomy-builder: /api/taxonomy, /api/search
# Graph-builder: /api/graph
# Architect: /api/provisions (CRUD)

from .routes import provisions, ingest, taxonomy, graph
from .studio.api import router as studio_router
from .studio.layers_api import router as layers_router

app.include_router(provisions.router)
app.include_router(ingest.router)
app.include_router(taxonomy.router)
app.include_router(graph.router)
app.include_router(studio_router, prefix="/api/studio")
app.include_router(layers_router, prefix="/api/layers")
