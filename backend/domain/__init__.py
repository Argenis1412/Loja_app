__all__ = []

# Alias para compatibilidade com testes e código legado.
from .calculadora import Calculadora, CalculadoraPagamentos  # noqa: F401

__all__.extend(["Calculadora", "CalculadoraPagamentos"])

from .recibo import Recibo  # noqa: E402, F401

__all__.append("Recibo")
