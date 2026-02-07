from anthropic import AsyncAnthropic
from app.config import Settings

settings = Settings()

client = AsyncAnthropic(api_key=settings.anthropic_api_key)
