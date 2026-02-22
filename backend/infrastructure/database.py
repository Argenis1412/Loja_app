from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from infrastructure.db.base import Base
from infrastructure.db.models.recibo_models import ReciboModel  # noqa: F401

engine_args = {
    "future": True,
    "pool_pre_ping": True,  # Verifica conexões antes de usar
    "pool_size": 5,  # Número de conexões permanentes
    "max_overflow": 10,  # Conexões extras sob demanda
    "pool_recycle": 3600,  # Recicla conexões após 1 hora
}

# Para SQLite, é necessário permitir o uso em múltiplos threads, como o FastAPI faz.
if settings.database_url.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}
    # SQLite não suporta pool_size/max_overflow da mesma forma
    engine_args.pop("pool_size", None)
    engine_args.pop("max_overflow", None)

# Engine e SessionLocal centralizados
engine = create_engine(settings.database_url, **engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """
    Função para criar as tabelas no banco de dados.
    Deve ser chamada na inicialização da aplicação.
    """
    Base.metadata.create_all(bind=engine)


def warmup_db():
    """
    Inicializa o pool de conexões para evitar latência na primeira requisição.
    """
    try:
        # Executa uma query simples para ativar o pool
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        # Ignora erros durante warmup
        pass


def get_db() -> Generator[Session, None, None]:
    """
    Dependência do FastAPI para obter uma sessão de banco de dados por requisição.
    Garante que a transação seja commitada em caso de sucesso ou revertida em caso de erro.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
