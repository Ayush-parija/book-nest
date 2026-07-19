import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for the React application
export default defineConfig({
  // Register the React plugin
  plugins: [react()],
})