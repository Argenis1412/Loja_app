from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.pagamentos_api import router as pagamentos_router
from domain.exceptions import DomainError
from infrastructure.database import create_db_and_tables, warmup_db

app = FastAPI(title="Loja Mini App")


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
@app.get("/saude", status_code=status.HTTP_200_OK)
def verificar_saude():
    return {"status": "operacional"}


app.include_router(pagamentos_router)
