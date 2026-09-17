from fastapi import APIRouter, Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Drug, Interaction
from app.schemas import AssistantQuery, AssistantAnswer

router = APIRouter()


async def find_drug_by_name(db: AsyncSession, name: str) -> Drug | None:
    stmt = select(Drug).where(
        (Drug.generic_en.ilike(name)) | (Drug.generic_ar.ilike(name))
    ).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


@router.post("/ask", response_model=AssistantAnswer)
async def ask(payload: AssistantQuery, db: AsyncSession = Depends(get_db)):
    """
    Grounded Q&A. In production: replace with LangGraph agent that
    extracts drug names via NER, then calls interaction tools.
    """
    q = payload.question.lower()

    # Very simple demo: look for two known drug names
    all_drugs = (await db.execute(select(Drug))).scalars().all()
    mentioned = [d for d in all_drugs
                 if d.generic_en.lower() in q or (d.generic_ar and d.generic_ar in q)]

    if len(mentioned) < 2:
        return AssistantAnswer(
            answer="أحتاج إلى اسمَي دواءين على الأقل. مثال: هل أستطيع أخذ بلافيكس مع لوسيك؟",
            grounded=False,
        )

    a, b = sorted(mentioned[:2], key=lambda d: str(d.id))
    stmt = select(Interaction).where(
        and_(Interaction.drug_a_id == a.id,
             Interaction.drug_b_id == b.id,
             Interaction.is_current.is_(True))
    )
    hits = (await db.execute(stmt)).scalars().all()

    if not hits:
        return AssistantAnswer(
            answer=f"لا يوجد سجل مراجع لـ {a.generic_ar or a.generic_en} و{b.generic_ar or b.generic_en}. هذا لا يعني أنه آمن — استشر الصيدلي.",
            grounded=True,
        )

    hit = hits[0]
    return AssistantAnswer(
        answer=f"{a.generic_ar or a.generic_en} و{b.generic_ar or b.generic_en}: {hit.effect_ar or hit.effect_en} ({hit.severity}). {hit.management_ar or hit.management_en or ''}",
        grounded=True,
        severity=hit.severity,
        sources=[hit.source_citation or hit.source],
    )