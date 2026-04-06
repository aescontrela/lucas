import { useReducer } from "react";
import type { ResearchEvent, AgentType } from "../types";
import { postResearchHandler } from "../handler/post-research-handler";

type AgentState = {
  status: "idle" | "delta" | "done" | "error";
  content: string;
  error?: string;
};

type State = {
  status: "idle" | "inProgress" | "complete" | "error";
  agents: Partial<Record<AgentType, AgentState>>;
};

function reducer(state: State, event: ResearchEvent): State {
  switch (event.status) {
    case "idle": {
      if (event.source === "system") {
        return state;
      }
      return {
        ...state,
        status: "inProgress",
        agents: {
          ...state.agents,
          [event.source]: {
            ...state.agents[event.source],
            status: event.status,
          },
        },
      };
    }
    case "delta": {
      if (event.source === "system") {
        return state;
      }
      return {
        ...state,
        status: "inProgress",
        agents: {
          ...state.agents,
          [event.source]: {
            ...state.agents[event.source],
            status: event.status,
            content:
              (state.agents[event.source]?.content || "") + event.content,
          },
        },
      };
    }
    case "error": {
      if (event.source === "system") {
        return { ...state, status: "error" };
      }
      return {
        ...state,
        status: "inProgress",
        agents: {
          ...state.agents,
          [event.source]: {
            ...state.agents[event.source],
            status: event.status,
            error: event.error,
          },
        },
      };
    }
    case "done": {
      if (event.source === "system") {
        return { ...state, status: "complete" };
      }
      return state;
    }
  }
}

export const useResearch = () => {
  const [state, dispatch] = useReducer(reducer, { status: "idle", agents: {} });

  const search = async (query: string) => {
    dispatch({ source: "system", status: "idle" });
    await postResearchHandler(query, dispatch);
  };

  return { state, search };
};
