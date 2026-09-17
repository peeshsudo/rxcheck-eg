from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Schedule
from app.schemas import ScheduleIn, ScheduleOut

router = APIRouter()


@router.post("/", response_model=ScheduleOut, status_code=201)
async def create_schedule(payload: ScheduleIn, db: AsyncSession = Depends(get_db)):
    sched = Schedule(**payload.model_dump())
    db.add(sched)
    await db.commit()
    await db.refresh(sched)
    return sched


@router.get("/user/{user_id}", response_model=list[ScheduleOut])
async def list_user_schedules(user_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Schedule).where(Schedule.user_id == user_id, Schedule.active.is_(True))
    result = await db.execute(stmt)
    return result.scalars().all()