from pydantic import BaseModel


class Section(BaseModel):
    heading: str
    content: str


class BaseAgentOutput(BaseModel):
    sections: list[Section]


class PlannerAgentOutput(BaseModel):
    query: str
    agents: list[str]
