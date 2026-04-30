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


def test_pagination_limit_and_offset():
    # 1. Criar 5 pagamentos
    for i in range(5):
        payload = {"opcao": 1, "valor": 10.0 + i, "parcelas": 1}
        client.post(
            "/api/v1/pagamentos/", json=payload, headers={"Idempotency-Key": f"key-{i}"}
        )

    # 2. Testar limite 2
    response = client.get("/api/v1/pagamentos/?limit=2")
    data = response.json()
    assert len(data) == 2

    # 3. Testar offset 3 (deve sobrar 2 registros de 5 totais)
    response = client.get("/api/v1/pagamentos/?limit=10&offset=3")
    data = response.json()
    assert len(data) == 2

    # 4. Testar default limit (20)
    response = client.get("/api/v1/pagamentos/")
    assert len(response.json()) == 5
