from supabase import Client, create_client

from app.config.settings import settings


def create_supabase_admin_client() -> Client:
    """
    Client backend dengan service-role key.

    Digunakan untuk operasi database internal dan rollback user.
    Key ini tidak boleh dikirim ke frontend.
    """
    return create_client(
        settings.supabase_url.strip(),
        settings.supabase_service_role_key.strip(),
    )


def create_supabase_auth_client() -> Client:
    """
    Client baru untuk register, login, validasi token, dan logout.
    """
    return create_client(
        settings.supabase_url.strip(),
        settings.supabase_anon_key.strip(),
    )


supabase_admin: Client = create_supabase_admin_client()