from typing import Any

from app.schemas.auth_schema import (
    AdminLoginRequest,
    AdminLogoutRequest,
    AdminRegisterRequest,
)
from app.services.auth_service import AuthService
from app.utils.response import success_response


class AuthController:
    @staticmethod
    def register(payload: AdminRegisterRequest):
        result = AuthService.register(payload)

        return success_response(
            message="Registrasi admin berhasil",
            data=result,
            status_code=201,
        )

    @staticmethod
    def login(payload: AdminLoginRequest):
        result = AuthService.login(payload)

        return success_response(
            message="Login admin berhasil",
            data=result,
        )

    @staticmethod
    def me(admin: dict[str, Any]):
        return success_response(
            message="Profil admin berhasil diambil",
            data=admin,
        )

    @staticmethod
    def logout(
        *,
        access_token: str,
        payload: AdminLogoutRequest,
        admin: dict[str, Any],
    ):
        AuthService.logout(
            access_token=access_token,
            payload=payload,
            admin=admin,
        )

        return success_response(
            message="Logout admin berhasil",
            data=None,
        )