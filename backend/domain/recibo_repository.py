from abc import ABC, abstractmethod

from domain.recibo import Recibo


class ReciboRepository(ABC):
    @abstractmethod
    def salvar(self, recibo: Recibo) -> None:
        ...

    @abstractmethod
    def listar(self, limit: int = 20, offset: int = 0) -> list[Recibo]:
        ...
    @abstractmethod
    def buscar_por_idempotency_key(self, key: str) -> Recibo | None:
        ...
