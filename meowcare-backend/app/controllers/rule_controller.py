from typing import Any

from app.schemas.rule_schema import (
    RuleCreateRequest,
    RuleUpdateRequest,
)
from app.services.rule_service import RuleService
from app.utils.response import success_response


class RuleController:
    @staticmethod
    def get_all(
        *,
        disease_id: str | None,
        symptom_id: str | None,
        is_active: bool | None,
        search: str | None,
        page: int,
        limit: int,
    ):
        result = RuleService.get_all(
            disease_id=disease_id,
            symptom_id=symptom_id,
            is_active=is_active,
            search=search,
            page=page,
            limit=limit,
        )

        return success_response(
            message="Daftar rule berhasil diambil",
            data=result["items"],
            meta=result["meta"],
        )

    @staticmethod
    def get_by_id(
        rule_id: str,
    ):
        result = RuleService.get_by_id(
            rule_id
        )

        return success_response(
            message="Detail rule berhasil diambil",
            data=result,
        )

    @staticmethod
    def create(
        *,
        payload: RuleCreateRequest,
        current_admin: dict[str, Any],
    ):
        result = RuleService.create(
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Rule berhasil ditambahkan",
            data=result,
            status_code=201,
        )

    @staticmethod
    def update(
        *,
        rule_id: str,
        payload: RuleUpdateRequest,
        current_admin: dict[str, Any],
    ):
        result = RuleService.update(
            rule_id=rule_id,
            payload=payload,
            current_admin=current_admin,
        )

        return success_response(
            message="Rule berhasil diperbarui",
            data=result,
        )

    @staticmethod
    def delete(
        *,
        rule_id: str,
        current_admin: dict[str, Any],
    ):
        result = RuleService.delete(
            rule_id=rule_id,
            current_admin=current_admin,
        )

        return success_response(
            message="Rule berhasil dihapus",
            data=result,
        )