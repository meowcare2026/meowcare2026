from app.repositories.symptom_repository import SymptomRepository


class PublicSymptomService:

    @staticmethod
    def get_all():
        return SymptomRepository.get_all()