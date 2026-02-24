import pytest
from app.agents.must_do import MustDoAgent


@pytest.mark.unit
def test_must_do_agent_build_prompt():
    agent = MustDoAgent()
    prompt = agent.build_prompt("Tokyo at spring")
    expected = (
        "Research the must-do activities and attractions in Tokyo at spring. "
        "Include iconic landmarks, hidden gems, unique local experiences, "
        "day trip options, and seasonal activities."
    )
    assert prompt == expected


@pytest.mark.asyncio
async def test_must_do_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = MustDoAgent()
    result = await agent.run("Tokyo at spring")
    expected = mock_anthropic_responses["must_do"]
    assert result == expected
