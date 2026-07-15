
import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import check_database_connection
from app.config.settings import settings
from app.middleware import (
    RequestLoggingMiddleware,
    register_exception_handlers,
)
from app.routers.dashboard_router import (
    router as dashboard_router,
)
from app.routers.disease_router import (
    router as disease_router,
)
from app.routers.symptom_router import (
    router as symptom_router,
)
from app.routers.rule_router import (
    router as rule_router,
)
from app.routers.admin_log_router import (
    router as admin_log_router,
)

from app.routers.diagnosis_router import (
    router as diagnosis_router
)
from app.routers.public_disease_router import (
    router as public_disease_router,
)

from app.routers.public_symptom_router import (
    router as public_symptom_router,
)
from app.routers.auth_router import router as auth_router
from app.utils.response import error_response, success_response


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
)

logger = logging.getLogger(__name__)


# ============================================================
# APPLICATION LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Menjalankan proses startup dan shutdown aplikasi.
    """

    logger.info(
        "Starting %s version %s",
        settings.app_name,
        settings.app_version,
    )

    logger.info(
        "Environment: %s | Debug: %s",
        settings.app_env,
        settings.debug,
    )

    database_status = check_database_connection()

    if database_status["connected"]:
        logger.info("Supabase database connected")
    else:
        logger.error(
            "Supabase database connection failed: %s",
            database_status.get("error"),
        )

    yield

    logger.info("%s stopped", settings.app_name)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "REST API untuk sistem pakar diagnosis penyakit kucing "
        "menggunakan metode Certainty Factor."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ============================================================
# MIDDLEWARE
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

register_exception_handlers(app)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    auth_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    dashboard_router,
    prefix=settings.api_v1_prefix,
)  

app.include_router(
    disease_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    symptom_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    rule_router,
    prefix=settings.api_v1_prefix,
)
app.include_router(
    admin_log_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    diagnosis_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    public_disease_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    public_symptom_router,
    prefix=settings.api_v1_prefix,
)
# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get(
    "/",
    tags=["Root"],
    summary="MeowCare API root",
)
async def root():
    return success_response(
        message="Welcome to MeowCare API",
        data={
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
            "documentation": {
                "swagger": "/docs",
                "redoc": "/redoc",
            },
        },
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    f"{settings.api_v1_prefix}/health",
    tags=["Health"],
    summary="Check API and database health",
)
async def health_check():
    database_status = check_database_connection()

    application_data = {
        "application": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
        },
        "database": {
            "connected": database_status["connected"],
            "message": database_status["message"],
        },
    }

    if not database_status["connected"]:
        return error_response(
            message="API berjalan, tetapi database tidak terhubung",
            code="DATABASE_UNAVAILABLE",
            status_code=503,
            details=application_data,
        )

    return success_response(
        message="MeowCare API is running",
        data=application_data,
    )
