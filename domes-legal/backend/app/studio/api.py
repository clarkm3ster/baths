"""Dome Studio API — character-driven production pipeline endpoints."""
import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.studio.models import (
    StudioCharacter, StudioProduction, StudioProductionStage,
    StudioTalentRole, StudioGap, StudioIPAsset, StudioLearningPackage,
)
from app.studio.schemas import (
    CharacterCreate, ProductionCreate, GapItemCreate, GapTriage,
    IPAssetCreate, LearningPackageCreate,
)
from app.studio.budgeting import full_financial_summary

router = APIRouter(tags=["studio"])


# ── Characters ─────────────────────────────────────────────────────

@router.post("/characters")
def create_character(body: CharacterCreate, db: Session = Depends(get_db)):
    character_id = str(uuid.uuid4())
    row = StudioCharacter(
        character_id=character_id,
        character_type=body.character_type,
        name_or_alias=body.name_or_alias,
        consent_tier=body.consent_tier,
        fictionalization_rules=json.dumps(body.fictionalization_rules),
        circumstances_summary=body.circumstances_summary,
        initial_conditions=json.dumps(body.initial_conditions),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row.to_dict()


@router.get("/characters")
def list_characters(
    character_type: str | None = None,
    consent_tier: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(StudioCharacter)
    if character_type:
        q = q.filter(StudioCharacter.character_type == character_type)
    if consent_tier:
        q = q.filter(StudioCharacter.consent_tier == consent_tier)
    return [c.to_dict() for c in q.order_by(StudioCharacter.created_at.desc()).all()]


@router.get("/characters/{character_id}")
def get_character(character_id: str, db: Session = Depends(get_db)):
    row = db.query(StudioCharacter).filter(
        StudioCharacter.character_id == character_id
    ).first()
    if not row:
        raise HTTPException(404, "Character not found")
    return row.to_dict()


# ── Productions ────────────────────────────────────────────────────

@router.post("/productions")
def create_production(body: ProductionCreate, db: Session = Depends(get_db)):
    # Validate character exists
    char = db.query(StudioCharacter).filter(
        StudioCharacter.character_id == body.character_id
    ).first()
    if not char:
        raise HTTPException(404, "Character not found")

    production_id = str(uuid.uuid4())
    prod = StudioProduction(
        production_id=production_id,
        title=body.title,
        medium=body.medium,
        character_id=body.character_id,
        stage=body.stage,
        budget_total=body.budget_total,
        financing_sources=json.dumps(body.financing_sources),
    )
    db.add(prod)
    db.flush()

    for s in body.stages:
        db.add(StudioProductionStage(
            production_id=production_id,
            stage=s.stage,
            start_date=s.start_date,
            end_date=s.end_date,
            cost_cap=s.cost_cap,
            deliverables=json.dumps(s.deliverables),
            risk_register=json.dumps(s.risk_register),
        ))

    for t in body.team:
        db.add(StudioTalentRole(
            production_id=production_id,
            person_or_entity=t.person_or_entity,
            role=t.role,
            rate_type=t.rate_type,
            rate=t.rate,
        ))

    db.commit()
    return _production_detail(production_id, db)


@router.get("/productions")
def list_productions(
    medium: str | None = None,
    stage: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(StudioProduction)
    if medium:
        q = q.filter(StudioProduction.medium == medium)
    if stage:
        q = q.filter(StudioProduction.stage == stage)
    return [p.to_dict() for p in q.order_by(StudioProduction.generated_at.desc()).all()]


@router.get("/productions/{production_id}")
def get_production(production_id: str, db: Session = Depends(get_db)):
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")
    return _production_detail(production_id, db)


@router.put("/productions/{production_id}/advance")
def advance_production(production_id: str, db: Session = Depends(get_db)):
    """Advance a production to the next stage."""
    STAGE_ORDER = ["greenlit", "in_progress", "paused", "shipped"]
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")

    idx = STAGE_ORDER.index(prod.stage) if prod.stage in STAGE_ORDER else 0
    if idx >= len(STAGE_ORDER) - 1:
        raise HTTPException(400, "Production already at final stage")

    old = prod.stage
    prod.stage = STAGE_ORDER[idx + 1]
    prod.updated_at = datetime.utcnow()
    db.commit()
    return {"production_id": production_id, "previous": old, "current": prod.stage}


# ── Gaps ───────────────────────────────────────────────────────────

@router.post("/productions/{production_id}/gaps")
def create_gap(
    production_id: str,
    body: GapItemCreate,
    db: Session = Depends(get_db),
):
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")

    gap_id = str(uuid.uuid4())
    row = StudioGap(
        gap_id=gap_id,
        production_id=production_id,
        character_id=body.character_id,
        area=body.area,
        severity=body.severity,
        description=body.description,
        reproduction_steps=json.dumps(body.reproduction_steps),
        proposed_fix=body.proposed_fix,
        owner_module=body.owner_module,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row.to_dict()


@router.get("/productions/{production_id}/gaps")
def list_gaps(
    production_id: str,
    severity: str | None = None,
    area: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(StudioGap).filter(StudioGap.production_id == production_id)
    if severity:
        q = q.filter(StudioGap.severity == severity)
    if area:
        q = q.filter(StudioGap.area == area)
    if status:
        q = q.filter(StudioGap.status == status)
    return [g.to_dict() for g in q.order_by(StudioGap.discovered_at.desc()).all()]


@router.get("/productions/{production_id}/backlog")
def get_backlog(production_id: str, db: Session = Depends(get_db)):
    """Return gaps grouped by severity, area, and owner_module."""
    gaps = db.query(StudioGap).filter(StudioGap.production_id == production_id).all()

    by_severity: dict[str, list] = {}
    by_area: dict[str, list] = {}
    by_owner: dict[str, list] = {}

    for g in gaps:
        d = g.to_dict()
        by_severity.setdefault(g.severity, []).append(d)
        by_area.setdefault(g.area, []).append(d)
        owner = g.owner_module or "unassigned"
        by_owner.setdefault(owner, []).append(d)

    return {
        "production_id": production_id,
        "total": len(gaps),
        "by_severity": {k: {"count": len(v), "items": v} for k, v in by_severity.items()},
        "by_area": {k: {"count": len(v), "items": v} for k, v in by_area.items()},
        "by_owner_module": {k: {"count": len(v), "items": v} for k, v in by_owner.items()},
    }


@router.put("/gaps/{gap_id}/triage")
def triage_gap(gap_id: str, body: GapTriage, db: Session = Depends(get_db)):
    gap = db.query(StudioGap).filter(StudioGap.gap_id == gap_id).first()
    if not gap:
        raise HTTPException(404, "Gap not found")
    if body.status is not None:
        gap.status = body.status
    if body.proposed_fix is not None:
        gap.proposed_fix = body.proposed_fix
    if body.owner_module is not None:
        gap.owner_module = body.owner_module
    db.commit()
    db.refresh(gap)
    return gap.to_dict()


# ── IP Assets ──────────────────────────────────────────────────────

@router.post("/productions/{production_id}/assets")
def create_asset(
    production_id: str,
    body: IPAssetCreate,
    db: Session = Depends(get_db),
):
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")

    asset_id = str(uuid.uuid4())
    row = StudioIPAsset(
        asset_id=asset_id,
        production_id=production_id,
        asset_type=body.asset_type,
        title=body.title,
        storage_uri=body.storage_uri,
        contributors=json.dumps(body.contributors),
        rights=json.dumps(body.rights),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row.to_dict()


@router.get("/productions/{production_id}/assets")
def list_assets(production_id: str, db: Session = Depends(get_db)):
    rows = db.query(StudioIPAsset).filter(
        StudioIPAsset.production_id == production_id
    ).order_by(StudioIPAsset.created_at.desc()).all()
    return [a.to_dict() for a in rows]


# ── Learning Packages ──────────────────────────────────────────────

@router.post("/productions/{production_id}/learning-package")
def create_learning_package(
    production_id: str,
    body: LearningPackageCreate,
    db: Session = Depends(get_db),
):
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")

    learning_id = str(uuid.uuid4())
    row = StudioLearningPackage(
        learning_id=learning_id,
        production_id=production_id,
        summary=body.summary,
        gap_ids=json.dumps(body.gap_ids),
        proposed_os_changes=json.dumps(body.proposed_os_changes),
        validation_needed=json.dumps(body.validation_needed),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row.to_dict()


@router.get("/productions/{production_id}/learning-packages")
def list_learning_packages(production_id: str, db: Session = Depends(get_db)):
    rows = db.query(StudioLearningPackage).filter(
        StudioLearningPackage.production_id == production_id
    ).order_by(StudioLearningPackage.generated_at.desc()).all()
    return [lp.to_dict() for lp in rows]


# ── Financials ─────────────────────────────────────────────────────

@router.get("/productions/{production_id}/financials")
def get_financials(production_id: str, db: Session = Depends(get_db)):
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        raise HTTPException(404, "Production not found")

    stages = db.query(StudioProductionStage).filter(
        StudioProductionStage.production_id == production_id
    ).all()
    gap_count = db.query(StudioGap).filter(
        StudioGap.production_id == production_id
    ).count()
    learning_count = db.query(StudioLearningPackage).filter(
        StudioLearningPackage.production_id == production_id
    ).count()

    prod_dict = prod.to_dict()
    prod_dict["stages"] = [s.to_dict() for s in stages]

    summary = full_financial_summary(prod_dict, gap_count, learning_count)
    return summary.model_dump()


# ── Dashboard ──────────────────────────────────────────────────────

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    """Aggregate stats across all studio data."""
    total_chars = db.query(StudioCharacter).count()
    total_prods = db.query(StudioProduction).count()

    stage_rows = (
        db.query(StudioProduction.stage, func.count(StudioProduction.id))
        .group_by(StudioProduction.stage).all()
    )

    total_gaps = db.query(StudioGap).count()
    sev_rows = (
        db.query(StudioGap.severity, func.count(StudioGap.id))
        .group_by(StudioGap.severity).all()
    )

    total_assets = db.query(StudioIPAsset).count()
    total_learnings = db.query(StudioLearningPackage).count()

    return {
        "total_characters": total_chars,
        "total_productions": total_prods,
        "productions_by_stage": {s: c for s, c in stage_rows},
        "total_gaps": total_gaps,
        "gaps_by_severity": {s: c for s, c in sev_rows},
        "total_assets": total_assets,
        "total_learning_packages": total_learnings,
    }


# ── Helpers ────────────────────────────────────────────────────────

@router.post("/seed-scenarios")
def seed_studio_from_scenarios(db: Session = Depends(get_db)):
    """Populate Studio DB with the 5 canonical person scenarios.

    Creates characters and a production based on seed_scenarios data.
    Idempotent — skips if characters already exist.
    """
    existing = db.query(StudioCharacter).filter(
        StudioCharacter.character_id.like("seed-%")
    ).count()
    if existing > 0:
        return {"status": "already_seeded", "characters": existing}

    from app.studio.seed_scenarios import PROFILES, build_scenario

    characters_created = []
    for name, profile in PROFILES.items():
        scenario = build_scenario(name)
        char_id = f"seed-{profile['person_id']}"

        char = StudioCharacter(
            character_id=char_id,
            character_type="real_person",
            name_or_alias=profile["name"],
            consent_tier="tier2_standard",
            fictionalization_rules=json.dumps({
                "name_changed": True,
                "location_generalized": True,
                "dates_shifted": True,
            }),
            circumstances_summary=(
                f"Age {profile['age']}, {profile['sex']}, "
                f"conditions: {', '.join(profile['conditions'])}. "
                f"Systems: {', '.join(profile['systems_involved'][:5])}. "
                f"Fragmented cost: ${profile['annual_cost_fragmented']:,.0f}/yr, "
                f"coordinated: ${profile['annual_cost_coordinated']:,.0f}/yr."
            ),
            initial_conditions=json.dumps({
                "age": profile["age"],
                "sex": profile["sex"],
                "earned_income": profile["earned_income"],
                "benefits": profile["benefits"],
                "conditions": profile["conditions"],
                "location": profile["location"],
            }),
        )
        db.add(char)
        characters_created.append(char_id)

    # Create a production using the first character as anchor
    prod_id = "seed-philly-prevention-2026"
    prod = StudioProduction(
        production_id=prod_id,
        title="Philadelphia Prevention Bond: Five Lives",
        medium="series",
        character_id=characters_created[0],
        stage="greenlit",
        budget_total=250000.0,
        financing_sources=json.dumps({
            "characters": characters_created,
            "bond_notional": "$137,972",
            "total_savings_potential": "$218,750",
            "episode_count": 5,
            "format": "One episode per person, intercut with bond pricing scenes",
        }),
    )
    db.add(prod)

    # Create 5 stage gates
    for gate_name in ["greenlight", "pre_production", "production", "post", "distribution"]:
        stage = StudioProductionStage(
            production_id=prod_id,
            stage=gate_name,
            cost_cap=50000.0,
            deliverables=json.dumps([f"{gate_name} deliverables"]),
        )
        db.add(stage)

    db.commit()
    return {
        "status": "seeded",
        "characters": len(characters_created),
        "character_ids": characters_created,
        "production_id": prod_id,
    }


def _production_detail(production_id: str, db: Session) -> dict:
    prod = db.query(StudioProduction).filter(
        StudioProduction.production_id == production_id
    ).first()
    if not prod:
        return {"error": "not found"}

    stages = db.query(StudioProductionStage).filter(
        StudioProductionStage.production_id == production_id
    ).all()
    team = db.query(StudioTalentRole).filter(
        StudioTalentRole.production_id == production_id
    ).all()
    gap_count = db.query(StudioGap).filter(
        StudioGap.production_id == production_id
    ).count()
    asset_count = db.query(StudioIPAsset).filter(
        StudioIPAsset.production_id == production_id
    ).count()

    result = prod.to_dict()
    result["stages"] = [s.to_dict() for s in stages]
    result["team"] = [t.to_dict() for t in team]
    result["stats"] = {"gaps": gap_count, "assets": asset_count}
    return result
