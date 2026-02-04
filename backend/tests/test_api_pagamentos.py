def test_criar_pagamento_com_juros(client):
    payload = {"opcao": 4, "valor": 440, "parcelas": 12}

    response = client.post("/pagamentos/", json=payload)

    assert response.status_code == 201

    data = response.json()

    # Contrato
    assert "id" in data
    assert data["metodo"] == "Cartão com juros"
    # Com juros padrão de 10% aplicado
    assert data["total"] == 484.0
    assert data["parcelas"] == 12
    assert data["valor_parcela"] == 40.33
    assert "informacoes_adicionais" in data
    assert "created_at" in data


def test_listar_pagamentos(client):
    response = client.get("/pagamentos/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        pagamento = data[0]

        assert "id" in pagamento
        assert "metodo" in pagamento
        assert "total" in pagamento
        assert "parcelas" in pagamento
        assert "valor_parcela" in pagamento
        assert "created_at" in pagamento
