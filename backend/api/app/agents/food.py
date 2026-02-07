from app.agents.base import BaseAgent


class FoodAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="food", description="Researches local food and dining")
        self.system = (
            "You are a food research expert for travelers. "
            "Research local dishes, food neighborhoods, street food, dietary info, and typical prices."
        )

    def build_prompt(self, query):
        return (
            f"Research the food scene in {query}. Include must-try local dishes, "
            "best food neighborhoods, street food, dietary considerations, and "
            "typical prices."
        )
