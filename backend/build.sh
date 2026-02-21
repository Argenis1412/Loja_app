#!/usr/bin/env bash
# sair em caso de erro
set -o errexit

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Executar migrações do banco de dados
alembic upgrade head
