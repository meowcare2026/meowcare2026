from fastapi import APIRouter, Depends

from app.controllers.dashboard_controller import (
    DashboardController,
)
from app.middleware.auth_middleware import require_admin


router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Admin Dashboard"],
)


@router.get(
    "",
    summary="Get admin dashboard",
    dependencies=[Depends(require_admin)],
)
def get_dashboard():
    return DashboardController.get_dashboard()