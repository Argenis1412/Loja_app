# Script de setup completo para Windows

Write-Host "Setup do Loja App" -ForegroundColor Cyan

# Backend
Write-Host "`nConfigurando Backend..." -ForegroundColor Yellow
Set-Location backend
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
Set-Location ..

# Frontend
Write-Host "`nConfigurando Frontend..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

Write-Host "`nSetup concluido!" -ForegroundColor Green
Write-Host "Para rodar:" -ForegroundColor Cyan
Write-Host "  Backend:  .\run_backend.ps1" -ForegroundColor White
Write-Host "  Frontend: .\run_frontend.ps1" -ForegroundColor White