Write-Host "Iniciando Backend em modo de desenvolvimento..." -ForegroundColor Green

# Navega para o diretório backend
Set-Location backend

# Ativa o ambiente virtual
& .\venv\Scripts\Activate.ps1

# Inicia o servidor FastAPI com SQLite
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000