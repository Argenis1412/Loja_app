import type { Pagamento } from '../types/api'

interface ReciboProps {
  pagamento: Pagamento
  onNovoPagamento: () => void
}

export function Recibo({ pagamento, onNovoPagamento }: ReciboProps) {
  const dataFormatada = pagamento?.created_at
    ? new Date(pagamento.created_at).toLocaleString('pt-BR')
    : new Date().toLocaleString('pt-BR')

  const numeroComprovante = pagamento?.id ?? Math.floor(Math.random() * 100000)

  return (
    <div className="mx-auto max-w-md space-y-6 rounded-xl bg-white p-6 shadow-lg dark:bg-zinc-900">
      <header className="text-center">
        <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">Loja Argenis Lopez</h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Comprovante de pagamento</p>
        <p className="text-xs text-zinc-400 mt-1">Nº {numeroComprovante} • {dataFormatada}</p>
      </header>

      <div className="mb-4 rounded-xl border p-4 bg-zinc-50 dark:bg-zinc-900">
        <h2 className="font-semibold text-zinc-700 dark:text-zinc-200">Resumo do pedido</h2>
        <p className="text-sm text-zinc-500">Dados do pagamento gerado pelo servidor</p>
      </div>

      <div className="space-y-3 text-sm">
        <Linha label="Forma" value={formatarMetodo(pagamento.metodo)} />
        <Linha label="Parcelas" value={`${pagamento.parcelas}x`} />
        <Linha label="Valor da parcela" value={`R$ ${pagamento.valor_parcela.toFixed(2)}`} />

        {pagamento.informacoes_adicionais && (
          <p className="text-xs text-zinc-500">{pagamento.informacoes_adicionais}</p>
        )}
      </div>

      <div className="border-t border-zinc-200 pt-4 dark:border-zinc-700">
        <div className="flex justify-between items-baseline">
          <span className="text-sm text-zinc-600">Total pago</span>
          <span className="text-2xl font-semibold text-green-600 dark:text-green-400">R$ {pagamento.total.toFixed(2)}</span>
        </div>
      </div>

      <div className="border-t border-dashed border-zinc-300 dark:border-zinc-700" />

      <div className="space-y-3 text-center">
        <p className="text-xs text-zinc-500">Obrigado pela sua compra!</p>

        <button
          onClick={onNovoPagamento}
          className="w-full rounded-lg bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Fazer outro pagamento
        </button>
      </div>
    </div>
  )
}

function Linha({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between">
      <span className="text-zinc-600 dark:text-zinc-400">{label}</span>
      <span className="font-medium text-zinc-800 dark:text-zinc-100">
        {value}
      </span>
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