import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  use: { ...devices['Desktop Chrome'], baseURL: 'http://127.0.0.1:5174' },
  webServer: {
    command: 'npm run dev:demo',
    url: 'http://127.0.0.1:5174',
    reuseExistingServer: true,
  },
})
