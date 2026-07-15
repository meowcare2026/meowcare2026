from typing import Any

from app.config.supabase import supabase_admin


def check_database_connection() -> dict[str, Any]:
    """
    Mengecek koneksi ke Supabase dengan membaca satu record
    dari tabel diseases.

    Query menggunakan limit 1 agar ringan.
    """
    try:
        response = (
            supabase_admin
            .table("diseases")
            .select("id")
            .limit(1)
            .execute()
        )

        return {
            "connected": True,
            "message": "Supabase database connected",
            "data": response.data,
        }

    except Exception as error:
        return {
            "connected": False,
            "message": "Supabase database connection failed",
            "error": str(error),
        }