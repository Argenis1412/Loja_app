from backend.domain.exceptions import RegraPagamentoInvalida
from backend.domain.recibo import Recibo


class Calculadora:
    def calcular(
        self,
        opcao: int,
        valor: float,
        parcelas: int,
        desconto_vista: float = 10.0,
        juros_parcelamento: float = 10.0,
    ) -> Recibo:

        if valor <= 0:
            raise RegraPagamentoInvalida("Valor inválido")

        if opcao == 1:
            total = valor * (1 - desconto_vista / 100)
            parcelas = 1
            metodo = "À vista"
            info = f"Desconto de {int(desconto_vista)}%"

        elif opcao == 2:
            # Débito à vista com desconto fixo de 5%
            total = valor * (1 - 5.0 / 100)
            parcelas = 1
            metodo = "Débito à vista"
            info = "Desconto de 5% no débito"

        elif opcao == 3:
            if parcelas < 2 or parcelas > 6:
                raise RegraPagamentoInvalida("Opção 3 suporta apenas de 2 a 6 parcelas")
            total = valor
            metodo = "Parcelado sem juros"
            info = None

        elif opcao == 4:
            if parcelas < 2 or parcelas > 12:
                raise RegraPagamentoInvalida("Parcelas inválidas")
            total = valor * (1 + juros_parcelamento / 100)
            metodo = "Cartão com juros"
            info = f"Juros de {int(juros_parcelamento)}%"

        else:
            raise RegraPagamentoInvalida("Opção inválida")

        valor_parcela = round(total / parcelas, 2)
        total = round(total, 2)

        recibo = Recibo(
            metodo=metodo,
            total=total,
            parcelas=parcelas,
            valor_parcela=valor_parcela,
            informacoes_adicionais=info,
        )
        # Armazena valor original para uso na API
        recibo._original_valor = valor
        return recibo
