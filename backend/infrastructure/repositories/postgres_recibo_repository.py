from typing import List
from sqlalchemy.orm import Session
from backend.domain.recibo import Recibo
from backend.infrastructure.db.models.recibo_models import ReciboModel
from backend.domain.recibo_repository import ReciboRepository
from backend.infrastructure.db.mappers.recibo_mapper import to_entity

class PostgresReciboRepository(ReciboRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def salvar(self, recibo: Recibo) -> ReciboModel:
        db_recibo = ReciboModel(
            total=recibo.total,
            metodo=recibo.metodo,
            parcelas=recibo.parcelas,
            valor_parcela=recibo.valor_parcela,
            informacoes_adicionais=recibo.informacoes_adicionais,
            created_at=recibo.data_hora,
        )
        self.db.add(db_recibo)
        self.db.commit()
        self.db.refresh(db_recibo)
        return db_recibo

    def listar(self):
        models = (
            self.db.query(ReciboModel)
            .order_by(ReciboModel.created_at.desc())
            .all()
        )
        return [to_entity(m) for m in models]