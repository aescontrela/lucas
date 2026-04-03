import pytest
from app.models.research_agent_logistics import LogisticsAgent


@pytest.mark.asyncio
async def test_research_agent_logistics_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = LogisticsAgent(client=mock_client, settings=mock_settings)
    result = await agent.run(
        "Research airport transit and transportation options for Tokyo"
    )
    expected = mock_anthropic_responses["logistics"]
    assert result == expected
