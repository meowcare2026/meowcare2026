from datetime import date, datetime, time, timezone
from math import ceil
from typing import Any

from app.repositories.admin_log_repository import (
    AdminLogRepository,
)
from app.utils.exceptions import (
    BadRequestException,
    NotFoundException,
)


ALLOWED_ACTIONS = {
    "create",
    "update",
    "delete",
    "login",
    "logout",
}


class AdminLogService:
    @staticmethod
    def get_all(
        *,
        action: str | None,
        table_name: str | None,
        admin_id: str | None,
        search: str | None,
        date_from: date | None,
        date_to: date | None,
        page: int,
        limit: int,
    ) -> dict[str, Any]:
        if page < 1:
            raise BadRequestException(
                message="Page minimal bernilai 1"
            )

        if limit < 1 or limit > 100:
            raise BadRequestException(
                message="Limit harus antara 1 sampai 100"
            )

        if action and action not in ALLOWED_ACTIONS:
            raise BadRequestException(
                message=(
                    "Action harus salah satu dari: "
                    "create, update, delete, login, logout"
                )
            )

        if (
            date_from is not None
            and date_to is not None
            and date_from > date_to
        ):
            raise BadRequestException(
                message=(
                    "Tanggal awal tidak boleh "
                    "lebih besar dari tanggal akhir"
                )
            )

        start_datetime = None
        end_datetime = None

        if date_from:
            start_datetime = datetime.combine(
                date_from,
                time.min,
                tzinfo=timezone.utc,
            ).isoformat()

        if date_to:
            end_datetime = datetime.combine(
                date_to,
                time.max,
                tzinfo=timezone.utc,
            ).isoformat()

        result = AdminLogRepository.find_all(
            action=action,
            table_name=table_name,
            admin_id=admin_id,
            search=search,
            date_from=start_datetime,
            date_to=end_datetime,
            page=page,
            limit=limit,
        )

        total = result["total"]

        return {
            "items": result["data"],
            "meta": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (
                    ceil(total / limit)
                    if total > 0
                    else 0
                ),
            },
        }

    @staticmethod
    def get_by_id(
        log_id: str,
    ) -> dict[str, Any]:
        log = AdminLogRepository.find_by_id(
            log_id
        )

        if log is None:
            raise NotFoundException(
                message="Admin log tidak ditemukan"
            )

        return log