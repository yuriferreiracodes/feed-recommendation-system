import Avatar from "./Avatar";

// Placeholder content until GET /recommendations is available.
const CURRENT_USER = { username: "alice_dev", subtitle: "Your feed" };

const SUGGESTED_TOPICS = [
  { topic: "golden-hour", reason: "From photos you liked" },
  { topic: "architecture", reason: "Similar to your saves" },
  { topic: "street", reason: "Popular with similar users" },
  { topic: "monochrome", reason: "Trending in your topics" },
];

export default function SuggestionsRail() {
  return (
    <aside className="hidden w-[320px] shrink-0 pl-8 pt-8 lg:block">
      <div className="flex items-center gap-3">
        <Avatar name={CURRENT_USER.username} />
        <div className="min-w-0 flex-1 leading-tight">
          <p className="truncate text-sm font-semibold">{CURRENT_USER.username}</p>
          <p className="truncate text-xs text-neutral-500 dark:text-neutral-400">
            {CURRENT_USER.subtitle}
          </p>
        </div>
        <button type="button" className="text-xs font-semibold text-sky-600 hover:text-sky-800">
          Switch
        </button>
      </div>

      <div className="mt-6">
        <h2 className="mb-3 text-sm font-semibold text-neutral-500 dark:text-neutral-400">
          Recommended for you
        </h2>
        <ul className="space-y-3">
          {SUGGESTED_TOPICS.map(({ topic, reason }) => (
            <li key={topic} className="flex items-center gap-3">
              <Avatar name={topic} size="sm" />
              <div className="min-w-0 flex-1 leading-tight">
                <p className="truncate text-sm font-semibold">#{topic}</p>
                <p className="truncate text-xs text-neutral-500 dark:text-neutral-400">{reason}</p>
              </div>
              <button
                type="button"
                className="text-xs font-semibold text-sky-600 hover:text-sky-800"
              >
                Follow
              </button>
            </li>
          ))}
        </ul>
      </div>

      <p className="mt-8 text-[11px] leading-relaxed text-neutral-400">
        Feed Recommendation System — ranking in Redis, visual similarity in Elasticsearch.
      </p>
    </aside>
  );
}
