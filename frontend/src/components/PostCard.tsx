import { useState } from "react";

import type { FeedItem } from "../api/types";
import Avatar from "./Avatar";
import StrategyBadge from "./StrategyBadge";
import { BookmarkIcon, HeartIcon, ShareIcon } from "./icons";

interface PostCardProps {
  item: FeedItem;
}

function relativeTime(iso: string): string {
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / 86_400_000);
  if (days <= 0) return "TODAY";
  if (days === 1) return "1 DAY AGO";
  if (days < 7) return `${days} DAYS AGO`;
  const weeks = Math.floor(days / 7);
  return weeks === 1 ? "1 WEEK AGO" : `${weeks} WEEKS AGO`;
}

export default function PostCard({ item }: PostCardProps) {
  // Local-only for now: these map to the weighted events (like 3.0, share 4.0,
  // bookmark 3.0) and get wired to POST /events in the tracking block.
  const [liked, setLiked] = useState(false);
  const [saved, setSaved] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const handle = item.author ?? item.source ?? "unknown";
  const likeCount = item.score + (liked ? 1 : 0);

  return (
    <article className="border-b border-neutral-200 bg-white pb-4 dark:border-neutral-800 dark:bg-neutral-950 sm:mb-6 sm:rounded-lg sm:border">
      <header className="flex items-center gap-3 px-4 py-3">
        <Avatar name={handle} ring />
        <div className="min-w-0 flex-1 leading-tight">
          <p className="truncate text-sm font-semibold">{handle}</p>
          {item.source && (
            <p className="truncate text-xs text-neutral-500 dark:text-neutral-400">{item.source}</p>
          )}
        </div>
        <StrategyBadge strategy={item.strategy} reason={item.reason} />
      </header>

      {/* The intrinsic ratio reserves the slot before the image arrives, so the
          feed never jumps while scrolling. Content with no upload yet keeps a
          square placeholder rather than collapsing the card. */}
      <div
        className="w-full overflow-hidden bg-neutral-100 dark:bg-neutral-900"
        style={{ aspectRatio: `${item.image_width ?? 1} / ${item.image_height ?? 1}` }}
      >
        {item.image_url && (
          <img
            src={item.image_url}
            alt={item.title}
            width={item.image_width ?? undefined}
            height={item.image_height ?? undefined}
            loading="lazy"
            decoding="async"
            className="h-full w-full object-cover"
          />
        )}
      </div>

      <div className="flex items-center gap-4 px-4 pt-3">
        <button
          type="button"
          onClick={() => setLiked((v) => !v)}
          aria-pressed={liked}
          aria-label={liked ? "Unlike" : "Like"}
          className={`transition-colors ${liked ? "text-rose-500" : "hover:text-neutral-500"}`}
        >
          <HeartIcon filled={liked} />
        </button>
        <button type="button" aria-label="Share" className="transition-colors hover:text-neutral-500">
          <ShareIcon />
        </button>
        <button
          type="button"
          onClick={() => setSaved((v) => !v)}
          aria-pressed={saved}
          aria-label={saved ? "Remove bookmark" : "Bookmark"}
          className="ml-auto transition-colors hover:text-neutral-500"
        >
          <BookmarkIcon filled={saved} />
        </button>
      </div>

      <div className="px-4 pt-2 text-sm">
        <p className="font-semibold">{likeCount.toLocaleString()} interactions</p>

        <p className={`mt-1 ${expanded ? "" : "line-clamp-2"}`}>
          <span className="mr-1.5 font-semibold">{handle}</span>
          {item.title}
        </p>
        {!expanded && item.title.length > 80 && (
          <button
            type="button"
            onClick={() => setExpanded(true)}
            className="text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300"
          >
            more
          </button>
        )}

        {item.topics && item.topics.length > 0 && (
          <p className="mt-1.5 text-sky-700 dark:text-sky-400">
            {item.topics.map((topic) => `#${topic}`).join(" ")}
          </p>
        )}

        {item.published_at && (
          <p className="mt-2 text-[11px] uppercase tracking-wide text-neutral-400">
            {relativeTime(item.published_at)}
          </p>
        )}
      </div>
    </article>
  );
}
