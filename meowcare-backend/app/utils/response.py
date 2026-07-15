from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    *,
    message: str,
    data: Any = None,
    status_code: int = 200,
    meta: dict[str, Any] | None = None,
) -> JSONResponse:
    content = {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta,
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
    )


def error_response(
    *,
    message: str,
    code: str,
    status_code: int,
    details: Any = None,
    headers: dict[str, str] | None = None,
) -> JSONResponse:
    content = {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details,
        },
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
        headers=headers,
    )