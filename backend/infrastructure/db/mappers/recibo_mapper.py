from backend.domain.recibo import Recibo
from backend.infrastructure.db.models import ReciboModel


def to_model(entity: Recibo) -> ReciboModel:
    return ReciboModel(
        total=entity.total,
        metodo=entity.metodo,
        parcelas=entity.parcelas,
        valor_parcela=entity.valor_parcela,
        informacoes_adicionais=entity.informacoes_adicionais,
        created_at=entity.data_hora,
    )


def to_entity(model: ReciboModel) -> Recibo:
    return Recibo(
        total=model.total,
        parcelas=model.parcelas,
        metodo=model.metodo,
        informacoes_adicionais=model.informacoes_adicionais,
        valor_parcela=model.valor_parcela,
        data_hora=model.created_at,
        id=getattr(model, "id", None),
    )

