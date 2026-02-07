import asyncio

from app.agents.culture import CultureAgent
from app.agents.food import FoodAgent
from app.agents.logistics import LogisticsAgent
from app.agents.must_do import MustDoAgent
from app.agents.safety import SafetyAgent
from app.agents.planner import PlannerAgent


async def run_research(query) -> dict[str, dict]:
    """Run the planner and selected research agents; return a dict of agent name -> result."""
    planner = PlannerAgent()
    agents = [
        CultureAgent(),
        FoodAgent(),
        LogisticsAgent(),
        MustDoAgent(),
        SafetyAgent(),
    ]
    agent_list = [{"name": a.name, "description": a.description} for a in agents]

    plan = await planner.run(query, agent_list)

    if not isinstance(plan, dict) or "query" not in plan or "agents" not in plan:
        raise ValueError("Planner did not return expected plan shape (query, agents)")

    selected = [agent for agent in agents if agent.name in plan["agents"]]

    results = await asyncio.gather(*[agent.run(plan["query"]) for agent in selected])

    return {agent.name: result for agent, result in zip(selected, results)}
