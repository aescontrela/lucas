from functools import lru_cache
from app.models.router import RouterAgent
from app.models.culture import CultureAgent
from app.models.food import FoodAgent
from app.models.logistics import LogisticsAgent
from app.models.must_do import MustDoAgent
from app.models.safety import SafetyAgent
from app.services.research_orchestrator import ResearchOrchestrator
from anthropic import AsyncAnthropic
from app.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_anthropic_client() -> AsyncAnthropic:
    return AsyncAnthropic(api_key=get_settings().anthropic_api_key)


def get_orchestrator() -> ResearchOrchestrator:
    client = get_anthropic_client()
    settings = get_settings()
    return ResearchOrchestrator(
        router=RouterAgent(client=client, settings=settings),
        agents=[
            CultureAgent(client=client, settings=settings),
            FoodAgent(client=client, settings=settings),
            LogisticsAgent(client=client, settings=settings),
            MustDoAgent(client=client, settings=settings),
            SafetyAgent(client=client, settings=settings),
        ],
    )
