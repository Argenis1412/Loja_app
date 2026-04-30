param (
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Task = "help"
)

$Root = $PSScriptRoot

switch ($Task) {
    "dev" {
        Write-Host "Starting full environment (2 windows)..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd $Root/backend; ./venv/Scripts/python -m uvicorn api.main:app --reload"
        Write-Host "Starting Frontend in current window..." -ForegroundColor Yellow
        Set-Location $Root/frontend
        npm run dev
    }
    "back" {
        Write-Host "Starting Backend..." -ForegroundColor Cyan
        Set-Location $Root/backend
        ./venv/Scripts/python -m uvicorn api.main:app --reload
    }
    "front" {
        Write-Host "Starting Frontend..." -ForegroundColor Cyan
        Set-Location $Root/frontend
        npm run dev
    }
    "test" {
        Write-Host "Running all tests..." -ForegroundColor Cyan
        Write-Host "--- Backend Tests ---" -ForegroundColor Blue
        Set-Location $Root/backend
        ./venv/Scripts/python -m pytest
        Write-Host "--- Frontend Tests ---" -ForegroundColor Blue
        Set-Location $Root/frontend
        npm test -- --run
        Set-Location $Root
    }
    "test-back" {
        Set-Location $Root/backend
        ./venv/Scripts/python -m pytest
    }
    "test-front" {
        Set-Location $Root/frontend
        npm test -- --run
    }
    "lint" {
        Write-Host "Running linters..." -ForegroundColor Cyan
        Set-Location $Root/backend
        ./venv/Scripts/python -m ruff check .
        Set-Location $Root/frontend
        npm run lint
    }
    default {
        Write-Host "Available commands:" -ForegroundColor Green
        Write-Host "  ./make dev         - Run everything"
        Write-Host "  ./make back        - Run backend"
        Write-Host "  ./make front       - Run frontend"
        Write-Host "  ./make test        - Run all tests"
        Write-Host "  ./make lint        - Run linters"
    }
}
