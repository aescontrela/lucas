import { researchApi } from "@/api";
import { SSEEventSchema, type SSEEvent } from "@/features/research/types";

export const postResearchHandler = async (
  query: string,
  dispatch: React.Dispatch<SSEEvent>
) => {
  await researchApi.postResearch(query, (raw: Record<string, unknown>) => {
    if (raw.event === "router") return;

    const event = SSEEventSchema.safeParse(raw);

    if (!event.success) {
      console.warn("Invalid SSE event:", raw, event.error);
      return;
    }
    dispatch(event.data);
  });
};
