from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="MeowCare API",
        validation_alias="APP_NAME",
    )
    app_version: str = Field(
        default="1.0.0",
        validation_alias="APP_VERSION",
    )
    app_env: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )
    debug: bool = Field(
        default=True,
        validation_alias="DEBUG",
    )

    api_v1_prefix: str = Field(
        default="/api/v1",
        validation_alias="API_V1_PREFIX",
    )
    host: str = Field(
        default="0.0.0.0",
        validation_alias="HOST",
    )
    port: int = Field(
        default=8000,
        validation_alias="PORT",
    )

    cors_origins: list[str] = Field(
        default=["http://localhost:3000"],
        validation_alias="CORS_ORIGINS",
    )

    supabase_url: str = Field(
        validation_alias="SUPABASE_URL",
    )
    supabase_anon_key: str = Field(
        validation_alias="SUPABASE_ANON_KEY",
    )
    supabase_service_role_key: str = Field(
        validation_alias="SUPABASE_SERVICE_ROLE_KEY",
    )

    jwt_secret_key: str = Field(
        validation_alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias="JWT_ALGORITHM",
    )
    jwt_access_token_expire_minutes: int = Field(
        default=60,
        validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()