from app.agents.base import BaseAgent


class SafetyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="safety",
            description="Researches safety and health information",
        )
        self.system = (
            "You are a safety and health research expert for travelers. "
            "Research areas to avoid, common scams, tap water safety, recommended "
            "vaccinations, emergency numbers, pharmacy availability, and general "
            "safety tips."
        )

    def build_prompt(self, query):
        return (
            f"Research safety and health information for visiting {query}. "
            "Include areas to avoid, common scams, tap water safety, vaccinations, "
            "emergency numbers, and general safety tips."
        )
