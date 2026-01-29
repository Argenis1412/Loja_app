from backend.domain.calculadora import Calculadora
from backend.domain.recibo import Recibo
from backend.services.recibo_repository import ReciboRepository


class PagamentoService:
    def __init__(
        self,
        repository: ReciboRepository | None = None,
        desconto_vista: float = 10.0,
        juros_parcelamento: float = 10.0,
    ):
        self.repository = repository
        self.desconto_vista = desconto_vista
        self.juros_parcelamento = juros_parcelamento
        self.calculadora = Calculadora()  # ← SEM argumentos

    def criar_pagamento(
        self,
        opcao: int = 1,
        valor: float = 0.0,
        parcelas: int | None = None,
        num_parcelas: int | None = None,
    ) -> Recibo:
        parcelas_finais = parcelas or num_parcelas or 1

        recibo = self.calculadora.calcular(
            opcao=opcao,
            valor=valor,
            parcelas=parcelas_finais,
            desconto_vista=self.desconto_vista,
            juros_parcelamento=self.juros_parcelamento,
        )

        if self.repository:
            db_recibo = self.repository.salvar(recibo)
            return db_recibo

        return recibo

    def listar_pagamentos(self):
        recibos = None
        if hasattr(self.repository, "listar_todos"):
            recibos = self.repository.listar_todos()
        else:
            recibos = self.repository.listar()

        # Normalizar: asegurar que cada recibo sea una entidad de dominio y
        # completar `informacoes_adicionais` si está ausente o desactualizada.
        normalized = []
        for r in recibos:
            # r esperado ser uma entidade `Recibo` do domínio ou objeto similar
            metodo = getattr(r, "metodo", None)
            info = getattr(r, "informacoes_adicionais", None)

            if metodo == "À vista" and not info:
                r.informacoes_adicionais = f"Desconto de {int(self.desconto_vista)}%"
            if metodo == "Cartão com juros":
                # sobrescrever si está ausente o tiene 0%
                if (not info) or ("0%" in str(info)):
                    r.informacoes_adicionais = f"Juros de {int(self.juros_parcelamento)}%"

            normalized.append(r)

        return normalized

