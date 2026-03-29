from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.base import BaseAgent


class SafetyAgent(BaseAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="safety",
            description="Researches safety and health information",
            client=client,
            settings=settings,
        )
        self.system = (
            "You are a safety and health research expert for travelers. "
            "You know safety risks, scams, health requirements, and emergency information for destinations."
        )
