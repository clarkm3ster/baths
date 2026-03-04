"""SPHERE/OS — FastAPI application root."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SPHERE/OS",
    description="Programmable material environments on vacant public land",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "sphere-os"}


# Register routers — imported lazily to avoid circular deps
def register_routers() -> None:
    from src.land.api import router as land_router
    from src.productions.api import router as productions_router
    from src.scheduling.api import router as scheduling_router
    from src.materials.api import router as materials_router
    from src.safety.api import router as safety_router

    app.include_router(land_router, prefix="/api/land", tags=["land"])
    app.include_router(productions_router, prefix="/api/productions", tags=["productions"])
    app.include_router(scheduling_router, prefix="/api", tags=["scheduling"])
    app.include_router(materials_router, prefix="/api", tags=["materials"])
    app.include_router(safety_router, prefix="/api/safety", tags=["safety"])


register_routers()
