import pytest
from app.models.food import FoodAgent


@pytest.mark.asyncio
async def test_food_agent_run(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = FoodAgent(client=mock_client, settings=mock_settings)
    result = await agent.run(
        "Research must-try local dishes and food neighborhoods in Tokyo at spring"
    )
    expected = mock_anthropic_responses["food"]
    assert result == expected
