from typing import Any

from app.schemas.disease_schema import (
    DiseaseCreateRequest,
    DiseaseUpdateRequest,
)
from app.services.disease_service import DiseaseService
from app.utils.response import success_response


class DiseaseController:
    @staticmethod
    def get_all(
        *,
        search: str | None,
        is_active: bool | None,
        page: int,
        limit: int,
    ):
        result = DiseaseService.get_all(
            search=search,
            is_active=is_active,
            page=page,
            limit=limit,
        )

        return success_response(
            message="Daftar penyakit berhasil diambil",
            data=result["items"],
            meta=result["meta"],
        )

    @staticmethod
    def get_by_id(
        disease_id: str,
    ):
        result = DiseaseService.get_by_id(disease_id)

        return success_response(
            message="Detail penyakit berhasil diambil",
            data=result,
        )

    @staticmethod
    def create(
        *,
        payload: DiseaseCreateRequest,
        current_admin: dict[str, Any],
    ):
        result = DiseaseService.create(
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Penyakit berhasil ditambahkan",
            data=result,
            status_code=201,
        )

    @staticmethod
    def update(
        *,
        disease_id: str,
        payload: DiseaseUpdateRequest,
        current_admin: dict[str, Any],
    ):
        result = DiseaseService.update(
            disease_id=disease_id,
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Penyakit berhasil diperbarui",
            data=result,
        )

    @staticmethod
    def delete(
        *,
        disease_id: str,
        current_admin: dict[str, Any],
    ):
        result = DiseaseService.delete(
            disease_id=disease_id,
            current_admin=current_admin,
        )

        return success_response(
            message="Penyakit berhasil dihapus",
            data=result,
        )