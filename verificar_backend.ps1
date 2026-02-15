# Script para verificar los cambios del backend

Write-Host "=== Verificando cambios del backend ===" -ForegroundColor Cyan

# Ir al directorio del backend
Set-Location "C:\Users\Sony Vaio I3\Desktop\Projetos GITHUB\Loja mini_app\backend"

# Ejecutar migración
Write-Host "`nEjecutando migración de Alembic..." -ForegroundColor Yellow
alembic upgrade head

# Ejecutar tests
Write-Host "`nEjecutando tests..." -ForegroundColor Yellow
pytest -v --tb=short

Write-Host "`n=== Verificación completada ===" -ForegroundColor Green
