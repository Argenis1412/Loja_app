param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("setup", "frontend", "backend", "test", "lint", "db-upgrade", "db-migrate")]
    [string]$Command
)

$RootDir = $PSScriptRoot
$BackendDir = Join-Path $RootDir "backend"
$FrontendDir = Join-Path $RootDir "frontend"

switch ($Command) {
    "setup" {
        Write-Host "Realizando setup do projeto..." -ForegroundColor Green
        Write-Host "-> Configurando Backend..."
        cd $BackendDir
        if (-not (Test-Path "venv")) { python -m venv venv }
        .\venv\Scripts\activate
        pip install -r requirements.txt
        
        Write-Host "-> Configurando Frontend..."
        cd $FrontendDir
        npm install
        
        Write-Host "Setup concluído!" -ForegroundColor Green
    }
    "frontend" {
        Write-Host "Iniciando Frontend (Vite)..." -ForegroundColor Green
        cd $FrontendDir
        npm run dev
    }
    "backend" {
        Write-Host "Iniciando Backend (FastAPI)..." -ForegroundColor Green
        cd $BackendDir
        .\venv\Scripts\activate
        # Set PYTHONPATH so absolute imports work
        $env:PYTHONPATH = $BackendDir
        uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    }
    "test" {
        Write-Host "Executando Testes (Backend)..." -ForegroundColor Green
        cd $BackendDir
        .\venv\Scripts\activate
        $env:PYTHONPATH = $BackendDir
        pytest
    }
    "lint" {
        Write-Host "Executando Linters..." -ForegroundColor Green
        cd $BackendDir
        .\venv\Scripts\activate
        isort .
        black .
        flake8 .
        mypy .
        cd $FrontendDir
        npm run lint
    }
    "db-migrate" {
        Write-Host "Gerando migração de banco de dados..." -ForegroundColor Green
        cd $BackendDir
        .\venv\Scripts\activate
        $env:PYTHONPATH = $BackendDir
        $Message = Read-Host "Digite a mensagem para a migração"
        alembic revision --autogenerate -m "$Message"
    }
    "db-upgrade" {
        Write-Host "Aplicando migrações no banco de dados..." -ForegroundColor Green
        cd $BackendDir
        .\venv\Scripts\activate
        $env:PYTHONPATH = $BackendDir
        alembic upgrade head
    }
}
