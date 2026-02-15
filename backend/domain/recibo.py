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
        # Ajustamos para garantir que o total seja sempre exato
        if valor_parcela is None:
            # Calcula a parcela base
            self.valor_parcela = round(self.total / self.parcelas, 2)
            # Calcula a última parcela para compensar erro de arredondamento
            if self.parcelas > 1:
                soma_parcelas_normais = self.valor_parcela * (self.parcelas - 1)
                self.valor_ultima_parcela = round(self.total - soma_parcelas_normais, 2)
            else:
                self.valor_ultima_parcela = self.valor_parcela
        else:
            self.valor_parcela = valor_parcela
            self.valor_ultima_parcela = valor_parcela

    @property
    def valor_da_parcela(self) -> float:
        # Para compatibilidade com testes antigos
        return self.valor_parcela
