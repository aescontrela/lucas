import { createBrowserRouter } from "react-router";
import { Search } from "./pages/search/page";

export const router = createBrowserRouter([{ path: "/", element: <Search /> }]);
