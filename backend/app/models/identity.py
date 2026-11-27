from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, IdMixin, TimestampMixin, VersionMixin


class Enterprise(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "enterprises"

    name: Mapped[str] = mapped_column(String(200), nullable=False)


class User(Base, IdMixin, VersionMixin, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('admin','coordinator','manager','approver','employee')", name="ck_users_role"),
        CheckConstraint(
            "(role = 'employee' AND enterprise_id IS NOT NULL) OR "
            "(role <> 'employee' AND enterprise_id IS NULL)",
            name="ck_users_enterprise_scope",
        ),
        Index("ix_users_enterprise_role", "enterprise_id", "role"),
    )

    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    login: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    enterprise_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("enterprises.id", ondelete="RESTRICT"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    enterprise: Mapped[Enterprise | None] = relationship()


Index("uq_users_login_normalized", func.lower(User.login), unique=True)


class AuthSession(Base, IdMixin):
    __tablename__ = "auth_sessions"

    user_id: Mapped[UUID | None] = mapped_column(Uuid, ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    csrf_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped[User | None] = relationship()
