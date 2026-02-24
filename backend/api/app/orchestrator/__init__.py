import asyncio

from app.agents.culture import CultureAgent
from app.agents.food import FoodAgent
from app.agents.logistics import LogisticsAgent
from app.agents.must_do import MustDoAgent
from app.agents.safety import SafetyAgent
from app.agents.planner import PlannerAgent


async def stream_research(query):
    """Stream the planner and selected agents, yielding planner and agent results as they complete."""
    planner = PlannerAgent()
    agents = [CultureAgent(), FoodAgent(), LogisticsAgent(), MustDoAgent(), SafetyAgent()]
    agent_list = [{"name": a.name, "description": a.system} for a in agents]
    plan = await planner.run(query, agent_list)

    if not isinstance(plan, dict) or "query" not in plan or "agents" not in plan:
        raise ValueError("Planner did not return expected plan shape (query, agents)")

    yield {"event": "plan", "data": plan}

    selected = [agent for agent in agents if agent.name in plan["agents"]]

    async def run_and_tag(agent):
        try:
            result = await agent.run(plan["query"])
            return agent.name, result, None
        except Exception as e:
            return agent.name, None, str(e)

    for coro in asyncio.as_completed([run_and_tag(agent) for agent in selected]):
        agent_name, result, error = await coro
        yield {"event": "agent", "agent": agent_name, "data": result, "error": error}