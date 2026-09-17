from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Proposal, AuditLog

router = APIRouter()


@router.get("/proposals")
async def list_proposals(db: AsyncSession = Depends(get_db)):
    # (Model not shown for brevity — mirror the schema.sql table)
    return []


@router.get("/audit-log")
async def get_audit_log(limit: int = 50, db: AsyncSession = Depends(get_db)):
    return []