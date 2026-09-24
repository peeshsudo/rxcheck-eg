"""Pydantic schemas for RxCheck-EG."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ==== Auth ====

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    PHARMACIST = "PHARMACIST"
    ADMIN = "ADMIN"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_role: UserRole


class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[UserRole] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.PATIENT


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime


# ==== Domain ====

class DrugOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    rxcui: str | None
    unii: str | None
    inchikey: str | None
    generic_en: str
    generic_ar: str | None
    drug_class: str | None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    drug_id: UUID
    brand_en: str | None
    brand_ar: str | None
    market: str
    form: str | None
    strength: str | None
    source: str


class InteractionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    drug_a_id: UUID
    drug_b_id: UUID
    severity: str
    effect_en: str
    effect_ar: str | None
    management_en: str | None
    management_ar: str | None
    source: str
    source_citation: str | None


class ScheduleIn(BaseModel):
    user_id: UUID
    product_id: UUID | None = None
    custom_name: str | None = None
    time_slots: list[str]
    food_relation: str | None = None
    dose_note: str | None = None


class ScheduleOut(ScheduleIn):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    active: bool
    created_at: datetime


class AssistantQuery(BaseModel):
    question: str
    locale: str = "ar"


class AssistantAnswer(BaseModel):
    answer: str
    grounded: bool
    severity: str | None = None
    sources: list[str] = []


class ProposalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    type: str
    summary: str
    proposed_by: str
    confidence_score: float | None
    status: str
    decided_by: str | None
    decided_at: datetime | None
    created_at: datetime


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ts: datetime
    actor: str
    action: str
    entity_type: str | None
    entity_id: UUID | None
    detail: dict | None
    prev_hash: str | None
    hash: str