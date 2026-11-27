from typing import Literal
from uuid import UUID

from pydantic import Field

from app.common.enums import ActivityStatus, DocumentKind, EffectType, ExternalStatus, ProjectStatus, ReviewStage, Role
from app.schemas.common import ApiModel


class PageQuery(ApiModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    sort: str | None = None
    direction: Literal["asc", "desc"] = "asc"


class EnterpriseQuery(PageQuery):
    sort: Literal["name"] = "name"
    search: str | None = None


class UserQuery(PageQuery):
    sort: Literal["displayName"] = "displayName"
    search: str | None = None
    role: Role | None = None
    enterprise_id: UUID | None = None
    is_active: bool | None = None


class AssigneeQuery(PageQuery):
    sort: Literal["displayName"] = "displayName"
    enterprise_id: UUID
    search: str | None = None


class PeopleQuery(PageQuery):
    sort: Literal["displayName"] = "displayName"
    search: str | None = None


class ProjectQuery(PageQuery):
    sort: Literal["name", "plannedEndDate", "status"] = "name"
    search: str | None = None
    enterprise_id: UUID | None = None
    manager_id: UUID | None = None
    status: ProjectStatus | None = None


class ActivityQuery(PageQuery):
    sort: Literal["sortOrder", "plannedEndDate", "status"] = "sortOrder"
    search: str | None = None
    assignee_id: UUID | None = None
    status: ActivityStatus | None = None
    external_status: ExternalStatus | None = None
    is_overdue: bool | None = None


class FileQuery(PageQuery):
    sort: Literal["uploadedAt"] = "uploadedAt"
    kind: DocumentKind | None = None


class ReviewQuery(PageQuery):
    sort: Literal["createdAt"] = "createdAt"
    stage: ReviewStage | None = None


class MetricQuery(PageQuery):
    sort: Literal["name", "recordedDate"] = "name"
    search: str | None = None


class EffectQuery(PageQuery):
    sort: Literal["periodStart"] = "periodStart"
    type: EffectType | None = None


class AuditQuery(PageQuery):
    sort: Literal["timestamp"] = "timestamp"
    entity_type: str | None = None
    entity_id: UUID | None = None
