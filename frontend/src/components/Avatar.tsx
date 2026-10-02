interface AvatarProps {
  name: string;
  size?: "sm" | "md";
  ring?: boolean;
}

// Deterministic hue from the name, so the same account always gets the same
// color without storing an avatar image anywhere.
function hueFor(name: string): number {
  let hash = 0;
  for (let i = 0; i < name.length; i += 1) {
    hash = (hash * 31 + name.charCodeAt(i)) % 360;
  }
  return hash;
}

export default function Avatar({ name, size = "md", ring = false }: AvatarProps) {
  const dimension = size === "sm" ? "h-8 w-8 text-xs" : "h-10 w-10 text-sm";
  const initials = name.slice(0, 2).toUpperCase();
  const hue = hueFor(name);

  return (
    <span
      className={[
        dimension,
        "flex shrink-0 items-center justify-center rounded-full font-semibold text-white",
        ring ? "ring-2 ring-offset-2 ring-rose-400 ring-offset-white dark:ring-offset-neutral-950" : "",
      ].join(" ")}
      style={{ backgroundColor: `hsl(${hue} 55% 45%)` }}
      aria-hidden="true"
    >
      {initials}
    </span>
  );
}
