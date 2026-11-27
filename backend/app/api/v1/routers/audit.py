from typing import Annotated

from fastapi import APIRouter, Query

from app.api.v1.deps import SESSION
from app.api.v1.pending import PENDING_RESPONSES, pending
from app.schemas.common import Page
from app.schemas.query import AuditQuery
from app.schemas.reporting import AuditDto

router = APIRouter(tags=["Audit"], dependencies=[SESSION])


@router.get("/audit", response_model=Page[AuditDto], responses=PENDING_RESPONSES)
def list_audit(query: Annotated[AuditQuery, Query()]):
    pending()
