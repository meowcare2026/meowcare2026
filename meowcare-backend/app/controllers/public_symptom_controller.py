from app.services.public_symptom_service import (
    PublicSymptomService,
)


class PublicSymptomController:

    @staticmethod
    def get_all():
        return PublicSymptomService.get_all()