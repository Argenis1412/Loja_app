from datetime import datetime
from typing import Optional

from pydantic import BaseModel , ConfigDict

from backend.domain.recibo import Recibo


class PagamentoResponse(BaseModel):
    id: Optional[int] = None
    metodo: str
    total: float
    parcelas: int
    valor_parcela: float
    informacoes_adicionais: Optional[str] = None
    taxa: float = 0.0
    tipo_taxa: Optional[str] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_domain(cls, recibo) -> "PagamentoResponse":
        # Suporta Recibo (domínio) e ReciboModel (ORM)
        d = dict(
            id=getattr(recibo, "id", None),
            metodo=getattr(recibo, "metodo", None),
            total=getattr(recibo, "total", None),
            parcelas=getattr(recibo, "parcelas", None),
            valor_parcela=getattr(recibo, "valor_parcela", None),
            informacoes_adicionais=getattr(recibo, "informacoes_adicionais", None),
            taxa=getattr(recibo, "taxa", 0.0),
            tipo_taxa=getattr(recibo, "tipo_taxa", None),
            created_at=getattr(recibo, "data_hora", getattr(recibo, "created_at", None)),
        )
        
        return cls(**d)

    model_config = ConfigDict(from_attributes=True)
