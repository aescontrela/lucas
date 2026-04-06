export type RouterEvent = {
  event: "router";
  data: {
    query: string;
    agents: { name: string; task: string }[];
  };
};

export type DeltaEvent = {
  event: "delta";
  agent: string;
  text: string;
};

export type DoneEvent = {
  event: "done";
  agent?: string;
};

export type ErrorEvent = {
  event: "error";
  agent?: string;
  error?: string;
  detail?: string;
};

export type SSEEvent = RouterEvent | DeltaEvent | DoneEvent | ErrorEvent;
