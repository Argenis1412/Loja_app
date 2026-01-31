from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.api.pagamentos_api import router as pagamentos_router
from backend.services.pagamento_service import PagamentoService
from backend.api.dtos.pagamento_response import PagamentoResponse

app = FastAPI(title="Loja App - Pagamentos")

origens_permitidas = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimularPagamentoRequest(BaseModel):
    opcao: int
    valor: float
    parcelas: int

@app.post("/pagamentos/simular", response_model=PagamentoResponse)
def simular_pagamento(dados: SimularPagamentoRequest):
    # inicializa o serviço de pagamento sem repositório para apenas simular
    service = PagamentoService(repository=None)
    
    recibo = service.criar_pagamento(
        opcao=dados.opcao,
        valor=dados.valor,
        parcelas=dados.parcelas
    )
    return PagamentoResponse.from_domain(recibo)

app.include_router(pagamentos_router)
