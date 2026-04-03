from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.research_agent import ResearchAgent


class ActivitiesAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="must_do",
            description="Researches must-do activities and attractions",
            client=client,
            settings=settings,
        )
        self.system_prompt = (
            "You are a travel activities expert for travelers. "
            "You know must-do experiences, iconic attractions, hidden gems, and seasonal activities for destinations intimately."
        )
