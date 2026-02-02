import type { Pagamento } from '../types/api'

interface ReciboProps {
  pagamento: Pagamento
  onNovoPagamento?: () => void
}

export function Recibo({ pagamento, onNovoPagamento }: ReciboProps) {
  // Formatar data para exibição amigável
  const dataFormatada = new Date(pagamento.created_at).toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  return (
    <div className="mx-auto max-w-md space-y-6 rounded-lg bg-white p-6 shadow dark:bg-zinc-900 animate-fade-in">
      <div className="text-center">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
            className="h-6 w-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M4.5 12.75l6 6 9-13.5"
            />
          </svg>
        </div>
        <h2 className="text-xl font-semibold text-zinc-800 dark:text-zinc-100">
          Pagamento confirmado!
        </h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Sua compra foi processada com sucesso.
        </p>
      </div>

      <div className="space-y-4 rounded-lg border border-zinc-100 bg-zinc-50 p-4 dark:border-zinc-800 dark:bg-zinc-800/50">
        <div className="flex justify-between text-sm">
          <span className="text-zinc-500">ID da Transação</span>
          <span className="font-mono text-zinc-700 dark:text-zinc-300">
            #{pagamento.id}
          </span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-zinc-500">Data</span>
          <span className="text-zinc-700 dark:text-zinc-300">
            {dataFormatada}
          </span>
        </div>
        
        <div className="my-2 border-t border-zinc-200 dark:border-zinc-700"></div>

        <div className="flex justify-between text-base font-bold">
          <span className="text-zinc-800 dark:text-zinc-100">Total Pago</span>
          <span className="text-green-600 dark:text-green-400">
            R$ {pagamento.total.toFixed(2)}
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span className="text-zinc-500">Método</span>
          <span className="text-zinc-700 dark:text-zinc-300">
            {pagamento.metodo}
          </span>
        </div>

        {pagamento.parcelas > 1 && (
          <div className="flex justify-between text-sm">
            <span className="text-zinc-500">Parcelas</span>
            <span className="text-zinc-700 dark:text-zinc-300">
              {pagamento.parcelas}x de R$ {pagamento.valor_parcela.toFixed(2)}
            </span>
          </div>
        )}
      </div>

      {pagamento.informacoes_adicionais && (
        <div className="rounded-md bg-blue-50 p-3 text-center text-sm text-blue-700 dark:bg-blue-900/20 dark:text-blue-200">
          {pagamento.informacoes_adicionais}
        </div>
      )}

      {onNovoPagamento && (
        <button
          onClick={onNovoPagamento}
          className="w-full rounded-lg bg-blue-600 py-2.5 font-medium text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-zinc-900"
        >
          Fazer novo pagamento
        </button>
      )}
    </div>
  )
}