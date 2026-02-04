from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.recibo import Recibo
from infrastructure.database import Base
from infrastructure.db.models import ReciboModel
from infrastructure.repositories.postgres_recibo_repository import (
    PostgresReciboRepository,
)


# Teste unitário para PostgresReciboRepository
def test_postgres_repository_salvar_com_sqlite():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        repo = PostgresReciboRepository(db)
        recibo = Recibo(total=100.0, metodo="teste", parcelas=1)
        repo.salvar(recibo)
        saved = db.query(ReciboModel).first()

        assert saved is not None
        assert saved.total == 100.0
        assert saved.metodo == "teste"
        assert saved.parcelas == 1
        assert isinstance(saved.created_at, datetime)
    finally:
        db.close()


def test_postgres_repository_salvar_multiplos():

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        repo = PostgresReciboRepository(db)

        recibo1 = Recibo(total=100.0, metodo="dinheiro", parcelas=1)
        recibo2 = Recibo(total=200.0, metodo="cartao", parcelas=6)

        repo.salvar(recibo1)
        repo.salvar(recibo2)

        all_recibos = db.query(ReciboModel).all()
        assert len(all_recibos) == 2
        assert all_recibos[0].total == 100.0
        assert all_recibos[1].total == 200.0
    finally:
        db.close()
