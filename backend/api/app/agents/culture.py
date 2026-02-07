from app.agents.base import BaseAgent


class CultureAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="culture",
            description="Research key culture and history",
        )
        self.system = (
            "You are a culture and history research expert for travelers. "
            "Research local customs, etiquette, historical context, language basics and useful phrases, "
            "local events and festivals, and cultural dos and don'ts."
        )

    def build_prompt(self, query):
        return (
            f"Research the culture and history of {query}. Include local customs, "
            "etiquette, key historical context, useful language phrases, upcoming "
            "events, and cultural dos and don'ts."
        )
