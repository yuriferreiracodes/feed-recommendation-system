// TypeScript mirrors of the backend Pydantic schemas (backend/schemas/*.py).
// Datetimes arrive as ISO-8601 strings over JSON, so they are typed as `string`.

export interface User {
  id: string;
  username: string;
  email: string;
  preferences: Record<string, string[]>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Content {
  id: string;
  external_id: string | null;
  title: string;
  body: string | null;
  url: string | null;
  source: string | null;
  topics: string[] | null;
  author: string | null;
  published_at: string | null;
  score: number;
  created_at: string;
  updated_at: string;

  // --- Media ---------------------------------------------------------------
  // Not on the backend model yet: the image pivot needs a migration adding
  // these columns. Intrinsic width/height are required, not decorative — the
  // feed reserves each slot's space before the image loads to avoid reflow.
  image_url: string;
  image_width: number;
  image_height: number;
  // Tiny base64 preview rendered while the full image streams in.
  thumbnail_url: string | null;
}

export type EventType = "view" | "click" | "like" | "share" | "skip" | "bookmark";

export interface EventCreate {
  user_id: string;
  content_id: string;
  event_type: EventType;
  metadata?: Record<string, unknown>;
  occurred_at?: string;
}

export interface Event {
  id: string;
  user_id: string;
  content_id: string;
  event_type: EventType;
  weight: number;
  metadata: Record<string, unknown> | null;
  occurred_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export interface HealthResponse {
  status: string;
  services: Record<string, string>;
}

// --- Feed & search -----------------------------------------------------------
// These endpoints do not exist on the backend yet (feed ranking and search are
// still to be built). The shapes below follow the planned API contract; verify
// them against the real Pydantic schemas once those routers land.

export type FeedStrategy = "ranked" | "collaborative" | "content_based" | "trending";

export interface FeedItem extends Content {
  ranking_score: number;
  strategy: FeedStrategy;
  reason: string;
}

export interface FeedResponse {
  items: FeedItem[];
  user_id: string;
  page: number;
  total: number;
  has_next: boolean;
  cache_hit: boolean;
  generated_at: string;
}

export interface SearchHit {
  id: string;
  title: string;
  source: string | null;
  topics: string[];
  score: number;
  highlights: string[];
}

export interface SearchResponse {
  hits: SearchHit[];
  total: number;
  took_ms: number;
  query: string;
}
