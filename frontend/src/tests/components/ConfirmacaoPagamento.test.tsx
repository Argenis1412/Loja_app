import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ConfirmacaoPagamento } from '../../components/ConfirmacaoPagamento';
import type { CriarPagamentoRequest } from '../../types/api';

describe('Componente ConfirmacaoPagamento', () => {
  it('deve exibir corretamente o total e dados de pagamento à vista', () => {
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'avista',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        onConfirmar={vi.fn()}
        onVoltar={vi.fn()}
      />
    );

    expect(screen.getByText('R$ 100.00')).toBeInTheDocument(); // Subtotal
    expect(screen.getByText(/À vista \(dinheiro\)/i)).toBeInTheDocument();
  });

  it('deve exibir informações de parcelamento quando parcelas > 1', () => {
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'parcelado_sem_juros',
      parcelas: 3,
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        onConfirmar={vi.fn()}
        onVoltar={vi.fn()}
      />
    );

    expect(screen.getByText('📊 Parcelamento')).toBeInTheDocument();
    expect(screen.getByText('3x parcelas')).toBeInTheDocument();
  });

  it('deve exibir última parcela diferente quando há ajuste de arredondamento', () => {
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'parcelado_sem_juros',
      parcelas: 6,
    };

    const simulacao = {
      total: 100.0,
      valor_parcela: 16.67,
      valor_ultima_parcela: 16.65,
      taxa: 0,
      tipo_taxa: 'sem_juros',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        simulacao={simulacao}
        onConfirmar={vi.fn()}
        onVoltar={vi.fn()}
      />
    );

    expect(screen.getByText(/5x de/i)).toBeInTheDocument();
    expect(screen.getByText(/1x de \(última\)/i)).toBeInTheDocument();
    expect(screen.getByText('R$ 16.67')).toBeInTheDocument();
    expect(screen.getByText('R$ 16.65')).toBeInTheDocument();
  });

  it('deve chamar onConfirmar quando o usuário confirma', () => {
    const onConfirmarMock = vi.fn();
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'avista',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        onConfirmar={onConfirmarMock}
        onVoltar={vi.fn()}
      />
    );

    fireEvent.click(screen.getByText(/Confirmar pagamento/i));

    expect(onConfirmarMock).toHaveBeenCalledTimes(1);
  });

  it('deve chamar onVoltar quando o usuário clica em voltar', () => {
    const onVoltarMock = vi.fn();
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'avista',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        onConfirmar={vi.fn()}
        onVoltar={onVoltarMock}
      />
    );

    fireEvent.click(screen.getByText('← Voltar'));

    expect(onVoltarMock).toHaveBeenCalledTimes(1);
  });

  it('deve desabilitar o botão de confirmar quando loading é true', () => {
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'avista',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        onConfirmar={vi.fn()}
        onVoltar={vi.fn()}
        loading={true}
      />
    );

    const botaoConfirmar = screen.getByText(/Processando/i).closest('button');
    expect(botaoConfirmar).toBeDisabled();
  });

  it('deve exibir informações de juros para opção 4 (cartão com juros)', () => {
    const dados: CriarPagamentoRequest = {
      valor: 100,
      metodo: 'cartao_com_juros',
      parcelas: 12,
    };

    const simulacao = {
      total: 110.0,
      valor_parcela: 9.17,
      taxa: 10,
      tipo_taxa: 'juros_cartao',
    };

    render(
      <ConfirmacaoPagamento
        dados={dados}
        simulacao={simulacao}
        onConfirmar={vi.fn()}
        onVoltar={vi.fn()}
      />
    );

    expect(screen.getByText(/10% de juros/i)).toBeInTheDocument();
    expect(screen.getByText('R$ 110.00')).toBeInTheDocument(); // Total com juros
  });
});
