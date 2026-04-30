def test_opcao_3_parcelas_invalidas(client):
    payload = {"opcao": 3, "valor": 100, "parcelas": 10}

    response = client.post("/api/v1/pagamentos/", json=payload)

    # FastAPI retorna 422 para erros de validação do Pydantic
    assert response.status_code == 422
