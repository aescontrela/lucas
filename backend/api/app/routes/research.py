from fastapi import APIRouter
from pydantic import BaseModel
from app.orchestrator import run_research

router = APIRouter()


class ResearchRequest(BaseModel):
    query: str


@router.post("/research")
async def research(request: ResearchRequest):
    result = await run_research(request.query)
    return {"result": result}
