
import { defineConfig } from 'vite'
import fs from 'fs'
import path from 'path'

export default defineConfig({
  server: {
    host: true,  // écoute toutes les interfaces réseau
    port: 5173,
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'mkcert_keys/172.20.10.2+2-key.pem')),
      cert: fs.readFileSync(path.resolve(__dirname, 'mkcert_keys/172.20.10.2+2.pem'))
    },
    proxy: {
      '/api': {
        target: 'https://172.20.10.2', // ou 'https://192.168.x.x'
        changeOrigin: true,
        secure: false // à cause du certificat self-signed
      },
      '/peer': {
        target: 'https://172.20.10.2',
        changeOrigin: true,
        secure: false
      }
    },
    hmr:{
      'overlay': false
    }
  }
})
