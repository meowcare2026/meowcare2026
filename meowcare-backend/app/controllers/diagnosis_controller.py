from app.services.diagnosis_service import DiagnosisService


class DiagnosisController:

    @staticmethod
    def create(data):
        return DiagnosisService.create(data)

    @staticmethod
    def get(diagnosis_id: str):
        return DiagnosisService.get(diagnosis_id)
    @staticmethod
    def generate_pdf(diagnosis_id):
        return DiagnosisService.generate_pdf(
        diagnosis_id)