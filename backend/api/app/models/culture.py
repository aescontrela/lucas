from anthropic import AsyncAnthropic
from app.config import Settings
from app.models.base import BaseAgent


class CultureAgent(BaseAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="culture",
            description="Research key culture and history",
            client=client,
            settings=settings,
        )
        self.system = (
            "You are a culture and history research expert for travelers. "
            "You know local customs, etiquette, history, language, and festivals intimately."
        )
