import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_orchestrator
from app.schemas.events import ResearchEvent, StreamDoneEvent, StreamErrorEvent
from app.schemas.research import ResearchRequest
from app.services.research_orchestrator import ResearchOrchestratorService

router = APIRouter(tags=["research"])
logger = logging.getLogger(__name__)

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
}


def sse(event: ResearchEvent) -> str:
    return f"data: {event.model_dump_json()}\n\n"


@router.post(
    "/research",
    summary="Stream multi-agent travel research",
    description=(
        "Runs the router agent to plan the research, then streams the "
        "selected agents' findings concurrently as Server-Sent Events. "
        "Each `data:` line is a JSON object discriminated by its `event` field:\n\n"
        "| Event | Payload | Meaning |\n"
        "| --- | --- | --- |\n"
        "| `router` | `data: {query, agents: [{name, task}]}` | The research plan |\n"
        "| `agent_delta` | `agent`, `text` | A streamed text chunk from one agent |\n"
        "| `agent_done` | `agent` | That agent finished successfully |\n"
        "| `agent_error` | `agent`, `detail` | That agent failed or timed out; the rest keep streaming |\n"
        "| `stream_error` | `detail` | The whole run failed; no more agent events follow |\n"
        "| `stream_done` | — | Terminal event, always sent last |\n\n"
        "Event models are defined in `app/schemas/events.py`.\n\n"
        "**Note:** Swagger UI's *Execute* button buffers the whole response and "
        "will appear to hang while the stream runs. To watch events arrive "
        "live, use `curl -N` instead."
    ),
    response_description="Server-Sent Events stream of research events",
    responses={
        200: {
            "content": {
                "text/event-stream": {
                    "schema": {"type": "string", "format": "sse"},
                    "example": (
                        'data: {"event":"agent_delta","agent":"food","text":"Try the..."}\n\n'
                        'data: {"event":"agent_done","agent":"food"}\n\n'
                        'data: {"event":"stream_done"}\n\n'
                    ),
                }
            },
        },
    },
)
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
