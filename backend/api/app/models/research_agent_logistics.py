from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR
from app.models.research_agent import ResearchAgent


class LogisticsAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="logistics",
            client=client,
            settings=settings,
        )
        self.system_prompt = (PROMPTS_DIR / "research_logistics.md").read_text()
