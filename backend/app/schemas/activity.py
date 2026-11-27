from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from app.common.enums import ActivityStatus, DocumentKind, ExternalStatus, ReviewDecision, ReviewStage
from app.schemas.common import ApiModel, LongText, Name, PatchModel


class ActivityCreate(ApiModel):
    title: Name
    assignee_id: UUID
    planned_end_date: date
    planned_start_date: date | None = None
    stage: Name | None = None
    is_required: bool = True
    requires_document: bool = True
    sort_order: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.planned_start_date and self.planned_end_date < self.planned_start_date:
            raise ValueError("plannedEndDate must be on or after plannedStartDate")
        return self


class ActivityUpdate(PatchModel):
    non_nullable_fields = frozenset({
        "title", "assignee_id", "planned_end_date", "is_required", "requires_document", "sort_order"
    })
    title: Name | None = None
    stage: Name | None = None
    assignee_id: UUID | None = None
    planned_start_date: date | None = None
    planned_end_date: date | None = None
    is_required: bool | None = None
    requires_document: bool | None = None
    sort_order: int | None = Field(default=None, ge=0)
    actual_end_date: date | None = None
    comment: LongText | None = None
    expected_version: int = Field(ge=1)


class ActivityTransition(ApiModel):
    action: Literal["start", "submit"]
    expected_version: int = Field(ge=1)


class ActivityDto(ApiModel):
    id: UUID
    project_id: UUID
    title: str
    stage: str | None
    assignee_id: UUID
    assignee_name: str
    planned_start_date: date | None
    planned_end_date: date
    actual_end_date: date | None
    comment: str | None
    is_required: bool
    requires_document: bool
    sort_order: int
    status: ActivityStatus
    external_status: ExternalStatus
    external_recorded_at: datetime | None
    external_recorded_by: UUID | None
    external_comment: str | None
    is_overdue: bool
    completed_late: bool
    review_cycle: int
    version: int
    created_at: datetime
    updated_at: datetime


class ReviewRequest(ApiModel):
    decision: ReviewDecision
    comment: LongText | None = None
    expected_version: int = Field(ge=1)

    @model_validator(mode="after")
    def require_return_reason(self):
        if self.decision == ReviewDecision.RETURN and not self.comment:
            raise ValueError("return requires comment")
        return self


class ReviewDto(ApiModel):
    id: UUID
    activity_id: UUID
    cycle: int
    stage: ReviewStage
    actor_id: UUID
    decision: ReviewDecision
    comment: str | None
    created_at: datetime


class ExternalStatusRequest(ApiModel):
    status: Literal[ExternalStatus.SENT, ExternalStatus.ACCEPTED, ExternalStatus.RETURNED]
    comment: LongText | None = None
    expected_version: int = Field(ge=1)

    @model_validator(mode="after")
    def require_return_reason(self):
        if self.status == ExternalStatus.RETURNED and not self.comment:
            raise ValueError("return requires comment")
        return self


class DocumentDto(ApiModel):
    id: UUID
    activity_id: UUID
    original_name: str
    media_type: str
    size_bytes: int
    uploaded_by: UUID
    uploaded_at: datetime
    kind: DocumentKind
    revision: int
    activity_version: int
