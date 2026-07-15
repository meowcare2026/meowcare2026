from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.controllers.symptom_controller import (
    SymptomController,
)
from app.middleware.auth_middleware import require_admin
from app.schemas.symptom_schema import (
    SymptomCreateRequest,
    SymptomUpdateRequest,
)


router = APIRouter(
    prefix="/admin/symptoms",
    tags=["Admin Symptoms"],
)


@router.get(
    "",
    summary="Get all symptoms",
)
def get_all_symptoms(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    category: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
    ),
    is_active: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return SymptomController.get_all(
        search=search,
        category=category,
        is_active=is_active,
        page=page,
        limit=limit,
    )


@router.post(
    "",
    summary="Create symptom",
    status_code=status.HTTP_201_CREATED,
)
def create_symptom(
    payload: SymptomCreateRequest,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return SymptomController.create(
        payload=payload,
        current_admin=current_admin,
    )


@router.get(
    "/{symptom_id}",
    summary="Get symptom by ID",
)
def get_symptom_by_id(
    symptom_id: UUID,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return SymptomController.get_by_id(
        str(symptom_id)
    )


@router.put(
    "/{symptom_id}",
    summary="Update symptom",
)
def update_symptom(
    symptom_id: UUID,
    payload: SymptomUpdateRequest,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return SymptomController.update(
        symptom_id=str(symptom_id),
        payload=payload,
        current_admin=current_admin,
    )


@router.delete(
    "/{symptom_id}",
    summary="Delete symptom",
)
def delete_symptom(
    symptom_id: UUID,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return SymptomController.delete(
        symptom_id=str(symptom_id),
        current_admin=current_admin,
    )