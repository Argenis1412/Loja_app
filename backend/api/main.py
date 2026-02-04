from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.pagamentos_api import router as pagamentos_router
from infrastructure.database import create_db_and_tables
from domain.exceptions import DomainError

# Garante que as tabelas sejam criadas ao iniciar
create_db_and_tables()

app = FastAPI(title="Loja Mini App")


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