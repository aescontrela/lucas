from anthropic import AsyncAnthropic
from app.config import Settings
from app.schemas.agents import BaseAgentOutput


class BaseAgent:
    """Base class for travel research agents. Subclasses set system prompt"""

    def __init__(self, name, description, client: AsyncAnthropic, settings: Settings):
        self.name = name
        self.description = description
        self.client = client
        self.model = settings.claude_model
        self.max_tokens = settings.claude_max_tokens
        self.base_instructions = (
            "Be concise and practical. Focus on actionable advice for travelers. "
            "You are a local expert with deep knowledge of this destination. "
            "Use exactly 3–4 sections. Use markdown only; no code blocks."
        )

    async def run(self, task) -> dict:
        """Run the agent and return structured output (sections with heading and content)."""
        response = await self.client.messages.parse(
            model=self.model,
            max_tokens=int(self.max_tokens),
            system=f"{self.system}\n\n{self.base_instructions}",
            output_format=BaseAgentOutput,
            messages=[{"role": "user", "content": task}],
        )

        result = response.parsed_output.model_dump()

        return result
