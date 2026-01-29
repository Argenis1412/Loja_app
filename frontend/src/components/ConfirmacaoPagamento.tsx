import type { CriarPagamentoRequest } from '../types/api'

interface ConfirmacaoPagamentoProps {
  dados: CriarPagamentoRequest
  onConfirmar: () => void
  onVoltar: () => void
  loading?: boolean
}

export function ConfirmacaoPagamento({
  dados,
  onConfirmar,
  onVoltar,
  loading,
}: ConfirmacaoPagamentoProps) {
  const DESCONTO_VISTA = 10 // percent
  const JUROS_PARCELAMENTO = 10 // percent
  const DESCONTO_DEBITO = 5 // percent

  const parcelas = dados.parcelas ?? 1

  let totalPreview = dados.valor
  let valorParcelaPreview = dados.valor
  let informacaoPreview: string | null = null

  if (dados.metodo === 'avista') {
    totalPreview = Number((dados.valor * (1 - DESCONTO_VISTA / 100)).toFixed(2))
    valorParcelaPreview = totalPreview
    informacaoPreview = `${DESCONTO_VISTA}% de desconto à vista`
  } else if (dados.metodo === 'parcelado_sem_juros') {
    totalPreview = Number(dados.valor.toFixed(2))
    valorParcelaPreview = Number((totalPreview / parcelas).toFixed(2))
    informacaoPreview = `Parcelado em ${parcelas}x sem juros`
  } else if (dados.metodo === 'cartao_com_juros') {
    totalPreview = Number((dados.valor * (1 + JUROS_PARCELAMENTO / 100)).toFixed(2))
    valorParcelaPreview = Number((totalPreview / parcelas).toFixed(2))
    informacaoPreview = `${JUROS_PARCELAMENTO}% de juros`
  }
  if (dados.metodo === 'debito') {
    totalPreview = Number((dados.valor * (1 - DESCONTO_DEBITO / 100)).toFixed(2))
    valorParcelaPreview = totalPreview
    informacaoPreview = `${DESCONTO_DEBITO}% de desconto no débito`
  }
  return (
    <div className="mx-auto max-w-md space-y-6 rounded-lg bg-white p-6 shadow dark:bg-zinc-900">
      <header className="text-center">
        <h2 className="text-xl font-semibold text-zinc-800 dark:text-zinc-100">
          Confirmação de pagamento
        </h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Revise os detalhes antes de confirmar o pagamento
        </p>
      </header>

      <div className="mb-4 rounded-xl border p-4 bg-zinc-50 dark:bg-zinc-900">
        <h3 className="font-semibold text-zinc-700 dark:text-zinc-200">Compra simulada</h3>
        <p className="text-sm text-zinc-500">Resumo rápido do pedido para validação</p>
      </div>

      <div className="space-y-2 text-sm text-zinc-700 dark:text-zinc-300">
        <div className="flex justify-between">
          <span className="font-medium">Forma</span>
          <span>{formatarMetodo(dados.metodo)}</span>
        </div>

        <div className="flex justify-between">
          <span className="font-medium">Total a pagar</span>
          <span>R$ {totalPreview.toFixed(2)}</span>
        </div>

        <div className="flex justify-between">
          <span className="font-medium">Parcelas</span>
          <span>{parcelas}x • R$ {valorParcelaPreview.toFixed(2)}</span>
        </div>

        {informacaoPreview && (
          <div className="text-xs text-zinc-500">{informacaoPreview}</div>
        )}
      </div>

      <div className="flex gap-3">
        <button
          onClick={onVoltar}
          className="w-full rounded border border-zinc-300 py-2 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800"
        >
          ← Voltar
        </button>

        <button
          onClick={onConfirmar}
          disabled={loading}
          className="w-full rounded bg-green-600 py-2 font-medium text-white hover:bg-green-700 disabled:opacity-60"
        >
          {loading ? 'Processando...' : 'Confirmar pagamento'}
        </button>
      </div>
    </div>
  )
}

function formatarMetodo(metodo: string) {
  switch (metodo) {
    case 'avista':
      return 'À vista (efectivo)'
    case 'debito':
      return 'À vista (débito)'
    case 'parcelado_sem_juros':
      return 'Parcelado sem juros'
    case 'cartao_com_juros':
      return 'Cartão com juros'
    default:
      return metodo
  }
}

