from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


ADMIN_LOG_COLUMNS = """
id,
admin_id,
action,
table_name,
record_id,
description,
old_data,
new_data,
created_at,
admin:admin_profiles(
    id,
    name,
    role
)
"""


class AdminLogRepository:
    @staticmethod
    def find_all(
        *,
        action: str | None = None,
        table_name: str | None = None,
        admin_id: str | None = None,
        search: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any]:
        try:
            offset = (page - 1) * limit
            end = offset + limit - 1

            query = (
                supabase_admin
                .table("admin_logs")
                .select(
                    ADMIN_LOG_COLUMNS,
                    count="exact",
                )
            )

            if action:
                query = query.eq("action", action)

            if table_name:
                query = query.eq(
                    "table_name",
                    table_name,
                )

            if admin_id:
                query = query.eq(
                    "admin_id",
                    admin_id,
                )

            if search:
                clean_search = search.strip()

                query = query.ilike(
                    "description",
                    f"%{clean_search}%",
                )

            if date_from:
                query = query.gte(
                    "created_at",
                    date_from,
                )

            if date_to:
                query = query.lte(
                    "created_at",
                    date_to,
                )

            response = (
                query
                .order("created_at", desc=True)
                .range(offset, end)
                .execute()
            )

            return {
                "data": response.data or [],
                "total": response.count or 0,
            }

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil admin logs",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_id(
        log_id: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("admin_logs")
                .select(ADMIN_LOG_COLUMNS)
                .eq("id", log_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil detail admin log",
                details=str(error),
            ) from error