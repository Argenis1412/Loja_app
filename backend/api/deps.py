
import os
from backend.infrastructure.repositories.postgres_recibo_repository import PostgresReciboRepository
from backend.services.pagamento_service import PagamentoService
from backend.infrastructure.database import SessionLocal

# Placeholder para repositório de arquivo (não implementado)
class ArquivoReciboRepository:
    def __init__(self):
        pass
    def salvar(self, recibo):
        raise NotImplementedError("ArquivoReciboRepository não implementado")
    def listar(self):
        return []



def get_pagamento_service():
    storage_backend = os.environ.get("STORAGE_BACKEND", "postgres").lower()
    if storage_backend == "file":
        repo = ArquivoReciboRepository()
        db = None
    else:
        db = SessionLocal()
        repo = PostgresReciboRepository(db)
    try:
        yield PagamentoService(repo)
    finally:
        if db:
            db.close()

