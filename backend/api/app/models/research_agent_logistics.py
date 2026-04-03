from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.research_agent import ResearchAgent


class LogisticsAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="logistics",
            description="Researches travel logistics",
            client=client,
            settings=settings,
        )
        self.system_prompt = (
            "You are a logistics research expert for travelers. "
            "You know transportation, local apps, SIM and WiFi options, currency, and practical travel tips intimately."
        )
