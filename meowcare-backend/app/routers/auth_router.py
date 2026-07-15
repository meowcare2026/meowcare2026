from typing import Any

from fastapi import APIRouter, Depends, status

from app.controllers.auth_controller import AuthController
from app.middleware.auth_middleware import (
    get_access_token,
    get_current_admin,
)
from app.schemas.auth_schema import (
    AdminLoginRequest,
    AdminLogoutRequest,
    AdminRegisterRequest,
)


router = APIRouter(
    prefix="/admin/auth",
    tags=["Admin Authentication"],
)


@router.post(
    "/register",
    summary="Register admin",
    status_code=status.HTTP_201_CREATED,
)
def register_admin(payload: AdminRegisterRequest):
    return AuthController.register(payload)


@router.post(
    "/login",
    summary="Login admin",
)
def login_admin(payload: AdminLoginRequest):
    return AuthController.login(payload)


@router.get(
    "/me",
    summary="Get current admin profile",
)
def get_me(
    admin: dict[str, Any] = Depends(get_current_admin),
):
    return AuthController.me(admin)


@router.post(
    "/logout",
    summary="Logout admin",
)
def logout_admin(
    payload: AdminLogoutRequest,
    access_token: str = Depends(get_access_token),
    admin: dict[str, Any] = Depends(get_current_admin),
):
    return AuthController.logout(
        access_token=access_token,
        payload=payload,
        admin=admin,
    )