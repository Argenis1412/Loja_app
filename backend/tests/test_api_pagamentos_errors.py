def test_opcao_3_parcelas_invalidas(client):
    payload = {"opcao": 3, "valor": 100, "parcelas": 10}

    response = client.post("/pagamentos/", json=payload)

    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "Opção 3 suporta" in data["detail"]
