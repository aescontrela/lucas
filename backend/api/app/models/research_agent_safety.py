from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR
from app.models.research_agent import ResearchAgent


class SafetyAgent(ResearchAgent):
    def __init__(self, client: AsyncAnthropic, settings: Settings):
        super().__init__(
            name="safety",
            client=client,
            settings=settings,
        )
        self.system_prompt = (PROMPTS_DIR / "research_safety.md").read_text()
