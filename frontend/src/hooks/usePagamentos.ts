import { useEffect, useState } from 'react';
import type { Pagamento } from '../types/api';
import { listarPagamentos } from '../services/api';

export function usePagamentos() {
  const [pagamentos, setPagamentos] = useState<Pagamento[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function carregar() {
      try {
        const dados = await listarPagamentos();
        setPagamentos(dados);
      } catch {
        setErro('Erro ao carregar pagamentos');
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, []);

  return { pagamentos, carregando, erro };
}
