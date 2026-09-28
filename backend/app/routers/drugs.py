from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import DrugOut

router = APIRouter(tags=["drugs"])

# Arabic character normalization: collapse letter variants
AR_FROM = "أإآىة"
AR_TO   = "ااايه"


def _normalize_ar(s: str) -> str:
    """Strip diacritics and collapse letter variants for fuzzy Arabic matching."""
    if not s:
        return ""
    for d in "ًٌٍَُِّْـ":
        s = s.replace(d, "")
    for a, b in zip(AR_FROM, AR_TO):  # noqa: B905
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

    Strategy:
      1. LIKE match (exact substring)
      2. Arabic-normalized LIKE match (handles أ/إ/ا variance)
      3. Trigram similarity > 0.4 (handles OCR typos like نيفيوروكسازيد vs نيفوروكسازيد)
    """
    base = q.strip()
    q_norm = _normalize_ar(base)

    stmt = text("""
        WITH scored AS (
            SELECT d.*,
                GREATEST(
                    similarity(LOWER(COALESCE(d.generic_en, '')), LOWER(:q)),
                    similarity(LOWER(COALESCE(d.generic_ar, '')), :q),
                    similarity(LOWER(COALESCE(p.brand_en, '')), LOWER(:q)),
                    similarity(LOWER(COALESCE(p.brand_ar, '')), :q),
                    similarity(
                        TRANSLATE(LOWER(COALESCE(d.generic_ar, '')), :ar_from, :ar_to),
                        :q_norm
                    )
                ) AS score
            FROM drugs d
            LEFT JOIN products p ON p.drug_id = d.id
            WHERE
                LOWER(d.generic_en) LIKE LOWER(:q_like)
                OR LOWER(COALESCE(p.brand_en, '')) LIKE LOWER(:q_like)
                OR TRANSLATE(LOWER(COALESCE(d.generic_ar, '')), :ar_from, :ar_to) LIKE :q_norm_like
                OR TRANSLATE(LOWER(COALESCE(p.brand_ar, '')), :ar_from, :ar_to) LIKE :q_norm_like
                OR similarity(LOWER(COALESCE(d.generic_en, '')), LOWER(:q)) > 0.4
                OR similarity(LOWER(COALESCE(d.generic_ar, '')), :q) > 0.4
                OR similarity(LOWER(COALESCE(p.brand_en, '')), LOWER(:q)) > 0.4
                OR similarity(LOWER(COALESCE(p.brand_ar, '')), :q) > 0.4
        )
        SELECT DISTINCT ON (id) *
        FROM scored
        ORDER BY id, score DESC
        LIMIT :lim
    """)

    result = await db.execute(stmt, {
        "q":           base,
        "q_like":      f"%{base}%",
        "q_norm":      q_norm,
        "q_norm_like": f"%{q_norm}%",
        "ar_from":     AR_FROM,
        "ar_to":       AR_TO,
        "lim":         limit,
    })

    return [DrugOut(**dict(row._mapping)) for row in result.fetchall()]