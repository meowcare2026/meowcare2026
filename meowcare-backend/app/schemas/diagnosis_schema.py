from typing import List, Optional
from pydantic import BaseModel, Field


class SymptomInput(BaseModel):
    symptom_id: str
    cf_user: float = Field(..., ge=0.0, le=1.0)


class DiagnosisCreate(BaseModel):
    owner_name: str
    cat_name: Optional[str] = None
    cat_age: Optional[str] = None
    cat_gender: Optional[str] = None

    symptoms: List[SymptomInput]


class DiagnosisResult(BaseModel):
    disease_name: str
    percentage: float
    recommendation: str
    urgency_level: str