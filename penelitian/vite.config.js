import { defineConfig } from 'vite';

export default defineConfig({
  root: './src',
  publicDir: './src/views',
  build: {
    outDir: 'build',
    rollupOptions: {
      input: {
        index: './src/views/index.html',
      },
    },
  },
  server: {
    port: 3000,
  },
});
