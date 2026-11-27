from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Response

from app.api.v1.deps import CSRF, SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.schemas.common import Page
from app.schemas.identity import UserSummary
from app.schemas.project import ProjectAssignments, ProjectCreate, ProjectDto, ProjectTransition, ProjectUpdate
from app.schemas.query import AssigneeQuery, PeopleQuery, ProjectQuery

router = APIRouter(tags=["Projects"], dependencies=[SESSION])


@router.get("/projects/assignees", response_model=Page[UserSummary], responses=PENDING_RESPONSES)
def list_assignees(query: Annotated[AssigneeQuery, Query()]):
    pending()


@router.get("/projects/managers", response_model=Page[UserSummary], responses=PENDING_RESPONSES)
def list_managers(query: Annotated[PeopleQuery, Query()]):
    pending()


@router.get("/projects/approvers", response_model=Page[UserSummary], responses=PENDING_RESPONSES)
def list_approvers(query: Annotated[PeopleQuery, Query()]):
    pending()


@router.get("/projects", response_model=Page[ProjectDto], responses=PENDING_RESPONSES)
def list_projects(query: Annotated[ProjectQuery, Query()]):
    pending()


@router.post("/projects", response_model=ProjectDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
def create_project(body: ProjectCreate):
    pending()


@router.get("/projects/{project_id}", response_model=ProjectDto, responses=PENDING_RESPONSES)
def get_project(project_id: UUID):
    pending()


@router.patch("/projects/{project_id}", response_model=ProjectDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_project(project_id: UUID, body: ProjectUpdate):
    pending()


@router.put("/projects/{project_id}/assignments", response_model=ProjectDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def replace_assignments(project_id: UUID, body: ProjectAssignments):
    pending()


@router.get("/projects/{project_id}/members", response_model=Page[UserSummary], responses=PENDING_RESPONSES)
def list_members(project_id: UUID, query: Annotated[PeopleQuery, Query()]):
    pending()


@router.post("/projects/{project_id}/status", response_model=ProjectDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def transition_project(project_id: UUID, body: ProjectTransition):
    pending()


@router.get(
    "/projects/{project_id}/export",
    response_class=Response,
    responses={
        200: {"description": "CSV export", "content": {"text/csv": {"schema": {"type": "string", "format": "binary"}}}},
        **PENDING_RESPONSES,
    },
)
def export_project(project_id: UUID, format: Annotated[str, Query(pattern="^csv$")] = "csv"):
    pending()
