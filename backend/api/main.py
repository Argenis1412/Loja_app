import os
import uuid
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from api.pagamentos_api import router as pagamentos_router
from domain.exceptions import DomainError
from infrastructure.database import create_db_and_tables, warmup_db

# ---------------------------------------------------------------------------
# Configuração de logs estruturados
# ---------------------------------------------------------------------------
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# ---------------------------------------------------------------------------
# Rate limiter (slowapi) — sem estado em memória manual
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

# ---------------------------------------------------------------------------
# Ciclo de vida da aplicação (substitui @app.on_event("startup") deprecated)
# ---------------------------------------------------------------------------
description = """
API para a Loja Mini App, permitindo simulação e processamento de pagamentos.
Gerencia regras de negócio para diferentes métodos de pagamento e parcelamento.
"""

APP_VERSION = "1.0.0"
APP_ENV = os.getenv("APP_ENV", "development")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização
    create_db_and_tables()
    warmup_db()
    logger.info("app_startup", version=APP_VERSION, env=APP_ENV, routes=[
        r.path for r in app.routes if hasattr(r, "path")
    ])
    yield
    # Encerramento
    logger.info("app_shutdown")


# ---------------------------------------------------------------------------
# Instância principal da aplicação
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Loja Mini App API",
    description=description,
    version=APP_VERSION,
    lifespan=lifespan,
    contact={
        "name": "Suporte Técnico",
        "url": "https://github.com/Argenis1412/Loja_app",
    },
)

# Integrar o estado do limiter na app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---------------------------------------------------------------------------
# Middleware: Trace ID por requisição
# ---------------------------------------------------------------------------
@app.middleware("http")
async def trace_id_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response


# ---------------------------------------------------------------------------
# Manipuladores de exceção padronizados
# ---------------------------------------------------------------------------
@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: Exception):
    trace_id = getattr(request.state, "trace_id", None)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "DOMAIN_ERROR",
                "message": str(exc),
                "trace_id": trace_id,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    trace_id = getattr(request.state, "trace_id", None)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.errors(),
                "trace_id": trace_id,
            }
        },
    )


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Rotas — prefixo /api/v1
# ---------------------------------------------------------------------------
app.include_router(pagamentos_router, prefix="/api/v1")


@app.get(
    "/api/v1/saude",
    status_code=status.HTTP_200_OK,
    tags=["Infraestrutura"],
)
def verificar_saude():
    return {"status": "operacional", "version": APP_VERSION, "env": APP_ENV}


# ---------------------------------------------------------------------------
# Servir frontend (React) em produção
# ---------------------------------------------------------------------------
static_path = os.path.join(os.getcwd(), "static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception):
        if request.url.path.startswith("/api/"):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Recurso não encontrado na API"},
            )
        return FileResponse(os.path.join(static_path, "index.html"))
