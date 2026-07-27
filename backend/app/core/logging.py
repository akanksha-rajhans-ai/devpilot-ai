import logging
import sys

from app.core.config import get_settings
from app.core.context import get_trace_id


class TraceIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "-"
        return True


def configure_logging() -> None:
    settings = get_settings()

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(TraceIdFilter())

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | trace_id=%(trace_id)s | %(name)s | %(message)s",
        handlers=[handler],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)