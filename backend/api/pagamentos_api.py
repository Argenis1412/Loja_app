from fastapi import APIRouter, Depends, status
from typing import List

from api.deps import get_pagamento_service
from api.dtos.pagamento_request import PagamentoRequest
from api.dtos.pagamento_response import PagamentoResponse
from services.pagamento_service import PagamentoService
from domain.calculadora import Calculadora

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_pagamento(
    dados: PagamentoRequest,
    service: PagamentoService = Depends(get_pagamento_service),
):
    """
    Cria um novo pagamento e o persiste no banco de dados.
    """
    recibo = service.criar_pagamento(
        opcao=dados.opcao, valor=dados.valor, parcelas=dados.parcelas
    )
    return PagamentoResponse.from_domain(recibo)


@router.post("/simular", response_model=PagamentoResponse, status_code=status.HTTP_200_OK)
def simular_pagamento(dados: PagamentoRequest):
    """
    Simula um pagamento para exibir os cálculos (juros, parcelas) sem persistir no banco.
    """
    calculadora = Calculadora()
    # Se parcelas for None, assume 1 para evitar erro na calculadora
    parcelas = dados.parcelas if dados.parcelas is not None else 1
    recibo = calculadora.calcular(
        opcao=dados.opcao, valor=dados.valor, parcelas=parcelas
    )
    return PagamentoResponse.from_domain(recibo)


@router.get("/", response_model=List[PagamentoResponse])
def listar_pagamentos(service: PagamentoService = Depends(get_pagamento_service)):
    """
    Lista todos os pagamentos persistidos.
    """
    recibos = service.listar_pagamentos()
    return [PagamentoResponse.from_domain(recibo) for recibo in recibos]
