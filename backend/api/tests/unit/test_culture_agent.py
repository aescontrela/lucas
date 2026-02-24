import pytest
from app.agents.culture import CultureAgent


@pytest.mark.unit
def test_culture_agent_build_prompt():
    agent = CultureAgent()
    prompt = agent.build_prompt("Tokyo at spring")
    expected = (
        "Research the culture and history of Tokyo at spring. Include local customs, "
        "etiquette, key historical context, useful language phrases, upcoming "
        "events, and cultural dos and don'ts."
    )
    assert prompt == expected


@pytest.mark.asyncio
async def test_culture_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = CultureAgent()
    result = await agent.run("Tokyo at spring")
    expected = mock_anthropic_responses["culture"]
    assert result == expected
