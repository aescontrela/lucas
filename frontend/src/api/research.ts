import { type SSEEvent } from "./types";

export const researchApi = {
  postResearch: async (query: string, onEvent: (event: SSEEvent) => void) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/research`, {
      method: "POST",
      body: JSON.stringify({ query }),
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      throw new Error("Failed to submit a research query");
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    if (!reader) {
      throw new Error("Failed to read the response");
    }

    while (true) {
      const { done, value } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      const chunks = buffer.split("\n\n");

      buffer = chunks.pop() || "";

      for (const chunk of chunks) {
        const line = chunk.replace(/^data: /, "");
        if (line) {
          onEvent(JSON.parse(line));
        }
      }
    }
  },
};
