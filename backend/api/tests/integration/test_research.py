import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research(client, mock_anthropic):
    query = "What is the weather in Tokyo?"
    response = client.post("/research", json={"query": query})
    data = response.json()['result']
    assert response.status_code == 200
    assert data.keys() == {"culture", "food", "logistics", "must_do", "safety"}



@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_invalid_query(client):
    with patch("app.routes.research.run_research", new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = ValueError("Invalid query")
        query = "What is the weather in Tokyo?"
        response = client.post("/research", json={"query": query})
        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid research plan or input."}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_error(client):
    with patch("app.routes.research.run_research", new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = Exception("Research failed")
        query = "What is the weather in Tokyo?"
        response = client.post("/research", json={"query": query})
        assert response.status_code == 502
        assert response.json() == {
            "detail": "Research service temporarily unavailable."
        }

@pytest.mark.integration
@pytest.mark.asyncio
async def test_research_invalid_input(client):
    response = client.post("/research", json={})
    assert response.status_code == 422

