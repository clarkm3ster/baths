import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Architecture, ComparisonSet
from app.coordination_engine import recommend_models, generate_architecture

router = APIRouter(prefix="/api/architectures", tags=["architectures"])


@router.get("")
def list_architectures(db: Session = Depends(get_db)):
    archs = db.query(Architecture).order_by(Architecture.created_at.desc()).all()
    return [a._dict() for a in archs]


@router.get("/{arch_id}")
def get_architecture(arch_id: int, db: Session = Depends(get_db)):
    arch = db.query(Architecture).get(arch_id)
    if not arch:
        return {"error": "Architecture not found"}
    return arch._dict()


@router.post("/generate")
async def generate(request: Request, db: Session = Depends(get_db)):
    """Generate architecture from constraints.
    Body: {population_size, population_description, annual_budget, geography,
           political_context, time_horizon, domains, constraints}
    """
    body = await request.json()
    constraints = {
        "population_size": body.get("population_size", 1000),
        "population_description": body.get("population_description", ""),
        "annual_budget": body.get("annual_budget", 0),
        "geography": body.get("geography", ""),
        "political_context": body.get("political_context", "neutral"),
        "time_horizon": body.get("time_horizon", "3yr"),
        "domains": body.get("domains", []),
        "constraints": body.get("constraints", {}),
    }
    arch = generate_architecture(db, constraints)
    return arch


@router.post("/recommend")
async def recommend(request: Request, db: Session = Depends(get_db)):
    """Score all models against constraints without creating an architecture."""
    body = await request.json()
    scores = recommend_models(db, body)
    return {"recommendations": scores}


@router.put("/{arch_id}/status")
async def update_status(arch_id: int, request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    arch = db.query(Architecture).get(arch_id)
    if not arch:
        return {"error": "Architecture not found"}
    arch.status = body.get("status", arch.status)
    db.commit()
    db.refresh(arch)
    return arch._dict()


@router.delete("/{arch_id}")
def delete_architecture(arch_id: int, db: Session = Depends(get_db)):
    arch = db.query(Architecture).get(arch_id)
    if not arch:
        return {"error": "Architecture not found"}
    db.delete(arch)
    db.commit()
    return {"deleted": arch_id}


# --- Comparison endpoints ---

@router.post("/compare")
async def create_comparison(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    comp = ComparisonSet(
        name=body.get("name", "Comparison"),
        architecture_ids=json.dumps(body.get("architecture_ids", [])),
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)

    # Fetch the actual architectures for the comparison
    arch_ids = json.loads(comp.architecture_ids)
    archs = db.query(Architecture).filter(Architecture.id.in_(arch_ids)).all()
    result = comp._dict()
    result["architectures"] = [a._dict() for a in archs]
    return result


@router.get("/compare/{comp_id}")
def get_comparison(comp_id: int, db: Session = Depends(get_db)):
    comp = db.query(ComparisonSet).get(comp_id)
    if not comp:
        return {"error": "Comparison not found"}
    arch_ids = json.loads(comp.architecture_ids)
    archs = db.query(Architecture).filter(Architecture.id.in_(arch_ids)).all()
    result = comp._dict()
    result["architectures"] = [a._dict() for a in archs]
    return result


@router.get("/export/{arch_id}")
def export_architecture(arch_id: int, db: Session = Depends(get_db)):
    """Export architecture as structured JSON (for download/print)."""
    arch = db.query(Architecture).get(arch_id)
    if not arch:
        return {"error": "Architecture not found"}

    from app.models import CoordinationModel
    primary = db.query(CoordinationModel).get(arch.primary_model_id) if arch.primary_model_id else None
    hybrid_ids = json.loads(arch.hybrid_model_ids or "[]")
    hybrids = db.query(CoordinationModel).filter(CoordinationModel.id.in_(hybrid_ids)).all() if hybrid_ids else []

    data = arch._dict()
    data["primary_model"] = primary._dict() if primary else None
    data["hybrid_models"] = [h._dict() for h in hybrids]
    return data
