import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const BACKEND_ORIGIN = /^https?:\/\//i.test(process.env.VITE_API_BASE_URL || '')
  ? new URL(process.env.VITE_API_BASE_URL).origin
  : 'http://127.0.0.1:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: BACKEND_ORIGIN,
        changeOrigin: true,
      },
      // Forward /uploads/* to the FastAPI backend so that uploaded images
      // (gallery, pastoral team photos) load correctly in the dev server.
      '/uploads': {
        target: BACKEND_ORIGIN,
        changeOrigin: true,
      },
    },
  },
})
