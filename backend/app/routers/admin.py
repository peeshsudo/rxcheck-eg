"""
Admin endpoints — curation queue and audit log.

Changes from prior version:
- Implemented real DB queries (was returning [])
- All routes require X-Admin-Key (enforced in main.py via dependency)
- Added proposal decision endpoint with forward-chained audit entry
"""
from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Proposal, AuditLog
from app.schemas import ProposalOut, AuditLogOut


router = APIRouter()


@router.get("/proposals", response_model=list[ProposalOut])
async def list_proposals(
    status: str | None = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Proposal).order_by(desc(Proposal.created_at)).limit(limit)
    if status:
        stmt = stmt.where(Proposal.status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/proposals/{proposal_id}/decide", response_model=ProposalOut)
async def decide_proposal(
    proposal_id: UUID,
    decision: str,           # "approved" | "rejected"
    decided_by: str,         # in production: extract from JWT
    db: AsyncSession = Depends(get_db),
):
    if decision not in ("approved", "rejected"):
        raise HTTPException(400, "decision must be 'approved' or 'rejected'")

    proposal = await db.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(404, "Proposal not found")
    if proposal.status != "pending":
        raise HTTPException(409, f"Proposal already {proposal.status}")

    proposal.status = decision
    proposal.decided_by = decided_by
    proposal.decided_at = datetime.now(timezone.utc)

    # Write forward-chained audit entry
    await _append_audit(
        db,
        actor=decided_by,
        action=f"proposal.{decision}",
        entity_type="proposal",
        entity_id=proposal.id,
        detail={"summary": proposal.summary, "type": proposal.type},
    )

    await db.commit()
    await db.refresh(proposal)
    return proposal


@router.get("/audit-log", response_model=list[AuditLogOut])
async def get_audit_log(
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AuditLog).order_by(desc(AuditLog.ts)).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def _append_audit(
    db: AsyncSession,
    *,
    actor: str,
    action: str,
    entity_type: str | None = None,
    entity_id: UUID | None = None,
    detail: dict | None = None,
) -> AuditLog:
    """Append a new audit row, chaining its hash to the previous row."""
    prev = (
        await db.execute(select(AuditLog).order_by(desc(AuditLog.id)).limit(1))
    ).scalar_one_or_none()

    prev_hash = prev.hash if prev else None
    row_hash = AuditLog.compute_hash(
        prev_hash=prev_hash,
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        detail=detail,
    )

    entry = AuditLog(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        detail=detail,
        prev_hash=prev_hash,
        hash=row_hash,
    )
    db.add(entry)
    return entry