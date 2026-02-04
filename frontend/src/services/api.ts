import type { CriarPagamentoRequest } from '../types/api';

function metodoParaOpcao(metodo: CriarPagamentoRequest['metodo']) {
  switch (metodo) {
    case 'avista':
      return 1;
    case 'debito':
      return 2;
    case 'parcelado_sem_juros':
      return 3;
    case 'cartao_com_juros':
      return 4;
    default:
      return 1;
  }
}

export async function criarPagamento(dados: CriarPagamentoRequest) {
  const payload = {
    opcao: metodoParaOpcao(dados.metodo),
    valor: dados.valor,
    parcelas: dados.parcelas ?? 1,
  };
  // Debug log do payload antes de enviar a requisição
  console.log('criarPagamento payload:', payload);

  const response = await fetch('http://127.0.0.1:8000/pagamentos/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const bodyText = await response.text();

  if (!response.ok) {
    console.error('criarPagamento error:', response.status, bodyText);
    let parsed = bodyText;
    try {
      parsed = JSON.parse(bodyText);
    } catch {
      // manter bodyText como está
    }
    throw new Error(
      `Erro ao processar pagamento (${response.status}): ${JSON.stringify(parsed)}`,
    );
  }

  try {
    return JSON.parse(bodyText);
  } catch {
    return bodyText;
  }
}

export async function listarPagamentos() {
  const response = await fetch('http://127.0.0.1:8000/pagamentos/');

  if (!response.ok) {
    throw new Error('Erro ao buscar pagamentos');
  }
  return response.json();
}
