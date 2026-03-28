/**
 * Utilitário para realizar chamadas fetch com retry automático em caso de falhas de rede.
 */
export async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retries = 3,
  backoff = 1000
): Promise<Response> {
  try {
    const response = await fetch(url, options);
    
    // Se for erro de servidor (5xx), podemos tentar de novo se o usuário desejar,
    // mas por padrão retentamos apenas erros de rede (lançados pelo fetch).
    // Aqui incluímos 503 (Service Unavailable) e 504 (Gateway Timeout) como passíveis de retry.
    if (!response.ok && [503, 504].includes(response.status) && retries > 0) {
      console.warn(`Erro ${response.status} detectado. Tentando novamente em ${backoff}ms... (${retries} tentativas restantes)`);
      await new Promise(resolve => setTimeout(resolve, backoff));
      return fetchWithRetry(url, options, retries - 1, backoff * 2);
    }
    
    return response;
  } catch (error) {
    if (retries > 0) {
      console.warn(`Falha na rede: ${error}. Tentando novamente em ${backoff}ms... (${retries} tentativas restantes)`);
      await new Promise(resolve => setTimeout(resolve, backoff));
      return fetchWithRetry(url, options, retries - 1, backoff * 2);
    }
    throw error;
  }
}
