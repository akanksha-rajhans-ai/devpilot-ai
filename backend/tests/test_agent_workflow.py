import pytest
import uuid
from fastapi.testclient import TestClient

from app.agents.workflow import agent_workflow
from app.main import app
from app.llm.mock_provider import transient_failure_attempts

client = TestClient(app)


@pytest.mark.asyncio
async def test_agent_workflow_routes_code_question():
    result = await agent_workflow.ainvoke(
        {
            "user_message": "Explain this FastAPI function",
        },
        config={
            "configurable": {
                "thread_id": f"test-code-{uuid.uuid4()}",
            }
        },
    )

    assert result["route"] == "code_explanation"
    assert result["prompt_id"] == "agent.code_explanation:v1"
    assert result["provider"] == "mock"
    assert result["status"] == "completed"
    assert "Explain this FastAPI function" in result["answer"]


@pytest.mark.asyncio
async def test_agent_workflow_routes_general_question():
    result = await agent_workflow.ainvoke(
        {
            "user_message": "What is good engineering communication?",
        },
        config={
            "configurable": {
                "thread_id": f"test-general-{uuid.uuid4()}",
            }
        },
    )

    assert result["route"] == "general_answer"
    assert result["prompt_id"] == "agent.answer:v1"
    assert result["provider"] == "mock"
    assert result["status"] == "completed"
    assert "Mock response to:" in result["answer"]


def test_agent_run_endpoint_includes_route():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "Explain trace IDs in FastAPI"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "completed"
    assert body["workflow"] == "conditional-langgraph:v4"
    assert body["route"] == "code_explanation"
    assert body["provider"] == "mock"
    assert body["prompt_id"] == "agent.code_explanation:v1"

def test_agent_run_endpoint_returns_workflow_failure_for_provider_failure():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "__simulate_provider_failure__"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "failed"
    assert body["error"] == "AI provider is temporarily unavailable"
    assert body["workflow"] == "conditional-langgraph:v4"
    assert body["provider"] == "mock"
    assert body["model"] == "mock-dev-model"

def test_agent_run_endpoint_recovers_from_transient_provider_failure():
    transient_failure_attempts.clear()

    response = client.post(
        "/api/v1/agent/run",
        json={"message": "__simulate_transient_provider_failure__"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "completed"
    assert body["provider"] == "mock"
    assert body["model"] == "mock-dev-model"
    assert "__simulate_transient_provider_failure__" in body["answer"]


def test_agent_run_endpoint_generates_thread_id_when_missing():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "Explain checkpointing"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["thread_id"]
    assert body["status"] == "completed"

def test_agent_run_endpoint_returns_waiting_for_approval_for_risky_request():
    response = client.post(
        "/api/v1/agent/run",
        json={
            "message": "Delete production data",
            "thread_id": f"approval-test-{uuid.uuid4()}",
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "waiting_for_approval"
    assert body["route"] == "needs_approval"
    assert body["approval_reason"] == "Request may perform a sensitive or irreversible action."
    assert body["answer"] is None


def test_agent_routes_knowledge_requests_through_rag():
    from app.rag.document_store import document_store

    document_store.clear()
    ingest_response = client.post(
        "/api/v1/documents",
        json={
            "title": "RAG Guide",
            "content": "RAG retrieves evidence before generating an answer.",
        },
    )
    assert ingest_response.status_code == 200

    response = client.post(
        "/api/v1/agent/run",
        json={"message": "According to the uploaded document, what is RAG?"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["route"] == "knowledge_answer"
    assert body["retrieval_count"] == 1
    assert body["citations"][0]["document_title"] == "RAG Guide"


def test_agent_can_run_read_only_document_tool():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "List documents"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["route"] == "tool_action"
    assert body["tool_name"] == "list_documents"


@pytest.mark.parametrize(
    ("message", "route", "prompt_id"),
    [
        ("Review this code for security", "code_review", "agent.code_review:v1"),
        ("Debug this exception", "debug", "agent.debug:v1"),
        ("Write documentation for this API", "documentation", "agent.documentation:v1"),
        ("Implement a cache adapter", "code_generation", "agent.code_generation:v1"),
    ],
)
def test_agent_routes_to_specialists(message, route, prompt_id):
    response = client.post("/api/v1/agent/run", json={"message": message})

    assert response.status_code == 200
    body = response.json()
    assert body["route"] == route
    assert body["prompt_id"] == prompt_id
