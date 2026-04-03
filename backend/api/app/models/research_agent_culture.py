from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.research_agent import ResearchAgent


class CultureAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="culture",
            description="Research key culture and history",
            client=client,
            settings=settings,
        )
        self.system_prompt = (
            "You are a culture and history research expert for travelers. "
            "You know local customs, etiquette, history, language, and festivals intimately."
        )
