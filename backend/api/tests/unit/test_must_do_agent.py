import pytest
from app.models.must_do import MustDoAgent


@pytest.mark.asyncio
async def test_must_do_agent_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = MustDoAgent(client=mock_client, settings=mock_settings)
    result = await agent.run(
        "Research top attractions and must-do activities in Tokyo at spring"
    )
    expected = mock_anthropic_responses["must_do"]
    assert result == expected
