import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.settings import settings
from app.utils.exceptions import AppException
from app.utils.response import error_response


logger = logging.getLogger(__name__)


def format_validation_errors(
    errors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    formatted_errors: list[dict[str, Any]] = []

    for error in errors:
        location = error.get("loc", [])
        field_parts = [
            str(item)
            for item in location
            if item not in ("body", "query", "path", "header")
        ]

        field = ".".join(field_parts) if field_parts else "request"

        formatted_errors.append(
            {
                "field": field,
                "message": error.get("msg", "Nilai tidak valid"),
                "type": error.get("type"),
            }
        )

    return formatted_errors


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exception: AppException,
    ):
        logger.warning(
            "Application error: method=%s path=%s code=%s message=%s",
            request.method,
            request.url.path,
            exception.code,
            exception.message,
        )

        return error_response(
            message=exception.message,
            code=exception.code,
            status_code=exception.status_code,
            details=exception.details,
            headers=exception.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exception: RequestValidationError,
    ):
        errors = format_validation_errors(exception.errors())

        logger.warning(
            "Validation error: method=%s path=%s errors=%s",
            request.method,
            request.url.path,
            errors,
        )

        return error_response(
            message="Validasi request gagal",
            code="VALIDATION_ERROR",
            status_code=422,
            details=errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exception: StarletteHTTPException,
    ):
        detail = exception.detail

        if isinstance(detail, dict):
            message = detail.get("message", "Request gagal")
            code = detail.get("code", "HTTP_ERROR")
            details = detail.get("details")
        else:
            message = str(detail)
            code = get_http_error_code(exception.status_code)
            details = None

        return error_response(
            message=message,
            code=code,
            status_code=exception.status_code,
            details=details,
            headers=exception.headers,
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exception: Exception,
    ):
        logger.exception(
            "Unhandled exception: method=%s path=%s",
            request.method,
            request.url.path,
        )

        details = None

        if settings.debug:
            details = {
                "type": exception.__class__.__name__,
                "message": str(exception),
            }

        return error_response(
            message="Terjadi kesalahan internal pada server",
            code="INTERNAL_SERVER_ERROR",
            status_code=500,
            details=details,
        )


def get_http_error_code(status_code: int) -> str:
    codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "TOO_MANY_REQUESTS",
        500: "INTERNAL_SERVER_ERROR",
    }

    return codes.get(status_code, "HTTP_ERROR")