import time
import os
from fastapi import FastAPI, Request, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

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
    if request.url.path == "/api/saude":
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
    """
    create_db_and_tables()
    warmup_db()

    # Log das rotas disponíveis para depuração
    print("\n--- Rotas da API disponíveis ---")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"Rote: {route.path}")
    print("--------------------------------\n")


# Manipulador de exceções de domínio para retornar 400 Bad Request
@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir rotas da API diretamente no app com o prefixo /api
app.include_router(pagamentos_router, prefix="/api")


# Rota de saúde diretamente no app para máxima visibilidade
@app.get(
    "/api/saude",
    status_code=status.HTTP_200_OK,
    tags=["Infraestrutura"],
)
def verificar_saude():
    return {"status": "operacional"}


# Servir arquivos estáticos do frontend (React) em produção
# O diretório 'static' é criado pelo Dockerfile
static_path = os.path.join(os.getcwd(), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception):
        # Para SPA (React), qualquer rota não encontrada deve retornar o index.html
        return FileResponse(os.path.join(static_path, "index.html"))
