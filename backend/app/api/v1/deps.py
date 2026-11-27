"""OpenAPI security declarations; authorization is not implemented in route stubs."""

from fastapi import Depends
from fastapi.security import APIKeyCookie, APIKeyHeader

session_cookie = APIKeyCookie(name="lean_session", auto_error=False)
csrf_header = APIKeyHeader(name="X-CSRF-Token", auto_error=False)

SESSION = Depends(session_cookie)
CSRF = Depends(csrf_header)
