import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_orchestrator
from app.schemas.events import ResearchEvent, StreamDoneEvent, StreamErrorEvent
from app.schemas.research import ResearchRequest
from app.services.research_orchestrator import ResearchOrchestratorService

router = APIRouter()
logger = logging.getLogger(__name__)

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
}


def sse(event: ResearchEvent) -> str:
    return f"data: {event.model_dump_json()}\n\n"


@router.post("/research")
async def research(
    request: ResearchRequest,
    orchestrator: Annotated[ResearchOrchestratorService, Depends(get_orchestrator)],
):
    async def generate():
        try:
            async for event in orchestrator.stream_research(request.query):
                yield sse(event)
        except ValueError as e:
            yield sse(StreamErrorEvent(detail=str(e)))
        except Exception:
            logger.exception("Research stream failed")
            yield sse(
                StreamErrorEvent(detail="Research service temporarily unavailable")
            )
        yield sse(StreamDoneEvent())

    return StreamingResponse(
        generate(), media_type="text/event-stream", headers=SSE_HEADERS
    )
