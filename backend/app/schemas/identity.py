from uuid import UUID

from pydantic import Field

from app.common.enums import Role
from app.schemas.common import ApiModel, DisplayName, Name, PatchModel


class EnterpriseCreate(ApiModel):
    name: Name


class EnterpriseUpdate(PatchModel):
    non_nullable_fields = frozenset({"name"})
    name: Name | None = None
    expected_version: int = Field(ge=1)


class EnterpriseDto(ApiModel):
    id: UUID
    name: str
    version: int


class LoginRequest(ApiModel):
    login: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9._-]+$")
    password: str = Field(min_length=1, max_length=256)


class CsrfDto(ApiModel):
    csrf_token: str


class UserCreate(ApiModel):
    display_name: DisplayName
    login: str = Field(min_length=3, max_length=100, pattern=r"^[A-Za-z0-9._-]+$")
    password: str = Field(min_length=12, max_length=256)
    role: Role
    enterprise_id: UUID | None


class UserUpdate(PatchModel):
    non_nullable_fields = frozenset({"display_name", "role", "is_active"})
    display_name: DisplayName | None = None
    role: Role | None = None
    enterprise_id: UUID | None = None
    is_active: bool | None = None
    expected_version: int = Field(ge=1)


class UserDto(ApiModel):
    id: UUID
    display_name: str
    login: str
    role: Role
    enterprise_id: UUID | None
    is_active: bool
    version: int


class UserSummary(ApiModel):
    id: UUID
    display_name: str
    role: Role
    enterprise_id: UUID | None
