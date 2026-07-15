from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


class DashboardRepository:
    @staticmethod
    def count_all(table_name: str) -> int:
        try:
            response = (
                supabase_admin
                .table(table_name)
                .select("id", count="exact")
                .limit(1)
                .execute()
            )

            return response.count or 0

        except Exception as error:
            raise DatabaseException(
                message=f"Gagal menghitung data {table_name}",
                details=str(error),
            ) from error

    @staticmethod
    def count_active(table_name: str) -> int:
        try:
            response = (
                supabase_admin
                .table(table_name)
                .select("id", count="exact")
                .eq("is_active", True)
                .limit(1)
                .execute()
            )

            return response.count or 0

        except Exception as error:
            raise DatabaseException(
                message=f"Gagal menghitung data aktif {table_name}",
                details=str(error),
            ) from error

    @staticmethod
    def get_recent_diagnoses(
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        try:
            response = (
                supabase_admin
                .table("diagnoses")
                .select(
                    """
                    id,
                    owner_name,
                    cat_name,
                    highest_percentage,
                    urgency_level,
                    created_at,
                    main_disease:diseases(
                        id,
                        code,
                        name
                    )
                    """
                )
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            return response.data or []

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil diagnosis terbaru",
                details=str(error),
            ) from error