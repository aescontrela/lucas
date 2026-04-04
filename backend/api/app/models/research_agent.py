from collections.abc import AsyncIterator
from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR


class ResearchAgent:
    """Travel research agent. Loads system prompt from prompts/research_{name}.md and base instructions from prompts/research_instructions.md."""

    def __init__(self, name, client: AsyncAnthropic, settings: Settings):
        self.name = name
        self.client = client
        self.model = settings.agents_model
        self.max_tokens = settings.claude_max_tokens
        self.base_instructions = (PROMPTS_DIR / "research_instructions.md").read_text()
        self.system_prompt = (PROMPTS_DIR / f"research_{name}.md").read_text()

    async def stream_tokens(self, task: str) -> AsyncIterator[str]:
        """Stream tokens from the agent for a given task."""

        async with self.client.messages.stream(
            model=self.model,
            max_tokens=int(self.max_tokens),
            system=f"{self.system_prompt}\n\n{self.base_instructions}",
            messages=[{"role": "user", "content": task}],
        ) as stream:
            async for text in stream.text_stream:
                yield text
