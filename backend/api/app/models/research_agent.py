from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR
from app.schemas.agents import BaseAgentOutput


class ResearchAgent:
    """Base class for travel research agents. Subclasses set ``role`` (system instruction for the model)."""

    def __init__(self, name, client: AsyncAnthropic, settings: Settings):
        self.name = name
        self.client = client
        self.model = settings.agents_model
        self.max_tokens = settings.claude_max_tokens
        self.base_instructions = (PROMPTS_DIR / "research_instructions.md").read_text()

    async def run(self, task) -> dict:
        """Run the agent and return structured output (sections with heading and content)."""
        response = await self.client.messages.parse(
            model=self.model,
            max_tokens=int(self.max_tokens),
            system=f"{self.system_prompt}\n\n{self.base_instructions}",
            output_format=BaseAgentOutput,
            messages=[{"role": "user", "content": task}],
        )

        result = response.parsed_output.model_dump()

        return result
