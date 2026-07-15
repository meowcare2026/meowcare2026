from fastapi import APIRouter
from app.controllers.diagnosis_controller import DiagnosisController
from app.schemas.diagnosis_schema import DiagnosisCreate

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnosis"]
)


@router.post("/")
def create_diagnosis(data: DiagnosisCreate):
    return DiagnosisController.create(data.dict())


@router.get("/{diagnosis_id}")
def get_diagnosis(diagnosis_id: str):
    return DiagnosisController.get(diagnosis_id)