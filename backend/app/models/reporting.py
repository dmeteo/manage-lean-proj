from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IdMixin, TimestampMixin, VersionMixin


class Metric(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "metrics"
    __table_args__ = (
        CheckConstraint("plan IS NOT NULL OR actual IS NOT NULL", name="ck_metrics_value"),
        Index("ix_metrics_project_date", "project_id", "recorded_date"),
    )

    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    plan: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    actual: Mapped[Decimal | None] = mapped_column(Numeric(18, 4))
    recorded_date: Mapped[date] = mapped_column(Date, nullable=False)
    source: Mapped[str | None] = mapped_column(Text)

    project = relationship("Project")


class EconomicEffect(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "economic_effects"
    __table_args__ = (
        CheckConstraint("type IN ('actual','potential','releasedFunds')", name="ck_effects_type"),
        CheckConstraint("currency = 'RUB'", name="ck_effects_currency"),
        CheckConstraint("period_end >= period_start", name="ck_effects_period"),
        Index("ix_effects_project_period", "project_id", "period_start"),
    )

    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    calculation_document_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("documents.id", ondelete="RESTRICT"))
    confirmation_document_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("documents.id", ondelete="RESTRICT"))

    project = relationship("Project")
