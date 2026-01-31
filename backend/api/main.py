from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from backend.api.pagamentos_api import router as pagamentos_router
from backend.services.pagamento_service import PagamentoService
from backend.api.dtos.pagamento_response import PagamentoResponse
from backend.infrastructure.database import engine
from backend.infrastructure.db.base import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Loja App - Pagamentos", lifespan=lifespan)

class Settings(BaseSettings):
    origens_permitidas: list[str] = ["http://localhost:5173"]

settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origens_permitidas,
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
