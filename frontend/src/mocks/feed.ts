import type { FeedItem } from "../api/types";

/**
 * TEMPORARY layout fixture — delete once GET /feed exists.
 *
 * Images come from picsum.photos with fixed seeds, so the same post always
 * renders the same photo. Aspect ratios deliberately vary (square, portrait,
 * landscape) to prove the feed reserves the right space for each one.
 */
function post(
  id: string,
  seed: string,
  width: number,
  height: number,
  author: string,
  source: string,
  title: string,
  topics: string[],
  strategy: FeedItem["strategy"],
  reason: string,
  score: number,
  daysAgo: number,
): FeedItem {
  const publishedAt = new Date(Date.now() - daysAgo * 86_400_000).toISOString();
  return {
    id,
    external_id: null,
    title,
    body: null,
    url: null,
    source,
    topics,
    author,
    published_at: publishedAt,
    score,
    created_at: publishedAt,
    updated_at: publishedAt,
    image_url: `https://picsum.photos/seed/${seed}/${width}/${height}`,
    image_width: width,
    image_height: height,
    image_content_type: "image/jpeg",
    image_bytes: null,
    thumbnail_url: null,
    ranking_score: score,
    strategy,
    reason,
  };
}

export const MOCK_FEED: FeedItem[] = [
  post(
    "1", "dolomites", 1080, 1080, "lina.hvass", "unsplash",
    "Golden hour over the Dolomites — three hours of hiking for ninety seconds of light.",
    ["mountains", "golden-hour", "landscape"],
    "ranked", "Popular in your feed", 1482, 1,
  ),
  post(
    "2", "tokyorain", 1080, 1350, "k.nakamura", "unsplash",
    "Shinjuku after the rain. Neon does something to wet asphalt that I still can't explain.",
    ["street", "night", "urban"],
    "collaborative", "People with your taste liked this", 967, 2,
  ),
  post(
    "3", "brutalism", 1200, 800, "marco.reyes", "flickr",
    "Concrete stairwell, Barbican Estate. Brutalism photographs better than it lives.",
    ["architecture", "minimal", "monochrome"],
    "content_based", "Similar to photos you saved", 734, 4,
  ),
  post(
    "4", "coastline", 1080, 1080, "ana.ferreira", "unsplash",
    "Low tide at dawn. Nobody on the beach except two dogs and a very committed heron.",
    ["ocean", "sunrise", "landscape"],
    "trending", "Trending in your topics", 2104, 5,
  ),
  post(
    "5", "studioportrait", 1080, 1350, "jules.weber", "unsplash",
    "One softbox, one reflector, one very patient friend.",
    ["portrait", "studio", "monochrome"],
    "collaborative", "People with your taste liked this", 553, 8,
  ),
];
