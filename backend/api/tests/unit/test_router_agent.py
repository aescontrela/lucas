from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.router import RouterAgent
from app.schemas.agents import AgentInfo, RouterAgentOutput

AGENT_LIST: list[AgentInfo] = [
    {"name": "food", "role": "Researches local dishes."},
    {"name": "culture", "role": "Researches customs and etiquette."},
]


def make_client(parsed_output):
    client = MagicMock()
    client.messages.parse = AsyncMock(
        return_value=MagicMock(parsed_output=parsed_output)
    )
    return client


@pytest.mark.asyncio
async def test_router_agent_run(mock_anthropic_responses, mock_settings):
    expected = RouterAgentOutput(**mock_anthropic_responses["router"])
    client = make_client(expected)
    agent = RouterAgent(client=client, settings=mock_settings)

    result = await agent.run("Tokyo at spring", AGENT_LIST)

    assert result == expected
    client.messages.parse.assert_awaited_once()


@pytest.mark.asyncio
async def test_router_agent_raises_when_output_missing(mock_settings):
    client = make_client(None)
    agent = RouterAgent(client=client, settings=mock_settings)

    with pytest.raises(ValueError, match="no parsed output"):
        await agent.run("Tokyo at spring", AGENT_LIST)
