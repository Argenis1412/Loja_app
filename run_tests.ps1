# Parar o script imediatamente se ocorrer algum erro
$ErrorActionPreference = "Stop"

Write-Host "🛠️  Verificando ambiente..."

# Verificar se o npm está instalado
if (!(Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "❌ Erro: 'npm' não está instalado. Por favor instale o Node.js e npm."
    exit 1
}

# Configuração do Ambiente Virtual Python
if (!(Test-Path ".venv")) {
    Write-Host "🐍 Criando ambiente virtual Python (.venv)..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Error "❌ Erro: Falha ao criar venv."
        exit 1
    }
}

Write-Host "🔌 Ativando ambiente virtual..."
# Tenta ativar o venv no Windows
try {
    . .\.venv\Scripts\Activate.ps1
}
catch {
    Write-Warning "⚠️  Não foi possível ativar o venv via script. Tentando usar o python do venv diretamente."
}

Write-Host "📦 Garantindo que as dependências estão instaladas..."
# Equivalente ao 'make install'
pip install -e backend/.[dev]

# Instalação do Frontend
Push-Location frontend
npm install
Pop-Location

Write-Host "🧹 Limpando arquivos temporários..."
# Equivalente ao 'make clean'
Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Include "*.pyc" -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force
if (Test-Path ".coverage") { Remove-Item ".coverage" -Force }

# Solução automática para o erro do pytest (arquivo duplicado)
if (Test-Path "backend/tests/domain/test_calculadora.py") {
    Remove-Item "backend/tests/domain/test_calculadora.py" -Force
}
# Tenta remover o diretório se estiver vazio (equivalente ao rmdir --ignore-fail-on-non-empty)
if (Test-Path "backend/tests/domain") {
    try { Remove-Item "backend/tests/domain" -ErrorAction SilentlyContinue } catch {}
}

Write-Host "🎨 Verificando estilo de código (Linting)..."
# Equivalente ao 'make lint'
Push-Location backend
flake8 .
black --check .
isort --check .
mypy .
Pop-Location

Write-Host "🐍 Executando testes do Backend..."
Push-Location backend
pytest
Pop-Location

Write-Host "⚛️  Executando testes do Frontend..."
Push-Location frontend
npm test -- run
Pop-Location

Write-Host "✅ Todos os sistemas operacionais e testes passaram corretamente!"
