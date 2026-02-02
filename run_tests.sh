#!/bin/bash

# Parar o script imediatamente se ocorrer algum erro
set -e

echo "🛠️  Verificando ambiente..."
if ! command -v make &> /dev/null; then
    echo "❌ Erro: 'make' não está instalado. Por favor execute: sudo apt install make"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Erro: 'npm' não está instalado. Por favor instale o Node.js e npm."
    exit 1
fi

# Configuração do Ambiente Virtual Python para evitar erro "externally-managed-environment"
if [ ! -d ".venv" ]; then
    echo "🐍 Criando ambiente virtual Python (.venv)..."
    python3 -m venv .venv || { echo "❌ Erro: Falha ao criar venv. Instale: sudo apt install python3-venv"; exit 1; }
fi

echo "🔌 Ativando ambiente virtual..."
# O ponto (.) é equivalente ao source, mas mais compatível
. .venv/bin/activate

echo "📦 Garantindo que as dependências estão instaladas..."
# Instala dependências do Python (flake8, pytest, etc.) e do Frontend
make install
(cd frontend && npm install)

echo "🧹 Limpando arquivos temporários..."
make clean

# Solução automática para o erro do pytest (arquivo duplicado)
rm -f backend/tests/domain/test_calculadora.py
if [ -d "backend/tests/domain" ]; then rmdir --ignore-fail-on-non-empty backend/tests/domain; fi

echo "🎨 Verificando estilo de código (Linting)..."
make lint

echo "🐍 Executando testes do Backend..."
(cd backend && pytest)

echo "⚛️  Executando testes do Frontend..."
(cd frontend && npm test -- run)

echo "✅ Todos os sistemas operacionais e testes passaram corretamente!"