# Pacote services: exporta os serviços públicos de forma compatível.
# Import defensivo para evitar que a importação do pacote quebre durante refatorações.

__all__ = []

try:
    from .pagamento_service import PagamentoService  # type: ignore

    __all__.append("PagamentoService")
except Exception:
    PagamentoService = None  # type: ignore
