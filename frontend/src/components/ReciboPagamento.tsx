import type { Pagamento } from '../types/api'

interface ReciboPagamentoProps {
  pagamento: Pagamento
  onNovoPagamento: () => void
}

export function ReciboPagamento({
  pagamento,
  onNovoPagamento,
}: ReciboPagamentoProps) {
  return (
    <div className="mx-auto max-w-md space-y-4 rounded-lg bg-white p-6 shadow dark:bg-zinc-900">
      <h1 className="text-xl font-semibold">Recibo de Pagamento</h1>

      <div className="space-y-1 text-sm text-zinc-700 dark:text-zinc-300">
        <p><strong>ID:</strong> #{pagamento.id}</p>
        <p><strong>Método:</strong> {pagamento.metodo}</p>
        <p><strong>Parcelas:</strong> {pagamento.parcelas}x</p>
        <p><strong>Valor da parcela:</strong> R$ {pagamento.valor_parcela}</p>

        {pagamento.informacoes_adicionais && (
          <p className="text-amber-600">
            {pagamento.informacoes_adicionais}
          </p>
        )}
      </div>

      <div className="border-t pt-4 text-lg font-semibold">
        Total pago: R$ {pagamento.total}
      </div>

      <button
        onClick={onNovoPagamento}
        className="w-full rounded bg-zinc-800 py-2 text-white hover:bg-zinc-700"
      >
        Novo pagamento
      </button>
    </div>
  )
}
