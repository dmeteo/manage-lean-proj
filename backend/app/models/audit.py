from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IdMixin


class AuditEvent(Base, IdMixin):
    __tablename__ = "audit_events"
    __table_args__ = (Index("ix_audit_entity_time", "entity_type", "entity_id", "timestamp"),)

    actor_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    project_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), index=True)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    change_summary: Mapped[str] = mapped_column(Text, nullable=False)

    actor = relationship("User")
