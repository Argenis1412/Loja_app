# Script para rodar testes

Write-Host "Executando Testes..." -ForegroundColor Cyan

# Backend
Write-Host "Backend Tests:" -ForegroundColor Yellow

if (Test-Path "backend") {
    Push-Location "backend"
    & ".\venv\Scripts\python.exe" -m pytest -v
    Pop-Location
} else {
    Write-Host "Pasta 'backend' nao encontrada!" -ForegroundColor Red
}

Write-Host "Testes de Backend finalizados." -ForegroundColor Green

# Frontend
Write-Host "Frontend Tests:" -ForegroundColor Yellow

if (Test-Path "frontend") {
    Push-Location "frontend"
    $env:CI = "true"
    npm test
    Pop-Location
} else {
    Write-Host "Pasta 'frontend' nao encontrada!" -ForegroundColor Red
}

Write-Host "Todos os testes concluidos!" -ForegroundColor Green
