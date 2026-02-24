import pytest
from app.agents.safety import SafetyAgent


@pytest.mark.unit
def test_safety_agent_build_prompt():
    agent = SafetyAgent()
    prompt = agent.build_prompt("Tokyo at spring")
    expected = (
        "Research safety and health information for visiting Tokyo at spring. "
        "Include areas to avoid, common scams, tap water safety, vaccinations, "
        "emergency numbers, and general safety tips."
    )
    assert prompt == expected


@pytest.mark.asyncio
async def test_safety_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = SafetyAgent()
    result = await agent.run("Tokyo at spring")
    expected = mock_anthropic_responses["safety"]
    assert result == expected
