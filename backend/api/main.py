from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import get_settings
from app.routes.health import router as health_router
from app.routes.research import router as research_router

settings = get_settings()

app = FastAPI(
    title="Travel Research API",
    description=(
        "Multi-agent travel research over Server-Sent Events. "
        "A router agent plans the research, then domain agents "
        "(food, culture, logistics, safety, activities) stream their "
        "findings concurrently through a single SSE response."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

app.include_router(health_router)
app.include_router(research_router)
