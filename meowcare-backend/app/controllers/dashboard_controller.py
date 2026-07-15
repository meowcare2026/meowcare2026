from app.services.dashboard_service import DashboardService
from app.utils.response import success_response


class DashboardController:
    @staticmethod
    def get_dashboard():
        result = DashboardService.get_dashboard()

        return success_response(
            message="Dashboard admin berhasil diambil",
            data=result,
        )