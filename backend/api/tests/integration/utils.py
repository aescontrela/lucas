import json
from unittest.mock import MagicMock


def parse_sse_events(response):
    events = [
        json.loads(line[len("data: ") :])
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    return {
        "results": {
            e["agent"]: e["data"]
            for e in events
            if e["event"] == "agent" and e["error"] is None
        },
        "errors": {
            e["agent"]: e["error"]
            for e in events
            if e["event"] == "agent" and e["error"] is not None
        },
        "stream_error": next(
            (e["detail"] for e in events if e["event"] == "error"), None
        ),
        "done": any(e["event"] == "done" for e in events),
    }


def make_agent_stream(agent_responses):
    async def stream(*args, **kwargs):
        for name, data in agent_responses.items():
            yield {
                "event": "agent",
                "agent": name,
                "data": data,
                "error": None if data is not None else f"{name} failed",
            }

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
