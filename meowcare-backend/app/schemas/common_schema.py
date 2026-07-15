from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


DataType = TypeVar("DataType")


class MetaResponse(BaseModel):
    page: int | None = None
    limit: int | None = None
    total: int | None = None
    total_pages: int | None = None


class SuccessResponse(BaseModel, Generic[DataType]):
    success: bool = True
    message: str
    data: DataType | None = None
    meta: MetaResponse | None = None


class ErrorDetail(BaseModel):
    code: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: ErrorDetail


class ValidationErrorItem(BaseModel):
    field: str
    message: str
    type: str | None = None


class ValidationErrorResponse(BaseModel):
    success: bool = False
    message: str = "Validasi request gagal"
    error: ErrorDetail = Field(
        default_factory=lambda: ErrorDetail(
            code="VALIDATION_ERROR",
            details=[],
        )
    )