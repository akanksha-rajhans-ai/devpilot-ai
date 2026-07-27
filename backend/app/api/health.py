from fastapi import APIRouter, Depends, status

from app.core.config import Settings
from app.core.dependencies import get_app_settings
from app.core.logging import get_logger

router = APIRouter(prefix="/health", tags=["health"])
logger = get_logger(__name__)


@router.get("/live")
async def liveness_check(settings: Settings = Depends(get_app_settings)):
    logger.info("Liveness check requested")

    return {
        "status": "alive",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check(settings: Settings = Depends(get_app_settings)):
    logger.info("Readiness check requested")

    return {
        "status": "ready",
        "service": settings.app_name,
        "checks": {
            "configuration": "ok"
        },
    }