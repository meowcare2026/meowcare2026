from datetime import date

from app.services.admin_log_service import (
    AdminLogService,
)
from app.utils.response import success_response


class AdminLogController:
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
    ):
        result = AdminLogService.get_all(
            action=action,
            table_name=table_name,
            admin_id=admin_id,
            search=search,
            date_from=date_from,
            date_to=date_to,
            page=page,
            limit=limit,
        )

        return success_response(
            message="Admin logs berhasil diambil",
            data=result["items"],
            meta=result["meta"],
        )

    @staticmethod
    def get_by_id(
        log_id: str,
    ):
        result = AdminLogService.get_by_id(
            log_id
        )

        return success_response(
            message="Detail admin log berhasil diambil",
            data=result,
        )