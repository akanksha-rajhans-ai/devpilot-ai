from app.core.audit import audit_event


def test_audit_event_returns_structured_record():
    record = audit_event(
        event="test.event",
        outcome="success",
        actor_id="user-123",
        metadata={"resource": "demo"},
    )

    assert record["event"] == "test.event"
    assert record["outcome"] == "success"
    assert record["actor_id"] == "user-123"
    assert record["metadata"]["resource"] == "demo"
    assert "trace_id" in record