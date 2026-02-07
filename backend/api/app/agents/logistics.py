from app.agents.base import BaseAgent


class LogisticsAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="logistics", description="Researches travel logistics")
        self.system = (
            "You are a logistics research expert for travelers. "
            "Research airport transit, public transportation, useful local apps, "
            "SIM and WiFi options, currency and tipping customs, and practical travel tips."
        )

    def build_prompt(self, query):
        return (
            f"Research travel logistics for visiting {query}. "
            "Include airport transit, local transportation, "
            "useful apps, SIM/WiFi, currency, and tipping customs."
        )
