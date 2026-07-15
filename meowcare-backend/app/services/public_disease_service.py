from app.repositories.disease_repository import DiseaseRepository


class PublicDiseaseService:

    @staticmethod
    def get_all():
        return DiseaseRepository.get_all()

    @staticmethod
    def get_by_id(disease_id: str):
        return DiseaseRepository.get_by_id(disease_id)