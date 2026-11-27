from datetime import date
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IdMixin, TimestampMixin, VersionMixin


class Project(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint("status IN ('draft','active','completed','archived')", name="ck_projects_status"),
        CheckConstraint("planned_end_date >= start_date", name="ck_projects_dates"),
        CheckConstraint("manager_id <> approver_id", name="ck_projects_distinct_reviewers"),
        Index("ix_projects_enterprise_status", "enterprise_id", "status"),
        Index("ix_projects_manager", "manager_id"),
        Index("ix_projects_approver", "approver_id"),
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    enterprise_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("enterprises.id", ondelete="RESTRICT"), nullable=False)
    manager_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    approver_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    actual_end_date: Mapped[date | None] = mapped_column(Date)
    goal: Mapped[str | None] = mapped_column(Text)
    problem: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    archived_from_status: Mapped[str | None] = mapped_column(String(20))

    enterprise = relationship("Enterprise")
    manager = relationship("User", foreign_keys=[manager_id])
    approver = relationship("User", foreign_keys=[approver_id])
    members = relationship("ProjectMember", back_populates="project")


class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("projects.id", ondelete="RESTRICT"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True)

    project: Mapped[Project] = relationship(back_populates="members")
    user = relationship("User")
