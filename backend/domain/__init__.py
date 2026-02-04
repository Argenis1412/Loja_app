__all__ = []

# Importa a calculadora e garante o alias para o nome antigo usado em testes/código.
from .calculadora import Calculadora, CalculadoraPagamentos

__all__.extend(["Calculadora", "CalculadoraPagamentos"])

from .recibo import Recibo

__all__.append("Recibo")