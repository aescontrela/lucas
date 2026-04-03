import pytest
from app.models.research_agent_culture import CultureAgent


@pytest.mark.asyncio
async def test_research_agent_culture_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = CultureAgent(client=mock_client, settings=mock_settings)
    result = await agent.run("Research cultural customs and etiquette for Tokyo.")
    expected = mock_anthropic_responses["culture"]
    assert result == expected
