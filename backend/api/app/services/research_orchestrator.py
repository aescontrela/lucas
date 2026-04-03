import asyncio

from app.models.router import RouterAgent
from app.models.research_agent import ResearchAgent


class ResearchOrchestrator:
    def __init__(self, router: RouterAgent, agents: list[ResearchAgent]):
        self.router = router
        self.agents = agents

    async def stream_research(self, query):
        """Stream the router and selected agents, yielding router and agent results as they complete."""
        agent_list = [
            {"name": agent.name, "role": agent.system_prompt} for agent in self.agents
        ]
        result = await self.router.run(query, agent_list)

        if (
            not isinstance(result, dict)
            or "query" not in result
            or "agents" not in result
        ):
            raise ValueError(
                "Router did not return expected response shape (query, agents)"
            )

        yield {"event": "router", "data": result}

        tasks = {a["name"]: a["task"] for a in result["agents"]}
        selected = [agent for agent in self.agents if agent.name in tasks]

        async def run_and_tag(agent):
            try:
                outcome = await agent.run(tasks[agent.name])
                return agent.name, outcome, None
            except Exception as e:
                return agent.name, None, str(e)

        for coro in asyncio.as_completed([run_and_tag(agent) for agent in selected]):
            agent_name, result, error = await coro
            yield {
                "event": "agent",
                "agent": agent_name,
                "data": result,
                "error": error,
            }
