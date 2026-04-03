import pytest
from app.models.research_agent_activities import ActivitiesAgent


@pytest.mark.asyncio
async def test_research_agent_activities_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ActivitiesAgent(client=mock_client, settings=mock_settings)
    result = await agent.run(
        "Research top attractions and must-do activities in Tokyo at spring"
    )
    expected = mock_anthropic_responses["activities"]
    assert result == expected
