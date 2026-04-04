import json
from unittest.mock import MagicMock


def parse_sse_events(response):
    events = [
        json.loads(line[len("data: ") :])
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    # Collect streamed tokens per agent
    agent_tokens = {}
    for e in events:
        if e["event"] == "delta":
            agent_tokens.setdefault(e["agent"], []).append(e["text"])

    # Build results from agents that completed with "done"
    done_agents = {e["agent"] for e in events if e["event"] == "done" and "agent" in e}
    results = {
        name: "".join(tokens)
        for name, tokens in agent_tokens.items()
        if name in done_agents
    }

    return {
        "results": results,
        "errors": {
            e["agent"]: e["error"]
            for e in events
            if e["event"] == "error" and "agent" in e
        },
        "stream_error": next(
            (e["detail"] for e in events if e["event"] == "error" and "detail" in e),
            None,
        ),
        "done": any(e["event"] == "done" and "agent" not in e for e in events),
    }


def make_agent_stream(agent_responses):
    async def stream(*args, **kwargs):
        yield {"event": "router", "data": {"query": "test", "agents": []}}
        for name, data in agent_responses.items():
            if data is not None:
                yield {"event": "delta", "agent": name, "text": str(data)}
                yield {"event": "done", "agent": name}
            else:
                yield {"event": "error", "agent": name, "error": f"{name} failed"}

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
