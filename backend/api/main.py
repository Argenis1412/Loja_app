import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.pagamentos_api import router as pagamentos_router
from domain.exceptions import DomainError
from infrastructure.database import create_db_and_tables, warmup_db

description = """
API para a Loja Mini App, permitindo simulação e processamento de pagamentos.
Gerencia regras de negócio para diferentes métodos de pagamento e parcelamento.
"""

app = FastAPI(
    title="Loja Mini App API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Suporte Técnico",
        "url": "https://github.com/Argenis1412/Loja_app",
    },
)

# Armazenamento simples para rate limiting (em memória)
# Estrutura: { ip: (timestamp_inicio_janela, contador) }
rate_limit_data = {}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Ignorar rate limit para o endpoint de saúde
    if request.url.path == "/saude":
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    if client_ip in rate_limit_data:
        start_time, count = rate_limit_data[client_ip]
        if now - start_time < 60:
            if count >= 30:  # Limite de 30 requisições por minuto
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "Limite de requisições excedido. Tente novamente em 1 minuto."
                    },
                )
            rate_limit_data[client_ip] = (start_time, count + 1)
        else:
            rate_limit_data[client_ip] = (now, 1)
    else:
        rate_limit_data[client_ip] = (now, 1)

    return await call_next(request)


@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação.
    Cria tabelas e aquece o pool de conexões.
    """
    create_db_and_tables()
    warmup_db()


# Manipulador de exceções de domínio para retornar 400 Bad Request
@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


# Endpoint de verificação de saúde da API
@app.get(
    "/saude",
    status_code=status.HTTP_200_OK,
    tags=["Infraestrutura"],
    summary="Verificar saúde da API",
)
def verificar_saude():
    """
    Retorna o status operacional da API e seus componentes.
    Útil para monitoramento e scripts de warm-up.
    """
    return {"status": "operacional"}


app.include_router(pagamentos_router)
