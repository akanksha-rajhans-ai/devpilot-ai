import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.context import reset_trace_id, set_trace_id
from app.core.logging import get_logger

logger = get_logger(__name__)


class TraceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        incoming_trace_id = request.headers.get("X-Trace-Id")
        trace_id = incoming_trace_id or str(uuid.uuid4())

        token = set_trace_id(trace_id)
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000

            response.headers["X-Trace-Id"] = trace_id

            logger.info(
                "HTTP request completed trace_id=%s method=%s path=%s status_code=%s duration_ms=%.2f",
                trace_id,
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )

            return response
        finally:
            reset_trace_id(token)