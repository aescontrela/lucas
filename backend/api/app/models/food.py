from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.base import BaseAgent


class FoodAgent(BaseAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="food",
            description="Researches local food and dining",
            client=client,
            settings=settings,
        )
        self.system = (
            "You are a food research expert for travelers. "
            "You know local cuisine, restaurants, street food, dietary considerations, and food culture intimately."
        )
