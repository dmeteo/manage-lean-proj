from fastapi import APIRouter

from app.api.v1.deps import CSRF, SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.schemas.common import EmptyBody
from app.schemas.identity import CsrfDto, LoginRequest, UserDto

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/csrf", response_model=CsrfDto, responses=PENDING_RESPONSES)
def get_csrf():
    pending()


@router.post("/login", response_model=UserDto, dependencies=[CSRF], responses=PENDING_RESPONSES)
def login(body: LoginRequest):
    pending()


@router.get("/me", response_model=UserDto, dependencies=[SESSION], responses=PENDING_RESPONSES)
def me():
    pending()


@router.post("/logout", status_code=204, dependencies=[SESSION, CSRF], responses=PENDING_RESPONSES)
def logout(body: EmptyBody):
    pending()
