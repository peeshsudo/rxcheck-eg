from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Drug
from app.schemas import DrugOut

router = APIRouter()


@router.get("/search", response_model=list[DrugOut])
async def search_drugs(
    q: str = Query(..., min_length=2),
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Fuzzy search across English and Arabic generic names."""
    stmt = (
        select(Drug)
        .where(or_(
            Drug.generic_en.ilike(f"%{q}%"),
            Drug.generic_ar.ilike(f"%{q}%"),
        ))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()