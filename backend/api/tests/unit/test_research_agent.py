import pytest
from app.models.research_agent import ResearchAgent


@pytest.mark.asyncio
async def test_research_agent_activities_stream(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ResearchAgent(name="activities", client=mock_client, settings=mock_settings)
    tokens = [
        token
        async for token in agent.stream_tokens(
            "Research top attractions and must-do activities in Tokyo at spring"
        )
    ]
    result = "".join(tokens).strip()
    assert result == mock_anthropic_responses["activities"]


@pytest.mark.asyncio
async def test_research_agent_culture_stream(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ResearchAgent(name="culture", client=mock_client, settings=mock_settings)
    tokens = [
        token
        async for token in agent.stream_tokens(
            "Research cultural customs and etiquette for Tokyo."
        )
    ]
    result = "".join(tokens).strip()
    assert result == mock_anthropic_responses["culture"]


@pytest.mark.asyncio
async def test_research_agent_food_stream(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ResearchAgent(name="food", client=mock_client, settings=mock_settings)
    tokens = [
        token
        async for token in agent.stream_tokens(
            "Research must-try local dishes and food neighborhoods in Tokyo at spring"
        )
    ]
    result = "".join(tokens).strip()
    assert result == mock_anthropic_responses["food"]


@pytest.mark.asyncio
async def test_research_agent_logistics_stream(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ResearchAgent(name="logistics", client=mock_client, settings=mock_settings)
    tokens = [
        token
        async for token in agent.stream_tokens(
            "Research airport transit and transportation options for Tokyo"
        )
    ]
    result = "".join(tokens).strip()
    assert result == mock_anthropic_responses["logistics"]


@pytest.mark.asyncio
async def test_research_agent_safety_stream(
    mock_anthropic, mock_anthropic_responses, mock_client, mock_settings
):
    agent = ResearchAgent(name="safety", client=mock_client, settings=mock_settings)
    tokens = [
        token
        async for token in agent.stream_tokens(
            "Research safety tips and health considerations for Tokyo at spring"
        )
    ]
    result = "".join(tokens).strip()
    assert result == mock_anthropic_responses["safety"]
