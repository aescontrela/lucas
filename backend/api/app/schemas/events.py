from typing import Literal

from pydantic import BaseModel

from app.schemas.agents import AgentName, RouterAgentOutput


class RouterEvent(BaseModel):
    """The research plan: which agents were selected and their tasks."""

    event: Literal["router"] = "router"
    data: RouterAgentOutput


class AgentDeltaEvent(BaseModel):
    """A streamed text chunk from one agent."""

    event: Literal["agent_delta"] = "agent_delta"
    agent: AgentName
    text: str


class AgentDoneEvent(BaseModel):
    """One agent finished streaming successfully."""

    event: Literal["agent_done"] = "agent_done"
    agent: AgentName


class AgentErrorEvent(BaseModel):
    """One agent failed; the rest of the stream continues."""

    event: Literal["agent_error"] = "agent_error"
    agent: AgentName
    detail: str


class StreamErrorEvent(BaseModel):
    """The whole research run failed; no further agent events will follow."""

    event: Literal["stream_error"] = "stream_error"
    detail: str


class StreamDoneEvent(BaseModel):
    """Terminal event: always the last event in the stream."""

    event: Literal["stream_done"] = "stream_done"


ResearchEvent = (
    RouterEvent
    | AgentDeltaEvent
    | AgentDoneEvent
    | AgentErrorEvent
    | StreamErrorEvent
    | StreamDoneEvent
)
