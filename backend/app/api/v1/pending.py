"""Explicit placeholder for contract routes without business logic yet."""

from typing import NoReturn
from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.common import Problem


class PendingEndpoint(Exception):
    pass


PROBLEM_CONTENT = {
    "application/problem+json": {"schema": Problem.model_json_schema(by_alias=True)}
}

PENDING_RESPONSES = {
    501: {
        "description": "Route is declared for OpenAPI; business logic is not implemented.",
        "content": PROBLEM_CONTENT,
    }
}


def pending() -> NoReturn:
    raise PendingEndpoint


async def pending_handler(request: Request, exc: PendingEndpoint) -> JSONResponse:
    problem = Problem(
        title="Маршрут не реализован",
        status=501,
        code="not_implemented",
        detail="Контракт маршрута описан, обработчик пока не реализован.",
        trace_id=str(uuid4()),
    )
    return JSONResponse(
        status_code=501,
        content=problem.model_dump(by_alias=True),
        media_type="application/problem+json",
    )


