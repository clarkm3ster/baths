from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from narrative import router as narrative_router

app = FastAPI(title="DOMES Viz API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(narrative_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
