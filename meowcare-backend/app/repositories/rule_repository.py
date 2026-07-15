from app.config.supabase import supabase


class RuleRepository:

    @staticmethod
    def get_active_rules():
        response = (
            supabase.table("rules")
            .select("""
                *,
                diseases(*),
                symptoms(*)
            """)
            .eq("is_active", True)
            .execute()
        )
        return response.data

    @staticmethod
    def get_all():
        response = (
            supabase.table("rules")
            .select("*")
            .eq("is_active", True)
            .execute()
        )

        return response.data

    @staticmethod
    def get_by_id(rule_id: str):
        response = (
            supabase.table("rules")
            .select("*")
            .eq("id", rule_id)
            .single()
            .execute()
        )


        return response.data
    