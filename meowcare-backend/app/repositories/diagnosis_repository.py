from app.config.supabase import supabase


class DiagnosisRepository:

    @staticmethod
    def create_diagnosis(data: dict):
        response = (
            supabase.table("diagnoses")
            .insert(data)
            .execute()
        )

        return response.data[0]

    @staticmethod
    def save_diagnosis_details(data: list):
        response = (
            supabase.table("diagnosis_details")
            .insert(data)
            .execute()
        )

        return response.data

    @staticmethod
    def save_diagnosis_results(data: list):
        response = (
            supabase.table("diagnosis_results")
            .insert(data)
            .execute()
        )

        return response.data

    @staticmethod
    def get_diagnosis(diagnosis_id: str):
        response = (
            supabase.table("diagnoses")
            .select("*")
            .eq("id", diagnosis_id)
            .single()
            .execute()
        )

        return response.data

    @staticmethod
    def get_results(id: str):
        response = (
            supabase.table("diagnosis_results")
            .select("""
                *,
                diseases(
                    code,
                    name,
                    description,
                    solution,
                    prevention,
                    severity_level
                )
            """)
            .eq("diagnosis_id", id)
            .order("rank")
            .execute()
        )

        return response.data

    @staticmethod
    def get_details(id: str):
        response = (
            supabase.table("diagnosis_details")
            .select("*")
            .eq("diagnosis_id", id)
            .execute()
        )

        return response.data