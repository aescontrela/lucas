from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.research_agent import ResearchAgent


class FoodAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="food",
            description="Researches local food and dining",
            client=client,
            settings=settings,
        )
        self.system_prompt = (
            "You are a food research expert for travelers. "
            "You know local cuisine, restaurants, street food, dietary considerations, and food culture intimately."
        )
