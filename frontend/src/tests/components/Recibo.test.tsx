import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Recibo } from '../../components/Recibo'
import type { Pagamento } from '../../types/api'

describe('Componente Recibo', () => {
  it('deve exibir as informações de parcelamento quando parcelas > 1', () => {
    // Mock de um pagamento parcelado (ex: 2x)
    const pagamentoParcelado = {
      id: 123,
      metodo: 'Cartão com juros',
      total: 110.00,
      parcelas: 2,
      valor_parcela: 55.00,
      informacoes_adicionais: 'Juros de 10%',
      created_at: '2023-10-27T10:00:00Z'
    } as Pagamento

    render(<Recibo pagamento={pagamentoParcelado} onNovoPagamento={vi.fn()} />)

    // Verifica se o label "Parcelas" está presente
    expect(screen.getByText('Parcelas')).toBeInTheDocument()
    
    // Verifica se o valor formatado das parcelas está correto: "2x de R$ 55.00"
    expect(screen.getByText('2x de R$ 55.00')).toBeInTheDocument()
  })

  it('não deve exibir linha de parcelas para pagamento à vista (parcelas = 1)', () => {
    // Mock de um pagamento à vista
    const pagamentoAvista = {
      id: 124,
      metodo: 'À vista',
      total: 90.00,
      parcelas: 1,
      valor_parcela: 90.00,
      informacoes_adicionais: 'Desconto de 10%',
      created_at: '2023-10-27T10:00:00Z'
    } as Pagamento

    render(<Recibo pagamento={pagamentoAvista} onNovoPagamento={vi.fn()} />)

    // Garante que o texto "Parcelas" NÃO está no documento
    expect(screen.queryByText('Parcelas')).not.toBeInTheDocument()
  })
})
