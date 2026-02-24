import pytest
from app.agents.planner import PlannerAgent
from app.agents.culture import CultureAgent
from app.agents.food import FoodAgent
from app.agents.safety import SafetyAgent

@pytest.mark.asyncio
async def test_planner_agent_run(mock_anthropic, mock_anthropic_responses):
    agent = PlannerAgent()
    agents = [CultureAgent(), FoodAgent(), SafetyAgent()]    
    result = await agent.run("Tokyo at spring", [{"name": a.name, "description": a.system} for a in agents])
    expected = mock_anthropic_responses["planner"]
    assert result == expected




