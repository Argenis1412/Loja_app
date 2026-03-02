# Script para aplicar as migrações do Alembic

Write-Host "Executando Migrações da Base de Dados..." -ForegroundColor Cyan

# Backend
Set-Location backend
# Ativar o ambiente virtual
.\venv\Scripts\activate
# Executar as migrações
alembic upgrade head
# Desativar o ambiente virtual
deactivate
Set-Location ..

Write-Host "Migrações concluídas!" -ForegroundColor Green
