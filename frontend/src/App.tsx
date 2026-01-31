import { useState } from 'react'
import { PagamentoForm, converterMetodoParaOpcao } from './components/PagamentoForm'
import { ConfirmacaoPagamento, type PagamentoSimulacao } from './components/ConfirmacaoPagamento'
import { Recibo } from './components/Recibo'
import { ErrorBanner } from './components/ErrorBanner'
import type { CriarPagamentoRequest, Pagamento, MetodoPagamento } from './types/api'

type Tela = 'form' | 'confirmacao' | 'recibo'

export default function App() {
  const [tela, setTela] = useState<Tela>('form')
  const [dadosPagamento, setDadosPagamento] = useState<CriarPagamentoRequest | null>(null)
  const [simulacao, setSimulacao] = useState<PagamentoSimulacao | undefined>(undefined)
  const [recibo, setRecibo] = useState<Pagamento | null>(null)
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState<string | null>(null)

  const handleContinuar = async (dados: { valor: number; metodo: MetodoPagamento; parcelas: number }) => {
    setLoading(true)
    setErro(null) // Limpiar errores previos
    setDadosPagamento(dados)
    setTela('confirmacao') // Navegación optimista

    try {
      // Usa a função auxiliar importada para converter string -> int
      const opcao = converterMetodoParaOpcao(dados.metodo)
      
      const response = await fetch('http://localhost:8000/pagamentos/simular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          opcao,
          valor: dados.valor,
          parcelas: dados.parcelas
        })
      })

      if (response.ok) {
        const data = await response.json()
        setSimulacao(data)
      } else {
        // Intentar obtener mensaje del backend o usar genérico
        try {
            const errData = await response.json()
            setErro(errData.detail || 'Erro ao simular pagamento')
        } catch {
            setErro('Erro ao comunicar com o servidor de simulação')
        }
      }
    } catch (error) {
      console.error("Error de red", error)
      setErro('Não foi possível conectar ao servidor. Verifique sua conexão.')
    } finally {
      setLoading(false)
    }
  }

  const handleConfirmarPagamento = async () => {
    if (!dadosPagamento) return
    setLoading(true)
    setErro(null)

    try {
      // Usa a função auxiliar importada para converter string -> int
      const opcao = converterMetodoParaOpcao(dadosPagamento.metodo)
      
      const response = await fetch('http://localhost:8000/pagamentos/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          opcao,
          valor: dadosPagamento.valor,
          parcelas: dadosPagamento.parcelas
        })
      })

      if (response.ok) {
        const data = await response.json()
        setRecibo(data)
        setTela('recibo')
      } else {
        try {
            const errData = await response.json()
            setErro(errData.detail || 'Erro ao processar pagamento')
        } catch {
            setErro('Ocorreu um erro inesperado no servidor')
        }
      }
    } catch (error) {
      console.error(error)
      setErro('Erro de conexão. Tente novamente mais tarde.')
    } finally {
      setLoading(false)
    }
  }

  const handleNovoPagamento = () => {
    setDadosPagamento(null)
    setSimulacao(undefined)
    setRecibo(null)
    setErro(null)
    setTela('form')
  }

  return (
    <div className="min-h-screen bg-zinc-50 p-4 text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
      <div className="mx-auto max-w-2xl py-10">
        
        {/* Banner de Error Global */}
        {erro && (
          <ErrorBanner 
            message={erro} 
            onClose={() => setErro(null)} 
          />
        )}

        {tela === 'form' && (
          <PagamentoForm 
            onContinuar={handleContinuar} 
          />
        )}

        {tela === 'confirmacao' && dadosPagamento && (
          <ConfirmacaoPagamento
            dados={dadosPagamento}
            simulacao={simulacao}
            loading={loading}
            onConfirmar={handleConfirmarPagamento}
            onVoltar={() => {
                setTela('form')
                setErro(null)
            }}
          />
        )}

        {tela === 'recibo' && recibo && (
          <Recibo 
            pagamento={recibo} 
            onNovoPagamento={handleNovoPagamento} 
          />
        )}

      </div>
    </div>
  )
}
