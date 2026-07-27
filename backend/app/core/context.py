from contextvars import ContextVar
from typing import Optional


trace_id_context: ContextVar[Optional[str]] = ContextVar(
    "trace_id",
    default=None,
)


def get_trace_id() -> Optional[str]:
    return trace_id_context.get()


def set_trace_id(trace_id: str):
    return trace_id_context.set(trace_id)


def reset_trace_id(token) -> None:
    trace_id_context.reset(token)