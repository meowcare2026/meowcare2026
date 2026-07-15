from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.controllers.disease_controller import (
    DiseaseController,
)
from app.middleware.auth_middleware import require_admin
from app.schemas.disease_schema import (
    DiseaseCreateRequest,
    DiseaseUpdateRequest,
)


router = APIRouter(
    prefix="/admin/diseases",
    tags=["Admin Diseases"],
)


@router.get(
    "",
    summary="Get all diseases",
)
def get_all_diseases(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    is_active: bool | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return DiseaseController.get_all(
        search=search,
        is_active=is_active,
        page=page,
        limit=limit,
    )


@router.post(
    "",
    summary="Create disease",
    status_code=status.HTTP_201_CREATED,
)
def create_disease(
    payload: DiseaseCreateRequest,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return DiseaseController.create(
        payload=payload,
        current_admin=current_admin,
    )


@router.get(
    "/{disease_id}",
    summary="Get disease by ID",
)
def get_disease_by_id(
    disease_id: UUID,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return DiseaseController.get_by_id(
        str(disease_id)
    )


@router.put(
    "/{disease_id}",
    summary="Update disease",
)
def update_disease(
    disease_id: UUID,
    payload: DiseaseUpdateRequest,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return DiseaseController.update(
        disease_id=str(disease_id),
        payload=payload,
        current_admin=current_admin,
    )


@router.delete(
    "/{disease_id}",
    summary="Delete disease",
)
def delete_disease(
    disease_id: UUID,
    current_admin: dict[str, Any] = Depends(require_admin),
):
    return DiseaseController.delete(
        disease_id=str(disease_id),
        current_admin=current_admin,
    )