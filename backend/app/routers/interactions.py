"""
Interaction endpoints.

Endpoints:
    GET  /api/v1/interactions/check?drug_a=UUID&drug_b=UUID
    POST /api/v1/interactions/check-batch   (JSON list of UUIDs, max 20)
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Interaction
from app.schemas import InteractionOut

router = APIRouter()

MAX_BATCH_SIZE = 20


@router.get("/check", response_model=list[InteractionOut])
async def check_interaction(
    drug_a: UUID = Query(...),
    drug_b: UUID = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Check a single pair. Order-independent."""
    if drug_a == drug_b:
        return []
    a, b = sorted([drug_a, drug_b], key=str)
    stmt = select(Interaction).where(
        and_(
            Interaction.drug_a_id == a,
            Interaction.drug_b_id == b,
            Interaction.is_current.is_(True),
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/check-batch", response_model=list[InteractionOut])
async def check_batch(
    drug_ids: list[UUID],
    db: AsyncSession = Depends(get_db),
):
    """Check all unique pairs among a list of drugs (capped at 20)."""
    unique_ids = sorted(set(drug_ids), key=str)
    if len(unique_ids) < 2:
        return []
    if len(unique_ids) > MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=422,
            detail=f"Too many drugs. Maximum is {MAX_BATCH_SIZE}, received {len(unique_ids)}.",
        )
    pairs = [
        (unique_ids[i], unique_ids[j])
        for i in range(len(unique_ids))
        for j in range(i + 1, len(unique_ids))
    ]
    conditions = [
        and_(Interaction.drug_a_id == a, Interaction.drug_b_id == b)
        for a, b in pairs
    ]
    stmt = (
        select(Interaction)
        .where(and_(Interaction.is_current.is_(True), or_(*conditions)))
        .order_by(Interaction.severity)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
