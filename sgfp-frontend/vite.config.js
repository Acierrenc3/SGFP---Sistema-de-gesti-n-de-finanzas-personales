// Configuración de Vite con Tailwind CSS
// Basado en: https://tailwindcss.com/docs/installation/using-vite

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    port: 5173,
  }
})