from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


SYMPTOM_COLUMNS = (
    "id, code, name, category, is_active, "
    "created_at, updated_at"
)


class SymptomRepository:
    @staticmethod
    def find_all(
        *,
        search: str | None = None,
        category: str | None = None,
        is_active: bool | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any]:
        try:
            offset = (page - 1) * limit
            end = offset + limit - 1

            query = (
                supabase_admin
                .table("symptoms")
                .select(SYMPTOM_COLUMNS, count="exact")
            )

            if search:
                clean_search = search.strip()

                query = query.or_(
                    f"code.ilike.%{clean_search}%,"
                    f"name.ilike.%{clean_search}%"
                )

            if category:
                query = query.ilike(
                    "category",
                    category.strip(),
                )

            if is_active is not None:
                query = query.eq(
                    "is_active",
                    is_active,
                )

            response = (
                query
                .order("code")
                .range(offset, end)
                .execute()
            )

            return {
                "data": response.data or [],
                "total": response.count or 0,
            }

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil daftar gejala",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_id(
        symptom_id: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .select(SYMPTOM_COLUMNS)
                .eq("id", symptom_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil data gejala",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_code(
        code: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .select("id, code")
                .eq("code", code)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal memeriksa kode gejala",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_name(
        name: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .select("id, name")
                .ilike("name", name)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal memeriksa nama gejala",
                details=str(error),
            ) from error

    @staticmethod
    def create(
        data: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .insert(data)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data gejala gagal dibuat"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal membuat data gejala",
                details=str(error),
            ) from error

    @staticmethod
    def update(
        symptom_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .update(data)
                .eq("id", symptom_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data gejala gagal diperbarui"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal memperbarui data gejala",
                details=str(error),
            ) from error

    @staticmethod
    def delete(
        symptom_id: str,
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("symptoms")
                .delete()
                .eq("id", symptom_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data gejala gagal dihapus"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal menghapus data gejala",
                details=str(error),
            ) from error