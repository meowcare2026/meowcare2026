import logging
from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


logger = logging.getLogger(__name__)


class AdminRepository:
    @staticmethod
    def find_by_id(admin_id: str) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("admin_profiles")
                .select(
                    "id, name, role, is_active, created_at, updated_at"
                )
                .eq("id", admin_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil profil admin",
                details=str(error),
            ) from error

    @staticmethod
    def create_profile(
        *,
        admin_id: str,
        name: str,
        role: str = "admin",
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("admin_profiles")
                .insert(
                    {
                        "id": admin_id,
                        "name": name.strip(),
                        "role": role,
                        "is_active": True,
                    }
                )
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Profil admin gagal dibuat"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal membuat profil admin",
                details=str(error),
            ) from error

    @staticmethod
    def create_log(
        *,
        admin_id: str,
        action: str,
        description: str,
        table_name: str = "admin_profiles",
        record_id: str | None = None,
    ) -> None:
        try:
            (
                supabase_admin
                .table("admin_logs")
                .insert(
                    {
                        "admin_id": admin_id,
                        "action": action,
                        "table_name": table_name,
                        "record_id": record_id,
                        "description": description,
                    }
                )
                .execute()
            )

        except Exception as error:
            logger.warning(
                "Gagal menyimpan admin log: %s",
                error,
            )