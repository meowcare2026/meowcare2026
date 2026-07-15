from typing import Any

from app.repositories.dashboard_repository import (
    DashboardRepository,
)


class DashboardService:
    @staticmethod
    def get_dashboard() -> dict[str, Any]:
        statistics = {
            "total_diseases": DashboardRepository.count_all(
                "diseases"
            ),
            "active_diseases": DashboardRepository.count_active(
                "diseases"
            ),
            "total_symptoms": DashboardRepository.count_all(
                "symptoms"
            ),
            "active_symptoms": DashboardRepository.count_active(
                "symptoms"
            ),
            "total_rules": DashboardRepository.count_all(
                "rules"
            ),
            "active_rules": DashboardRepository.count_active(
                "rules"
            ),
            "total_diagnoses": DashboardRepository.count_all(
                "diagnoses"
            ),
        }

        recent_diagnoses = (
            DashboardRepository.get_recent_diagnoses(limit=5)
        )

        return {
            "statistics": statistics,
            "recent_diagnoses": recent_diagnoses,
        }