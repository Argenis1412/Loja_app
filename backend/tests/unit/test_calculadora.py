import pytest
from backend.domain.calculadora import Calculadora
from backend.domain.exceptions import RegraPagamentoInvalida

class TestCalculadora:
    def setup_method(self):
        self.calculadora = Calculadora()

    def test_valor_invalido_deve_lancar_excecao(self):
        with pytest.raises(RegraPagamentoInvalida, match="Valor inválido"):
            self.calculadora.calcular(opcao=1, valor=0, parcelas=1)
        
        with pytest.raises(RegraPagamentoInvalida, match="Valor inválido"):
            self.calculadora.calcular(opcao=1, valor=-10, parcelas=1)

    def test_opcao_invalida_deve_lancar_excecao(self):
        with pytest.raises(RegraPagamentoInvalida, match="Opção inválida"):
            self.calculadora.calcular(opcao=99, valor=100, parcelas=1)

    def test_pagamento_a_vista_deve_aplicar_desconto(self):
        # Opção 1: À vista com 10% de desconto (padrão)
        recibo = self.calculadora.calcular(opcao=1, valor=100.0, parcelas=1)
        
        assert recibo.total == 90.0
        assert recibo.parcelas == 1
        assert recibo.metodo == "À vista"
        assert "Desconto de 10%" in recibo.informacoes_adicionais

    def test_pagamento_debito_deve_aplicar_desconto_fixo(self):
        # Opção 2: Débito com 5% de desconto fixo
        recibo = self.calculadora.calcular(opcao=2, valor=100.0, parcelas=1)
        
        assert recibo.total == 95.0
        assert recibo.parcelas == 1
        assert recibo.metodo == "Débito à vista"
        assert "Desconto de 5%" in recibo.informacoes_adicionais

    def test_parcelado_sem_juros_deve_validar_parcelas(self):
        # Opção 3: 2 a 6 parcelas
        recibo = self.calculadora.calcular(opcao=3, valor=120.0, parcelas=3)
        assert recibo.total == 120.0
        assert recibo.valor_parcela == 40.0
        assert recibo.metodo == "Parcelado sem juros"

        # Testar limites
        with pytest.raises(RegraPagamentoInvalida):
            self.calculadora.calcular(opcao=3, valor=100, parcelas=1)
        
        with pytest.raises(RegraPagamentoInvalida):
            self.calculadora.calcular(opcao=3, valor=100, parcelas=7)

    def test_cartao_com_juros_deve_aplicar_taxa(self):
        # Opção 4: Juros simples de 10% (padrão)
        # Valor 100 + 10% = 110
        recibo = self.calculadora.calcular(
            opcao=4, 
            valor=100.0, 
            parcelas=10,
            juros_parcelamento=10.0
        )
        
        assert recibo.total == 110.0
        assert recibo.valor_parcela == 11.0  # 110 / 10
        assert recibo.metodo == "Cartão com juros"

        # Testar limites (2 a 12 parcelas)
        with pytest.raises(RegraPagamentoInvalida):
            self.calculadora.calcular(opcao=4, valor=100, parcelas=13)