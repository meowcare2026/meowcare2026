from typing import Any

from app.config.supabase import supabase_admin
from app.utils.exceptions import DatabaseException


RULE_COLUMNS = """
id,
disease_id,
symptom_id,
cf_expert,
notes,
source_reference,
is_active,
created_at,
updated_at,
disease:diseases(
    id,
    code,
    name,
    severity_level,
    is_active
),
symptom:symptoms(
    id,
    code,
    name,
    category,
    is_active
)
"""


class RuleRepository:
    @staticmethod
    def find_all(
        *,
        disease_id: str | None = None,
        symptom_id: str | None = None,
        is_active: bool | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
    ) -> dict[str, Any]:
        try:
            offset = (page - 1) * limit
            end = offset + limit - 1

            query = (
                supabase_admin
                .table("rules")
                .select(RULE_COLUMNS, count="exact")
            )

            if disease_id:
                query = query.eq(
                    "disease_id",
                    disease_id,
                )

            if symptom_id:
                query = query.eq(
                    "symptom_id",
                    symptom_id,
                )

            if is_active is not None:
                query = query.eq(
                    "is_active",
                    is_active,
                )

            if search:
                clean_search = search.strip()

                query = query.or_(
                    (
                        f"disease.name.ilike.%{clean_search}%,"
                        f"disease.code.ilike.%{clean_search}%,"
                        f"symptom.name.ilike.%{clean_search}%,"
                        f"symptom.code.ilike.%{clean_search}%"
                    )
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
                message="Gagal mengambil daftar rule",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_id(
        rule_id: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("rules")
                .select(RULE_COLUMNS)
                .eq("id", rule_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal mengambil detail rule",
                details=str(error),
            ) from error

    @staticmethod
    def find_by_relation(
        *,
        disease_id: str,
        symptom_id: str,
    ) -> dict[str, Any] | None:
        try:
            response = (
                supabase_admin
                .table("rules")
                .select(
                    "id, disease_id, symptom_id"
                )
                .eq("disease_id", disease_id)
                .eq("symptom_id", symptom_id)
                .limit(1)
                .execute()
            )

            if not response.data:
                return None

            return response.data[0]

        except Exception as error:
            raise DatabaseException(
                message="Gagal memeriksa relasi rule",
                details=str(error),
            ) from error

    @staticmethod
    def create(
        data: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("rules")
                .insert(data)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Rule gagal dibuat"
                )

            rule_id = response.data[0]["id"]

            created_rule = RuleRepository.find_by_id(
                rule_id
            )

            if created_rule is None:
                raise DatabaseException(
                    message="Rule dibuat tetapi gagal dibaca kembali"
                )

            return created_rule

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal membuat rule",
                details=str(error),
            ) from error

    @staticmethod
    def update(
        *,
        rule_id: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            response = (
                supabase_admin
                .table("rules")
                .update(data)
                .eq("id", rule_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Rule gagal diperbarui"
                )

            updated_rule = RuleRepository.find_by_id(
                rule_id
            )

            if updated_rule is None:
                raise DatabaseException(
                    message=(
                        "Rule diperbarui tetapi gagal dibaca kembali"
                    )
                )

            return updated_rule

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal memperbarui rule",
                details=str(error),
            ) from error

    @staticmethod
    def delete(
        rule_id: str,
    ) -> dict[str, Any]:
        existing_rule = RuleRepository.find_by_id(
            rule_id
        )

        if existing_rule is None:
            raise DatabaseException(
                message="Rule tidak ditemukan"
            )

        try:
            response = (
                supabase_admin
                .table("rules")
                .delete()
                .eq("id", rule_id)
                .execute()
            )

            if not response.data:
                raise DatabaseException(
                    message="Rule gagal dihapus"
                )

            return existing_rule

        except DatabaseException:
            raise

        except Exception as error:
            raise DatabaseException(
                message="Gagal menghapus rule",
                details=str(error),
            ) from error