from fastapi import Depends
from sqlalchemy.orm import Session

from domain.recibo_repository import ReciboRepository
from infrastructure.database import get_db
from infrastructure.repositories.postgres_recibo_repository import (
    PostgresReciboRepository,
)
from services.pagamento_service import PagamentoService


def get_recibo_repository(db: Session = Depends(get_db)) -> ReciboRepository:
    """
    Dependência para injetar o repositório de recibos com uma sessão de banco de dados.
    """
    return PostgresReciboRepository(db=db)


def get_pagamento_service(
    repository: ReciboRepository = Depends(get_recibo_repository),
) -> PagamentoService:
    """
    Dependência para injetar o serviço de pagamento com seu repositório.
    """
    return PagamentoService(repository=repository)
