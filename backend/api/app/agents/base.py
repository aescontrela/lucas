from app import client
from app import settings
from app.models.agents import BaseAgentOutput


class BaseAgent:
    """Base class for travel research agents. Subclasses set system prompt and implement build_prompt."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.client = client
        self.model = settings.claude_model
        self.max_tokens = settings.claude_max_tokens
        self.base_instructions = (
            "Be concise and practical. Focus on actionable advice for travelers. "
            "You have lived in this city for 10 years and know it intimately. "
            "Total response: under 300 words. "
            "Your response goes in the 'sections' array: use exactly 3–4 sections. "
            "Each section is an object with a heading and content property. "
            "Use markdown only; no code blocks and no JSON inside heading or content."
        )

    def build_prompt(self, query) -> str:
        """Build the user message for this agent. Subclasses must implement."""
        raise NotImplementedError("Subclasses must implement build_prompt()")

    async def run(self, query) -> dict:
        """Run the agent and return structured output (sections with heading and content)."""
        response = await self.client.messages.parse(
            model=self.model,
            max_tokens=int(self.max_tokens),
            system=f"{self.system}\n\n{self.base_instructions}",
            output_format=BaseAgentOutput,
            messages=[{"role": "user", "content": self.build_prompt(query)}],
        )

        result = response.parsed_output.model_dump()

        return result
