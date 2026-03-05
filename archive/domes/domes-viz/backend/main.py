import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from narrative import router as narrative_router
from marble_routes import router as marble_router
from marble import ensure_worlds_ready

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("domes-viz")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: ensure Marble worlds are cached and ready."""
    logger.info("Starting up — checking Marble world cache...")
    try:
        worlds = await ensure_worlds_ready()
        logger.info("Marble worlds ready: %d worlds available", len(worlds))
    except Exception as exc:
        logger.error("Marble startup seeding failed (will use fallbacks): %s", exc)
    yield


app = FastAPI(
    title="DOMES Viz API",
    description="Narrative visualization engine with World Labs Marble integration",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(narrative_router, prefix="/api")
app.include_router(marble_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
