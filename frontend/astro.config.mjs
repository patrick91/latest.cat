import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import vercel from "@astrojs/vercel/serverless";
import react from "@astrojs/react";

import metaTags from "astro-meta-tags";

// https://astro.build/config
export default defineConfig({
  output: "server",
  integrations: [tailwind(), react(), metaTags()],
  adapter: vercel()
});