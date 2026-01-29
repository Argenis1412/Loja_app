export interface DadosPagamentoPreview {
  valor: number;
  metodo: 'avista' | 'parcelado_sem_juros' | 'cartao_com_juros';
  parcelas: number;
  total: number;
  valorParcela: number;
  informacoesAdicionais?: string | null;
}
