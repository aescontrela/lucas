import pytest
from app.constants import AGENTS_CONFIG
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
        ResearchAgent(
            name=name, max_tokens=max_tokens, client=mock_client, settings=mock_settings
        )
        for name, max_tokens in AGENTS_CONFIG.items()
    ]
    result = await agent.run(
        "Tokyo at spring",
        [{"name": a.name, "system_prompt": a.system_prompt} for a in agents],
    )
    expected = mock_anthropic_responses["router"]
    assert result == RouterAgentOutput(**expected)
