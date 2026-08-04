import time
import uuid
import json
from collections import defaultdict, deque
from collections.abc import Callable
from typing import Deque

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from collections import defaultdict, deque

from app.core.config import get_settings
from app.core.context import reset_trace_id, set_trace_id
from app.core.errors import build_error_response
from app.core.logging import get_logger

logger = get_logger(__name__)

def get_runtime_settings(request: Request):
    return getattr(request.app.state, "settings_override", None) or get_settings()


class TraceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests: dict[str, Deque[float]] = defaultdict(deque)

    def reset(self) -> None:
        self.requests.clear()

    async def dispatch(self, request: Request, call_next: Callable):
        settings = get_runtime_settings(request)

    async def dispatch(self, request: Request, call_next: Callable):
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


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests: dict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next: Callable):
        settings = get_runtime_settings(request)

        if not settings.rate_limit_enabled:
            return await call_next(request)

        client_host = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - settings.rate_limit_window_seconds

        rate_limit_store = getattr(request.app.state, "rate_limit_store", self.requests)
        request_times = rate_limit_store[client_host]

        while request_times and request_times[0] < window_start:
            request_times.popleft()

        remaining = settings.rate_limit_requests - len(request_times)

        if remaining <= 0:
            logger.warning(
                "Rate limit exceeded client=%s path=%s",
                client_host,
                request.url.path,
            )

            return Response(
                content=json.dumps(
                    build_error_response(
                        code="RATE_LIMIT_EXCEEDED",
                        message="Too many requests",
                        details={
                            "path": request.url.path,
                            "limit": settings.rate_limit_requests,
                            "window_seconds": settings.rate_limit_window_seconds,
                        },
                    )
                ),
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json",
                headers={
                    "X-RateLimit-Limit": str(settings.rate_limit_requests),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(settings.rate_limit_window_seconds),
                },
            )

        request_times.append(now)

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(settings.rate_limit_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(remaining - 1, 0))

        return response