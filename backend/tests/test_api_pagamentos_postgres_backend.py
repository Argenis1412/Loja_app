import os
import importlib
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

import backend.infrastructure.database as database
from backend.infrastructure.database import Base
from backend.infrastructure.db.models.recibo_models import ReciboModel  # ensure model is imported into Base metadata


def test_deve_persistir_e_recuperar_lista_de_pagamentos_usando_repositorio_postgres():
    # Força o backend como 'postgres' para o fluxo de seleção
    os.environ["STORAGE_BACKEND"] = "postgres"

    # Cria um engine sqlite in-memory para simular um banco disponível
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Garantir que os modelos estejam registrados antes de criar tabelas
    import backend.infrastructure.db.models.recibo_models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Substitui SessionLocal localmente e instancia o repositório com a sessão
    SessionLocalTest = sessionmaker(bind=engine)
    db = SessionLocalTest()

    from backend.infrastructure.repositories.postgres_recibo_repository import PostgresReciboRepository
    from backend.services.pagamento_service import PagamentoService
    from backend.domain.calculadora import Calculadora
    from backend.api.deps import get_pagamento_service

    repo = PostgresReciboRepository(db)
    calculadora = Calculadora()
    taxas = {"desconto_vista": 10.0, "juros_parcelamento": 10.0}
    service = PagamentoService(repo, calculadora, taxas)

    # Recarrega a app principal e sobrescreve a dependência para usar nosso service
    main = importlib.reload(importlib.import_module("backend.api.main"))
    main.app.dependency_overrides[get_pagamento_service] = lambda: service

    client = TestClient(main.app)

    # Criar 3 pagamentos
    payloads = [
        {"opcao": 1, "valor": 90, "parcelas": 1},
        {"opcao": 2, "valor": 95, "parcelas": 1},
        {"opcao": 3, "valor": 100, "parcelas": 6},
    ]

    for p in payloads:
        resp = client.post("/pagamentos/", json=p)
        assert resp.status_code == 201

    # Recuperar lista e verificar quantidade
    resp = client.get("/pagamentos/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == len(payloads)

    # Verificações básicas do primeiro recibo
    first = data[0]
    assert "id" in first
    assert "metodo" in first
    assert "total" in first
    assert "parcelas" in first
    assert "valor_parcela" in first
    assert "created_at" in first
