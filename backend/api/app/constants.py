from pathlib import Path

from app.schemas.agents import AgentName

PROMPTS_DIR = Path(__file__).parent / "prompts"

ROUTER_MAX_TOKENS = 3000

AGENT_DEADLINE_SECONDS = 60

AGENTS_CONFIG: dict[AgentName, int] = {
    "activities": 4096,
    "food": 3000,
    "culture": 4096,
    "logistics": 2048,
    "safety": 2048,
}
