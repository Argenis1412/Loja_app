__all__ = []

# Importa a calculadora e garante o alias para o nome antigo usado em testes/código.
try:
    from .calculadora import Calculadora, CalculadoraPagamentos  # type: ignore

    __all__.extend(["Calculadora", "CalculadoraPagamentos"])
except Exception:
    Calculadora = None  # type: ignore
    CalculadoraPagamentos = None  # type: ignore

# Tenta exportar Recibo se existir
try:
    from .recibo import Recibo  # type: ignore

    __all__.append("Recibo")
except Exception:
    Recibo = None  # type: ignore
