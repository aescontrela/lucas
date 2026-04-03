from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    agents_model: str = "claude-sonnet-4-6"
    router_model: str = "claude-haiku-4-5-20251001"
    claude_max_tokens: int = 2048

    model_config = {"env_file": ".env"}
