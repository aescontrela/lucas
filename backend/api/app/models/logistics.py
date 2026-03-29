from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.base import BaseAgent


class LogisticsAgent(BaseAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="logistics",
            description="Researches travel logistics",
            client=client,
            settings=settings,
        )
        self.system = (
            "You are a logistics research expert for travelers. "
            "You know transportation, local apps, SIM and WiFi options, currency, and practical travel tips intimately."
        )
