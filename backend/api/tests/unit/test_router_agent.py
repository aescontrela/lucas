import pytest
from app.models.router import RouterAgent
from app.models.culture import CultureAgent
from app.models.food import FoodAgent
from app.models.safety import SafetyAgent


@pytest.mark.asyncio
async def test_router_agent_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = RouterAgent(client=mock_client, settings=mock_settings)
    agents = [
        CultureAgent(client=mock_client, settings=mock_settings),
        FoodAgent(client=mock_client, settings=mock_settings),
        SafetyAgent(client=mock_client, settings=mock_settings),
    ]
    result = await agent.run(
        "Tokyo at spring", [{"name": a.name, "description": a.system} for a in agents]
    )
    expected = mock_anthropic_responses["router"]
    assert result == expected
