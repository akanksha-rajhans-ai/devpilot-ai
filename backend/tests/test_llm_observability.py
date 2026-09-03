from app.observability.llm import record_llm_call
from app.schemas.llm import LLMResult, LLMUsage


def test_record_llm_call_returns_safe_metadata():
    result = LLMResult(
        content="This should not be logged in the observability record",
        provider="mock",
        model="mock-dev-model",
        latency_ms=12.5,
        usage=LLMUsage(
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
        ),
    )

    record = record_llm_call(
        prompt_id="chat.general:v1",
        result=result,
        metadata={"route": "/api/v1/chat"},
    )

    assert record["event"] == "llm.call"
    assert record["outcome"] == "success"
    assert record["prompt_id"] == "chat.general:v1"
    assert record["provider"] == "mock"
    assert record["model"] == "mock-dev-model"
    assert record["latency_ms"] == 12.5
    assert record["usage"]["input_tokens"] == 10
    assert record["usage"]["output_tokens"] == 20
    assert record["usage"]["total_tokens"] == 30
    assert record["metadata"]["route"] == "/api/v1/chat"

    assert "content" not in record