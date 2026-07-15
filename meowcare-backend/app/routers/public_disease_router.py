from fastapi import APIRouter

from app.controllers.public_disease_controller import (
    PublicDiseaseController,
)

router = APIRouter(
    prefix="/diseases",
    tags=["Public Diseases"],
)


@router.get("")
def get_all_diseases():
    return PublicDiseaseController.get_all()


@router.get("/{disease_id}")
def get_disease(disease_id: str):
    return PublicDiseaseController.get_by_id(disease_id)