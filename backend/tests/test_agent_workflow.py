import pytest
from fastapi.testclient import TestClient

from app.agents.workflow import agent_workflow
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_agent_workflow_routes_code_question():
    result = await agent_workflow.ainvoke(
        {
            "user_message": "Explain this FastAPI function",
        }
    )

    assert result["route"] == "code_explanation"
    assert result["prompt_id"] == "agent.code_explanation:v1"
    assert result["provider"] == "mock"
    assert "Explain this FastAPI function" in result["answer"]


@pytest.mark.asyncio
async def test_agent_workflow_routes_general_question():
    result = await agent_workflow.ainvoke(
        {
            "user_message": "What is good engineering communication?",
        }
    )

    assert result["route"] == "general_answer"
    assert result["prompt_id"] == "agent.answer:v1"
    assert result["provider"] == "mock"
    assert "What is good engineering communication?" in result["answer"]


def test_agent_run_endpoint_includes_route():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "Explain trace IDs in FastAPI"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["workflow"] == "conditional-langgraph:v1"
    assert body["route"] == "code_explanation"
    assert body["provider"] == "mock"
    assert body["prompt_id"] == "agent.code_explanation:v1"