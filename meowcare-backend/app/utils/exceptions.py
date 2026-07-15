from typing import Any


class AppException(Exception):
    def __init__(
        self,
        *,
        message: str,
        code: str,
        status_code: int = 400,
        details: Any = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        self.headers = headers

        super().__init__(message)


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Request tidak valid",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            status_code=400,
            details=details,
        )


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Autentikasi diperlukan",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
            details=details,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Anda tidak memiliki akses",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
            details=details,
        )


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Data tidak ditemukan",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details=details,
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Data sudah tersedia",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details=details,
        )


class DatabaseException(AppException):
    def __init__(
        self,
        message: str = "Terjadi kesalahan database",
        details: Any = None,
    ) -> None:
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details=details,
        )