import pytest
from app.agents.food import FoodAgent


@pytest.mark.unit
def test_food_agent_build_prompt():
    agent = FoodAgent()
    prompt = agent.build_prompt("Tokyo at spring")
    expected = (
        "Research the food scene in Tokyo at spring. Include must-try local dishes, "
        "best food neighborhoods, street food, dietary considerations, and "
        "typical prices."
    )
    assert prompt == expected


@pytest.mark.asyncio
async def test_food_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = FoodAgent()
    result = await agent.run("Tokyo at spring")
    expected = mock_anthropic_responses["food"]
    assert result == expected
