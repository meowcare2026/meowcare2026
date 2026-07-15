from fastapi import APIRouter

from app.controllers.public_symptom_controller import (
    PublicSymptomController,
)

router = APIRouter(
    prefix="/symptoms",
    tags=["Public Symptoms"],
)


@router.get("")
def get_all_symptoms():
    return PublicSymptomController.get_all()