import { useEffect, useState } from "react";
import { listarPagamentos } from "../services/api";
import type { PagamentoResponse } from "../types/api";
import { Recibo } from "../components/Recibo";

export function Home() {
  const [pagamentos, setPagamentos] = useState<PagamentoResponse[]>([]);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    listarPagamentos()
      .then(setPagamentos)
      .catch(() => setErro("Erro ao carregar pagamentos"));
  }, []);

  if (erro) {
    return <p className="text-red-500 text-center">{erro}</p>;
  }

  return (
    <div className="min-h-screen bg-zinc-100 dark:bg-zinc-950 p-6">
      <div className="space-y-6">
        {pagamentos.map((pagamento, index) => (
          <Recibo key={pagamento.id ?? index} pagamento={pagamento} />
        ))}
      </div>
    </div>
  );
}