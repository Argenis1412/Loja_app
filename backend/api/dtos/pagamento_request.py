from pydantic import BaseModel, Field

class CriarPagamentoRequest(BaseModel):
    opcao: int = Field(..., ge=1, le=4)
    valor: float = Field(..., gt=0)
    parcelas: int = Field(..., ge=1)

