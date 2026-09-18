"""
SQLAlchemy ORM models.

Changes from prior version:
- Added Proposal ORM class (was missing, causing startup crash)
- Added AuditLog ORM class with SHA-256 forward chain
- Added UNII and InChIKey columns to Drug (per AI #2 recommendation)
- Added confidence_score to Proposal
"""
import uuid
import hashlib
from datetime import datetime
from sqlalchemy import (
    String,
    Text,
    Boolean,
    Integer,
    ForeignKey,
    DateTime,
    JSON,
    Numeric,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Drug(Base):
    __tablename__ = "drugs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    rxcui: Mapped[str | None] = mapped_column(String(20), unique=True)
    unii: Mapped[str | None] = mapped_column(String(20), unique=True)
    inchikey: Mapped[str | None] = mapped_column(String(30), unique=True)
    generic_en: Mapped[str] = mapped_column(String(255), nullable=False)
    generic_ar: Mapped[str | None] = mapped_column(String(255))
    drug_class: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    products: Mapped[list["Product"]] = relationship(back_populates="drug")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("drugs.id", ondelete="CASCADE")
    )
    brand_en: Mapped[str | None] = mapped_column(String(255))
    brand_ar: Mapped[str | None] = mapped_column(String(255))
    market: Mapped[str] = mapped_column(String(10))
    registration_no: Mapped[str | None] = mapped_column(String(100))
    manufacturer: Mapped[str | None] = mapped_column(String(255))
    form: Mapped[str | None] = mapped_column(String(100))
    strength: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="active")
    source: Mapped[str] = mapped_column(String(20))
    source_url: Mapped[str | None] = mapped_column(Text)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    drug: Mapped[Drug] = relationship(back_populates="products")


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    drug_a_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("drugs.id"))
    drug_b_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("drugs.id"))
    severity: Mapped[str] = mapped_column(String(20))
    effect_en: Mapped[str] = mapped_column(Text)
    effect_ar: Mapped[str | None] = mapped_column(Text)
    management_en: Mapped[str | None] = mapped_column(Text)
    management_ar: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(50))
    source_citation: Mapped[str | None] = mapped_column(Text)
    reviewer_name: Mapped[str | None] = mapped_column(String(255))
    reviewer_approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    product_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("products.id"))
    custom_name: Mapped[str | None] = mapped_column(String(255))
    time_slots: Mapped[dict] = mapped_column(JSON)
    food_relation: Mapped[str | None] = mapped_column(String(20))
    dose_note: Mapped[str | None] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# ============================================================
# NEW in this version — required by admin.py imports
# ============================================================

class Proposal(Base):
    """
    Maker-checker curation queue.
    A draft is created by one reviewer; only a second can approve it.
    """
    __tablename__ = "proposals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type: Mapped[str] = mapped_column(String(20))  # add | update | delete
    payload: Mapped[dict] = mapped_column(JSON)
    summary: Mapped[str] = mapped_column(Text)
    proposed_by: Mapped[str] = mapped_column(String(255))
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    decided_by: Mapped[str | None] = mapped_column(String(255))
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class AuditLog(Base):
    """
    Append-only audit log with SHA-256 forward chain.
    Each row's hash covers (prev_hash + this row's fields), so tampering
    with any past row breaks the chain and is detectable.
    """
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    actor: Mapped[str] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(100))
    entity_type: Mapped[str | None] = mapped_column(String(50))
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    detail: Mapped[dict | None] = mapped_column(JSON)
    prev_hash: Mapped[str | None] = mapped_column(String(64))
    hash: Mapped[str] = mapped_column(String(64), nullable=False)

    @staticmethod
    def compute_hash(
        prev_hash: str | None,
        actor: str,
        action: str,
        entity_type: str | None,
        entity_id: str | None,
        detail: dict | None,
    ) -> str:
        """Deterministic hash for a row given the previous row's hash."""
        payload = "|".join(
            [
                prev_hash or "GENESIS",
                actor,
                action,
                entity_type or "",
                str(entity_id) if entity_id else "",
                str(sorted((detail or {}).items())),
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()