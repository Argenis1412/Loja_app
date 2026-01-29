import { useState } from 'react'
import { PagamentoForm } from './components/PagamentoForm'
import { ConfirmacaoPagamento } from './components/ConfirmacaoPagamento'
import { Recibo } from './components/Recibo'
import { criarPagamento } from './services/api'
import type { CriarPagamentoRequest, Pagamento } from './types/api'

type Etapa = 'form' | 'confirmacao' | 'recibo'

export default function App() {
  const [etapa, setEtapa] = useState<Etapa>('form')
  const [pedido, setPedido] = useState<CriarPagamentoRequest | null>(null)
  const [pagamento, setPagamento] = useState<Pagamento | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleContinuar(dados: CriarPagamentoRequest) {
    setPedido(dados)
    setEtapa('confirmacao')
  }

  async function handleConfirmar() {
    if (!pedido) return

    try {
      setLoading(true)
      const resultado = await criarPagamento(pedido)
      setPagamento(resultado)
      setEtapa('recibo')
    } catch (e) {
      alert('Erro ao processar pagamento')
    } finally {
      setLoading(false)
    }
  }

  function handleNovoPagamento() {
    setPedido(null)
    setPagamento(null)
    setEtapa('form')
  }

  return (
    <main className="min-h-screen bg-zinc-100 dark:bg-zinc-950 flex items-center justify-center p-4">
      {etapa === 'form' && (
        <PagamentoForm onContinuar={handleContinuar} />
      )}

      {etapa === 'confirmacao' && pedido && (
        <ConfirmacaoPagamento
          dados={pedido}
          onConfirmar={handleConfirmar}
          loading={loading}
          onVoltar={() => setEtapa('form')}
        />
      )}

      {etapa === 'recibo' && pagamento && (
        <Recibo pagamento={pagamento} onNovoPagamento={handleNovoPagamento} />
      )}
    </main>
  )
}