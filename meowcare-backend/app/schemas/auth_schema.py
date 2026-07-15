from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class AdminRegisterRequest(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
        examples=["Admin MeowCare"],
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=100,
        examples=["Admin12345"],
    )


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=100,
    )


class AdminLogoutRequest(BaseModel):
    refresh_token: str = Field(
        min_length=10,
    )


class AdminProfileResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: Literal["superadmin", "pakar", "admin"]
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int | None = None


class AdminLoginResponse(BaseModel):
    admin: AdminProfileResponse
    token: TokenResponse