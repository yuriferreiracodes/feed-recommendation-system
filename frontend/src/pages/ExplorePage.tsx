import { MOCK_FEED } from "../mocks/feed";

/** Explore is a dense grid: the same items, no post chrome. */
export default function ExplorePage() {
  const items = [...MOCK_FEED, ...MOCK_FEED].slice(0, 9);

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="mb-4 text-lg font-semibold">Explore</h1>
      <div className="grid grid-cols-3 gap-1 sm:gap-2">
        {items.map((item, index) => (
          <div
            key={`${item.id}-${index}`}
            className="aspect-square overflow-hidden bg-neutral-100 dark:bg-neutral-900"
          >
            <img
              src={item.image_url}
              alt={item.title}
              loading="lazy"
              decoding="async"
              className="h-full w-full object-cover transition-transform hover:scale-105"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
