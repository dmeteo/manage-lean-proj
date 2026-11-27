from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import Field, field_validator, model_validator

from app.common.enums import EffectType
from app.schemas.activity import ActivityDto
from app.schemas.common import ApiModel, LongText, MetricDecimal, MoneyDecimal, Name, PatchModel, Unit


class MetricCreate(ApiModel):
    name: Name
    unit: Unit
    plan: MetricDecimal | None
    actual: MetricDecimal | None
    recorded_date: date
    source: LongText | None = None

    @model_validator(mode="after")
    def require_value(self):
        if self.plan is None and self.actual is None:
            raise ValueError("plan or actual is required")
        return self


class MetricUpdate(PatchModel):
    non_nullable_fields = frozenset({"name", "unit", "recorded_date"})
    name: Name | None = None
    unit: Unit | None = None
    plan: MetricDecimal | None = None
    actual: MetricDecimal | None = None
    recorded_date: date | None = None
    source: LongText | None = None
    expected_version: int = Field(ge=1)


class MetricDto(ApiModel):
    id: UUID
    project_id: UUID
    name: str
    unit: str
    plan: MetricDecimal | None
    actual: MetricDecimal | None
    recorded_date: date
    source: str | None
    version: int

    @field_validator("plan", "actual", mode="before")
    @classmethod
    def decimal_to_string(cls, value):
        return format(value, "f") if isinstance(value, Decimal) else value


class EffectCreate(ApiModel):
    type: EffectType
    amount: MoneyDecimal
    currency: str = Field(pattern="^RUB$")
    period_start: date
    period_end: date
    calculation_document_id: UUID | None = None
    confirmation_document_id: UUID | None = None

    @model_validator(mode="after")
    def validate_period(self):
        if self.period_end < self.period_start:
            raise ValueError("periodEnd must be on or after periodStart")
        return self


class EffectUpdate(PatchModel):
    non_nullable_fields = frozenset({"type", "amount", "currency", "period_start", "period_end"})
    type: EffectType | None = None
    amount: MoneyDecimal | None = None
    currency: str | None = Field(default=None, pattern="^RUB$")
    period_start: date | None = None
    period_end: date | None = None
    calculation_document_id: UUID | None = None
    confirmation_document_id: UUID | None = None
    expected_version: int = Field(ge=1)


class EffectDto(ApiModel):
    id: UUID
    project_id: UUID
    type: EffectType
    amount: MoneyDecimal
    currency: str
    period_start: date
    period_end: date
    calculation_document_id: UUID | None
    confirmation_document_id: UUID | None
    version: int

    @field_validator("amount", mode="before")
    @classmethod
    def decimal_to_string(cls, value):
        return format(value, "f") if isinstance(value, Decimal) else value


class DashboardDto(ApiModel):
    active_projects: int
    in_progress_activities: int
    overdue_activities: int
    pending_reviews: int
    upcoming_activities: list[ActivityDto]
    as_of: datetime


class AuditDto(ApiModel):
    id: UUID
    actor_id: UUID
    entity_type: str
    entity_id: UUID
    action: str
    timestamp: datetime
    change_summary: str
