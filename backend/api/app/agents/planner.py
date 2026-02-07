from app import client, settings
from app.models.agents import PlannerAgentOutput


class PlannerAgent:
    """Selects which research agents to run and returns an enriched query and agent list."""

    def __init__(self):
        self.client = client
        self.model = settings.claude_model
        self.max_tokens = settings.claude_max_tokens
        self.system = (
            "You are a travel planning assistant. Analyze the user's query, "
            "extract key travel details, and select which research agents to activate. "
            "Respond with ONLY valid JSON, no other text."
        )

    async def run(self, query, agent_list) -> dict:
        """Return a plan with 'query' (enriched string) and 'agents' (list of agent names)."""
        agent_list_str = "\n".join(
            f"{agent['name']}: {agent['description']}" for agent in agent_list
        )
        response = await self.client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system,
            output_format=PlannerAgentOutput,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"User query: {query}\n\n"
                        f"Available agents: {agent_list_str}\n\n"
                        "Agents must be from the list above. "
                        "Return a JSON object with exactly two keys: 'query' (string: a single enriched/normalized "
                        "version of the user's request) and 'agents' (array of strings: agent names to run, chosen "
                        "from the available agents above)."
                    ),
                }
            ],
        )

        result = response.parsed_output.model_dump()

        return result
