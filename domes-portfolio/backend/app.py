"""
domes.cc — Portfolio backend
Serves completed DOMES productions from talent-agent production files.
"""

import os
import json
import glob
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="domes.cc")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Production data path — reads from talent-agent's output
PRODUCTION_DIR = os.environ.get(
    "PRODUCTION_DIR",
    os.path.join(os.path.dirname(__file__), "../../talent-agent/backend/production_files")
)


def _load_productions():
    """Scan production_files for completed DOMES productions."""
    productions = []
    if not os.path.exists(PRODUCTION_DIR):
        return productions

    for project_dir in sorted(os.listdir(PRODUCTION_DIR)):
        full_path = os.path.join(PRODUCTION_DIR, project_dir)
        if not os.path.isdir(full_path):
            continue

        # Find Data.json files
        for data_file in glob.glob(os.path.join(full_path, "*_Data.json")):
            try:
                with open(data_file) as f:
                    data = json.load(f)
                project = data.get("project", {})
                if project.get("game_type") != "domes":
                    continue
                if project.get("status") not in ("completed", "published"):
                    continue
                productions.append(data)
            except (json.JSONDecodeError, IOError):
                continue

    return productions


@app.get("/api/productions")
def list_productions(sort: str = "score"):
    """List all completed DOMES productions."""
    prods = _load_productions()

    # Build summaries
    items = []
    for p in prods:
        project = p.get("project", {})
        char = project.get("character", {})
        scores = p.get("final_scores", {})

        items.append({
            "project_id": project.get("project_id"),
            "title": project.get("title"),
            "character_name": char.get("name"),
            "source": char.get("source"),
            "source_citation": char.get("source_citation"),
            "principal_name": p.get("principal", {}).get("name"),
            "team_size": len(p.get("team", {}).get("members", [])),
            "cosm_total": scores.get("total", 0),
            "dimensions": scores.get("dimensions", {}),
            "weakest": scores.get("weakest"),
            "strongest": scores.get("strongest"),
            "ip_count": len(p.get("ip_log", [])),
            "sources_count": len(p.get("sources_cited", [])),
            "production_number": project.get("production_number", 1),
            "stage_count": len(p.get("stages", [])),
        })

    if sort == "score":
        items.sort(key=lambda x: x["cosm_total"], reverse=True)
    elif sort == "title":
        items.sort(key=lambda x: x["title"])
    elif sort == "ip":
        items.sort(key=lambda x: x["ip_count"], reverse=True)

    return {"productions": items, "count": len(items)}


@app.get("/api/productions/{project_id}")
def get_production(project_id: str):
    """Get a complete DOMES production."""
    prods = _load_productions()
    for p in prods:
        if p.get("project", {}).get("project_id") == project_id:
            return p
    raise HTTPException(status_code=404, detail="Production not found")


@app.get("/api/productions/{project_id}/files")
def list_production_files(project_id: str):
    """List downloadable files for a production."""
    project_dir = os.path.join(PRODUCTION_DIR, project_id)
    if not os.path.isdir(project_dir):
        raise HTTPException(status_code=404, detail="Production not found")

    files = []
    for fname in sorted(os.listdir(project_dir)):
        if fname.endswith("_Data.json"):
            continue  # Skip the big data file from downloads list
        fpath = os.path.join(project_dir, fname)
        files.append({
            "filename": fname,
            "size": os.path.getsize(fpath),
            "url": f"/api/productions/{project_id}/files/{fname}",
        })
    return {"files": files}


@app.get("/api/productions/{project_id}/files/{filename}")
def download_file(project_id: str, filename: str):
    """Download a production file."""
    filepath = os.path.join(PRODUCTION_DIR, project_id, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    media = "application/json" if filename.endswith(".json") else "text/markdown"
    return FileResponse(filepath, media_type=media, filename=filename)


# Serve frontend
if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404)
        return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9010)
