from abc import ABC, abstractmethod
from backend.domain.recibo import Recibo

class ReciboRepository(ABC):
    @abstractmethod
    def salvar(self, recibo: Recibo) -> None: ...

    @abstractmethod
    def listar(self) -> list[Recibo]: ...
