import pytest
from main import app
from app.dependencies import get_orchestrator
from tests.integration.utils import (
    parse_sse_events,
    make_agent_stream,
    make_upstream_error_stream,
    mock_orchestrator,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research(client):
    app.dependency_overrides[get_orchestrator] = lambda: mock_orchestrator(
        make_agent_stream(
            {
                "culture": {"sections": []},
                "food": {"sections": []},
                "logistics": {"sections": []},
                "activities": {"sections": []},
                "safety": {"sections": []},
            }
        )
    )
    sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    app.dependency_overrides.clear()

    assert sse["done"] is True
    assert sse["stream_error"] is None
    assert sse["errors"] == {}
    assert sse["results"].keys() == {
        "culture",
        "food",
        "logistics",
        "activities",
        "safety",
    }


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_agent_errors(client):
    app.dependency_overrides[get_orchestrator] = lambda: mock_orchestrator(
        make_agent_stream(
            {
                "culture": {"sections": []},
                "food": None,
                "logistics": {"sections": []},
                "activities": {"sections": []},
                "safety": None,
            }
        )
    )
    sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    app.dependency_overrides.clear()

    assert sse["results"].keys() == {"culture", "logistics", "activities"}
    assert sse["errors"].keys() == {"food", "safety"}
    assert sse["stream_error"] is None
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_upstream_value_error(client):
    app.dependency_overrides[get_orchestrator] = lambda: mock_orchestrator(
        make_upstream_error_stream(ValueError("Invalid query"))
    )
    sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    app.dependency_overrides.clear()

    assert "Invalid" in sse["stream_error"]
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_upstream_error(client):
    app.dependency_overrides[get_orchestrator] = lambda: mock_orchestrator(
        make_upstream_error_stream(Exception("Research failed"))
    )
    sse = parse_sse_events(client.post("/research", json={"query": "Tokyo?"}))
    app.dependency_overrides.clear()

    assert "unavailable" in sse["stream_error"]
    assert sse["done"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_invalid_input(client):
    response = client.post("/research", json={})
    assert response.status_code == 422
