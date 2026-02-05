from sqlalchemy import Column, DateTime, Float, Integer, String, func

from infrastructure.db.base import Base


class ReciboModel(Base):
    __tablename__ = "recibos"

    id = Column(Integer, primary_key=True)
    total = Column(Float, nullable=False)
    metodo = Column(String(50), nullable=False)
    parcelas = Column(Integer, nullable=False)
    valor_parcela = Column(Float, nullable=False)
    informacoes_adicionais = Column(String)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
