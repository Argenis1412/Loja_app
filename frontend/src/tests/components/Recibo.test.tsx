import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Recibo } from '../../components/Recibo';
import type { Pagamento } from '../../types/api';

describe('Componente Recibo', () => {
  it('deve exibir as informações de parcelamento quando parcelas > 1', () => {
    // Mock de um pagamento parcelado (ex: 2x)
    const pagamentoParcelado = {
      id: 123,
      metodo: 'Cartão com juros',
      total: 110.0,
      parcelas: 2,
      valor_parcela: 55.0,
      informacoes_adicionais: 'Juros de 10%',
      taxa: 10,
      tipo_taxa: 'juros_cartao',
      created_at: '2023-10-27T10:00:00Z',
    } as Pagamento;

    render(<Recibo pagamento={pagamentoParcelado} onNovoPagamento={vi.fn()} />);

    // Verifica se o label "📊 Parcelamento" está presente
    expect(screen.getByText('📊 Parcelamento')).toBeInTheDocument();

    // Verifica se mostra "2x parcelas"
    expect(screen.getByText('2x parcelas')).toBeInTheDocument();
  });

  it('não deve exibir linha de parcelas para pagamento à vista (parcelas = 1)', () => {
    // Mock de um pagamento à vista
    const pagamentoAvista = {
      id: 124,
      metodo: 'À vista',
      total: 90.0,
      parcelas: 1,
      valor_parcela: 90.0,
      informacoes_adicionais: 'Desconto de 10%',
      taxa: 10,
      tipo_taxa: 'desconto_vista',
      created_at: '2023-10-27T10:00:00Z',
    } as Pagamento;

    render(<Recibo pagamento={pagamentoAvista} onNovoPagamento={vi.fn()} />);

    // Garante que o texto "📊 Parcelamento" NÃO está no documento
    expect(screen.queryByText('📊 Parcelamento')).not.toBeInTheDocument();
  });

  it('deve exibir última parcela diferente quando há ajuste de arredondamento', () => {
    // Mock de um pagamento com 6 parcelas onde a última é diferente
    const pagamentoComAjuste = {
      id: 125,
      metodo: 'Parcelado sem juros',
      total: 100.0,
      parcelas: 6,
      valor_parcela: 16.67,
      valor_ultima_parcela: 16.65,
      informacoes_adicionais: null,
      taxa: 0,
      tipo_taxa: 'sem_juros',
      created_at: '2023-10-27T10:00:00Z',
    } as Pagamento;

    render(<Recibo pagamento={pagamentoComAjuste} onNovoPagamento={vi.fn()} />);

    // Verifica se mostra o detalhe das parcelas
    expect(screen.getByText(/5x de/i)).toBeInTheDocument();
    expect(screen.getByText(/1x de \(última\)/i)).toBeInTheDocument();
    expect(screen.getByText('R$ 16.67')).toBeInTheDocument();
    expect(screen.getByText('R$ 16.65')).toBeInTheDocument();
  });

  it('deve exibir parcelas iguais quando não há diferença', () => {
    // Mock de um pagamento com parcelas todas iguais
    const pagamentoParcelasIguais = {
      id: 126,
      metodo: 'Parcelado sem juros',
      total: 100.0,
      parcelas: 4,
      valor_parcela: 25.0,
      valor_ultima_parcela: 25.0,
      informacoes_adicionais: null,
      taxa: 0,
      tipo_taxa: 'sem_juros',
      created_at: '2023-10-27T10:00:00Z',
    } as Pagamento;

    render(<Recibo pagamento={pagamentoParcelasIguais} onNovoPagamento={vi.fn()} />);

    // Deve mostrar apenas o valor simples, não o detalhamento
    expect(screen.getByText('R$ 25.00 cada parcela')).toBeInTheDocument();
    expect(screen.queryByText(/1x de \(última\)/i)).not.toBeInTheDocument();
  });
});
