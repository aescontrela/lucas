import logging
from fastapi import APIRouter, HTTPException
from app.models.research import ResearchRequest
from app.orchestrator import run_research

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/research")
async def research(request: ResearchRequest):
    try:
        result = await run_research(request.query)
        return {"result": result}
    except ValueError as e:
        logger.warning("ValueError: %s", e)
        raise HTTPException(status_code=400, detail="Invalid research plan or input.")
    except Exception:
        logger.exception("Research failed")
        raise HTTPException(
            status_code=502,
            detail="Research service temporarily unavailable.",
        )
