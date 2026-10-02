import type { FeedStrategy } from "../api/types";

interface StrategyBadgeProps {
  strategy: FeedStrategy;
  reason: string;
}

// One color per strategy, so you can read the feed's composition at a glance:
// how much is trending vs. collaborative vs. visual similarity.
const STYLES: Record<FeedStrategy, { label: string; className: string }> = {
  trending: {
    label: "Trending",
    className: "bg-sky-50 text-sky-700 dark:bg-sky-950 dark:text-sky-300",
  },
  collaborative: {
    label: "For you",
    className: "bg-violet-50 text-violet-700 dark:bg-violet-950 dark:text-violet-300",
  },
  content_based: {
    label: "Similar",
    className: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300",
  },
  ranked: {
    label: "Ranked",
    className: "bg-neutral-100 text-neutral-600 dark:bg-neutral-800 dark:text-neutral-300",
  },
};

export default function StrategyBadge({ strategy, reason }: StrategyBadgeProps) {
  const { label, className } = STYLES[strategy];
  return (
    <span
      // The reason is the tooltip: the badge says which engine picked this,
      // hovering says why.
      title={reason}
      className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${className}`}
    >
      {label}
    </span>
  );
}
