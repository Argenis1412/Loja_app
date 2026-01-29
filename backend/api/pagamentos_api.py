from fastapi import APIRouter, Depends, HTTPException

from backend.services.pagamento_service import PagamentoService
from backend.api.dtos.pagamento_request import CriarPagamentoRequest
from backend.api.dtos.pagamento_response import PagamentoResponse
from backend.api.deps import get_pagamento_service
from backend.domain.exceptions import RegraNegocioException

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"],
)


@router.post(
    "/",
    response_model=PagamentoResponse,
    status_code=201,
)
def criar_pagamento(
    dados: CriarPagamentoRequest,
    service: PagamentoService = Depends(get_pagamento_service),
):
    """
    Cria um novo pagamento e retorna o recibo formatado para API.
    """
    try:
        recibo = service.criar_pagamento(
            opcao=dados.opcao,
            valor=dados.valor,
            parcelas=dados.parcelas,
        )

        return PagamentoResponse.from_domain(recibo)

    except RegraNegocioException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[PagamentoResponse],
)
def listar_pagamentos(
    service: PagamentoService = Depends(get_pagamento_service),
):
    """
    Lista todos os pagamentos registrados.
    """
    recibos = service.listar_pagamentos()

    return [
        PagamentoResponse.from_domain(recibo)
        for recibo in recibos
    ]


