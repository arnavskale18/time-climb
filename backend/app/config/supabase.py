# app/config/supabase.py
from supabase import create_client, Client
from functools import lru_cache
from app.config.settings import get_settings


@lru_cache
def get_supabase() -> Client:
    """
    Returns a cached Supabase client using the ANON key.
    Use get_supabase_admin() for privileged server-side operations.
    """
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_anon_key)


@lru_cache
def get_supabase_admin() -> Client:
    """
    Supabase admin client (service role key).
    Use ONLY in server-side trusted operations — never expose to clients.
    """
    s = get_settings()
    return create_client(s.supabase_url, s.supabase_service_role_key)
