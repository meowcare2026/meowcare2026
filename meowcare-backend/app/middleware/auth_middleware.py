from typing import Any, Callable

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.services.auth_service import AuthService
from app.utils.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)


bearer_scheme = HTTPBearer(
    scheme_name="AdminBearerAuth",
    description="Masukkan access token dari login admin",
    auto_error=False,
)


def get_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
) -> str:
    if credentials is None:
        raise UnauthorizedException(
            message="Bearer token wajib disertakan"
        )

    if credentials.scheme.lower() != "bearer":
        raise UnauthorizedException(
            message="Skema autentikasi harus Bearer"
        )

    return credentials.credentials


def get_current_admin(
    access_token: str = Depends(get_access_token),
) -> dict[str, Any]:
    return AuthService.get_admin_from_token(access_token)


def require_roles(
    *allowed_roles: str,
) -> Callable[..., dict[str, Any]]:
    def role_dependency(
        admin: dict[str, Any] = Depends(get_current_admin),
    ) -> dict[str, Any]:
        if admin["role"] not in allowed_roles:
            raise ForbiddenException(
                message="Role admin tidak memiliki izin"
            )

        return admin

    return role_dependency


require_admin = require_roles(
    "superadmin",
    "pakar",
    "admin",
)

require_expert = require_roles(
    "superadmin",
    "pakar",
)

require_superadmin = require_roles(
    "superadmin",
)