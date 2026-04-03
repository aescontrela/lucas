import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from app.config import Settings


@pytest.fixture
def mock_settings():
    return Settings(
        anthropic_api_key="test-key",
        agents_model="claude-test",
        router_model="claude-test",
        claude_max_tokens=100,
    )


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_anthropic_responses():
    """Mock Anthropic API responses for router and agents."""

    return {
        "router": {
            "query": "What is the weather in Tokyo?",
            "agents": [
                {
                    "name": "culture",
                    "task": "Research cultural customs and etiquette for Tokyo.",
                },
                {
                    "name": "food",
                    "task": "Research must-try local dishes and food neighborhoods in Tokyo.",
                },
                {
                    "name": "logistics",
                    "task": "Research airport transit and transportation options for Tokyo.",
                },
                {
                    "name": "activities",
                    "task": "Research top attractions and must-do activities in Tokyo.",
                },
                {
                    "name": "safety",
                    "task": "Research safety tips and health considerations for Tokyo.",
                },
            ],
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
        "activities": {
            "sections": [{"heading": "Overview", "content": "Must-do content."}],
        },
        "safety": {
            "sections": [{"heading": "Overview", "content": "Safety content."}],
        },
    }


@pytest.fixture
def mock_anthropic(mock_anthropic_responses):
    """Mock Anthropic API: router gets plan shape, agents get sections shape."""
    responses = mock_anthropic_responses

    async def fake_run(self, query):
        return responses[self.name]

    async def fake_router_run(self, query, agent_list):
        return responses["router"]

    with (
        patch("app.models.router.RouterAgent.run", fake_router_run),
        patch("app.models.research_agent.ResearchAgent.run", fake_run),
    ):
        yield responses
