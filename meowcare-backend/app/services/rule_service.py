from math import ceil
from typing import Any

from app.repositories.admin_repository import (
    AdminRepository,
)
from app.repositories.disease_repository import (
    DiseaseRepository,
)
from app.repositories.rule_repository import (
    RuleRepository,
)
from app.repositories.symptom_repository import (
    SymptomRepository,
)
from app.schemas.rule_schema import (
    RuleCreateRequest,
    RuleUpdateRequest,
)
from app.utils.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class RuleService:
    @staticmethod
    def get_all(
        *,
        disease_id: str | None,
        symptom_id: str | None,
        is_active: bool | None,
        search: str | None,
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

        result = RuleRepository.find_all(
            disease_id=disease_id,
            symptom_id=symptom_id,
            is_active=is_active,
            search=search,
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
        rule_id: str,
    ) -> dict[str, Any]:
        rule = RuleRepository.find_by_id(
            rule_id
        )

        if rule is None:
            raise NotFoundException(
                message="Rule tidak ditemukan"
            )

        return rule

    @staticmethod
    def create(
        *,
        payload: RuleCreateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        disease = DiseaseRepository.find_by_id(
            payload.disease_id
        )

        if disease is None:
            raise NotFoundException(
                message="Penyakit tidak ditemukan"
            )

        symptom = SymptomRepository.find_by_id(
            payload.symptom_id
        )

        if symptom is None:
            raise NotFoundException(
                message="Gejala tidak ditemukan"
            )

        if not disease.get("is_active", False):
            raise BadRequestException(
                message=(
                    "Rule tidak dapat dibuat karena penyakit "
                    "sedang nonaktif"
                )
            )

        if not symptom.get("is_active", False):
            raise BadRequestException(
                message=(
                    "Rule tidak dapat dibuat karena gejala "
                    "sedang nonaktif"
                )
            )

        existing_rule = RuleRepository.find_by_relation(
            disease_id=payload.disease_id,
            symptom_id=payload.symptom_id,
        )

        if existing_rule is not None:
            raise ConflictException(
                message=(
                    "Relasi penyakit dan gejala tersebut "
                    "sudah memiliki rule"
                )
            )

        rule = RuleRepository.create(
            payload.model_dump()
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="create",
            table_name="rules",
            record_id=rule["id"],
            description=(
                f"Membuat rule {disease['code']} "
                f"→ {symptom['code']} "
                f"dengan CF Pakar {payload.cf_expert}"
            ),
        )

        return rule

    @staticmethod
    def update(
        *,
        rule_id: str,
        payload: RuleUpdateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_rule = RuleRepository.find_by_id(
            rule_id
        )

        if existing_rule is None:
            raise NotFoundException(
                message="Rule tidak ditemukan"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise BadRequestException(
                message="Tidak ada data yang diperbarui"
            )

        final_disease_id = update_data.get(
            "disease_id",
            existing_rule["disease_id"],
        )

        final_symptom_id = update_data.get(
            "symptom_id",
            existing_rule["symptom_id"],
        )

        disease = DiseaseRepository.find_by_id(
            final_disease_id
        )

        if disease is None:
            raise NotFoundException(
                message="Penyakit tidak ditemukan"
            )

        symptom = SymptomRepository.find_by_id(
            final_symptom_id
        )

        if symptom is None:
            raise NotFoundException(
                message="Gejala tidak ditemukan"
            )

        relation_changed = (
            final_disease_id
            != existing_rule["disease_id"]
            or final_symptom_id
            != existing_rule["symptom_id"]
        )

        if relation_changed:
            duplicated_rule = (
                RuleRepository.find_by_relation(
                    disease_id=final_disease_id,
                    symptom_id=final_symptom_id,
                )
            )

            if (
                duplicated_rule is not None
                and duplicated_rule["id"] != rule_id
            ):
                raise ConflictException(
                    message=(
                        "Relasi penyakit dan gejala tersebut "
                        "sudah memiliki rule"
                    )
                )

        if (
            "is_active" not in update_data
            or update_data["is_active"] is True
        ):
            if not disease.get("is_active", False):
                raise BadRequestException(
                    message=(
                        "Rule aktif tidak boleh memakai "
                        "penyakit nonaktif"
                    )
                )

            if not symptom.get("is_active", False):
                raise BadRequestException(
                    message=(
                        "Rule aktif tidak boleh memakai "
                        "gejala nonaktif"
                    )
                )

        rule = RuleRepository.update(
            rule_id=rule_id,
            data=update_data,
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="update",
            table_name="rules",
            record_id=rule["id"],
            description=(
                f"Memperbarui rule "
                f"{disease['code']} → {symptom['code']}"
            ),
        )

        return rule

    @staticmethod
    def delete(
        *,
        rule_id: str,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_rule = RuleRepository.find_by_id(
            rule_id
        )

        if existing_rule is None:
            raise NotFoundException(
                message="Rule tidak ditemukan"
            )

        rule = RuleRepository.delete(
            rule_id
        )

        disease = rule.get("disease") or {}
        symptom = rule.get("symptom") or {}

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="delete",
            table_name="rules",
            record_id=rule["id"],
            description=(
                f"Menghapus rule "
                f"{disease.get('code', rule['disease_id'])} "
                f"→ "
                f"{symptom.get('code', rule['symptom_id'])}"
            ),
        )

        return rule