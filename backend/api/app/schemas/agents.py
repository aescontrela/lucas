from pydantic import BaseModel
from typing import TypedDict, Literal

AgentName = Literal["food", "safety", "culture", "logistics", "activities"]


class AgentInfo(TypedDict):
    name: AgentName
    role: str


class AgentTask(BaseModel):
    name: AgentName
    task: str


class RouterAgentOutput(BaseModel):
    query: str
    agents: list[AgentTask]
