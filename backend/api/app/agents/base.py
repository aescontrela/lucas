from app import client


class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.client = client
        self.model = "claude-sonnet-4-5-20250929"
        self.max_tokens = 500
        self.base_instructions = (
            "Be concise and practical. Focus on actionable advice for travelers. "
            "Use markdown formatting with headers and bullet points. "
            "You have lived in this city for 10 years and know it intimately."
        )

    def build_prompt(self, query):
        raise NotImplementedError("Subclasses must implement get_user_message()")

    async def run(self, query):
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=f"{self.system}\n\n{self.base_instructions}",
            messages=[{"role": "user", "content": self.build_prompt(query)}],
        )

        return response.content[0].text
