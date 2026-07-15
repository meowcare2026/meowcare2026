from app.config.supabase import supabase


class DiseaseRepository:

    @staticmethod
    def get_all():
        response = (
            supabase.table("diseases")
            .select("*")
            .eq("is_active", True)
            .order("code")
            .execute()
        )

        return response.data


    @staticmethod
    def get_by_id(disease_id):
        response = (
            supabase.table("diseases")
            .select("*")
            .eq("id", disease_id)
            .single()
            .execute()
        )

        return response.data