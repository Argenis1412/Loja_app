from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.pagamentos_api import router as pagamentos_router

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

app.include_router(pagamentos_router)


