from supabase import Client, create_client

from app.config.settings import settings


def create_supabase_admin_client() -> Client:
    """
    Client backend menggunakan Service Role Key.
    Digunakan untuk operasi database internal.
    """
    return create_client(
        settings.supabase_url.strip(),
        settings.supabase_service_role_key.strip(),
    )


def create_supabase_auth_client() -> Client:
    """
    Client menggunakan Anon Key.
    Digunakan untuk login/register.
    """
    return create_client(
        settings.supabase_url.strip(),
        settings.supabase_anon_key.strip(),
    )


supabase_admin: Client = create_supabase_admin_client()
supabase_auth: Client = create_supabase_auth_client()

# Alias supaya kode Backend 2 tetap jalan
supabase = supabase_admin