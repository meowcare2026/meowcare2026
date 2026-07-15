from pydantic import BaseModel, Field, field_validator


class RuleCreateRequest(BaseModel):
    disease_id: str = Field(
        min_length=36,
        max_length=36,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    symptom_id: str = Field(
        min_length=36,
        max_length=36,
        examples=["550e8400-e29b-41d4-a716-446655440001"],
    )
    cf_expert: float = Field(
        ge=0,
        le=1,
        examples=[0.8],
    )
    notes: str | None = Field(
        default=None,
        max_length=1000,
    )
    source_reference: str | None = Field(
        default=None,
        max_length=500,
    )
    is_active: bool = True

    @field_validator(
        "notes",
        "source_reference",
        mode="before",
    )
    @classmethod
    def normalize_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class RuleUpdateRequest(BaseModel):
    disease_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )
    symptom_id: str | None = Field(
        default=None,
        min_length=36,
        max_length=36,
    )
    cf_expert: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    notes: str | None = Field(
        default=None,
        max_length=1000,
    )
    source_reference: str | None = Field(
        default=None,
        max_length=500,
    )
    is_active: bool | None = None

    @field_validator(
        "notes",
        "source_reference",
        mode="before",
    )
    @classmethod
    def normalize_optional_text(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class RuleResponse(BaseModel):
    id: str
    disease_id: str
    symptom_id: str
    cf_expert: float
    notes: str | None
    source_reference: str | None
    is_active: bool
    created_at: str
    updated_at: str