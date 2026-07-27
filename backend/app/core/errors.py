from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger
from typing import Any, Optional

logger = get_logger(__name__)


def build_error_response(
    code: str,
    message: str,
    details: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    logger.warning(
        "HTTP exception path=%s status_code=%s detail=%s",
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    code = "HTTP_ERROR"
    message = str(exc.detail)

    if exc.status_code == status.HTTP_404_NOT_FOUND:
        code = "NOT_FOUND"
        message = "Resource not found"

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(
            code=code,
            message=message,
            details={"path": request.url.path},
        ),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    logger.warning(
        "Validation error path=%s errors=%s",
        request.url.path,
        exc.errors(),
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={
                "path": request.url.path,
                "errors": exc.errors(),
            },
        ),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled exception path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=build_error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred",
            details={"path": request.url.path},
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)