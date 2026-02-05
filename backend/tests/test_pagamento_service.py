from services.pagamento_service import PagamentoService


def test_servico_utiliza_taxas_injetadas():
    # testes não fazem I/O: passamos valores diretamente
    taxas_mock = {"desconto_vista": 5.0, "juros_parcelamento": 1.5}
    service = PagamentoService(taxas=taxas_mock)
    recibo = service.criar_pagamento(valor=200.0, num_parcelas=1)
    # desconto de 5% sobre 200 -> 190
    assert recibo.total == 190.0
    assert recibo.valor_parcela == 190.0
    assert recibo.parcelas == 1
