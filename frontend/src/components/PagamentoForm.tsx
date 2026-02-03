import { useState, type FormEvent } from 'react'

export type MetodoPagamento = 'avista' | 'debito' | 'parcelado_sem_juros' | 'cartao_com_juros'

interface PagamentoFormProps {
  onSubmit?: (dados: {
    valor: number
    metodo: MetodoPagamento
    parcelas: number
  }) => void
  onContinuar?: (dados: {
    valor: number
    metodo: MetodoPagamento
    parcelas: number
  }) => void
  limitesParcelas?: Record<
    Exclude<MetodoPagamento, 'avista' | 'debito'>,
    { min: number; max: number }
  >
}

const DEFAULT_LIMITES_PARCELAS: Record<
  Exclude<MetodoPagamento, 'avista' | 'debito'>,
  { min: number; max: number }
> = {
  parcelado_sem_juros: { min: 2, max: 6 },
  cartao_com_juros: { min: 2, max: 12 },
}

export function converterMetodoParaOpcao(metodo: MetodoPagamento): number {
  const mapa: Record<MetodoPagamento, number> = {
    avista: 1,
    debito: 2,
    parcelado_sem_juros: 3,
    cartao_com_juros: 4,
  }
  return mapa[metodo]
}

export function PagamentoForm({ onSubmit, onContinuar, limitesParcelas = DEFAULT_LIMITES_PARCELAS }: PagamentoFormProps) {
  const [valor, setValor] = useState<number | ''>('')
  const [metodo, setMetodo] = useState<MetodoPagamento>('avista')
  const [parcelas, setParcelas] = useState<number>(2)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()

    if (!valor || valor <= 0) {
      alert('Informe um valor válido')
      return
    }

    if (metodo !== 'avista' && metodo !== 'debito') {
      const { min, max } = limitesParcelas[metodo as Exclude<MetodoPagamento, 'avista' | 'debito'>]
      if (parcelas < min || parcelas > max) {
        alert('Número de parcelas inválido')
        return
      }
    }

    const parcelasEnvio = metodo === 'avista' || metodo === 'debito' ? 1 : parcelas

    onSubmit?.({
      valor,
      metodo,
      parcelas: parcelasEnvio,
    })

    onContinuar?.({
      valor,
      metodo,
      parcelas: parcelasEnvio,
    })
  }

  const showParcelas = metodo !== 'avista' && metodo !== 'debito'
  const limitesAtuais = showParcelas
    ? (limitesParcelas[metodo as Exclude<MetodoPagamento, 'avista' | 'debito'>] as {
        min: number
        max: number
      })
    : null

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto max-w-md space-y-5 rounded-xl bg-white p-6 shadow-md dark:bg-zinc-900"
    >
      <header className="mb-4 text-center">
        <h1 className="text-2xl font-bold text-zinc-800 dark:text-zinc-100">
          Loja Argenis Lopez
        </h1>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Simulação de pagamento com regras reais de negócio
        </p>
      </header>

      <div className="mb-4 rounded-xl border p-4 bg-zinc-50 dark:bg-zinc-900">
        <h2 className="font-semibold text-zinc-700 dark:text-zinc-200">
          Compra simulada
        </h2>
        <p className="text-sm text-zinc-500">
          Utilize este fluxo para testar diferentes formas de pagamento
        </p>
      </div>

      {/* Valor */}
      <div>
        <label htmlFor="valor" className="block text-sm text-zinc-700 dark:text-zinc-300">
          Valor da compra
        </label>
        <input
          id="valor"
          type="number"
          min={1}
          step="0.01"
          placeholder="Digite o valor da compra"
          value={valor || ''}
          onKeyDown={(e) => {
            if (['e', 'E', '+', '-'].includes(e.key)) {
              e.preventDefault()
            }
          }}
          onChange={e => setValor(e.target.value === '' ? '' : Number(e.target.value))}
          className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        />
      </div>

      {/* Método - opções de rádio com badges */}
      <div>
        <label className="block text-sm text-zinc-700 dark:text-zinc-300 mb-2">
          Como deseja pagar?
        </label>

        <div className="space-y-2">
          <label className="flex items-center gap-3">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'avista'}
              onChange={() => setMetodo('avista')}
            />
            <span className="font-medium">À vista (dinheiro)</span>
            <span className="text-xs text-green-600 ml-2">10% de desconto</span>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'debito'}
              onChange={() => setMetodo('debito')}
            />
            <span className="font-medium">À vista (débito)</span>
            <span className="text-xs text-green-600 ml-2">5% de desconto</span>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'parcelado_sem_juros'}
              onChange={() => setMetodo('parcelado_sem_juros')}
            />
            <span className="font-medium">Parcelado sem juros</span>
            <span className="text-xs text-zinc-500 ml-2">até 6x</span>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'cartao_com_juros'}
              onChange={() => setMetodo('cartao_com_juros')}
            />
            <span className="font-medium">Cartão com juros</span>
            <span className="text-xs text-red-500 ml-2">10% de juros · até 12x</span>
          </label>
        </div>
      </div>

      {/* Parcelas */}
      {showParcelas && (
        <div>
          <label htmlFor="parcelas" className="block text-sm text-zinc-700 dark:text-zinc-300">
            Parcelas
          </label>
          <select
            id="parcelas"
            value={parcelas}
            onChange={e => setParcelas(Number(e.target.value))}
            className="w-full rounded-lg border p-2 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
          >
            {Array.from(
              {
                length: limitesAtuais!.max - limitesAtuais!.min + 1,
              },
              (_, i) => {
                const valorParcela = limitesAtuais!.min + i
                return (
                  <option key={valorParcela} value={valorParcela}>
                    {valorParcela}x
                  </option>
                )
              }
            )}
          </select>

          <p className="mt-1 text-xs text-zinc-500">
            De {limitesAtuais!.min} até {limitesAtuais!.max} parcelas
          </p>
        </div>
      )}

      <button
        type="submit"
        className="w-full rounded-lg bg-blue-600 py-2 font-medium text-white transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-zinc-900"
      >
        Continuar →
      </button>
    </form>
  )
}
