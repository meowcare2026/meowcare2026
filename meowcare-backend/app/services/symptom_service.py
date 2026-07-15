from math import ceil
from typing import Any

from app.repositories.admin_repository import AdminRepository
from app.repositories.symptom_repository import SymptomRepository
from app.schemas.symptom_schema import (
    SymptomCreateRequest,
    SymptomUpdateRequest,
)
from app.utils.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class SymptomService:
    @staticmethod
    def get_all(
        *,
        search: str | None,
        category: str | None,
        is_active: bool | None,
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

        result = SymptomRepository.find_all(
            search=search,
            category=category,
            is_active=is_active,
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
        symptom_id: str,
    ) -> dict[str, Any]:
        symptom = SymptomRepository.find_by_id(
            symptom_id
        )

        if symptom is None:
            raise NotFoundException(
                message="Gejala tidak ditemukan"
            )

        return symptom

    @staticmethod
    def create(
        *,
        payload: SymptomCreateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_code = SymptomRepository.find_by_code(
            payload.code
        )

        if existing_code is not None:
            raise ConflictException(
                message="Kode gejala sudah digunakan"
            )

        existing_name = SymptomRepository.find_by_name(
            payload.name
        )

        if existing_name is not None:
            raise ConflictException(
                message="Nama gejala sudah digunakan"
            )

        symptom = SymptomRepository.create(
            payload.model_dump()
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="create",
            table_name="symptoms",
            record_id=symptom["id"],
            description=(
                f"Membuat gejala {symptom['code']} "
                f"- {symptom['name']}"
            ),
        )

        return symptom

    @staticmethod
    def update(
        *,
        symptom_id: str,
        payload: SymptomUpdateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_symptom = SymptomRepository.find_by_id(
            symptom_id
        )

        if existing_symptom is None:
            raise NotFoundException(
                message="Gejala tidak ditemukan"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        if not update_data:
            raise BadRequestException(
                message="Tidak ada data yang diperbarui"
            )

        new_code = update_data.get("code")

        if new_code:
            existing_code = SymptomRepository.find_by_code(
                new_code
            )

            if (
                existing_code is not None
                and existing_code["id"] != symptom_id
            ):
                raise ConflictException(
                    message="Kode gejala sudah digunakan"
                )

        new_name = update_data.get("name")

        if new_name:
            existing_name = SymptomRepository.find_by_name(
                new_name
            )

            if (
                existing_name is not None
                and existing_name["id"] != symptom_id
            ):
                raise ConflictException(
                    message="Nama gejala sudah digunakan"
                )

        symptom = SymptomRepository.update(
            symptom_id,
            update_data,
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="update",
            table_name="symptoms",
            record_id=symptom["id"],
            description=(
                f"Memperbarui gejala {symptom['code']} "
                f"- {symptom['name']}"
            ),
        )

        return symptom

    @staticmethod
    def delete(
        *,
        symptom_id: str,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_symptom = SymptomRepository.find_by_id(
            symptom_id
        )

        if existing_symptom is None:
            raise NotFoundException(
                message="Gejala tidak ditemukan"
            )

        symptom = SymptomRepository.delete(
            symptom_id
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="delete",
            table_name="symptoms",
            record_id=symptom["id"],
            description=(
                f"Menghapus gejala {symptom['code']} "
                f"- {symptom['name']}"
            ),
        )

        return symptom