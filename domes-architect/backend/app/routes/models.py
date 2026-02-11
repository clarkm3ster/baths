from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CoordinationModel

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("")
def list_models(db: Session = Depends(get_db)):
    models = db.query(CoordinationModel).all()
    return [m._dict() for m in models]


@router.get("/{model_id}")
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(CoordinationModel).get(model_id)
    if not model:
        return {"error": "Model not found"}
    return model._dict()


@router.get("/category/{category}")
def models_by_category(category: str, db: Session = Depends(get_db)):
    models = db.query(CoordinationModel).filter(CoordinationModel.category == category).all()
    return [m._dict() for m in models]


@router.get("/compare/{ids}")
def compare_models(ids: str, db: Session = Depends(get_db)):
    """Compare multiple models side by side. ids = comma-separated model IDs."""
    id_list = [int(x.strip()) for x in ids.split(",") if x.strip()]
    models = db.query(CoordinationModel).filter(CoordinationModel.id.in_(id_list)).all()
    return {
        "models": [m._dict() for m in models],
        "comparison_dimensions": [
            "domains_covered", "authority_type", "funding_sources", "timeline_to_launch",
            "political_feasibility", "evidence_rating", "typical_budget_range",
            "key_features", "limitations",
        ],
    }
