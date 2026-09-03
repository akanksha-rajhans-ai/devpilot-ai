from fastapi.testclient import TestClient

from app.agents.workflow import agent_workflow
from app.main import app

client = TestClient(app)


def test_agent_workflow_runs_directly():
    result = agent_workflow.invoke(
        {
            "user_message": "Explain dependency injection",
        }
    )

    assert "plan" in result
    assert "answer" in result
    assert "Explain dependency injection" in result["answer"]


def test_agent_run_endpoint():
    response = client.post(
        "/api/v1/agent/run",
        json={"message": "Explain trace IDs"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["workflow"] == "minimal-langgraph:v1"
    assert "Explain trace IDs" in body["answer"]
    assert "plan" in body