import pytest
from app.models.culture import CultureAgent


@pytest.mark.asyncio
async def test_culture_agent_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = CultureAgent(client=mock_client, settings=mock_settings)
    result = await agent.run("Research cultural customs and etiquette for Tokyo.")
    expected = mock_anthropic_responses["culture"]
    assert result == expected
