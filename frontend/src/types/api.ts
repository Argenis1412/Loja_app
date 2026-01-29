export type MetodoPagamento =
  | 'avista'
  | 'debito'
  | 'parcelado_sem_juros'
  | 'cartao_com_juros'

export interface CriarPagamentoRequest {
  valor: number
  metodo: MetodoPagamento
  parcelas?: number
}

export interface Pagamento {
  id: number
  metodo: string
  total: number
  parcelas: number
  valor_parcela: number
  informacoes_adicionais: string | null
  created_at: string
}


