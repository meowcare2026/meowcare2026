from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.controllers.rule_controller import (
    RuleController,
)
from app.middleware.auth_middleware import (
    require_admin,
    require_expert,
)
from app.schemas.rule_schema import (
    RuleCreateRequest,
    RuleUpdateRequest,
)


router = APIRouter(
    prefix="/admin/rules",
    tags=["Admin Rules"],
)


@router.get(
    "",
    summary="Get all rules",
)
def get_all_rules(
    disease_id: UUID | None = Query(default=None),
    symptom_id: UUID | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    current_admin: dict[str, Any] = Depends(
        require_admin
    ),
):
    return RuleController.get_all(
        disease_id=(
            str(disease_id)
            if disease_id is not None
            else None
        ),
        symptom_id=(
            str(symptom_id)
            if symptom_id is not None
            else None
        ),
        is_active=is_active,
        search=search,
        page=page,
        limit=limit,
    )


@router.post(
    "",
    summary="Create rule and CF expert",
    status_code=status.HTTP_201_CREATED,
)
def create_rule(
    payload: RuleCreateRequest,
    current_admin: dict[str, Any] = Depends(
        require_expert
    ),
):
    return RuleController.create(
        payload=payload,
        current_admin=current_admin,
    )


@router.get(
    "/{rule_id}",
    summary="Get rule by ID",
)
def get_rule_by_id(
    rule_id: UUID,
    current_admin: dict[str, Any] = Depends(
        require_admin
    ),
):
    return RuleController.get_by_id(
        str(rule_id)
    )


@router.put(
    "/{rule_id}",
    summary="Update rule and CF expert",
)
def update_rule(
    rule_id: UUID,
    payload: RuleUpdateRequest,
    current_admin: dict[str, Any] = Depends(
        require_expert
    ),
):
    return RuleController.update(
        rule_id=str(rule_id),
        payload=payload,
        current_admin=current_admin,
    )


@router.delete(
    "/{rule_id}",
    summary="Delete rule",
)
def delete_rule(
    rule_id: UUID,
    current_admin: dict[str, Any] = Depends(
        require_expert
    ),
):
    return RuleController.delete(
        rule_id=str(rule_id),
        current_admin=current_admin,
    )