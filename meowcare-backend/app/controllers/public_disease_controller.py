from app.services.public_disease_service import PublicDiseaseService


class PublicDiseaseController:

    @staticmethod
    def get_all():
        return PublicDiseaseService.get_all()

    @staticmethod
    def get_by_id(disease_id: str):
        return PublicDiseaseService.get_by_id(disease_id)