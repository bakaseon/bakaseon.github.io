import { defineConfig } from 'astro/config';

export default defineConfig({
  site: process.env.PUBLIC_SITE_URL || 'https://smart-calc-hub.pages.dev',
  build: {
    format: 'directory'
  }
});
