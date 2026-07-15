from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


DISEASE_COLUMNS = (
    "id, code, name, description, solution, prevention, "
    "severity_level, expert_source, is_active, "
    "created_at, updated_at"
)


class DiseaseRepository:

    # ===========================
    # BACKEND 2 (Public API)
    # ===========================

    @staticmethod
    def get_all():
        response = (
            supabase_admin
            .table("diseases")
            .select("*")
            .eq("is_active", True)
            .order("code")
            .execute()
        )

        return response.data

    @staticmethod
    def get_by_id(disease_id):
        response = (
            supabase_admin
            .table("diseases")
            .select("*")
            .eq("id", disease_id)
            .single()
            .execute()
        )

        return response.data

    # ===========================
    # BACKEND 1 (Admin CRUD)
    # ===========================

    @staticmethod
    def find_all(
        *,
        search: str | None = None,
        is_active: bool | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any]:

        try:
            offset = (page - 1) * limit
            end = offset + limit - 1

            query = (
                supabase_admin
                .table("diseases")
                .select(DISEASE_COLUMNS, count="exact")
            )

            if search:
                clean_search = search.strip()

                query = query.or_(
                    f"code.ilike.%{clean_search}%,"
                    f"name.ilike.%{clean_search}%"
                )

            if is_active is not None:
                query = query.eq("is_active", is_active)

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
                message="Gagal mengambil daftar penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_id(disease_id: str):

        try:
            response = (
                supabase_admin
                .table("diseases")
                .select(DISEASE_COLUMNS)
                .eq("id", disease_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil data penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_code(code: str):

        try:
            response = (
                supabase_admin
                .table("diseases")
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
                message="Gagal memeriksa kode penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_name(name: str):

        try:
            response = (
                supabase_admin
                .table("diseases")
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
                message="Gagal memeriksa nama penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def create(data):

        try:
            response = (
                supabase_admin
                .table("diseases")
                .insert(data)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data penyakit gagal dibuat"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal membuat data penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def update(disease_id: str, data):

        try:
            response = (
                supabase_admin
                .table("diseases")
                .update(data)
                .eq("id", disease_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data penyakit gagal diperbarui"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal memperbarui data penyakit",
                details=str(error),
            ) from error

    @staticmethod
    def delete(disease_id: str):

        try:
            response = (
                supabase_admin
                .table("diseases")
                .delete()
                .eq("id", disease_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Data penyakit gagal dihapus"
                )

            return response.data[0]

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal menghapus data penyakit",
                details=str(error),
            ) from error