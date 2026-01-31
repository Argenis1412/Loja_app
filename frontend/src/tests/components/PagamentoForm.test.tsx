import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { PagamentoForm } from '../../components/PagamentoForm'

describe('Componente PagamentoForm', () => {
  it('deve renderizar os campos iniciais corretamente', () => {
    render(<PagamentoForm />)
    
    expect(screen.getByText('Loja Argenis Lopez')).toBeInTheDocument()
    expect(screen.getByLabelText('Valor da compra')).toBeInTheDocument()
    // Verifica se o método padrão (à vista) está selecionado
    expect(screen.getByLabelText(/À vista \(efectivo\)/i)).toBeChecked()
  })

  it('deve atualizar o valor quando o usuário digita', () => {
    render(<PagamentoForm />)
    
    const input = screen.getByLabelText('Valor da compra')
    fireEvent.change(input, { target: { value: '150.50' } })
    
    expect(input).toHaveValue(150.50)
  })

  it('deve mostrar o seletor de parcelas apenas para métodos parcelados', () => {
    render(<PagamentoForm />)
    
    // Inicialmente (à vista) não deve mostrar parcelas
    expect(screen.queryByText('Parcelas')).not.toBeInTheDocument()

    // Seleciona Cartão com juros
    fireEvent.click(screen.getByLabelText(/Cartão com juros/i))
    
    // Agora deve mostrar
    expect(screen.getByText('Parcelas')).toBeInTheDocument()
    expect(screen.getByRole('combobox')).toBeInTheDocument()
  })

  it('deve chamar onContinuar com os dados corretos', () => {
    const onContinuarMock = vi.fn()
    render(<PagamentoForm onContinuar={onContinuarMock} />)

    // Preenche valor
    fireEvent.change(screen.getByLabelText('Valor da compra'), { target: { value: '200' } })
    
    // Seleciona método parcelado
    fireEvent.click(screen.getByLabelText(/Parcelado sem juros/i))
    
    // Seleciona 3 parcelas (assumindo que 3 está disponível no range padrão)
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '3' } })

    // Submete
    fireEvent.click(screen.getByText('Continuar →'))

    expect(onContinuarMock).toHaveBeenCalledWith({
      valor: 200,
      metodo: 'parcelado_sem_juros',
      parcelas: 3
    })
  })

  it('não deve submeter se o valor for inválido', () => {
    const onContinuarMock = vi.fn()
    // Mock do window.alert pois o componente usa alert()
    const alertMock = vi.spyOn(window, 'alert').mockImplementation(() => {})
    
    render(<PagamentoForm onContinuar={onContinuarMock} />)

    // Tenta submeter sem preencher valor
    fireEvent.click(screen.getByText('Continuar →'))

    expect(alertMock).toHaveBeenCalledWith('Informe um valor válido')
    expect(onContinuarMock).not.toHaveBeenCalled()
  })
})