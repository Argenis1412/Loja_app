param (
    [Parameter(Mandatory=$false, Position=0)]
    [string]$Task = "help"
)

switch ($Task) {
    "dev" {
        Write-Host "Starting full environment (2 windows)..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; ./venv/Scripts/python -m uvicorn api.main:app --reload"
        Write-Host "Starting Frontend in current window..." -ForegroundColor Yellow
        cd frontend; npm run dev
    }
    "back" {
        Write-Host "Starting Backend..." -ForegroundColor Cyan
        cd backend; ./venv/Scripts/python -m uvicorn api.main:app --reload
    }
    "front" {
        Write-Host "Starting Frontend..." -ForegroundColor Cyan
        cd frontend; npm run dev
    }
    "test" {
        Write-Host "Running all tests..." -ForegroundColor Cyan
        cd backend; ./venv/Scripts/python -m pytest
        cd frontend; npm test -- --run
    }
    "test-back" {
        cd backend; ./venv/Scripts/python -m pytest
    }
    "test-front" {
        cd frontend; npm test -- --run
    }
    "lint" {
        Write-Host "Running linters..." -ForegroundColor Cyan
        cd backend; ./venv/Scripts/python -m ruff check .
        cd frontend; npm run lint
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
