from pydantic import BaseModel, Field, model_validator


class PagamentoRequest(BaseModel):
    opcao: int = Field(..., ge=1, le=4, description="Opção de pagamento (1-4)")
    valor: float = Field(..., gt=0, le=1000000, description="Valor do pagamento")
    parcelas: int | None = Field(
        None, ge=1, le=24, description="Número de parcelas (opcional)"
    )

    @model_validator(mode="after")
    def validar_parcelas_por_opcao(self) -> "PagamentoRequest":
        if self.opcao == 3:
            if self.parcelas is None or not (2 <= self.parcelas <= 6):
                raise ValueError("Opção 3 exige entre 2 e 6 parcelas")
        elif self.opcao == 4:
            if self.parcelas is None or not (12 <= self.parcelas <= 24):
                raise ValueError("Opção 4 exige entre 12 e 24 parcelas")
        elif self.opcao in [1, 2]:
            # Forçar parcelas=1 para opções à vista
            self.parcelas = 1
        return self
