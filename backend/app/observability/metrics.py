import time
from contextlib import contextmanager
from typing import Iterator

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

    HTTP_REQUESTS = Counter(
        "devpilot_http_requests_total",
        "Total HTTP requests",
        ["method", "path", "status"],
    )
    HTTP_DURATION = Histogram(
        "devpilot_http_request_duration_seconds",
        "HTTP request latency",
        ["method", "path"],
    )
    RAG_OPERATIONS = Counter(
        "devpilot_rag_operations_total",
        "RAG operations",
        ["operation", "outcome"],
    )
except ImportError:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"
    HTTP_REQUESTS = None
    HTTP_DURATION = None
    RAG_OPERATIONS = None


def record_http_request(method: str, path: str, status_code: int, duration: float) -> None:
    if HTTP_REQUESTS is None:
        return
    HTTP_REQUESTS.labels(method=method, path=path, status=str(status_code)).inc()
    HTTP_DURATION.labels(method=method, path=path).observe(duration)


def render_metrics() -> bytes:
    if HTTP_REQUESTS is None:
        return b"# prometheus-client is not installed\n"
    return generate_latest()


@contextmanager
def observe_rag(operation: str) -> Iterator[None]:
    started_at = time.perf_counter()
    try:
        yield
    except Exception:
        if RAG_OPERATIONS is not None:
            RAG_OPERATIONS.labels(operation=operation, outcome="failure").inc()
        raise
    else:
        if RAG_OPERATIONS is not None:
            RAG_OPERATIONS.labels(operation=operation, outcome="success").inc()
    finally:
        _ = time.perf_counter() - started_at
