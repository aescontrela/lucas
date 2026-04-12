from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"

ROUTER_MAX_TOKENS = 3000

AGENTS_CONFIG = {
    "activities": 4096,
    "food": 3000,
    "culture": 4096,
    "logistics": 2048,
    "safety": 2048,
}
