from domain.calculadora import Calculadora
from domain.recibo import Recibo
from domain.recibo_repository import ReciboRepository


def _enrich_with_flags(recibo: Recibo, taxas: dict) -> Recibo:
    """Enriquece o recibo com flags estruturadas para a UI."""
    metodo = getattr(recibo, "metodo", None)
    recibo.taxa = 0.0
    recibo.tipo_taxa = "neutro"

    if metodo == "À vista":
        recibo.taxa = taxas.get("desconto_vista", 10.0)
        recibo.tipo_taxa = "desconto_vista"
    elif metodo == "Cartão com juros":
        recibo.taxa = taxas.get("juros_parcelamento", 10.0)
        recibo.tipo_taxa = "juros_cartao"
    elif metodo == "Parcelado sem juros":
        recibo.tipo_taxa = "sem_juros"
    elif metodo == "Débito à vista":
        recibo.taxa = 5.0
        recibo.tipo_taxa = "desconto_debito"
    return recibo


class ProcessarPagamentoUseCase:
    def __init__(
        self,
        calculadora: Calculadora,
        repository: ReciboRepository | None,
        taxas: dict,
    ):
        self.calculadora = calculadora
        self.repository = repository
        self.taxas = taxas

    def execute(
        self,
        opcao: int,
        valor: float,
        parcelas: int,
    ) -> Recibo:
        recibo = self.calculadora.calcular(
            opcao=opcao,
            valor=valor,
            parcelas=parcelas,
            desconto_vista=self.taxas.get("desconto_vista", 10.0),
            juros_parcelamento=self.taxas.get("juros_parcelamento", 10.0),
        )

        # Enriquecer com metadados estruturados
        _enrich_with_flags(recibo, self.taxas)

        if self.repository:
            return self.repository.salvar(recibo)
        return recibo


class ListarPagamentosUseCase:
    """Listar todos os recibos do banco de dados."""

    def __init__(
        self,
        repository: ReciboRepository | None,
        taxas: dict,
    ):
        self.repository = repository
        self.taxas = taxas

    def execute(self):
        if not self.repository:
            return []

        recibos = (
            self.repository.listar_todos()
            if hasattr(self.repository, "listar_todos")
            else self.repository.listar()
        )

        # Normalizar: garantir que cada recibo seja uma entidade de domínio
        normalized = []
        for r in recibos:
            normalized.append(_enrich_with_flags(r, self.taxas))
        return normalized


class PagamentoService:
    """
    Fachada que orquestra os casos de uso.
    Mantém a compatibilidade com o resto do sistema (deps.py, main.py).
    """

    def __init__(
        self,
        repository: ReciboRepository | None = None,
        calculadora: Calculadora | None = None,
        taxas: dict | None = None,
    ):
        self.repository = repository
        # Injeção de dependências com valores padrão (padrão Composition Root)
        self.calculadora = calculadora or Calculadora()
        self.taxas = taxas or {"desconto_vista": 10.0, "juros_parcelamento": 10.0}

        # Inicializar Casos de Uso
        self.processar_pagamento_uc = ProcessarPagamentoUseCase(
            self.calculadora, self.repository, self.taxas
        )
        self.listar_pagamentos_uc = ListarPagamentosUseCase(self.repository, self.taxas)

    def criar_pagamento(
        self,
        opcao: int = 1,
        valor: float = 0.0,
        parcelas: int | None = None,
        num_parcelas: int | None = None,
    ) -> Recibo:
        parcelas_finais = parcelas or num_parcelas or 1
        return self.processar_pagamento_uc.execute(opcao, valor, parcelas_finais)

    def listar_pagamentos(self):
        return self.listar_pagamentos_uc.execute()
