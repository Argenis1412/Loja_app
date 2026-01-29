import type { CriarPagamentoRequest } from '../types/api'

function metodoParaOpcao(metodo: CriarPagamentoRequest['metodo']) {
  switch (metodo) {
    case 'avista':
      return 1
    case 'debito':
      return 2
    case 'parcelado_sem_juros':
      return 3
    case 'cartao_com_juros':
      return 4
    default:
      return 1
  }
}

export async function criarPagamento(dados: CriarPagamentoRequest) {
  const payload = {
    opcao: metodoParaOpcao(dados.metodo),
    valor: dados.valor,
    parcelas: dados.parcelas ?? 1,
  }
  // Debug: log payload being sent
  // eslint-disable-next-line no-console
  console.log('criarPagamento payload:', payload)

  const response = await fetch('http://127.0.0.1:8000/pagamentos/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  const bodyText = await response.text()

  if (!response.ok) {
    // eslint-disable-next-line no-console
    console.error('criarPagamento error:', response.status, bodyText)
    let parsed = bodyText
    try {
      parsed = JSON.parse(bodyText)
    } catch (_e) {
      // manter bodyText como está
    }
    throw new Error(
      `Erro ao processar pagamento (${response.status}): ${JSON.stringify(parsed)}`,
    )
  }

  try {
    return JSON.parse(bodyText)
  } catch (_e) {
    return bodyText
  }
}


