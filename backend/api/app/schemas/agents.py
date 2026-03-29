from pydantic import BaseModel


class Section(BaseModel):
    heading: str
    content: str


class BaseAgentOutput(BaseModel):
    sections: list[Section]


class AgentTask(BaseModel):
    name: str
    task: str


class RouterAgentOutput(BaseModel):
    query: str
    agents: list[AgentTask]
