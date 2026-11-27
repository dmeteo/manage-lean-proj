import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig(({ command, mode }) => ({
  plugins: [react()],
  publicDir: command === 'serve' && mode === 'demo' ? 'demo-public' : false,
}))
