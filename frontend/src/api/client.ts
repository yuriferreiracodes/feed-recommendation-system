import axios, { AxiosError } from "axios";

/** Normalized error shape every caller can rely on, whatever axios threw. */
export interface ApiError {
  message: string;
  code?: string;
  status?: number;
}

// Relative base URL: in dev the Vite proxy forwards to the backend, in
// production a reverse proxy serves both the app and the API on one origin.
export const api = axios.create({
  baseURL: "/api/v1",
  headers: { "Content-Type": "application/json" },
  timeout: 15_000,
});

api.interceptors.request.use((config) => {
  if (import.meta.env.DEV) {
    console.debug(`[api] ${config.method?.toUpperCase()} ${config.url}`);
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string; code?: string }>) => {
    const data = error.response?.data;
    const apiError: ApiError = {
      // The backend's error handler returns { detail, code } (backend/exceptions.py).
      message: data?.detail ?? error.message ?? "Unexpected error",
      code: data?.code,
      status: error.response?.status,
    };
    return Promise.reject(apiError);
  },
);

export function isApiError(error: unknown): error is ApiError {
  return typeof error === "object" && error !== null && "message" in error;
}
