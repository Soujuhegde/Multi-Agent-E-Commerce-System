from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "Multi-Agent-Ecommerce"
    }


@router.get("/ping")
async def ping():
    return {
        "message": "pong"
    }