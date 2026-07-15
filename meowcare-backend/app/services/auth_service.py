import logging
from typing import Any

from app.config.supabase import (
    create_supabase_auth_client,
    supabase_admin,
)
from app.repositories.admin_repository import AdminRepository
from app.schemas.auth_schema import (
    AdminLoginRequest,
    AdminLogoutRequest,
    AdminRegisterRequest,
)
from app.utils.exceptions import (
    ConflictException,
    DatabaseException,
    ForbiddenException,
    UnauthorizedException,
)


logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def register(
        payload: AdminRegisterRequest,
    ) -> dict[str, Any]:
        email = str(payload.email).strip().lower()
        name = payload.name.strip()
        created_user_id: str | None = None

        try:
            auth_response = supabase_admin.auth.admin.create_user(
                {
                    "email": email,
                    "password": payload.password,
                    "email_confirm": True,
                    "user_metadata": {
                        "name": name,
                    },
                }
            )

            user = auth_response.user

            if user is None:
                raise DatabaseException(
                    message="Akun autentikasi admin gagal dibuat"
                )

            created_user_id = str(user.id)

            profile = AdminRepository.create_profile(
                admin_id=created_user_id,
                name=name,
                role="admin",
            )

            AdminRepository.create_log(
                admin_id=created_user_id,
                action="create",
                description="Admin melakukan registrasi",
            )

            return {
                "id": created_user_id,
                "email": user.email,
                "name": profile["name"],
                "role": profile["role"],
                "is_active": profile["is_active"],
                "email_confirmed": True,
                "can_login_now": True,
            }

        except Exception as error:
            error_message = str(error).lower()

            if (
                "already registered" in error_message
                or "already exists" in error_message
                or "email_exists" in error_message
                or "user_already_exists" in error_message
            ):
                raise ConflictException(
                    message="Email admin sudah terdaftar"
                ) from error

            if created_user_id is not None:
                try:
                    supabase_admin.auth.admin.delete_user(
                        created_user_id
                    )
                except Exception as rollback_error:
                    logger.warning(
                        "Rollback user gagal: %s",
                        rollback_error,
                    )

            logger.exception("Registrasi admin gagal")

            raise DatabaseException(
                message="Registrasi admin gagal",
                details=str(error),
            ) from error

    @staticmethod
    def login(
        payload: AdminLoginRequest,
    ) -> dict[str, Any]:
        auth_client = create_supabase_auth_client()

        email = str(payload.email).strip().lower()

        try:
            auth_response = auth_client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": payload.password,
                }
            )

        except Exception as error:
            error_code = getattr(error, "code", None)
            error_status = getattr(error, "status", None)
            error_message = str(error)

            logger.error(
                "SUPABASE LOGIN ERROR | type=%s | code=%s | "
                "status=%s | message=%s",
                error.__class__.__name__,
                error_code,
                error_status,
                error_message,
            )

            raise UnauthorizedException(
                message=(
                    f"Login gagal. Supabase: {error_message} "
                    f"(code={error_code})"
                )
            ) from error

        user = auth_response.user
        session = auth_response.session

        if user is None:
            raise UnauthorizedException(
                message="Supabase tidak mengembalikan data user"
            )

        if session is None:
            raise UnauthorizedException(
                message=(
                    "Supabase tidak membuat session. "
                    "Kemungkinan email belum dikonfirmasi."
                )
            )

        admin_profile = AdminRepository.find_by_id(str(user.id))

        if admin_profile is None:
            raise ForbiddenException(
                message="Login Auth berhasil, tetapi profil admin tidak ditemukan"
            )

        if not admin_profile.get("is_active", False):
            raise ForbiddenException(
                message="Akun admin sedang dinonaktifkan"
            )

        AdminRepository.create_log(
            admin_id=str(user.id),
            action="login",
            description="Admin berhasil login",
        )

        return {
            "admin": {
                "id": str(user.id),
                "email": user.email,
                "name": admin_profile["name"],
                "role": admin_profile["role"],
                "is_active": admin_profile["is_active"],
            },
            "token": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "token_type": "bearer",
                "expires_in": session.expires_in,
            },
        }

    @staticmethod
    def get_admin_from_token(
        access_token: str,
    ) -> dict[str, Any]:
        auth_client = create_supabase_auth_client()

        try:
            user_response = auth_client.auth.get_user(
                access_token
            )
            user = user_response.user

        except Exception as error:
            raise UnauthorizedException(
                message="Token tidak valid atau sudah kedaluwarsa"
            ) from error

        if user is None:
            raise UnauthorizedException(
                message="Token tidak valid atau sudah kedaluwarsa"
            )

        admin_profile = AdminRepository.find_by_id(
            str(user.id)
        )

        if admin_profile is None:
            raise ForbiddenException(
                message="Profil admin tidak ditemukan"
            )

        if not admin_profile.get("is_active", False):
            raise ForbiddenException(
                message="Akun admin sedang dinonaktifkan"
            )

        return {
            "id": str(user.id),
            "email": user.email,
            "name": admin_profile["name"],
            "role": admin_profile["role"],
            "is_active": admin_profile["is_active"],
        }

    @staticmethod
    def logout(
        *,
        access_token: str,
        payload: AdminLogoutRequest,
        admin: dict[str, Any],
    ) -> None:
        auth_client = create_supabase_auth_client()

        try:
            auth_client.auth.set_session(
                access_token,
                payload.refresh_token,
            )

            auth_client.auth.sign_out()

        except Exception as error:
            raise UnauthorizedException(
                message="Session logout tidak valid"
            ) from error

        AdminRepository.create_log(
            admin_id=admin["id"],
            action="logout",
            description="Admin berhasil logout",
        )