import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert schema["info"]["title"] == "Travel Research API"

    research = schema["paths"]["/research"]["post"]
    assert research["tags"] == ["research"]
    assert "text/event-stream" in research["responses"]["200"]["content"]
    assert schema["paths"]["/health"]["get"]["tags"] == ["health"]
