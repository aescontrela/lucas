import asyncio
from collections.abc import AsyncIterator
from app.models.router import RouterAgent
from app.models.research_agent import ResearchAgent


class ResearchOrchestratorService:
    def __init__(self, router: RouterAgent, agents: list[ResearchAgent]):
        self.router = router
        self.agents = agents

    async def stream_research(self, query: str) -> AsyncIterator[dict]:
        agent_list = [
            {"name": agent.name, "role": agent.system_prompt} for agent in self.agents
        ]
        plan = await self.router.run(query, agent_list)

        yield {"event": "router", "data": plan.model_dump()}

        agents_by_name = {agent.name: agent for agent in self.agents}

        selected = [
            (agents_by_name[a.name], a.task)
            for a in plan.agents
            if a.name in agents_by_name
        ]

        queue = asyncio.Queue()
        finished = 0

        async def run_agent(agent, task):
            try:
                async for token in agent.stream_tokens(task):
                    await queue.put(
                        {"event": "delta", "agent": agent.name, "text": token}
                    )
                await queue.put({"event": "done", "agent": agent.name})
            except Exception as e:
                await queue.put(
                    {"event": "error", "agent": agent.name, "error": str(e)}
                )

        tasks = [
            asyncio.create_task(run_agent(agent, task)) for agent, task in selected
        ]

        try:
            while finished < len(tasks):
                event = await queue.get()
                yield event
                if event["event"] in ("done", "error"):
                    finished += 1
        finally:
            for task in tasks:
                task.cancel()
