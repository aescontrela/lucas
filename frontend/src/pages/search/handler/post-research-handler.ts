import { researchApi } from "../../../api";
import { type ResearchEvent, ResearchEventSchema } from "../types";

export const postResearchHandler = async (
  query: string,
  dispatch: React.Dispatch<ResearchEvent>
) => {
  await researchApi.postResearch(query, (raw: Record<string, unknown>) => {
    const event = ResearchEventSchema.safeParse({
      source: raw.agent,
      status: raw.event,
      content: raw.text,
      error: raw.error,
    });

    if (event.error) {
      console.warn("Invalid SSE event:", raw, event.error);
      return;
    }
    dispatch(event.data);
  });
};
