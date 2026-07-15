from app.config.supabase import supabase


class SymptomRepository:

    @staticmethod
    def get_all():
        response = (
            supabase.table("symptoms")
            .select("*")
            .eq("is_active", True)
            .order("code")
            .execute()
        )

        return response.data

    @staticmethod
    def get_by_id(symptom_id: str):
        response = (
            supabase.table("symptoms")
            .select("*")
            .eq("id", symptom_id)
            .single()
            .execute()
        )

        return response.data