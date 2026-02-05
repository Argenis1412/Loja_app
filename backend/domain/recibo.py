from datetime import datetime, timezone


class Recibo:
    def __init__(
        self,
        total: float,
        parcelas: int,
        metodo: str | None = None,
        informacoes_adicionais: str | None = None,
        valor_parcela: float | None = None,
        data_hora: datetime | None = None,
        id: int | None = None,
    ):
        if total <= 0:
            raise ValueError("Total inválido")
        if parcelas <= 0:
            raise ValueError("Parcelas inválidas")
        self.total = total
        self.parcelas = parcelas
        self.metodo = metodo
        self.informacoes_adicionais = informacoes_adicionais
        # Opcional: id persistido no banco
        self.id = id
        self.data_hora = data_hora or datetime.now(timezone.utc)
        # Se valor_parcela não for passado, calcula automaticamente
        self.valor_parcela = (
            round(self.total / self.parcelas, 2)
            if valor_parcela is None
            else valor_parcela
        )

    @property
    def valor_da_parcela(self) -> float:
        # Para compatibilidade com testes antigos
        return self.valor_parcela