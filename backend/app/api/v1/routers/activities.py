from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, Form, Query, Response, UploadFile

from app.api.v1.deps import CSRF, SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.common.enums import DocumentKind
from app.schemas.activity import (
    ActivityCreate,
    ActivityDto,
    ActivityTransition,
    ActivityUpdate,
    DocumentDto,
    ExternalStatusRequest,
    ReviewDto,
    ReviewRequest,
)
from app.schemas.common import Page
from app.schemas.query import ActivityQuery, FileQuery, ReviewQuery

router = APIRouter(tags=["Activities and documents"], dependencies=[SESSION])


@router.get("/projects/{project_id}/activities", response_model=Page[ActivityDto], responses=PENDING_RESPONSES)
def list_activities(project_id: UUID, query: Annotated[ActivityQuery, Query()]):
    pending()


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityDto,
    status_code=201,
    dependencies=[CSRF],
    responses=PENDING_RESPONSES,
)
def create_activity(project_id: UUID, body: ActivityCreate):
    pending()


@router.get("/activities/{activity_id}", response_model=ActivityDto, responses=PENDING_RESPONSES)
def get_activity(activity_id: UUID):
    pending()


@router.patch("/activities/{activity_id}", response_model=ActivityDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_activity(activity_id: UUID, body: ActivityUpdate):
    pending()


@router.post("/activities/{activity_id}/transitions", response_model=ActivityDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def transition_activity(activity_id: UUID, body: ActivityTransition):
    pending()


@router.post("/activities/{activity_id}/review", response_model=ActivityDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def review_activity(activity_id: UUID, body: ReviewRequest):
    pending()


@router.get("/activities/{activity_id}/reviews", response_model=Page[ReviewDto], responses=PENDING_RESPONSES)
def list_reviews(activity_id: UUID, query: Annotated[ReviewQuery, Query()]):
    pending()


@router.post("/activities/{activity_id}/external-status", response_model=ActivityDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def record_external_status(activity_id: UUID, body: ExternalStatusRequest):
    pending()


@router.get("/activities/{activity_id}/files", response_model=Page[DocumentDto], responses=PENDING_RESPONSES)
def list_files(activity_id: UUID, query: Annotated[FileQuery, Query()]):
    pending()


@router.post("/activities/{activity_id}/files", response_model=DocumentDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
async def upload_file(
    activity_id: UUID,
    file: Annotated[UploadFile, File(description="One PDF, DOCX, XLSX, PNG or JPEG file (up to 20 MiB)")],
    kind: Annotated[DocumentKind, Form()],
    expected_version: Annotated[int, Form(alias="expectedVersion", ge=1)],
):
    pending()


@router.get(
    "/files/{file_id}/download",
    response_class=Response,
    responses={
        200: {"description": "Attachment", "content": {"application/octet-stream": {"schema": {"type": "string", "format": "binary"}}}},
        **PENDING_RESPONSES,
    },
)
def download_file(file_id: UUID):
    pending()
