import { NavLink } from "react-router-dom";

import { CompassIcon, HomeIcon, SearchIcon, UserIcon } from "./icons";

const LINKS = [
  { to: "/", label: "Home", Icon: HomeIcon },
  { to: "/search", label: "Search", Icon: SearchIcon },
  { to: "/explore", label: "Explore", Icon: CompassIcon },
  { to: "/users/alice", label: "Profile", Icon: UserIcon },
];

export default function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-20 hidden w-[72px] flex-col border-r border-neutral-200 bg-white px-3 py-6 dark:border-neutral-800 dark:bg-neutral-950 sm:flex xl:w-60">
      <span className="mb-8 px-2 text-xl font-semibold tracking-tight">
        <span className="xl:hidden">F</span>
        <span className="hidden xl:inline">Feed</span>
      </span>

      <nav className="flex flex-col gap-1" aria-label="Main">
        {LINKS.map(({ to, label, Icon }) => (
          <NavLink
            key={to}
            to={to}
            // `end` keeps "/" from matching every route as active.
            end={to === "/"}
            className={({ isActive }) =>
              [
                "flex items-center gap-4 rounded-lg px-3 py-3 transition-colors",
                "hover:bg-neutral-100 dark:hover:bg-neutral-900",
                isActive ? "font-semibold" : "",
              ].join(" ")
            }
          >
            {({ isActive }) => (
              <>
                <Icon filled={isActive} />
                <span className="hidden xl:inline">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
