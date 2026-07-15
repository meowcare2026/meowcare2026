from pydantic import BaseModel, Field, field_validator


class SymptomCreateRequest(BaseModel):
    code: str = Field(
        min_length=2,
        max_length=20,
        examples=["G01"],
    )
    name: str = Field(
        min_length=3,
        max_length=255,
        examples=["Demam tinggi"],
    )
    category: str | None = Field(
        default=None,
        max_length=50,
        examples=["Suhu Tubuh"],
    )
    is_active: bool = True

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class SymptomUpdateRequest(BaseModel):
    code: str | None = Field(
        default=None,
        min_length=2,
        max_length=20,
    )
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )
    category: str | None = Field(
        default=None,
        max_length=50,
    )
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

    @field_validator("name")
    @classmethod
    def normalize_name(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(
        cls,
        value: str | None,
    ) -> str | None:
        if isinstance(value, str):
            cleaned = value.strip()
            return cleaned or None

        return value


class SymptomResponse(BaseModel):
    id: str
    code: str
    name: str
    category: str | None
    is_active: bool
    created_at: str
    updated_at: str