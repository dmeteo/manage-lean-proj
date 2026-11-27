from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.v1.deps import CSRF, SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.schemas.common import Page
from app.schemas.query import EffectQuery, MetricQuery
from app.schemas.reporting import (
    DashboardDto,
    EffectCreate,
    EffectDto,
    EffectUpdate,
    MetricCreate,
    MetricDto,
    MetricUpdate,
)

router = APIRouter(tags=["Reporting"], dependencies=[SESSION])


@router.get("/projects/{project_id}/metrics", response_model=Page[MetricDto], responses=PENDING_RESPONSES)
def list_metrics(project_id: UUID, query: Annotated[MetricQuery, Query()]):
    pending()


@router.post("/projects/{project_id}/metrics", response_model=MetricDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
def create_metric(project_id: UUID, body: MetricCreate):
    pending()


@router.patch("/metrics/{metric_id}", response_model=MetricDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_metric(metric_id: UUID, body: MetricUpdate):
    pending()


@router.get("/projects/{project_id}/effects", response_model=Page[EffectDto], responses=PENDING_RESPONSES)
def list_effects(project_id: UUID, query: Annotated[EffectQuery, Query()]):
    pending()


@router.post("/projects/{project_id}/effects", response_model=EffectDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
def create_effect(project_id: UUID, body: EffectCreate):
    pending()


@router.patch("/effects/{effect_id}", response_model=EffectDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_effect(effect_id: UUID, body: EffectUpdate):
    pending()


@router.get("/dashboard", response_model=DashboardDto, responses=PENDING_RESPONSES)
def dashboard(enterprise_id: Annotated[UUID | None, Query(alias="enterpriseId")] = None):
    pending()
