from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import DrugOut

router = APIRouter(tags=["drugs"])

# Arabic character normalization: collapse letter variants
# أ إ آ ى ة  →  ا ا ا ي ه
AR_FROM = "أإآىة"
AR_TO   = "ااايه"


def _normalize_ar(s: str) -> str:
    """Strip diacritics and collapse letter variants for fuzzy Arabic matching."""
    if not s:
        return ""
    # Remove diacritics
    for d in "ًٌٍَُِّْـ":
        s = s.replace(d, "")
    # Collapse variants
    for a, b in zip(AR_FROM, AR_TO):
        s = s.replace(a, b)
    return s.lower().strip()


@router.get("/search", response_model=list[DrugOut])
async def search_drugs(
    q: str = Query(..., min_length=2),
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """
    Search across generic names (AR/EN) and product brand names.
    Arabic is normalized on both sides so 'التروكسين' matches 'إلتروكسين'.
    """
    base = q.strip()
    q_norm = _normalize_ar(base)

    stmt = text("""
        SELECT DISTINCT d.*
        FROM drugs d
        LEFT JOIN products p ON p.drug_id = d.id
        WHERE
            LOWER(d.generic_en) LIKE LOWER(:q_like)
            OR LOWER(COALESCE(p.brand_en, '')) LIKE LOWER(:q_like)
            OR TRANSLATE(
                 LOWER(COALESCE(d.generic_ar, '')),
                 :ar_from, :ar_to
               ) LIKE :q_norm_like
            OR TRANSLATE(
                 LOWER(COALESCE(p.brand_ar, '')),
                 :ar_from, :ar_to
               ) LIKE :q_norm_like
        ORDER BY d.generic_en
        LIMIT :lim
    """)

    result = await db.execute(stmt, {
        "q_like":       f"%{base}%",
        "q_norm_like":  f"%{q_norm}%",
        "ar_from":      AR_FROM,
        "ar_to":        AR_TO,
        "lim":          limit,
    })

    # Convert rows to dicts, then let Pydantic validate them via DrugOut
    return [DrugOut(**dict(row._mapping)) for row in result.fetchall()]