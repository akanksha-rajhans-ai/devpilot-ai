from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter(tags=["health"])
logger = get_logger(__name__)


@router.get("/health")
async def health_check():
    settings = get_settings()

    logger.info("Health check requested")

    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }