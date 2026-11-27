from typing import Annotated, ClassVar, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra="forbid",
    )


class PatchModel(ApiModel):
    non_nullable_fields: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        for name in self.non_nullable_fields & self.model_fields_set:
            if getattr(self, name) is None:
                raise ValueError(f"{name} cannot be null")
        return self


Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
DisplayName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
LongText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=4000)]
RequiredComment = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)]
Unit = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]
MetricDecimal = Annotated[str, StringConstraints(pattern=r"^-?\d{1,14}(\.\d{1,4})?$", max_length=20)]
MoneyDecimal = Annotated[str, StringConstraints(pattern=r"^-?\d{1,16}(\.\d{1,2})?$", max_length=20)]


T = TypeVar("T")


class Page(ApiModel, Generic[T]):
    items: list[T]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total: int = Field(ge=0)


class Problem(ApiModel):
    type: str = "about:blank"
    title: str
    status: int
    code: str
    detail: str
    trace_id: str
    errors: dict[str, list[str]] = Field(default_factory=dict)
