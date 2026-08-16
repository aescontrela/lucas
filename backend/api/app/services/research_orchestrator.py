import asyncio
import logging
from collections.abc import AsyncIterator

from app.constants import AGENT_DEADLINE_SECONDS
from app.models.research_agent import ResearchAgent
from app.models.router import RouterAgent
from app.schemas.agents import AgentInfo
from app.schemas.events import (
    AgentDeltaEvent,
    AgentDoneEvent,
    AgentErrorEvent,
    ResearchEvent,
    RouterEvent,
)

logger = logging.getLogger(__name__)


class ResearchOrchestratorService:
    def __init__(
        self,
        router: RouterAgent,
        agents: list[ResearchAgent],
        agent_deadline: float = AGENT_DEADLINE_SECONDS,
    ):
        self.router = router
        self.agents = agents
        self.agent_deadline = agent_deadline

    async def stream_research(self, query: str) -> AsyncIterator[ResearchEvent]:
        agent_list: list[AgentInfo] = [
            {"name": agent.name, "role": agent.system_prompt} for agent in self.agents
        ]
        plan = await self.router.run(query, agent_list)

        yield RouterEvent(data=plan)

        agents_by_name = {agent.name: agent for agent in self.agents}

        selected = [
            (agents_by_name[a.name], a.task)
            for a in plan.agents
            if a.name in agents_by_name
        ]

        queue: asyncio.Queue[ResearchEvent] = asyncio.Queue()
        finished = 0

        async def run_agent(agent: ResearchAgent, task: str) -> None:
            try:
                async with asyncio.timeout(self.agent_deadline):
                    async for token in agent.stream_tokens(task):
                        await queue.put(AgentDeltaEvent(agent=agent.name, text=token))
                await queue.put(AgentDoneEvent(agent=agent.name))
            except TimeoutError:
                logger.warning("Agent %s exceeded %ss deadline", agent.name, self.agent_deadline)
                await queue.put(
                    AgentErrorEvent(
                        agent=agent.name, detail=f"{agent.name} agent timed out"
                    )
                )
            except Exception:
                logger.exception("Agent %s failed", agent.name)
                await queue.put(
                    AgentErrorEvent(
                        agent=agent.name, detail=f"{agent.name} agent failed"
                    )
                )

        tasks = [
            asyncio.create_task(run_agent(agent, task)) for agent, task in selected
        ]

        try:
            while finished < len(tasks):
                event = await queue.get()
                yield event
                if isinstance(event, (AgentDoneEvent, AgentErrorEvent)):
                    finished += 1
        finally:
            for task in tasks:
                task.cancel()
