import PostCard from "../components/PostCard";
import { MOCK_FEED } from "../mocks/feed";

export default function FeedPage() {
  // Fixture data: swap for the useFeed() query once GET /feed exists.
  const items = MOCK_FEED;

  return (
    <div>
      {items.map((item) => (
        <PostCard key={item.id} item={item} />
      ))}

      <p className="px-4 py-8 text-center text-sm text-neutral-400">
        End of feed — more items arrive once the feed API is wired up.
      </p>
    </div>
  );
}
