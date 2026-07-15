from math import ceil
from typing import Any

from app.repositories.admin_repository import AdminRepository
from app.repositories.disease_repository import DiseaseRepository
from app.schemas.disease_schema import (
    DiseaseCreateRequest,
    DiseaseUpdateRequest,
)
from app.utils.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class DiseaseService:
    @staticmethod
    def get_all(
        *,
        search: str | None,
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

        result = DiseaseRepository.find_all(
            search=search,
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
        disease_id: str,
    ) -> dict[str, Any]:
        disease = DiseaseRepository.find_by_id(disease_id)

        if disease is None:
            raise NotFoundException(
                message="Penyakit tidak ditemukan"
            )

        return disease

    @staticmethod
    def create(
        *,
        payload: DiseaseCreateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_code = DiseaseRepository.find_by_code(
            payload.code
        )

        if existing_code is not None:
            raise ConflictException(
                message="Kode penyakit sudah digunakan"
            )

        existing_name = DiseaseRepository.find_by_name(
            payload.name
        )

        if existing_name is not None:
            raise ConflictException(
                message="Nama penyakit sudah digunakan"
            )

        disease = DiseaseRepository.create(
            payload.model_dump()
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="create",
            table_name="diseases",
            record_id=disease["id"],
            description=(
                f"Membuat penyakit {disease['code']} "
                f"- {disease['name']}"
            ),
        )

        return disease

    @staticmethod
    def update(
        *,
        disease_id: str,
        payload: DiseaseUpdateRequest,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_disease = DiseaseRepository.find_by_id(
            disease_id
        )

        if existing_disease is None:
            raise NotFoundException(
                message="Penyakit tidak ditemukan"
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
            existing_code = DiseaseRepository.find_by_code(
                new_code
            )

            if (
                existing_code is not None
                and existing_code["id"] != disease_id
            ):
                raise ConflictException(
                    message="Kode penyakit sudah digunakan"
                )

        new_name = update_data.get("name")

        if new_name:
            existing_name = DiseaseRepository.find_by_name(
                new_name
            )

            if (
                existing_name is not None
                and existing_name["id"] != disease_id
            ):
                raise ConflictException(
                    message="Nama penyakit sudah digunakan"
                )

        disease = DiseaseRepository.update(
            disease_id,
            update_data,
        )

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="update",
            table_name="diseases",
            record_id=disease["id"],
            description=(
                f"Memperbarui penyakit {disease['code']} "
                f"- {disease['name']}"
            ),
        )

        return disease

    @staticmethod
    def delete(
        *,
        disease_id: str,
        current_admin: dict[str, Any],
    ) -> dict[str, Any]:
        existing_disease = DiseaseRepository.find_by_id(
            disease_id
        )

        if existing_disease is None:
            raise NotFoundException(
                message="Penyakit tidak ditemukan"
            )

        disease = DiseaseRepository.delete(disease_id)

        AdminRepository.create_log(
            admin_id=current_admin["id"],
            action="delete",
            table_name="diseases",
            record_id=disease["id"],
            description=(
                f"Menghapus penyakit {disease['code']} "
                f"- {disease['name']}"
            ),
        )

        return disease