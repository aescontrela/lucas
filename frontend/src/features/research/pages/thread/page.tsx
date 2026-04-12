import { useOutletContext, useSearchParams } from "react-router";
import type { useResearch } from "../../hooks";
import { useEffect } from "react";

export const Thread = () => {
  const [params] = useSearchParams();
  const { search, state } = useOutletContext<ReturnType<typeof useResearch>>();
  const query = params.get("q") ?? "";

  useEffect(() => {
    if (state.status === "idle" && query) {
      search(query);
    }
  }, [query, search, state.status]);

  return (
    <div>
      thread {JSON.stringify(state)} {params.get("q")}
    </div>
  );
};
