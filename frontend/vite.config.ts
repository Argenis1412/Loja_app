/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/tests/setup.ts'],
    // Configurações para evitar timeout em máquinas mais lentas
    fileParallelism: false,
    testTimeout: 60000,
    hookTimeout: 60000,
    env: {
      // Define URL do backend para testes (localhost)
      VITE_API_URL: 'http://localhost:8000',
    },
  },
})
