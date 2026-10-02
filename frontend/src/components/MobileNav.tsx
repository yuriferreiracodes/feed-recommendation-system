import { NavLink } from "react-router-dom";

import { CompassIcon, HomeIcon, SearchIcon, UserIcon } from "./icons";

const LINKS = [
  { to: "/", label: "Home", Icon: HomeIcon },
  { to: "/search", label: "Search", Icon: SearchIcon },
  { to: "/explore", label: "Explore", Icon: CompassIcon },
  { to: "/users/alice", label: "Profile", Icon: UserIcon },
];

/** Bottom tab bar: the sidebar's role below the `sm` breakpoint. */
export default function MobileNav() {
  return (
    <nav
      aria-label="Main"
      className="fixed inset-x-0 bottom-0 z-20 flex justify-around border-t border-neutral-200 bg-white py-2 dark:border-neutral-800 dark:bg-neutral-950 sm:hidden"
    >
      {LINKS.map(({ to, label, Icon }) => (
        <NavLink key={to} to={to} end={to === "/"} aria-label={label} className="p-2">
          {({ isActive }) => <Icon filled={isActive} />}
        </NavLink>
      ))}
    </nav>
  );
}
