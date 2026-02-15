import type { Pagamento } from '../types/api';

interface ReciboProps {
  pagamento: Pagamento;
  onNovoPagamento?: () => void;
}

export function Recibo({ pagamento, onNovoPagamento }: ReciboProps) {
  // Formatar data para exibição amigável
  const dataFormatada = new Date(pagamento.created_at).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  // Determinar cor do badge baseado no método
  const getMetodoColor = (metodo: string) => {
    if (metodo.includes('vista') || metodo.toLowerCase().includes('débito')) {
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300';
    }
    if (metodo.toLowerCase().includes('sem juros')) {
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300';
    }
    return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300';
  };

  return (
    <div className="mx-auto max-w-md space-y-6 rounded-xl bg-white p-8 shadow-xl dark:bg-zinc-900 animate-fade-in border border-zinc-200 dark:border-zinc-800">
      <div className="text-center">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-green-400 to-green-600 text-white dark:from-green-500 dark:to-green-700 shadow-lg animate-bounce-once">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={3}
            stroke="currentColor"
            className="h-8 w-8"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M4.5 12.75l6 6 9-13.5"
            />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-zinc-800 dark:text-zinc-100 mb-2">
          🎉 Pagamento confirmado!
        </h2>
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          Sua compra foi processada com sucesso
        </p>
      </div>

      <div className="space-y-4 rounded-xl border-2 border-zinc-200 bg-gradient-to-br from-zinc-50 to-zinc-100 p-5 dark:border-zinc-800 dark:from-zinc-800/50 dark:to-zinc-800/30 shadow-inner">
        <div className="flex justify-between items-center text-sm pb-3 border-b border-zinc-300 dark:border-zinc-700">
          <span className="text-zinc-600 dark:text-zinc-400 font-medium">🔖 ID da Transação</span>
          <span className="font-mono font-bold text-zinc-800 dark:text-zinc-200 bg-white dark:bg-zinc-900 px-3 py-1 rounded-md border border-zinc-300 dark:border-zinc-700">
            #{pagamento.id}
          </span>
        </div>
        
        <div className="flex justify-between items-center text-sm pb-3 border-b border-zinc-300 dark:border-zinc-700">
          <span className="text-zinc-600 dark:text-zinc-400 font-medium">📅 Data e Hora</span>
          <span className="text-zinc-800 dark:text-zinc-200 font-semibold">
            {dataFormatada}
          </span>
        </div>

        <div className="flex justify-between items-center text-sm pb-3 border-b border-zinc-300 dark:border-zinc-700">
          <span className="text-zinc-600 dark:text-zinc-400 font-medium">💳 Método de Pagamento</span>
          <span className={`text-xs font-bold px-3 py-1.5 rounded-full ${getMetodoColor(pagamento.metodo)}`}>
            {pagamento.metodo}
          </span>
        </div>

        {pagamento.parcelas > 1 && (
          <div className="text-sm pb-3 border-b border-zinc-300 dark:border-zinc-700 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-zinc-600 dark:text-zinc-400 font-medium">📊 Parcelamento</span>
              <div className="text-zinc-800 dark:text-zinc-200 font-bold">
                {pagamento.parcelas}x parcelas
              </div>
            </div>
            {pagamento.valor_ultima_parcela && Math.abs(pagamento.valor_ultima_parcela - pagamento.valor_parcela) > 0.01 ? (
              <div className="text-xs text-zinc-600 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-900 p-3 rounded-lg border border-zinc-200 dark:border-zinc-700">
                <div className="flex justify-between mb-1">
                  <span>• {pagamento.parcelas - 1}x de</span>
                  <span className="font-semibold">R$ {pagamento.valor_parcela.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>• 1x de (última)</span>
                  <span className="font-semibold text-green-600 dark:text-green-400">R$ {pagamento.valor_ultima_parcela.toFixed(2)}</span>
                </div>
              </div>
            ) : (
              <div className="text-xs text-zinc-600 dark:text-zinc-400 text-right">
                R$ {pagamento.valor_parcela.toFixed(2)} cada parcela
              </div>
            )}
          </div>
        )}

        <div className="pt-2">
          <div className="flex justify-between items-center">
            <span className="text-base font-bold text-zinc-700 dark:text-zinc-200">💰 Total Pago</span>
            <span className="text-2xl font-bold text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-4 py-2 rounded-lg">
              R$ {pagamento.total.toFixed(2)}
            </span>
          </div>
        </div>
      </div>

      {pagamento.informacoes_adicionais && (
        <div className="rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-4 text-center border-2 border-blue-200 dark:border-blue-800">
          <div className="flex items-center justify-center gap-2 text-sm font-semibold text-blue-800 dark:text-blue-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
            </svg>
            {pagamento.informacoes_adicionais}
          </div>
        </div>
      )}

      {onNovoPagamento && (
        <button
          onClick={onNovoPagamento}
          className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 py-3 font-semibold text-white transition-all hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-zinc-900 shadow-md hover:shadow-lg transform hover:scale-[1.02]"
        >
          🛒 Fazer novo pagamento
        </button>
      )}
    </div>
  );
}
