import { useCallback, useReducer } from "react";
import type { SSEEvent } from "@/features/research/types";
import { postResearchHandler } from "@/features/research/handler/post-research-handler";

type AgentState = {
  status: "idle" | "delta" | "done" | "error";
  content: string;
  error?: string;
};

type State = {
  status: "idle" | "inProgress" | "complete" | "error";
  agents: Partial<Record<string, AgentState>>;
};

type Action = SSEEvent | { type: "reset" };

function reducer(state: State, action: Action): State {
  if ("type" in action) {
    return { status: "inProgress", agents: {} };
  }

  switch (action.event) {
    case "delta": {
      return {
        ...state,
        status: "inProgress",
        agents: {
          ...state.agents,
          [action.agent]: {
            ...state.agents[action.agent],
            status: "delta",
            content: (state.agents[action.agent]?.content || "") + action.text,
          },
        },
      };
    }
    case "error": {
      if (!action.agent) {
        return { ...state, status: "error" };
      }
      return {
        ...state,
        status: "inProgress",
        agents: {
          ...state.agents,
          [action.agent]: {
            ...state.agents[action.agent],
            content: "",
            status: "error",
            error: action.error,
          },
        },
      };
    }
    case "done": {
      if (!action.agent) {
        return { ...state, status: "complete" };
      }
      return {
        ...state,
        agents: {
          ...state.agents,
          [action.agent]: {
            ...state.agents[action.agent],
            content: "",
            status: "done",
          },
        },
      };
    }
  }
}

export const useResearch = () => {
  const [state, dispatch] = useReducer(reducer, { status: "idle", agents: {} });

  const search = useCallback(async (query: string) => {
    dispatch({ type: "reset" });
    await postResearchHandler(query, dispatch);
  }, []);

  return { state, search };
};
