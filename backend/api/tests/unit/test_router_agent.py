import pytest
from app.models.router import RouterAgent
from app.models.research_agent_culture import CultureAgent
from app.models.research_agent_food import FoodAgent
from app.models.research_agent_logistics import LogisticsAgent
from app.models.research_agent_activities import ActivitiesAgent
from app.models.research_agent_safety import SafetyAgent


@pytest.mark.asyncio
async def test_router_agent_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = RouterAgent(client=mock_client, settings=mock_settings)
    agents = [
        CultureAgent(client=mock_client, settings=mock_settings),
        FoodAgent(client=mock_client, settings=mock_settings),
        SafetyAgent(client=mock_client, settings=mock_settings),
        LogisticsAgent(client=mock_client, settings=mock_settings),
        ActivitiesAgent(client=mock_client, settings=mock_settings),
    ]
    result = await agent.run(
        "Tokyo at spring",
        [{"name": a.name, "system_prompt": a.system_prompt} for a in agents],
    )
    expected = mock_anthropic_responses["router"]
    assert result == expected
