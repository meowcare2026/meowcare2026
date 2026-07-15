from datetime import date
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.controllers.admin_log_controller import (
    AdminLogController,
)
from app.middleware.auth_middleware import (
    require_superadmin,
)


router = APIRouter(
    prefix="/admin/logs",
    tags=["Admin Logs"],
)


@router.get(
    "",
    summary="Get all admin activity logs",
)
def get_all_admin_logs(
    action: str | None = Query(
        default=None,
        max_length=30,
    ),
    table_name: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    admin_id: UUID | None = Query(
        default=None,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    date_from: date | None = Query(
        default=None,
        description="Tanggal awal dengan format YYYY-MM-DD",
    ),
    date_to: date | None = Query(
        default=None,
        description="Tanggal akhir dengan format YYYY-MM-DD",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    current_admin: dict[str, Any] = Depends(
        require_superadmin
    ),
):
    return AdminLogController.get_all(
        action=action,
        table_name=table_name,
        admin_id=(
            str(admin_id)
            if admin_id is not None
            else None
        ),
        search=search,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )


@router.get(
    "/{log_id}",
    summary="Get admin log by ID",
)
def get_admin_log_by_id(
    log_id: UUID,
    current_admin: dict[str, Any] = Depends(
        require_superadmin
    ),
):
    return AdminLogController.get_by_id(
        str(log_id)
    )