# Script para rodar backend no Windows

Write-Host "Iniciando Backend..." -ForegroundColor Cyan

# Ativar ambiente virtual
Set-Location backend
.\venv\Scripts\activate

# Rodar servidor
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000