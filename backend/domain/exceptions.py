class RegraNegocioException(Exception):
    """Exceção base para violações de regras de negócio"""
    pass


class RegraPagamentoInvalida(RegraNegocioException):
    """Erro específico de pagamento"""
    pass