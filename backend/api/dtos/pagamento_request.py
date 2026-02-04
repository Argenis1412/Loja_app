from pydantic import BaseModel


class PagamentoRequest(BaseModel):
    opcao: int
    valor: float
    parcelas: int | None = None