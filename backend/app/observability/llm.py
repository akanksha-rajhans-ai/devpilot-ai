from typing import Any, Optional

from app.core.context import get_trace_id
from app.core.logging import get_logger
from app.schemas.llm import LLMResult

logger = get_logger("llm.observability")


def record_llm_call(
    prompt_id: str,
    result: LLMResult,
    outcome: str = "success",
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    record = {
        "event": "llm.call",
        "outcome": outcome,
        "trace_id": get_trace_id(),
        "prompt_id": prompt_id,
        "provider": result.provider,
        "model": result.model,
        "latency_ms": result.latency_ms,
        "usage": result.usage.model_dump(),
        "metadata": metadata or {},
    }

    logger.info(
        "llm_call outcome=%s trace_id=%s prompt_id=%s provider=%s model=%s latency_ms=%.2f usage=%s metadata=%s",
        record["outcome"],
        record["trace_id"],
        record["prompt_id"],
        record["provider"],
        record["model"],
        record["latency_ms"],
        record["usage"],
        record["metadata"],
    )

    return record