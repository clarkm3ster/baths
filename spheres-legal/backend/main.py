"""
SPHERES Legal — FastAPI backend
Every legal pathway to activating public space.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from permits import (
    get_all_permits,
    get_permit_by_id,
    get_permit_pathway,
    serialize_pathway,
    search_permits,
)
from contracts import (
    get_all_templates,
    get_template,
    get_templates_by_category,
    get_permanence_requirements,
    generate_agreement,
)
from policy import (
    MODEL_LEGISLATION,
    COMPARATIVE_ANALYSIS,
    EQUITY_FRAMEWORK,
    get_city_comparison,
    calculate_equity_score,
)

app = FastAPI(
    title="SPHERES Legal",
    description="Every legal pathway to activating public space",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class PathwayRequest(BaseModel):
    parcel_type: str
    zoning: str = ""
    activation_type: str


class ContractGenerateRequest(BaseModel):
    template_id: str
    variables: dict = {}


class EquityScoreRequest(BaseModel):
    dormant_space_density: float = 0
    median_income: float = 52649
    activation_history: float = 0.5
    community_organization_density: float = 0.5
    health_outcome_gaps: float = 0.5


# ---------------------------------------------------------------------------
# Permit endpoints
# ---------------------------------------------------------------------------

@app.get("/api/permits")
def list_permits():
    """Return all permit types."""
    return {"permits": get_all_permits()}


@app.get("/api/permits/{permit_id}")
def get_permit(permit_id: str):
    """Return a single permit type by ID."""
    p = get_permit_by_id(permit_id)
    if not p:
        raise HTTPException(404, f"Permit '{permit_id}' not found")
    return p


@app.post("/api/permits/pathway")
def find_pathway(req: PathwayRequest):
    """Find the permit pathway for a given parcel + activation type."""
    try:
        raw = get_permit_pathway(req.parcel_type, req.zoning, req.activation_type)
        return serialize_pathway(raw)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/api/permits/search")
def permit_search(
    property_type: Optional[str] = None,
    zoning: Optional[str] = None,
    keyword: Optional[str] = None,
):
    """Search permits by property type, zoning, or keyword."""
    return {"permits": search_permits(property_type, zoning, keyword)}


# ---------------------------------------------------------------------------
# Contract endpoints
# ---------------------------------------------------------------------------

@app.get("/api/contracts/templates")
def list_templates(category: Optional[str] = None):
    """Return all agreement templates, optionally filtered by category."""
    if category:
        return {"templates": get_templates_by_category(category)}
    return {"templates": get_all_templates()}


@app.get("/api/contracts/templates/{template_id}")
def get_contract_template(template_id: str):
    """Return a single template by ID."""
    t = get_template(template_id)
    if not t:
        raise HTTPException(404, f"Template '{template_id}' not found")
    return t


@app.post("/api/contracts/generate")
def gen_contract(req: ContractGenerateRequest):
    """Generate an agreement from a template and variables."""
    try:
        return generate_agreement(req.template_id, req.variables)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/api/contracts/permanence")
def permanence_reqs():
    """Return the permanence requirements framework."""
    return {"permanence": get_permanence_requirements()}


# ---------------------------------------------------------------------------
# Policy endpoints
# ---------------------------------------------------------------------------

@app.get("/api/policy/models")
def list_models():
    """Return all model legislation."""
    return {"models": MODEL_LEGISLATION}


@app.get("/api/policy/models/{model_id}")
def get_model(model_id: str):
    """Return a single legislative model by ID."""
    for m in MODEL_LEGISLATION:
        if m["id"] == model_id:
            return m
    raise HTTPException(404, f"Model '{model_id}' not found")


@app.get("/api/policy/comparative")
def comparative():
    """Return comparative analysis of all cities."""
    return {"cities": COMPARATIVE_ANALYSIS}


@app.get("/api/policy/comparative/{city_name}")
def city_detail(city_name: str):
    """Return comparative data for a single city."""
    for c in COMPARATIVE_ANALYSIS:
        if c["name"].lower() == city_name.lower():
            return c
    raise HTTPException(404, f"City '{city_name}' not found")


@app.get("/api/policy/compare")
def compare_cities(city1: str, city2: str):
    """Compare two cities side by side."""
    result = get_city_comparison(city1, city2)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@app.get("/api/policy/equity")
def equity_framework():
    """Return the full equity framework."""
    return {"framework": EQUITY_FRAMEWORK}


@app.post("/api/policy/equity/score")
def equity_score(req: EquityScoreRequest):
    """Calculate equity priority score for a neighborhood."""
    return calculate_equity_score({
        "dormant_space_density": req.dormant_space_density,
        "median_income": req.median_income,
        "activation_history": req.activation_history,
        "community_organization_density": req.community_organization_density,
        "health_outcome_gaps": req.health_outcome_gaps,
    })


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "spheres-legal"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
