import { useState, useEffect, type FormEvent } from 'react';

export type MetodoPagamento =
  | 'avista'
  | 'debito'
  | 'parcelado_sem_juros'
  | 'cartao_com_juros';

interface PagamentoFormProps {
  onSubmit?: (dados: {
    valor: number;
    metodo: MetodoPagamento;
    parcelas: number;
  }) => void;
  onContinuar?: (dados: {
    valor: number;
    metodo: MetodoPagamento;
    parcelas: number;
  }) => void;
  limitesParcelas?: Record<
    Exclude<MetodoPagamento, 'avista' | 'debito'>,
    { min: number; max: number }
  >;
}

const DEFAULT_LIMITES_PARCELAS: Record<
  Exclude<MetodoPagamento, 'avista' | 'debito'>,
  { min: number; max: number }
> = {
  parcelado_sem_juros: { min: 2, max: 6 },
  cartao_com_juros: { min: 12, max: 24 },
};

// eslint-disable-next-line react-refresh/only-export-components
export function converterMetodoParaOpcao(metodo: MetodoPagamento): number {
  const mapa: Record<MetodoPagamento, number> = {
    avista: 1,
    debito: 2,
    parcelado_sem_juros: 3,
    cartao_com_juros: 4,
  };
  return mapa[metodo];
}

export function PagamentoForm({
  onSubmit,
  onContinuar,
  limitesParcelas = DEFAULT_LIMITES_PARCELAS,
}: PagamentoFormProps) {
  const [valor, setValor] = useState<number | ''>('');
  const [metodo, setMetodo] = useState<MetodoPagamento>('avista');
  const [parcelas, setParcelas] = useState<number>(2);

  // Ajustar parcelas quando o método muda
  useEffect(() => {
    if (metodo === 'cartao_com_juros') {
      setParcelas(12); // Mínimo para cartão com juros (12-24 parcelas)
    } else if (metodo === 'parcelado_sem_juros') {
      setParcelas(2); // Mínimo para parcelado sem juros (2-6 parcelas)
    }
  }, [metodo]);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();

    if (!valor || valor <= 0) {
      alert('Informe um valor válido');
      return;
    }

    if (metodo !== 'avista' && metodo !== 'debito') {
      const { min, max } =
        limitesParcelas[
          metodo as Exclude<MetodoPagamento, 'avista' | 'debito'>
        ];
      if (parcelas < min || parcelas > max) {
        alert('Número de parcelas inválido');
        return;
      }
    }

    const parcelasEnvio =
      metodo === 'avista' || metodo === 'debito' ? 1 : parcelas;

    onSubmit?.({
      valor,
      metodo,
      parcelas: parcelasEnvio,
    });

    onContinuar?.({
      valor,
      metodo,
      parcelas: parcelasEnvio,
    });
  }

  const showParcelas = metodo !== 'avista' && metodo !== 'debito';
  const limitesAtuais = showParcelas
    ? (limitesParcelas[
        metodo as Exclude<MetodoPagamento, 'avista' | 'debito'>
      ] as {
        min: number;
        max: number;
      })
    : null;

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

      <div className="mb-4 rounded-xl border border-blue-200 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-zinc-800 dark:to-zinc-800 dark:border-zinc-700">
        <h2 className="font-semibold text-blue-900 dark:text-blue-300 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
          </svg>
          Compra simulada
        </h2>
        <p className="text-sm text-blue-700 dark:text-blue-200 mt-1">
          Escolha a melhor forma de pagamento para sua compra
        </p>
      </div>

      {/* Valor */}
      <div>
        <label
          htmlFor="valor"
          className="block text-sm text-zinc-700 dark:text-zinc-300"
        >
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
              e.preventDefault();
            }
          }}
          onChange={(e) =>
            setValor(e.target.value === '' ? '' : Number(e.target.value))
          }
          className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100"
        />
      </div>

      {/* Método - opções de rádio com badges */}
      <div>
        <label className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-3">
          💳 Como deseja pagar?
        </label>

        <div className="space-y-3">
          <label className="flex items-center gap-3 p-3 rounded-lg border-2 transition-all cursor-pointer hover:bg-green-50 dark:hover:bg-zinc-800 has-[:checked]:border-green-500 has-[:checked]:bg-green-50 dark:has-[:checked]:bg-green-900/20">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'avista'}
              onChange={() => setMetodo('avista')}
              className="w-4 h-4 text-green-600 focus:ring-green-500"
            />
            <div className="flex-1">
              <div className="font-medium text-zinc-800 dark:text-zinc-100">À vista (dinheiro)</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Pagamento em espécie</div>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300">💰 10% OFF</span>
          </label>

          <label className="flex items-center gap-3 p-3 rounded-lg border-2 transition-all cursor-pointer hover:bg-green-50 dark:hover:bg-zinc-800 has-[:checked]:border-green-500 has-[:checked]:bg-green-50 dark:has-[:checked]:bg-green-900/20">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'debito'}
              onChange={() => setMetodo('debito')}
              className="w-4 h-4 text-green-600 focus:ring-green-500"
            />
            <div className="flex-1">
              <div className="font-medium text-zinc-800 dark:text-zinc-100">À vista (débito)</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Cartão de débito</div>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-300">💳 5% OFF</span>
          </label>

          <label className="flex items-center gap-3 p-3 rounded-lg border-2 transition-all cursor-pointer hover:bg-blue-50 dark:hover:bg-zinc-800 has-[:checked]:border-blue-500 has-[:checked]:bg-blue-50 dark:has-[:checked]:bg-blue-900/20">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'parcelado_sem_juros'}
              onChange={() => setMetodo('parcelado_sem_juros')}
              className="w-4 h-4 text-blue-600 focus:ring-blue-500"
            />
            <div className="flex-1">
              <div className="font-medium text-zinc-800 dark:text-zinc-100">Parcelado sem juros</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Divide em até 6x sem acréscimo</div>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300">2x a 6x</span>
          </label>

          <label className="flex items-center gap-3 p-3 rounded-lg border-2 transition-all cursor-pointer hover:bg-orange-50 dark:hover:bg-zinc-800 has-[:checked]:border-orange-500 has-[:checked]:bg-orange-50 dark:has-[:checked]:bg-orange-900/20">
            <input
              type="radio"
              name="metodo"
              checked={metodo === 'cartao_com_juros'}
              onChange={() => setMetodo('cartao_com_juros')}
              className="w-4 h-4 text-orange-600 focus:ring-orange-500"
            />
            <div className="flex-1">
              <div className="font-medium text-zinc-800 dark:text-zinc-100">Cartão com juros</div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">Parcelas longas com juros</div>
            </div>
            <span className="text-xs font-semibold px-2 py-1 rounded-full bg-orange-100 text-orange-700 dark:bg-orange-900/50 dark:text-orange-300">📈 10% juros · 12x a 24x</span>
          </label>
        </div>
      </div>

      {/* Parcelas */}
      {showParcelas && (
        <div className="border-t pt-4">
          <label
            htmlFor="parcelas"
            className="block text-sm font-semibold text-zinc-700 dark:text-zinc-300 mb-2"
          >
            📊 Número de parcelas
          </label>
          <select
            id="parcelas"
            value={parcelas}
            onChange={(e) => setParcelas(Number(e.target.value))}
            className="w-full rounded-lg border-2 p-3 text-base font-medium dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
          >
            {Array.from(
              {
                length: limitesAtuais!.max - limitesAtuais!.min + 1,
              },
              (_, i) => {
                const valorParcela = limitesAtuais!.min + i;
                const valorExemplo = valor ? (Number(valor) / valorParcela).toFixed(2) : '0.00';
                return (
                  <option key={valorParcela} value={valorParcela}>
                    {valorParcela}x {valor ? `de R$ ${valorExemplo}` : ''}
                  </option>
                );
              },
            )}
          </select>

          <div className="mt-2 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800">
            <p className="text-xs text-amber-800 dark:text-amber-200 flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
              </svg>
              Disponível de {limitesAtuais!.min}x até {limitesAtuais!.max}x parcelas para este método
            </p>
          </div>
        </div>
      )}

      <button
        type="submit"
        className="w-full rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 py-3 font-semibold text-white transition-all hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-zinc-900 shadow-md hover:shadow-lg transform hover:scale-[1.02]"
      >
        Continuar para pagamento →
      </button>
    </form>
  );
}
