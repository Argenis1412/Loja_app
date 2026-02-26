import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import App from '../App';
import { API_ENDPOINTS } from '../config/api';

// Mock global do fetch para interceptar as chamadas de API
const fetchMock = vi.fn();
vi.stubGlobal('fetch', fetchMock);

describe('Fluxo Completo de Pagamento (Integração)', () => {
  beforeEach(() => {
    fetchMock.mockReset();
    // Default: resposta genérica para chamadas inesperadas (ex: warm-up/saude)
    fetchMock.mockResolvedValue({ ok: true, json: async () => ({}) });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('deve percorrer o fluxo: Formulário -> Simulação -> Confirmação -> Criação -> Recibo', async () => {
    render(<App />);

    // 1. Verificar estado inicial (Formulário)
    expect(screen.getByText('Loja Argenis Lopez')).toBeInTheDocument();

    // 2. Preencher formulário
    // Valor: 100
    const inputValor = screen.getByLabelText('Valor da compra');
    fireEvent.change(inputValor, { target: { value: '100' } });

    // Método: Cartão com juros
    const radioCartao = screen.getByLabelText(/Cartão com juros/i);
    fireEvent.click(radioCartao);

    // Parcelas: 12x (o select aparece após selecionar cartão - mínimo para opção 4)
    const selectParcelas = screen.getByLabelText('📊 Número de parcelas');
    fireEvent.change(selectParcelas, { target: { value: '12' } });

    // Mock da resposta da API de Simulação (backend/pagamentos/simular)
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        total: 110.0,
        valor_parcela: 9.17,
        valor_ultima_parcela: 9.13,
        taxa: 10,
        tipo_taxa: 'juros_cartao',
      }),
    });

    // 3. Submeter formulário (Simular)
    const btnContinuar = screen.getByText('Continuar para pagamento →');
    fireEvent.click(btnContinuar);

    // Verificar chamada da API de simulação
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        API_ENDPOINTS.simular,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            opcao: 4, // 4 = Cartão com juros
            valor: 100,
            parcelas: 12,
          }),
        }),
      );
    });

    // 4. Verificar Tela de Confirmação
    expect(
      await screen.findByText('Confirmação de pagamento'),
    ).toBeInTheDocument();
    expect(screen.getByText('R$ 110.00')).toBeInTheDocument(); // Total simulado
    expect(screen.getByText('12x parcelas')).toBeInTheDocument(); // Parcelas simuladas

    // Mock da resposta da API de Criação (backend/pagamentos/)
    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: 12345,
        metodo: 'Cartão com juros',
        total: 110.0,
        parcelas: 12,
        valor_parcela: 9.17,
        valor_ultima_parcela: 9.13,
        informacoes_adicionais: 'Juros de 10%',
        taxa: 10,
        tipo_taxa: 'juros_cartao',
        created_at: new Date().toISOString(),
      }),
    });

    // 5. Confirmar Pagamento
    const btnConfirmar = screen.getByText(/Confirmar pagamento/i);
    fireEvent.click(btnConfirmar);

    // Verificar chamada da API de criação
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        API_ENDPOINTS.pagamentos,
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            opcao: 4,
            valor: 100,
            parcelas: 12,
          }),
        }),
      );
    });

    // 6. Verificar Tela de Recibo
    expect(
      await screen.findByText(/Pagamento confirmado!/i),
    ).toBeInTheDocument();
    expect(screen.getByText('#12345')).toBeInTheDocument(); // ID do recibo

    // 7. Reiniciar fluxo (Novo Pagamento)
    const btnNovo = screen.getByText(/Fazer novo pagamento/i);
    fireEvent.click(btnNovo);

    // Verificar se voltou para o formulário limpo
    expect(await screen.findByText('Loja Argenis Lopez')).toBeInTheDocument();
    // O valor deve estar vazio (null ou string vazia)
    expect(screen.getByLabelText('Valor da compra')).toHaveValue(null);
  });
});
