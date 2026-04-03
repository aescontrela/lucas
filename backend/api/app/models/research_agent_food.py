from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR
from app.models.research_agent import ResearchAgent


class FoodAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="food",
            client=client,
            settings=settings,
        )
        self.system_prompt = (PROMPTS_DIR / "research_food.md").read_text()
