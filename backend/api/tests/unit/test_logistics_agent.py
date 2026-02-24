import pytest
from app.agents.logistics import LogisticsAgent


@pytest.mark.unit
def test_logistics_agent_build_prompt():
    agent = LogisticsAgent()
    prompt = agent.build_prompt("Tokyo at spring")
    expected = (
        "Research travel logistics for visiting Tokyo at spring. "
        "Include airport transit, local transportation, "
        "useful apps, SIM/WiFi, currency, and tipping customs."
    )
    assert prompt == expected


@pytest.mark.asyncio
async def test_logistics_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = LogisticsAgent()
    result = await agent.run("Tokyo at spring")
    expected = mock_anthropic_responses["logistics"]
    assert result == expected
