import pytest
from collections import defaultdict


@pytest.mark.asyncio
async def test_research_orchestrator_service_run(
    mock_anthropic, mock_anthropic_responses, orchestrator
):
    events = [event async for event in orchestrator.stream_research("Tokyo trip")]
    deltas = [e for e in events if e["event"] == "delta"]
    dones = [e for e in events if e["event"] == "done"]
    errors = [e for e in events if e["event"] == "error"]

    text_by_agent = defaultdict(list)

    assert events[0]["event"] == "router"
    assert len(errors) == 0
    assert len(dones) == 5

    for delta in deltas:
        text_by_agent[delta["agent"]].append(delta["text"])

    for a in ("food", "culture", "activities", "safety", "logistics"):
        result = "".join(text_by_agent[a]).strip()
        assert result == mock_anthropic_responses[a]


@pytest.mark.asyncio
async def test_router_agent_failure(
    mock_anthropic_with_failure, mock_anthropic_responses, orchestrator
):
    with mock_anthropic_with_failure({"food", "logistics"}):
        events = [event async for event in orchestrator.stream_research("Tokyo trip")]
        deltas = [e for e in events if e["event"] == "delta"]
        dones = [e for e in events if e["event"] == "done"]
        errors = [e for e in events if e["event"] == "error"]

        text_by_agent = defaultdict(list)

        assert events[0]["event"] == "router"
        assert len(errors) == 2
        assert len(dones) == 3

        for delta in deltas:
            text_by_agent[delta["agent"]].append(delta["text"])

        for a in ("culture", "activities", "safety"):
            result = "".join(text_by_agent[a]).strip()
            assert result == mock_anthropic_responses[a]
