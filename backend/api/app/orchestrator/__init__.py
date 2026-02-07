import asyncio

from app.agents.culture import CultureAgent
from app.agents.food import FoodAgent
from app.agents.logistics import LogisticsAgent
from app.agents.must_do import MustDoAgent
from app.agents.safety import SafetyAgent


async def run_research(query):
    culture_agent = CultureAgent()
    food_agent = FoodAgent()
    logistics_agent = LogisticsAgent()
    must_do_agent = MustDoAgent()
    safety_agent = SafetyAgent()

    agents = [culture_agent, food_agent, logistics_agent, must_do_agent, safety_agent]

    results = await asyncio.gather(*[agent.run(query) for agent in agents])

    return {agent.name: result for agent, result in zip(agents, results)}
