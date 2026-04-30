from typing import List

from fastapi import APIRouter, Depends, Header, status

from api.deps import get_pagamento_service
from api.dtos.pagamento_request import PagamentoRequest
from api.dtos.pagamento_response import PagamentoResponse
from domain.calculadora import Calculadora
from services.pagamento_service import PagamentoService

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post(
    "/",
    response_model=PagamentoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo pagamento",
)
def criar_pagamento(
    dados: PagamentoRequest,
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
    service: PagamentoService = Depends(get_pagamento_service),
):
    """
    Cria um novo pagamento e o persiste no banco de dados.
    Suporta Idempotency-Key para evitar duplicados.
    """
    recibo = service.criar_pagamento(
        opcao=dados.opcao,
        valor=dados.valor,
        parcelas=dados.parcelas,
        idempotency_key=idempotency_key,
    )
    return PagamentoResponse.from_domain(recibo)


@router.post(
    "/simular",
    response_model=PagamentoResponse,
    status_code=status.HTTP_200_OK,
    summary="Simular pagamento",
)
def simular_pagamento(dados: PagamentoRequest):
    """
    Simula um pagamento para exibir os cálculos sem persistir no banco.
    """
    calculadora = Calculadora()
    # Se parcelas for None, assume 1 para evitar erro na calculadora
    parcelas = dados.parcelas if dados.parcelas is not None else 1
    recibo = calculadora.calcular(
        opcao=dados.opcao, valor=dados.valor, parcelas=parcelas
    )
    return PagamentoResponse.from_domain(recibo)


@router.get(
    "/",
    response_model=List[PagamentoResponse],
    summary="Listar pagamentos",
)
def listar_pagamentos(
    limit: int = 20,
    offset: int = 0,
    service: PagamentoService = Depends(get_pagamento_service),
):
    """
    Lista todos os pagamentos persistidos com suporte a paginação.
    Default limit=20, offset=0.
    """
    recibos = service.listar_pagamentos(limit=limit, offset=offset)
    return [PagamentoResponse.from_domain(recibo) for recibo in recibos]
