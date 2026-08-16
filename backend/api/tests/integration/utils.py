import json
from unittest.mock import MagicMock

from app.schemas.agents import RouterAgentOutput
from app.schemas.events import (
    AgentDeltaEvent,
    AgentDoneEvent,
    AgentErrorEvent,
    RouterEvent,
)


def parse_sse_events(response):
    events = [
        json.loads(line[len("data: ") :])
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    # Collect streamed tokens per agent
    agent_tokens = {}
    for e in events:
        if e["event"] == "agent_delta":
            agent_tokens.setdefault(e["agent"], []).append(e["text"])

    # Build results from agents that completed with "agent_done"
    done_agents = {e["agent"] for e in events if e["event"] == "agent_done"}
    results = {
        name: "".join(tokens)
        for name, tokens in agent_tokens.items()
        if name in done_agents
    }

    return {
        "results": results,
        "errors": {
            e["agent"]: e["detail"] for e in events if e["event"] == "agent_error"
        },
        "stream_error": next(
            (e["detail"] for e in events if e["event"] == "stream_error"),
            None,
        ),
        "done": any(e["event"] == "stream_done" for e in events),
    }


def make_agent_stream(agent_responses):
    async def stream(*args, **kwargs):
        yield RouterEvent(data=RouterAgentOutput(query="test", agents=[]))
        for name, data in agent_responses.items():
            if data is not None:
                yield AgentDeltaEvent(agent=name, text=str(data))
                yield AgentDoneEvent(agent=name)
            else:
                yield AgentErrorEvent(agent=name, detail=f"{name} failed")

    return stream


def make_upstream_error_stream(error):
    async def error_stream(*args, **kwargs):
        raise error
        yield

    return error_stream


def mock_orchestrator(stream_fn):
    mock = MagicMock()
    mock.stream_research = stream_fn
    return mock
