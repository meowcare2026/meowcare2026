from typing import Literal

from pydantic import BaseModel, Field, field_validator


SeverityLevel = Literal[
    "ringan",
    "sedang",
    "berat",
    "darurat",
]


class DiseaseCreateRequest(BaseModel):
    code: str = Field(
        min_length=2,
        max_length=20,
        examples=["P01"],
    )
    name: str = Field(
        min_length=3,
        max_length=150,
        examples=["Flu Kucing"],
    )
    description: str = Field(
        min_length=10,
    )
    solution: str = Field(
        min_length=10,
    )
    prevention: str | None = None
    severity_level: SeverityLevel = "sedang"
    expert_source: str | None = None
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator(
        "name",
        "description",
        "solution",
        "prevention",
        "expert_source",
        mode="before",
    )
    @classmethod
    def strip_text(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class DiseaseUpdateRequest(BaseModel):
    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )
    description: str | None = Field(
        default=None,
        min_length=10,
    )
    solution: str | None = Field(
        default=None,
        min_length=10,
    )
    prevention: str | None = None
    severity_level: SeverityLevel | None = None
    expert_source: str | None = None
    is_active: bool | None = None

    @field_validator("code")
    @classmethod
    def normalize_code(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.strip().upper()

    @field_validator(
        "name",
        "description",
        "solution",
        "prevention",
        "expert_source",
        mode="before",
    )
    @classmethod
    def strip_text(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class DiseaseResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str
    solution: str
    prevention: str | None
    severity_level: SeverityLevel
    expert_source: str | None
    is_active: bool
    created_at: str
    updated_at: str