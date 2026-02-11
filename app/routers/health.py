from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])

# Verifica el estado de salud de la API
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }