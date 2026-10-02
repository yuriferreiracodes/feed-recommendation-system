import { QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import ErrorBoundary from "./components/ErrorBoundary";
import Layout from "./components/Layout";
import { queryClient } from "./lib/queryClient";
import ExplorePage from "./pages/ExplorePage";
import FeedPage from "./pages/FeedPage";
import SearchPage from "./pages/SearchPage";
import UserPage from "./pages/UserPage";

export default function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            {/* Layout renders the chrome and an <Outlet /> for these children. */}
            <Route element={<Layout />}>
              <Route path="/" element={<FeedPage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/explore" element={<ExplorePage />} />
              <Route path="/users/:id" element={<UserPage />} />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

function NotFound() {
  return (
    <div className="py-16 text-center">
      <h1 className="text-2xl font-semibold text-neutral-900 dark:text-neutral-100">Page not found</h1>
      <p className="mt-2 text-neutral-500 dark:text-neutral-400">
        The page you are looking for does not exist.
      </p>
    </div>
  );
}
