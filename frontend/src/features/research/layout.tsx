import { Outlet } from "react-router";
import { useResearch } from "@/features/research/hooks";

export const ResearchLayout = () => {
  const research = useResearch();

  return (
    <>
      <Outlet context={research} />
    </>
  );
};
