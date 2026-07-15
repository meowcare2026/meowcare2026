from typing import Any

from app.schemas.symptom_schema import (
    SymptomCreateRequest,
    SymptomUpdateRequest,
)
from app.services.symptom_service import SymptomService
from app.utils.response import success_response


class SymptomController:
    @staticmethod
    def get_all(
        *,
        search: str | None,
        category: str | None,
        is_active: bool | None,
        page: int,
        limit: int,
    ):
        result = SymptomService.get_all(
            search=search,
            category=category,
            is_active=is_active,
            page=page,
            limit=limit,
        )

        return success_response(
            message="Daftar gejala berhasil diambil",
            data=result["items"],
            meta=result["meta"],
        )

    @staticmethod
    def get_by_id(
        symptom_id: str,
    ):
        result = SymptomService.get_by_id(
            symptom_id
        )

        return success_response(
            message="Detail gejala berhasil diambil",
            data=result,
        )

    @staticmethod
    def create(
        *,
        payload: SymptomCreateRequest,
        current_admin: dict[str, Any],
    ):
        result = SymptomService.create(
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Gejala berhasil ditambahkan",
            data=result,
            status_code=201,
        )

    @staticmethod
    def update(
        *,
        symptom_id: str,
        payload: SymptomUpdateRequest,
        current_admin: dict[str, Any],
    ):
        result = SymptomService.update(
            symptom_id=symptom_id,
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Gejala berhasil diperbarui",
            data=result,
        )

    @staticmethod
    def delete(
        *,
        symptom_id: str,
        current_admin: dict[str, Any],
    ):
        result = SymptomService.delete(
            symptom_id=symptom_id,
            current_admin=current_admin,
        )

        return success_response(
            message="Gejala berhasil dihapus",
            data=result,
        )