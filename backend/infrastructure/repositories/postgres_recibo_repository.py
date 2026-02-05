from typing import List

from sqlalchemy.orm import Session

from domain.recibo import Recibo
from domain.recibo_repository import ReciboRepository
from infrastructure.db.models.recibo_models import ReciboModel


class PostgresReciboRepository(ReciboRepository):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, recibo: Recibo) -> Recibo:
        """
        Salva um objeto Recibo no banco de dados.
        A sessão (self.db) é gerenciada pela dependência do FastAPI (get_db).
        O commit é feito automaticamente ao final da requisição.
        """
        # Mapeamento manual de Domínio -> Banco de Dados
        recibo_db = ReciboModel(
            total=recibo.total,
            parcelas=recibo.parcelas,
            metodo=recibo.metodo,
            informacoes_adicionais=recibo.informacoes_adicionais,
            valor_parcela=recibo.valor_parcela,
            created_at=recibo.data_hora,
        )
        self.db.add(recibo_db)
        self.db.flush()  # Garante que o ID e outros defaults sejam carregados no objeto
        self.db.refresh(recibo_db)
        return self._to_domain(recibo_db)

    def listar(self) -> List[Recibo]:
        """
        Lista todos os recibos do banco de dados.
        """
        recibos_db = self.db.query(ReciboModel).order_by(ReciboModel.id.desc()).all()
        return [self._to_domain(recibo) for recibo in recibos_db]

    def _to_domain(self, recibo_db: ReciboModel) -> Recibo:
        return Recibo(
            id=recibo_db.id,
            total=recibo_db.total,
            parcelas=recibo_db.parcelas,
            metodo=recibo_db.metodo,
            informacoes_adicionais=recibo_db.informacoes_adicionais,
            valor_parcela=recibo_db.valor_parcela,
            data_hora=recibo_db.created_at,
        )
