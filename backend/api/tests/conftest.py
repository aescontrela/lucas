import pytest
from contextlib import contextmanager
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app
from app.config import Settings
from app.models.router import RouterAgent
from app.models.research_agent import ResearchAgent
from app.schemas.agents import RouterAgentOutput
from app.services.research_orchestrator import ResearchOrchestratorService


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
                    "task": "Research top attractions and activities in Tokyo.",
                },
                {
                    "name": "safety",
                    "task": "Research safety tips and health considerations for Tokyo.",
                },
            ],
        },
        "culture": "Culture content.",
        "food": "Food content.",
        "logistics": "Logistics content.",
        "activities": "Activities content.",
        "safety": "Safety content.",
    }


@pytest.fixture
def mock_anthropic(mock_anthropic_responses):
    """Mock Anthropic API: router gets plan shape, agents stream tokens."""
    responses = mock_anthropic_responses

    async def fake_router_run(self, query, agent_list):
        return RouterAgentOutput(**responses["router"])

    async def fake_stream_tokens(self, task):
        text = responses[self.name]
        for word in text.split(" "):
            yield word + " "

    with (
        patch("app.models.router.RouterAgent.run", fake_router_run),
        patch(
            "app.models.research_agent.ResearchAgent.stream_tokens", fake_stream_tokens
        ),
    ):
        yield responses


@pytest.fixture
def mock_anthropic_with_failure(mock_anthropic_responses):
    responses = mock_anthropic_responses

    @contextmanager
    def _mock(failing_agents: set[str]):
        async def fake_router_run(self, query, agent_list):
            return RouterAgentOutput(**responses["router"])

        async def fake_stream_tokens(self, task):
            if self.name in failing_agents:
                raise Exception(f"{self.name} agent failed")
            text = responses[self.name]
            for word in text.split(" "):
                yield word + " "

        with (
            patch("app.models.router.RouterAgent.run", fake_router_run),
            patch(
                "app.models.research_agent.ResearchAgent.stream_tokens",
                fake_stream_tokens,
            ),
        ):
            yield responses

    return _mock


@pytest.fixture
def orchestrator(mock_client, mock_settings):
    router = RouterAgent(client=mock_client, settings=mock_settings)

    agents = [
        ResearchAgent(client=mock_client, settings=mock_settings, name=name)
        for name in ["food", "culture", "logistics", "activities", "safety"]
    ]
    return ResearchOrchestratorService(router=router, agents=agents)
