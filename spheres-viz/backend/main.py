"""
SPHERES Viz API
================
Backend service for the SPHERES visual experience.
Ten episodes. Ten dormant spaces. One city.

Run:
    uvicorn main:app --host 0.0.0.0 --port 8008 --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.episodes import router as episodes_router
from routes.marble import router as marble_router

app = FastAPI(
    title="SPHERES Viz API",
    version="1.0.0",
    description=(
        "API for the SPHERES visual experience — ten episodes documenting the "
        "activation of dormant spaces across Philadelphia."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(episodes_router)
app.include_router(marble_router)


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "spheres-viz"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8008)
