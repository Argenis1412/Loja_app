/**
 * Configuração centralizada da API
 * Por padrão usa a URL do backend no Render (produção)
 * Para desenvolvimento local, criar .env.local com VITE_API_URL=http://localhost:8000
 * 
 * @see https://vitejs.dev/guide/env-and-mode.html for environment variables
 */
// Garante que a URL base termine sem barra para evitar // na concatenação
const rawBaseUrl = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://127.0.0.1:8000');
const cleanBaseUrl = rawBaseUrl.replace(/\/$/, '');

// O prefixo /api/v1 é obrigatório para o contrato atual do backend
// Se a URL já contém /api/v1, não duplicamos
export const API_BASE_URL = cleanBaseUrl.includes('/api/v1') 
  ? cleanBaseUrl 
  : `${cleanBaseUrl}/api/v1`;

export const API_ENDPOINTS = {
  pagamentos: `${API_BASE_URL}/pagamentos/`,
  simular: `${API_BASE_URL}/pagamentos/simular`,
  saude: `${API_BASE_URL}/saude`,
} as const;
