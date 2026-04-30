import pytest
from fastapi.testclient import TestClient
from api.main import app
from infrastructure.database import create_db_and_tables
from tests.utils import clear_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    create_db_and_tables()
    clear_db()


def test_idempotency_key_prevents_duplicate_creation():
    # 1. Primeira requisição
    payload = {"opcao": 1, "valor": 100.0, "parcelas": 1}
    headers = {"Idempotency-Key": "unique-key-123"}

    response1 = client.post("/api/v1/pagamentos/", json=payload, headers=headers)
    assert response1.status_code == 201
    data1 = response1.json()
    id1 = data1["id"]

    # 2. Segunda requisição com a mesma chave
    response2 = client.post("/api/v1/pagamentos/", json=payload, headers=headers)
    assert (
        response2.status_code == 201
    )  # Retorna 201 ou 200 dependendo da implementação, mas o importante é o mesmo ID
    data2 = response2.json()
    assert data2["id"] == id1

    # 3. Verificar que apenas um registro foi criado
    response_list = client.get("/api/v1/pagamentos/")
    pagamentos = response_list.json()
    assert len(pagamentos) == 1


def test_different_idempotency_keys_create_different_records():
    payload = {"opcao": 1, "valor": 100.0, "parcelas": 1}

    client.post(
        "/api/v1/pagamentos/", json=payload, headers={"Idempotency-Key": "key-a"}
    )
    client.post(
        "/api/v1/pagamentos/", json=payload, headers={"Idempotency-Key": "key-b"}
    )

    response_list = client.get("/api/v1/pagamentos/")
    assert len(response_list.json()) == 2
