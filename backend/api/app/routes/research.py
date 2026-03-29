import json
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.schemas.research import ResearchRequest
from app.services.research_orchestrator import ResearchOrchestrator
from app.dependencies import get_orchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/research")
async def research(
    request: ResearchRequest,
    orchestrator: ResearchOrchestrator = Depends(get_orchestrator),
):
    async def generate():
        try:
            async for event in orchestrator.stream_research(request.query):
                yield f"data: {json.dumps(event)}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'event': 'error', 'detail': str(e)})}\n\n"
        except Exception:
            yield f"data: {json.dumps({'event': 'error', 'detail': 'Research service temporarily unavailable.'})}\n\n"
        finally:
            yield 'data: {"event": "done"}\n\n'

    return StreamingResponse(generate(), media_type="text/event-stream")
