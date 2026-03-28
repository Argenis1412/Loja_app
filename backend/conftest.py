import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Define o banco de dados como SQLite em memória para os testes
# Isso evita o erro de falta do driver 'psycopg' se o padrão for Postgres
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

import infrastructure.database  # noqa: E402
from infrastructure.db.base import Base  # noqa: E402

# Importar models para garantir que sejam registrados no Base.metadata
from infrastructure.db.models import recibo_models  # noqa: E402, F401

# Configura engine com StaticPool para persistir o banco em memória nos testes
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Substitui o engine e SessionLocal globais pelo de teste
infrastructure.database.engine = test_engine
infrastructure.database.SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
