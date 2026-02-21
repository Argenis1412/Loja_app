/**
 * Configuração centralizada da API
 * Por padrão usa a URL do backend no Render (produção)
 * Para desenvolvimento local, criar .env.local com VITE_API_URL=http://localhost:8000
 */
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://loja-app.onrender.com';

export const API_ENDPOINTS = {
  pagamentos: `${API_BASE_URL}/pagamentos/`,
  simular: `${API_BASE_URL}/pagamentos/simular`,
} as const;
