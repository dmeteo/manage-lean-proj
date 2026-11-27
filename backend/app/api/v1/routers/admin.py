from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.v1.deps import CSRF, SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.schemas.common import Page
from app.schemas.identity import (
    EnterpriseCreate,
    EnterpriseDto,
    EnterpriseUpdate,
    UserCreate,
    UserDto,
    UserUpdate,
)
from app.schemas.query import EnterpriseQuery, UserQuery

router = APIRouter(tags=["Administration"], dependencies=[SESSION])


@router.get("/enterprises", response_model=Page[EnterpriseDto], responses=PENDING_RESPONSES)
def list_enterprises(query: Annotated[EnterpriseQuery, Query()]):
    pending()


@router.post("/enterprises", response_model=EnterpriseDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
def create_enterprise(body: EnterpriseCreate):
    pending()


@router.patch("/enterprises/{enterprise_id}", response_model=EnterpriseDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_enterprise(enterprise_id: UUID, body: EnterpriseUpdate):
    pending()


@router.get("/users", response_model=Page[UserDto], responses=PENDING_RESPONSES)
def list_users(query: Annotated[UserQuery, Query()]):
    pending()


@router.post("/users", response_model=UserDto, status_code=201, dependencies=[CSRF], responses=PENDING_RESPONSES)
def create_user(body: UserCreate):
    pending()


@router.patch("/users/{user_id}", response_model=UserDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def update_user(user_id: UUID, body: UserUpdate):
    pending()
