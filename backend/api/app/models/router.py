from anthropic import AsyncAnthropic
from app.config import Settings
from app.constants import PROMPTS_DIR
from app.schemas.agents import RouterAgentOutput


class RouterAgent:
    """Selects which agents to run and returns an enriched list of agent tasks."""

    def __init__(self, client: AsyncAnthropic, settings: Settings):
        self.client = client
        self.model = settings.router_model
        self.max_tokens = int(settings.claude_max_tokens)
        self.name = "router"
        self.system_prompt = (PROMPTS_DIR / "router.md").read_text()

    async def run(self, query, agent_list) -> dict:
        """Return a dict with 'query' (enriched string) and 'agents' (list of {name, task} objects)."""
        agent_list_str = "\n".join(
            f"{agent['name']}: {agent['role']}" for agent in agent_list
        )
        response = await self.client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            output_format=RouterAgentOutput,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"User query: {query}\n\n"
                        f"Available agents: {agent_list_str}\n\n"
                        "Agents must be from the list above. "
                        "Return a JSON object with exactly two keys: 'query' (string: a single enriched/normalized "
                        "version of the user's request) and 'agents' (array of objects, each with 'name' (the agent "
                        "name from the list above) and 'task' (a specific instruction tailored for that agent))."
                    ),
                }
            ],
        )

        result = response.parsed_output.model_dump()

        return result
