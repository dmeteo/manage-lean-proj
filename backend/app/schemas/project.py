from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import Field, model_validator

from app.common.enums import ProjectStatus
from app.schemas.common import ApiModel, LongText, Name, PatchModel


class ProjectCreate(ApiModel):
    name: Name
    enterprise_id: UUID
    manager_id: UUID
    approver_id: UUID
    member_ids: list[UUID]
    start_date: date
    planned_end_date: date
    goal: LongText | None = None
    problem: LongText | None = None
    description: LongText | None = None

    @model_validator(mode="after")
    def validate_plan(self):
        if self.planned_end_date < self.start_date:
            raise ValueError("plannedEndDate must be on or after startDate")
        if self.manager_id == self.approver_id:
            raise ValueError("managerId and approverId must differ")
        if len(self.member_ids) != len(set(self.member_ids)):
            raise ValueError("memberIds must be unique")
        return self


class ProjectUpdate(PatchModel):
    non_nullable_fields = frozenset({"name", "start_date", "planned_end_date"})
    name: Name | None = None
    start_date: date | None = None
    planned_end_date: date | None = None
    goal: LongText | None = None
    problem: LongText | None = None
    description: LongText | None = None
    expected_version: int = Field(ge=1)


class ProjectAssignments(ApiModel):
    manager_id: UUID
    approver_id: UUID
    member_ids: list[UUID]
    expected_version: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_assignments(self):
        if self.manager_id == self.approver_id:
            raise ValueError("managerId and approverId must differ")
        if len(self.member_ids) != len(set(self.member_ids)):
            raise ValueError("memberIds must be unique")
        return self


class ProjectTransition(ApiModel):
    action: Literal["activate", "complete", "archive"]
    actual_end_date: date | None = None
    expected_version: int = Field(ge=1)

    @model_validator(mode="after")
    def require_completion_date(self):
        if self.action == "complete" and self.actual_end_date is None:
            raise ValueError("complete requires actualEndDate")
        return self


class ProjectDto(ApiModel):
    id: UUID
    name: str
    enterprise_id: UUID
    enterprise_name: str
    manager_id: UUID
    manager_name: str
    approver_id: UUID
    approver_name: str
    start_date: date
    planned_end_date: date
    actual_end_date: date | None
    goal: str | None
    problem: str | None
    description: str | None
    status: ProjectStatus
    archived_from_status: ProjectStatus | None
    progress_percent: int = Field(ge=0, le=100)
    version: int
    created_at: datetime
    updated_at: datetime
