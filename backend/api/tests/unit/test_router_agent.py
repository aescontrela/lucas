import pytest
from app.models.router import RouterAgent
from app.models.research_agent import ResearchAgent
from app.schemas.agents import RouterAgentOutput


@pytest.mark.asyncio
async def test_router_agent_run(
    mock_anthropic,
    mock_anthropic_responses,
    mock_client,
    mock_settings,
):
    agent = RouterAgent(client=mock_client, settings=mock_settings)
    agents = [
        ResearchAgent(name="food", client=mock_client, settings=mock_settings),
        ResearchAgent(name="culture", client=mock_client, settings=mock_settings),
        ResearchAgent(name="activities", client=mock_client, settings=mock_settings),
        ResearchAgent(name="logistics", client=mock_client, settings=mock_settings),
        ResearchAgent(name="safety", client=mock_client, settings=mock_settings),
    ]
    result = await agent.run(
        "Tokyo at spring",
        [{"name": a.name, "system_prompt": a.system_prompt} for a in agents],
    )
    expected = mock_anthropic_responses["router"]
    assert result == RouterAgentOutput(**expected)
