import type { CriarPagamentoRequest } from '../types/api';

export interface PagamentoSimulacao {
  total: number;
  valor_parcela: number;
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
  // Corrigimos o total usando o valor da parcela para garantir que o desconto/juros esteja aplicado
  let totalPreview = simulacao ? simulacao.valor_parcela * parcelas : undefined;
  let valorParcelaPreview = simulacao?.valor_parcela;
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
        <h3 className="font-semibold text-zinc-700 dark:text-zinc-200">
          Compra simulada
        </h3>
        <p className="text-sm text-zinc-500">
          Resumo rápido do pedido para validação
        </p>
      </div>

      <div className="space-y-2 text-sm text-zinc-700 dark:text-zinc-300">
        <div className="flex justify-between">
          <span className="font-medium">Forma</span>
          <span>{formatarMetodo(dados.metodo)}</span>
        </div>

        <div className="flex justify-between">
          <span className="text-zinc-500">Subtotal (Valor base)</span>
          <span className="text-zinc-500">R$ {dados.valor.toFixed(2)}</span>
        </div>

        <div className="flex justify-between">
          <span className="font-bold text-zinc-900 dark:text-zinc-100">
            Total a pagar
          </span>
          <span className="font-bold text-zinc-900 dark:text-zinc-100">
            R$ {totalPreview.toFixed(2)}
          </span>
        </div>

        {parcelas > 1 && (
          <div className="flex justify-between">
            <span className="font-medium">Parcelas</span>
            <span>
              {parcelas}x • R$ {valorParcelaPreview.toFixed(2)}
            </span>
          </div>
        )}

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
