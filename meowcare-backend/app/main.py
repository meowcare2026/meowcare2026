from fastapi import FastAPI
from app.routers.diagnosis_router import router as diagnosis_router

app = FastAPI(
    title="MeowCare API",
    version="1.0.0",
    description="Backend Sistem Pakar Diagnosis Penyakit Kucing"
)

app.include_router(diagnosis_router)



@app.get("/")
def root():
    return {
        "status": "success",
        "message": "MeowCare Backend Running 🚀"
    }