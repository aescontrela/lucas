import json
import pytest
from unittest.mock import patch


def parse_sse_events(response):
    events = [
        json.loads(line[len("data: "):])
        for line in response.text.splitlines()
        if line.startswith("data: ")
    ]
    return {
        "results": {e["agent"]: e["data"] for e in events if e["event"] == "agent" and e["error"] is None},
        "errors": {e["agent"]: e["error"] for e in events if e["event"] == "agent" and e["error"] is not None},
        "stream_error": next((e["detail"] for e in events if e["event"] == "error"), None),
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


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research(client):
    with patch("app.routes.research.stream_research", make_agent_stream({
        "culture": {"sections": []},
        "food": {"sections": []},
        "logistics": {"sections": []},
        "must_do": {"sections": []},
        "safety": {"sections": []},
    })):
        sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))

    assert sse["done"] is True
    assert sse["stream_error"] is None
    assert sse["errors"] == {}
    assert sse["results"].keys() == {"culture", "food", "logistics", "must_do", "safety"}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_agent_errors(client):
    with patch("app.routes.research.stream_research", make_agent_stream({
        "culture": {"sections": []},
        "food": None,
        "logistics": {"sections": []},
        "must_do": {"sections": []},
        "safety": None,
    })):
        sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))

    assert sse["results"].keys() == {"culture", "logistics", "must_do"}
    assert sse["errors"].keys() == {"food", "safety"}
    assert sse["stream_error"] is None
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_upstream_value_error(client):
    with patch("app.routes.research.stream_research", make_upstream_error_stream(ValueError("Invalid query"))):
        sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    assert "Invalid" in sse["stream_error"]
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_upstream_error(client):
    with patch("app.routes.research.stream_research", make_upstream_error_stream(Exception("Research failed"))):
        sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    assert "unavailable" in sse["stream_error"]
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_invalid_input(client):
    response = client.post("/research", json={})
    assert response.status_code == 422