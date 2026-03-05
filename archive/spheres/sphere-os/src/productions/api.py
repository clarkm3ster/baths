"""FastAPI routes for Production Proposals."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.land.models import ParcelRecord
from src.productions.generator import generate_production_proposal, iterate_proposal
from src.productions.models import (
    GenerateRequest,
    IterateRequest,
    MaterialScriptResponse,
    ProductionProposal,
    ProposalResponse,
)
from src.shared.database import get_db

router = APIRouter()


@router.post("/generate", response_model=ProposalResponse)
async def generate(
    req: GenerateRequest,
    db: AsyncSession = Depends(get_db),
) -> ProposalResponse:
    """Generate a production proposal for a parcel using Claude API."""
    # Fetch parcel context
    result = await db.execute(select(ParcelRecord).where(ParcelRecord.id == req.parcel_id))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    proposal = await generate_production_proposal(
        parcel_id=parcel.id,
        area_sqft=parcel.area_sqft,
        census_block_group=parcel.census_block_group,
        zoning=parcel.zoning,
        street_frontage_ft=parcel.street_frontage_ft,
        creative_brief=req.creative_brief,
        tier_filter=req.tier_filter,
        format_constraint=req.format,
    )

    db.add(proposal)
    await db.flush()

    return ProposalResponse.model_validate(proposal)


@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ProposalResponse:
    """Get a production proposal by ID."""
    result = await db.execute(
        select(ProductionProposal).where(ProductionProposal.id == proposal_id)
    )
    proposal = result.scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return ProposalResponse.model_validate(proposal)


@router.get("/{proposal_id}/material-script", response_model=MaterialScriptResponse)
async def get_material_script(
    proposal_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MaterialScriptResponse:
    """Get just the material script timeline for a proposal."""
    result = await db.execute(
        select(ProductionProposal).where(ProductionProposal.id == proposal_id)
    )
    proposal = result.scalar_one_or_none()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    return MaterialScriptResponse(
        proposal_id=proposal.id,
        title=proposal.title,
        material_script=proposal.material_script,
    )


@router.post("/{proposal_id}/iterate", response_model=ProposalResponse)
async def iterate(
    proposal_id: uuid.UUID,
    req: IterateRequest,
    db: AsyncSession = Depends(get_db),
) -> ProposalResponse:
    """Regenerate a proposal with user feedback."""
    result = await db.execute(
        select(ProductionProposal).where(ProductionProposal.id == proposal_id)
    )
    original = result.scalar_one_or_none()
    if not original:
        raise HTTPException(status_code=404, detail="Proposal not found")

    new_proposal = await iterate_proposal(original, feedback=req.feedback)
    db.add(new_proposal)
    await db.flush()

    return ProposalResponse.model_validate(new_proposal)
