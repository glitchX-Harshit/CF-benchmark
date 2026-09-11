import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    // Keep React and its renderer on the same module instance as libraries such as Framer Motion.
    dedupe: ['react', 'react-dom'],
  },
})
