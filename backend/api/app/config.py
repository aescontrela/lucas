from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-5-20250929"
    claude_max_tokens: int = 2048

    model_config = {"env_file": ".env"}
