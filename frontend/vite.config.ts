import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  // Empty prefix so plain (non-VITE_) process env vars are visible here. Nothing
  // from this object is exposed to the client — it only configures the dev server.
  const env = loadEnv(mode, process.cwd(), "");
  // On the host the backend is on localhost; inside Docker it answers to the
  // compose service name, which is why this is an env var and not a literal.
  const backendUrl = env.BACKEND_URL || "http://localhost:8000";

  return {
    plugins: [react()],
    server: {
      port: 5173,
      // Dev-only: lets the app call "/api/v1/..." on its own origin, so there are
      // no CORS preflights and no base-URL switching between environments.
      // In production this hop is a reverse proxy's job (nginx), not Vite's.
      proxy: {
        "/api": {
          target: backendUrl,
          changeOrigin: true,
        },
      },
    },
  };
});
