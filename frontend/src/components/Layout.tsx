import { Outlet, useLocation } from "react-router-dom";

import MobileNav from "./MobileNav";
import Sidebar from "./Sidebar";
import SuggestionsRail from "./SuggestionsRail";

export default function Layout() {
  // The rail is feed-specific chrome; search and profile get the full width.
  const showRail = useLocation().pathname === "/";

  return (
    <div className="min-h-full bg-neutral-50 text-neutral-900 dark:bg-black dark:text-neutral-100">
      <Sidebar />
      <MobileNav />

      {/* Offset matches the sidebar's two widths (72px, then 240px at xl). */}
      <div className="sm:pl-[72px] xl:pl-60">
        <div className="mx-auto flex justify-center gap-0 px-0 pb-20 sm:px-6 sm:pb-8">
          <main className="w-full max-w-[470px] py-0 sm:py-8">
            <Outlet />
          </main>
          {showRail && <SuggestionsRail />}
        </div>
      </div>
    </div>
  );
}
