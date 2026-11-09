import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The API (db/api.py) has no CORS: in development Vite proxies /v1 to it.
export default defineConfig({
  plugins: [react()],
  server: { port: 5345, strictPort: true, proxy: { "/v1": process.env.CCP_API || "http://127.0.0.1:5344" } },
});
