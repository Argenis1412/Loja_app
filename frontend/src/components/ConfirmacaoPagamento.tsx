import type { CriarPagamentoRequest } from '../types/api';

export interface PagamentoSimulacao {
  total: number;
  valor_parcela: number;
  valor_ultima_parcela?: number;
  taxa: number;
  tipo_taxa: string;
}

interface ConfirmacaoPagamentoProps {
  dados: CriarPagamentoRequest;
  simulacao?: PagamentoSimulacao;
  onConfirmar: () => void;
  onVoltar: () => void;
  loading?: boolean;
}

export function ConfirmacaoPagamento({
  dados,
  simulacao,
  onConfirmar,
  onVoltar,
  loading,
}: ConfirmacaoPagamentoProps) {
  const parcelas = dados.parcelas ?? 1;

  // Fallback de taxas para exibição imediata (caso a simulação ainda não tenha carregado)
  const taxasPadrao = {
    descontoVista: 10,
    jurosParcelamento: 10,
    descontoDebito: 5,
  };

  // Usar valores simulados se existirem, ou fallback para cálculo local
  // Calculamos usando valor_ultima_parcela si existe para garantir total exacto
  let totalPreview = simulacao ? simulacao.total : undefined;
  let valorParcelaPreview = simulacao?.valor_parcela;
  let valorUltimaParcelaPreview = simulacao?.valor_ultima_parcela;
  let informacaoPreview: string | null = null;

  if (totalPreview === undefined) {
    if (dados.metodo === 'avista') {
      totalPreview = dados.valor * (1 - taxasPadrao.descontoVista / 100);
    } else if (dados.metodo === 'debito') {
      totalPreview = dados.valor * (1 - taxasPadrao.descontoDebito / 100);
    } else if (dados.metodo === 'cartao_com_juros') {
      totalPreview = dados.valor * (1 + taxasPadrao.jurosParcelamento / 100);
    } else {
      totalPreview = dados.valor;
    }
  }
  if (valorParcelaPreview === undefined) {
    valorParcelaPreview = totalPreview / parcelas;
  }
  // Calcular última parcela para garantir total exacto
  if (valorUltimaParcelaPreview === undefined && parcelas > 1) {
    const somaParcelasNormais = valorParcelaPreview * (parcelas - 1);
    valorUltimaParcelaPreview = totalPreview - somaParcelasNormais;
  }

  if (simulacao) {
    switch (simulacao.tipo_taxa) {
      case 'desconto_vista':
        informacaoPreview = `${simulacao.taxa}% de desconto à vista`;
        break;
      case 'juros_cartao':
        informacaoPreview = `${simulacao.taxa}% de juros`;
        break;
      case 'sem_juros':
        informacaoPreview = `Parcelado em ${parcelas}x sem juros`;
        break;
      case 'desconto_debito':
        informacaoPreview = `${simulacao.taxa}% de desconto no débito`;
        break;
    }
  } else {
    // Fallback de texto
    if (dados.metodo === 'avista')
      informacaoPreview = `${taxasPadrao.descontoVista}% de desconto à vista`;
    if (dados.metodo === 'debito')
      informacaoPreview = `${taxasPadrao.descontoDebito}% de desconto no débito`;
    if (dados.metodo === 'cartao_com_juros')
      informacaoPreview = `${taxasPadrao.jurosParcelamento}% de juros`;
    if (dados.metodo === 'parcelado_sem_juros')
      informacaoPreview = `Parcelado em ${parcelas}x sem juros`;
  }
  return (
    <div className="mx-auto max-w-md space-y-6 rounded-xl bg-white p-8 shadow-xl dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 animate-fade-in">
      <header className="text-center pb-4 border-b border-zinc-200 dark:border-zinc-800">
        <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-7 h-7 text-blue-600 dark:text-blue-400">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-zinc-800 dark:text-zinc-100 mb-1">
          Confirmação de pagamento
        </h2>
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          Revise os detalhes antes de confirmar
        </p>
      </header>

      <div className="rounded-xl border-2 border-blue-200 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-zinc-800 dark:to-zinc-800 dark:border-zinc-700">
        <h3 className="font-bold text-blue-900 dark:text-blue-300 flex items-center gap-2 mb-1">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
          </svg>
          📋 Resumo do Pedido
        </h3>
        <p className="text-sm text-blue-700 dark:text-blue-200">
          Confira todos os detalhes da sua compra
        </p>
      </div>

      <div className="space-y-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/50 p-5 border border-zinc-200 dark:border-zinc-700">
        <div className="flex justify-between items-center pb-3 border-b border-zinc-300 dark:border-zinc-600">
          <span className="text-sm font-medium text-zinc-600 dark:text-zinc-400">💳 Forma de Pagamento</span>
          <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100 bg-white dark:bg-zinc-900 px-3 py-1 rounded-md border border-zinc-300 dark:border-zinc-700">
            {formatarMetodo(dados.metodo)}
          </span>
        </div>

        <div className="flex justify-between items-center pb-3 border-b border-zinc-300 dark:border-zinc-600">
          <span className="text-sm text-zinc-600 dark:text-zinc-400">Subtotal (Valor base)</span>
          <span className="text-sm text-zinc-700 dark:text-zinc-300">R$ {dados.valor.toFixed(2)}</span>
        </div>

        <div className="flex justify-between items-center pt-2">
          <span className="text-base font-bold text-zinc-900 dark:text-zinc-100">
            💰 Total a pagar
          </span>
          <span className="text-xl font-bold text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-4 py-2 rounded-lg">
            R$ {totalPreview.toFixed(2)}
          </span>
        </div>

        {parcelas > 1 && (
          <div className="pt-3 border-t border-zinc-300 dark:border-zinc-600 space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">📊 Parcelamento</span>
              <div className="text-right">
                <span className="text-sm font-bold text-zinc-900 dark:text-zinc-100 block">
                  {parcelas}x parcelas
                </span>
              </div>
            </div>
            {valorUltimaParcelaPreview && Math.abs(valorUltimaParcelaPreview - valorParcelaPreview) > 0.01 ? (
              <div className="text-xs text-zinc-600 dark:text-zinc-400 bg-zinc-100 dark:bg-zinc-900 p-3 rounded-lg border border-zinc-200 dark:border-zinc-700">
                <div className="flex justify-between mb-1">
                  <span>• {parcelas - 1}x de</span>
                  <span className="font-semibold">R$ {valorParcelaPreview.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>• 1x de (última)</span>
                  <span className="font-semibold text-blue-600 dark:text-blue-400">R$ {valorUltimaParcelaPreview.toFixed(2)}</span>
                </div>
              </div>
            ) : (
              <div className="text-xs text-zinc-600 dark:text-zinc-400 text-center">
                R$ {valorParcelaPreview.toFixed(2)} cada parcela
              </div>
            )}
          </div>
        )}

        {informacaoPreview && (
          <div className="mt-3 pt-3 border-t border-zinc-300 dark:border-zinc-600">
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-700 dark:text-blue-300 bg-blue-50 dark:bg-blue-900/20 px-3 py-2 rounded-lg border border-blue-200 dark:border-blue-800">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
              </svg>
              {informacaoPreview}
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-3 pt-2">
        <button
          onClick={onVoltar}
          className="flex-1 rounded-lg border-2 border-zinc-300 py-3 font-semibold text-zinc-700 hover:bg-zinc-100 dark:border-zinc-600 dark:text-zinc-300 dark:hover:bg-zinc-800 transition-all hover:scale-[1.02] shadow-sm"
        >
          ← Voltar
        </button>

        <button
          onClick={onConfirmar}
          disabled={loading}
          className="flex-1 rounded-lg bg-gradient-to-r from-green-600 to-green-700 py-3 font-bold text-white hover:from-green-700 hover:to-green-800 disabled:opacity-60 disabled:cursor-not-allowed transition-all hover:scale-[1.02] shadow-md hover:shadow-lg flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processando...
            </>
          ) : (
            <>
              ✓ Confirmar pagamento
            </>
          )}
        </button>
      </div>
    </div>
  );
}

function formatarMetodo(metodo: string) {
  switch (metodo) {
    case 'avista':
      return 'À vista (dinheiro)';
    case 'debito':
      return 'À vista (débito)';
    case 'parcelado_sem_juros':
      return 'Parcelado sem juros';
    case 'cartao_com_juros':
      return 'Cartão com juros';
    default:
      return metodo;
  }
}
