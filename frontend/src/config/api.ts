/**
 * Configuração centralizada da API
 * Por padrão usa a URL do backend no Render (produção)
 * Para desenvolvimento local, criar .env.local com VITE_API_URL=http://localhost:8000
 * 
 * @see https://vitejs.dev/guide/env-and-mode.html for environment variables
 */
// Normalização da URL base para evitar duplicação de prefixos como /api/api/v1
const rawBaseUrl = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://127.0.0.1:8000');
const cleanBaseUrl = rawBaseUrl.replace(/\/$/, '');

function getBaseApiUrl(baseUrl: string): string {
  // Se já tem o caminho completo, retorna como está
  if (baseUrl.includes('/api/v1')) return baseUrl;
  
  // Se tem apenas /api, adiciona o /v1
  if (baseUrl.endsWith('/api')) return `${baseUrl}/v1`;
  
  // Se não tem nada, adiciona o caminho completo padrão
  return `${baseUrl}/api/v1`;
}

export const API_BASE_URL = getBaseApiUrl(cleanBaseUrl);

export const API_ENDPOINTS = {
  pagamentos: `${API_BASE_URL}/pagamentos/`,
  simular: `${API_BASE_URL}/pagamentos/simular`,
  saude: `${API_BASE_URL}/saude`,
} as const;
