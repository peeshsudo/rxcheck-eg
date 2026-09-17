from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Product
from app.schemas import ProductOut

router = APIRouter()


@router.get("/search", response_model=list[ProductOut])
async def search_products(
    q: str = Query(..., min_length=2),
    market: str = Query("EG"),
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """Search by brand name (AR or EN) within a market."""
    stmt = (
        select(Product)
        .where(Product.market == market)
        .where(or_(
            Product.brand_en.ilike(f"%{q}%"),
            Product.brand_ar.ilike(f"%{q}%"),
        ))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()