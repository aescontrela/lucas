from app.agents.base import BaseAgent


class MustDoAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="must_do", description="Researches must-do activities and attractions"
        )
        self.system = (
            "You are a travel activities expert. Research the top must-do experiences, "
            "iconic attractions, hidden gems, day trips, seasonal activities, and unique "
            "local experiences that visitors should not miss."
        )

    def build_prompt(self, query):
        return (
            f"Research the must-do activities and attractions in {query}. "
            "Include iconic landmarks, hidden gems, unique local experiences, "
            "day trip options, and seasonal activities."
        )
