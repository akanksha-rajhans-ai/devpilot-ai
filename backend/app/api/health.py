from fastapi import APIRouter, Depends, Response, status

from app.core.config import Settings
from app.core.dependencies import get_app_settings
from app.core.logging import get_logger
from app.db.session import SessionLocal
from sqlalchemy import text

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
async def readiness_check(
    response: Response,
    settings: Settings = Depends(get_app_settings),
):
    logger.info("Readiness check requested")

    database_status = "not_configured"
    if settings.document_repository == "database":
        try:
            with SessionLocal() as session:
                session.scalar(text("SELECT 1"))
            database_status = "ok"
        except Exception:
            logger.exception("Database readiness check failed")
            database_status = "failed"

    if database_status == "failed":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ready" if database_status != "failed" else "not_ready",
        "service": settings.app_name,
        "checks": {
            "configuration": "ok",
            "database": database_status,
        },
    }
