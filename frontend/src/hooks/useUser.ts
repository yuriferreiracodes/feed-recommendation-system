import { useQuery } from "@tanstack/react-query";

import { api } from "../api/client";
import type { User } from "../api/types";

/** Fetches a single user. Idle until a non-empty id is supplied. */
export function useUser(userId: string | null) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: async (): Promise<User> => {
      const { data } = await api.get<User>(`/users/${userId}`);
      return data;
    },
    enabled: Boolean(userId),
  });
}
