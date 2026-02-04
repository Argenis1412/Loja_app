class DomainError(Exception):
    """Exceção base para todos os erros de regra de negócio/domínio."""
    pass


class OpcaoInvalidaError(DomainError):
    """Exceção levantada para opções de pagamento inválidas."""
    pass


class ValorInvalidoError(DomainError):
    """Exceção levantada para valores ou parcelas inválidas."""
    pass


class RegraPagamentoInvalida(DomainError):
    """Exceção levantada para regras de pagamento inválidas na calculadora."""
    pass