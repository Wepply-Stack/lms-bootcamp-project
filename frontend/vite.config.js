import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from "path"

export default defineConfig(({ mode }) => {
  const apiUrl = mode === 'production' 
    ? 'https://lms-wfpq.onrender.com'
    : 'http://localhost:8000'
  
  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl),
      'import.meta.env.VITE_APP_NAME': JSON.stringify('frontend'),
    }
  }
})
