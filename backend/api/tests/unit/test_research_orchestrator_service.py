import asyncio
from collections import defaultdict
from unittest.mock import patch

import pytest

from app.schemas.agents import RouterAgentOutput
from app.schemas.events import (
    AgentDeltaEvent,
    AgentDoneEvent,
    AgentErrorEvent,
    RouterEvent,
)


@pytest.mark.asyncio
async def test_research_orchestrator_service_run(
    mock_anthropic, mock_anthropic_responses, orchestrator
):
    events = [event async for event in orchestrator.stream_research("Tokyo trip")]
    deltas = [e for e in events if isinstance(e, AgentDeltaEvent)]
    dones = [e for e in events if isinstance(e, AgentDoneEvent)]
    errors = [e for e in events if isinstance(e, AgentErrorEvent)]

    text_by_agent = defaultdict(list)

    assert isinstance(events[0], RouterEvent)
    assert len(errors) == 0
    assert len(dones) == 5

    for delta in deltas:
        text_by_agent[delta.agent].append(delta.text)

    for a in ("food", "culture", "activities", "safety", "logistics"):
        result = "".join(text_by_agent[a]).strip()
        assert result == mock_anthropic_responses[a]


@pytest.mark.asyncio
async def test_orchestrator_continues_when_agents_fail(
    mock_anthropic_with_failure, mock_anthropic_responses, orchestrator
):
    with mock_anthropic_with_failure({"food", "logistics"}):
        events = [event async for event in orchestrator.stream_research("Tokyo trip")]
        deltas = [e for e in events if isinstance(e, AgentDeltaEvent)]
        dones = [e for e in events if isinstance(e, AgentDoneEvent)]
        errors = [e for e in events if isinstance(e, AgentErrorEvent)]

        text_by_agent = defaultdict(list)

        assert isinstance(events[0], RouterEvent)
        assert len(errors) == 2
        assert len(dones) == 3

        # Raw exception messages must not leak to the client.
        assert {e.detail for e in errors} == {
            "food agent failed",
            "logistics agent failed",
        }

        for delta in deltas:
            text_by_agent[delta.agent].append(delta.text)

        for a in ("culture", "activities", "safety"):
            result = "".join(text_by_agent[a]).strip()
            assert result == mock_anthropic_responses[a]


@pytest.mark.asyncio
async def test_agent_exceeding_deadline_becomes_agent_error(
    mock_anthropic_responses, orchestrator
):
    responses = mock_anthropic_responses

    async def fake_router_run(self, query, agent_list):
        return RouterAgentOutput(**responses["router"])

    async def fake_stream_tokens(self, task):
        if self.name == "food":
            await asyncio.sleep(5)
        yield responses[self.name]

    orchestrator.agent_deadline = 0.05

    with (
        patch("app.models.router.RouterAgent.run", fake_router_run),
        patch(
            "app.models.research_agent.ResearchAgent.stream_tokens",
            fake_stream_tokens,
        ),
    ):
        events = [event async for event in orchestrator.stream_research("Tokyo trip")]

    dones = [e for e in events if isinstance(e, AgentDoneEvent)]
    errors = [e for e in events if isinstance(e, AgentErrorEvent)]

    assert len(dones) == 4
    assert len(errors) == 1
    assert errors[0].agent == "food"
    assert errors[0].detail == "food agent timed out"
