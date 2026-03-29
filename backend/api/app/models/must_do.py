from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.base import BaseAgent


class MustDoAgent(BaseAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="must_do",
            description="Researches must-do activities and attractions",
            client=client,
            settings=settings,
        )
        self.system = (
            "You are a travel activities expert for travelers. "
            "You know must-do experiences, iconic attractions, hidden gems, and seasonal activities for destinations intimately."
        )
