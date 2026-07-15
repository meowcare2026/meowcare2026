from app.repositories.diagnosis_repository import DiagnosisRepository
from app.repositories.disease_repository import DiseaseRepository
from app.repositories.rule_repository import RuleRepository
from app.repositories.symptom_repository import SymptomRepository
from app.services.certainty_factor_service import CertaintyFactorService
from app.services.pdf_service import PdfService


class DiagnosisService:

    @staticmethod
    def create(data):

        # Ambil data master
        diseases = DiseaseRepository.get_all()
        rules = RuleRepository.get_all()

        # Hitung Certainty Factor
        results = CertaintyFactorService.calculate(
            data["symptoms"],
            rules,
            diseases
        )

        if not results:
            return {
                "message": "Tidak ditemukan hasil diagnosis."
            }

        # Ambil hasil tertinggi
        best_result = results[0]

        # Simpan diagnosis utama
        diagnosis = DiagnosisRepository.create_diagnosis({
            "owner_name": data["owner_name"],
            "cat_name": data["cat_name"],
            "cat_age": data["cat_age"],
            "cat_gender": data["cat_gender"],
            "main_disease_id": best_result["id"],
            "highest_percentage": best_result["percentage"],
            "urgency_level": best_result["urgency_level"],
            "recommendation": best_result["solution"]
        })

        # Simpan gejala yang dipilih user
        details = []

        for symptom in data["symptoms"]:

            symptom_data = SymptomRepository.get_by_id(
                symptom["symptom_id"]
            )

            details.append({
                "diagnosis_id": diagnosis["id"],
                "symptom_id": symptom["symptom_id"],
                "cf_user": symptom["cf_user"],
                "symptom_name_snapshot": symptom_data["name"]
            })

        DiagnosisRepository.save_diagnosis_details(details)

        # Simpan seluruh hasil perhitungan
        diagnosis_results = []

        for index, result in enumerate(results, start=1):

            diagnosis_results.append({
                "diagnosis_id": diagnosis["id"],
                "disease_id": result["id"],
                "cf_value": result["cf_value"],
                "percentage": result["percentage"],
                "rank": index
            })

        DiagnosisRepository.save_diagnosis_results(
            diagnosis_results
        )

        # Return hasil lengkap
        return {
            "diagnosis": diagnosis,
            "results": results
        }

    @staticmethod
    def get(diagnosis_id: str):

        diagnosis = DiagnosisRepository.get_diagnosis(
            diagnosis_id
        )

        if not diagnosis:
            return None

        details = DiagnosisRepository.get_details(
            diagnosis_id
        )

        results = DiagnosisRepository.get_results(
            diagnosis_id
        )

        return {
            "diagnosis": diagnosis,
            "details": details,
            "results": results
        }
    
    @staticmethod
    def generate_pdf(diagnosis_id):

        diagnosis = DiagnosisRepository.get_by_id(
            diagnosis_id
        )

        if diagnosis is None:
            raise NotFoundException(
                "Diagnosis tidak ditemukan"
            )

        return PdfService.generate(diagnosis)