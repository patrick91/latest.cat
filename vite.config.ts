import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
	plugins: [react()],
	publicDir: "frontend/public",
	build: {
		manifest: true,
		outDir: "static/build",
		rollupOptions: {
			input: "frontend/app.tsx",
		},
	},
	server: {
		origin: "http://localhost:5173",
	},
});
