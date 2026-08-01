from typing import Any, Optional

from app.core.context import get_trace_id
from app.core.logging import get_logger

audit_logger = get_logger("audit")


def audit_event(
    event: str,
    outcome: str,
    actor_id: Optional[str] = None,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    record = {
        "event": event,
        "outcome": outcome,
        "actor_id": actor_id,
        "trace_id": get_trace_id(),
        "metadata": metadata or {},
    }

    audit_logger.info(
        "audit_event event=%s outcome=%s actor_id=%s trace_id=%s metadata=%s",
        record["event"],
        record["outcome"],
        record["actor_id"],
        record["trace_id"],
        record["metadata"],
    )

    return record