import pytest
from app.models.research_agent_safety import SafetyAgent


@pytest.mark.asyncio
async def test_research_agent_safety_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = SafetyAgent(client=mock_client, settings=mock_settings)
    result = await agent.run(
        "Research safety tips and health considerations for Tokyo at spring"
    )
    expected = mock_anthropic_responses["safety"]
    assert result == expected
