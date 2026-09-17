from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Interaction, Drug
from app.schemas import InteractionOut

router = APIRouter()


@router.get("/check", response_model=list[InteractionOut])
async def check_interaction(
    drug_a: UUID,
    drug_b: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Check a single pair. Order-independent."""
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
    """Check all pairs among a list of drugs."""
    if len(drug_ids) < 2:
        return []
    sorted_ids = sorted(drug_ids, key=str)
    pairs = []
    for i in range(len(sorted_ids)):
        for j in range(i + 1, len(sorted_ids)):
            pairs.append((sorted_ids[i], sorted_ids[j]))

    conditions = [
        and_(Interaction.drug_a_id == a, Interaction.drug_b_id == b)
        for a, b in pairs
    ]
    stmt = select(Interaction).where(
        and_(Interaction.is_current.is_(True), or_(*conditions))
    )
    result = await db.execute(stmt)
    return result.scalars().all()