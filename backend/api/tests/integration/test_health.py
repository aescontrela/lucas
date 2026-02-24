import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"result": "OK"}
