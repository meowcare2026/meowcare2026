from fastapi import APIRouter
from app.controllers.diagnosis_controller import DiagnosisController
from app.schemas.diagnosis_schema import DiagnosisCreate
from app.services.diagnosis_service import DiagnosisService
from fastapi.responses import StreamingResponse


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

@router.get("/{diagnosis_id}/pdf")
def export_pdf(diagnosis_id: str):

    pdf = DiagnosisService.generate_pdf(
        diagnosis_id
    )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f"attachment; filename=diagnosis-{diagnosis_id}.pdf"
        }
    )