from fastapi import FastAPI

#configure_logging()
#Runs before we create loggers and before the app starts handling requests.
#get_logger(__name__)
#Creates a logger named after the current Python module, likely app.main.
#logger.info(...)
#Logs a startup event. This proves logging works when the app boots.

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger

configure_logging()

settings = get_settings()
logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)

logger.info("Application started: %s version=%s environment=%s", settings.app_name, settings.app_version, settings.environment)