import pytest

from domain.recibo import Recibo


@pytest.mark.parametrize(
    "total, parcelas",
    [
        (-10.0, 1),
        (100.0, 0),
    ],
)
def test_recibo_validacoes_obrigatorias(total, parcelas):
    with pytest.raises(ValueError):
        Recibo(total=total, metodo="Teste", parcelas=parcelas)


def test_recibo_calcula_valor_da_parcela_corretamente():
    recibo = Recibo(total=100.0, metodo="Pix", parcelas=2)
    assert recibo.valor_da_parcela == 50.0