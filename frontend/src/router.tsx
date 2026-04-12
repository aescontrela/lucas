import { createBrowserRouter } from "react-router";
import { ResearchLayout } from "./features/research/layout";
import { Search } from "./features/research/pages/search/page";
import { Thread } from "./features/research/pages/thread/page";

export const router = createBrowserRouter([
  {
    element: <ResearchLayout />,
    children: [
      { path: "/", element: <Search /> },
      { path: "/thread", element: <Thread /> },
    ],
  },
]);
