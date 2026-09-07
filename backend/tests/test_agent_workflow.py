import pytest
from fastapi.testclient import TestClient

from app.agents.workflow import agent_workflow
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_agent_workflow_runs_directly():
    result = await agent_workflow.ainvoke(
        {
            "user_message": "Explain dependency injection",
        }
    )

    assert "plan" in result
    assert "answer" in result
    assert result["provider"] == "mock"
    assert result["model"] == "mock-dev-model"
    assert result["prompt_id"] == "agent.answer:v1"
    assert "Explain dependency injection" in result["answer"]


def test_agent_run_endpoint():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "Explain trace IDs"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["workflow"] == "minimal-langgraph:v2"
    assert body["provider"] == "mock"
    assert body["model"] == "mock-dev-model"
    assert body["prompt_id"] == "agent.answer:v1"
    assert "Explain trace IDs" in body["answer"]
    assert "plan" in body
    assert "usage" in body