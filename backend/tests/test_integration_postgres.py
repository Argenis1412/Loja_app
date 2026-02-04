import os
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.recibo import Recibo
from infrastructure.database import Base
from infrastructure.db.models import ReciboModel
from infrastructure.repositories.postgres_recibo_repository import (
    PostgresReciboRepository,
)

# Teste de integração para PostgresReciboRepository
def test_integration_postgres_repository_with_env_var():

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:

        repo = PostgresReciboRepository(db)
        recibo1 = Recibo(total=90.0, metodo="dinheiro", parcelas=1)
        recibo2 = Recibo(total=95.0, metodo="cartao", parcelas=1)
        recibo3 = Recibo(total=100.0, metodo="parcelado", parcelas=6)
        repo.salvar(recibo1)
        repo.salvar(recibo2)
        repo.salvar(recibo3)

        all_recibos = db.query(ReciboModel).all()
        assert len(all_recibos) == 3

        assert all_recibos[0].total == 90.0
        assert all_recibos[0].metodo == "dinheiro"

        assert all_recibos[1].total == 95.0
        assert all_recibos[1].metodo == "cartao"

        assert all_recibos[2].total == 100.0
        assert all_recibos[2].metodo == "parcelado"
        assert all_recibos[2].parcelas == 6

    finally:
        db.close()


def test_database_created_with_sqlite_url():

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        engine = create_engine(f"sqlite:///{tmp_path}")
        Base.metadata.create_all(bind=engine)

        assert os.path.exists(tmp_path)

        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()

        try:
            repo = PostgresReciboRepository(db)
            recibo = Recibo(total=100.0, metodo="test", parcelas=1)
            repo.salvar(recibo)
            saved = db.query(ReciboModel).first()
            assert saved is not None
            assert saved.total == 100.0
        finally:
            db.close()
            engine.dispose()

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)