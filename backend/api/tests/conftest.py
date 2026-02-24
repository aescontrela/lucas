import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_anthropic_responses():
    """Mock Anthropic API responses for planner and agents."""

    return {
        "planner": {
            "query": "What is the weather in Tokyo?",
            "agents": ["culture", "food", "logistics", "must_do", "safety"],
        },
        "culture": {
            "sections": [{"heading": "Overview", "content": "Culture content."}],
        },
        "food": {
            "sections": [{"heading": "Overview", "content": "Food content."}],
        },
        "logistics": {
            "sections": [{"heading": "Overview", "content": "Logistics content."}],
        },
        "must_do": {
            "sections": [{"heading": "Overview", "content": "Must-do content."}],
        },
        "safety": {
            "sections": [{"heading": "Overview", "content": "Safety content."}],
        },
    }


@pytest.fixture
def mock_anthropic(mock_anthropic_responses):
    """Mock Anthropic API: planner gets plan shape, agents get sections shape."""
    responses = mock_anthropic_responses

    async def fake_run(self, query):
        return responses[self.name]
    
    async def fake_planner_run(self, query, agent_list):
        return responses["planner"]

    with (
        patch("app.agents.planner.PlannerAgent.run", fake_planner_run),
        patch("app.agents.base.BaseAgent.run", fake_run),
    ):
       yield responses
