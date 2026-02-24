import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 9021,
    proxy: {
      '/api': 'http://localhost:9020'
    }
  },
  build: {
    outDir: '../backend/static'
  }
})
