import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// /api проксується на FastAPI, тож CORS у dev не потрібен
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
