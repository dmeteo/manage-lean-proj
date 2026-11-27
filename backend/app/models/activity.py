from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IdMixin, TimestampMixin, VersionMixin


class Activity(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("status IN ('planned','inProgress','managerReview','approverReview','returned','internallyApproved')", name="ck_activities_status"),
        CheckConstraint("external_status IN ('notSent','sent','accepted','returned')", name="ck_activities_external_status"),
        CheckConstraint("planned_start_date IS NULL OR planned_end_date >= planned_start_date", name="ck_activities_dates"),
        CheckConstraint("sort_order >= 0 AND review_cycle >= 0", name="ck_activities_order_cycle"),
        Index("ix_activities_project_status", "project_id", "status"),
        Index("ix_activities_assignee", "assignee_id"),
        Index("ix_activities_deadline", "planned_end_date"),
    )

    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    stage: Mapped[str | None] = mapped_column(String(200))
    assignee_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    planned_start_date: Mapped[date | None] = mapped_column(Date)
    planned_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="planned", nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    requires_document: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    external_status: Mapped[str] = mapped_column(String(20), default="notSent", nullable=False)
    external_recorded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    external_recorded_by: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"))
    external_comment: Mapped[str | None] = mapped_column(Text)
    review_cycle: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    project = relationship("Project")
    assignee = relationship("User", foreign_keys=[assignee_id])
    files = relationship("Document", back_populates="activity")
    reviews = relationship("Review", back_populates="activity")


class Document(Base, IdMixin):
    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint("kind IN ('report','calculation','confirmation','other')", name="ck_documents_kind"),
        CheckConstraint("size_bytes > 0 AND revision >= 1", name="ck_documents_size_revision"),
        UniqueConstraint("activity_id", "kind", "revision", name="uq_documents_revision"),
    )

    activity_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("activities.id", ondelete="RESTRICT"), nullable=False, index=True)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    media_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    uploaded_by: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)

    activity: Mapped[Activity] = relationship(back_populates="files")


class Review(Base, IdMixin):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("stage IN ('manager','approver')", name="ck_reviews_stage"),
        CheckConstraint("decision IN ('approve','return')", name="ck_reviews_decision"),
        CheckConstraint("cycle >= 1", name="ck_reviews_cycle"),
        UniqueConstraint("activity_id", "cycle", "stage", name="uq_reviews_stage_per_cycle"),
    )

    activity_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("activities.id", ondelete="RESTRICT"), nullable=False, index=True)
    cycle: Mapped[int] = mapped_column(Integer, nullable=False)
    stage: Mapped[str] = mapped_column(String(20), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    decision: Mapped[str] = mapped_column(String(20), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    activity: Mapped[Activity] = relationship(back_populates="reviews")
