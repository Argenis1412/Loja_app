import pytest
from backend.infrastructure.database import engine
from backend.infrastructure.db.base import Base
# Importar models para garantir que sejam registrados no Base.metadata
from backend.infrastructure.db.models import recibo_models  # noqa: F401

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield