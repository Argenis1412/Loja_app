import pytest

from backend.domain.calculadora import Calculadora
from backend.domain.exceptions import RegraPagamentoInvalida


def test_opcao_1_avista():
    calc = Calculadora()

    recibo = calc.calcular(
        opcao=1,
        valor=100,
        parcelas=1,
    )

    assert recibo.metodo == "À vista"
    assert recibo.total == 90.0
    assert recibo.valor_parcela == 90.0
    assert recibo.informacoes_adicionais == "Desconto de 10%"


def test_opcao_3_parcelas_invalidas():
    calc = Calculadora()

    with pytest.raises(RegraPagamentoInvalida):
        calc.calcular(
            opcao=3,
            valor=100,
            parcelas=1,  # inválido (opção 3 exige 2–6)
        )


def test_opcao_4_com_juros():
    calc = Calculadora()

    recibo = calc.calcular(
        opcao=4,
        valor=440,
        parcelas=12,
    )

    assert recibo.metodo == "Cartão com juros"
    assert recibo.total == 484.0
    assert recibo.valor_parcela == 40.33
    assert "10%" in recibo.informacoes_adicionais

