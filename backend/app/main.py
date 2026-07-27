from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.middleware import TraceMiddleware

configure_logging()

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(TraceMiddleware)
register_exception_handlers(app)

app.include_router(health_router)


@app.get("/__test__/error", include_in_schema=False)
async def test_error():
    raise RuntimeError("Intentional test error")


@app.get("/__test__/validation", include_in_schema=False)
async def test_validation(required_value: int):
    return {"required_value": required_value}


logger.info(
    "Application started: %s version=%s environment=%s",
    settings.app_name,
    settings.app_version,
    settings.environment,
)