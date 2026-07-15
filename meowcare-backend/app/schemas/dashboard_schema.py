from typing import Any

from pydantic import BaseModel


class DashboardStatistics(BaseModel):
    total_diseases: int
    active_diseases: int
    total_symptoms: int
    active_symptoms: int
    total_rules: int
    active_rules: int
    total_diagnoses: int


class RecentDiagnosisItem(BaseModel):
    id: str
    owner_name: str
    cat_name: str | None = None
    highest_percentage: float
    urgency_level: str
    created_at: str
    main_disease: dict[str, Any] | None = None


class DashboardResponse(BaseModel):
    statistics: DashboardStatistics
    recent_diagnoses: list[RecentDiagnosisItem]