/**
 * Configuração centralizada da API
 * Por padrão usa a URL do backend no Render (produção)
 * Para desenvolvimento local, criar .env.local com VITE_API_URL=http://localhost:8000
 * 
 * @see https://vitejs.dev/guide/env-and-mode.html for environment variables
 */
export const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '/api/v1' : 'http://127.0.0.1:8000/api/v1');

export const API_ENDPOINTS = {
  pagamentos: `${API_BASE_URL}/pagamentos/`,
  simular: `${API_BASE_URL}/pagamentos/simular`,
  saude: `${API_BASE_URL}/saude`,
} as const;
