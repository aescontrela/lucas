from functools import lru_cache

from anthropic import AsyncAnthropic

from app.config import Settings
from app.constants import AGENTS_CONFIG
from app.models.research_agent import ResearchAgent
from app.models.router import RouterAgent
from app.services.research_orchestrator import ResearchOrchestratorService


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_anthropic_client() -> AsyncAnthropic:
    return AsyncAnthropic(api_key=get_settings().anthropic_api_key)


@lru_cache
def get_orchestrator() -> ResearchOrchestratorService:
    client = get_anthropic_client()
    settings = get_settings()
    return ResearchOrchestratorService(
        router=RouterAgent(client=client, settings=settings),
        agents=[
            ResearchAgent(
                client=client, settings=settings, name=name, max_tokens=max_tokens
            )
            for name, max_tokens in AGENTS_CONFIG.items()
        ],
    )
