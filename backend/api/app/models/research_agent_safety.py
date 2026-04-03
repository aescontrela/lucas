from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.research_agent import ResearchAgent


class SafetyAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="safety",
            description="Researches safety and health information",
            client=client,
            settings=settings,
        )
        self.system_prompt = (
            "You are a safety and health research expert for travelers. "
            "You know safety risks, scams, health requirements, and emergency information for destinations."
        )
