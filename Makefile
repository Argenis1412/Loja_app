.PHONY: help install install-backend install-frontend test test-backend lint lint-backend lint-frontend format format-backend format-frontend run-backend run-frontend clean

# Cores
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

help: ## 📋 Mostra este menu de ajuda
	@echo "$(BLUE)════════════════════════════════════════$(RESET)"
	@echo "$(BLUE)  Loja App - Comandos Disponíveis$(RESET)"
	@echo "$(BLUE)════════════════════════════════════════$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

install: install-backend install-frontend ## 📦 Instala todas as dependências

install-backend: ## 🐍 Instala dependências do backend
	@echo "$(BLUE)📦 Instalando dependências do backend...$(RESET)"
	@cd backend && python -m venv venv
	@cd backend && ./venv/bin/pip install --upgrade pip
	@cd backend && ./venv/bin/pip install -r requirements.txt
	@echo "$(GREEN)✅ Backend pronto!$(RESET)"

install-frontend: ## 📦 Instala dependências do frontend
	@echo "$(BLUE)📦 Instalando dependências do frontend...$(RESET)"
	@cd frontend && npm install
	@echo "$(GREEN)✅ Frontend pronto!$(RESET)"

test: test-backend ## 🧪 Roda todos os testes

test-backend: ## 🧪 Roda testes do backend
	@echo "$(BLUE)🧪 Executando testes do backend...$(RESET)"
	@cd backend && ./venv/bin/pytest -v --tb=short

lint: lint-backend lint-frontend ## 🔍 Verifica qualidade de código

lint-backend: ## 🔍 Verifica código Python
	@echo "$(BLUE)🔍 Verificando qualidade do código Python...$(RESET)"
	@cd backend && ./venv/bin/pip install flake8 black isort 2>/dev/null || true
	@cd backend && ./venv/bin/flake8 . || echo "$(YELLOW)⚠️ Avisos do Flake8$(RESET)"
	@cd backend && ./venv/bin/black --check . || echo "$(YELLOW)⚠️ Código precisa ser formatado$(RESET)"
	@cd backend && ./venv/bin/isort --check-only . || echo "$(YELLOW)⚠️ Imports precisam ser organizados$(RESET)"

lint-frontend: ## 🔍 Verifica código TypeScript
	@echo "$(BLUE)🔍 Verificando qualidade do código TypeScript...$(RESET)"
	@cd frontend && npm run lint || echo "$(YELLOW)⚠️ Configure ESLint$(RESET)"

format: format-backend format-frontend ## ✨ Formata todo o código

format-backend: ## ✨ Formata código Python
	@echo "$(BLUE)✨ Formatando código Python...$(RESET)"
	@cd backend && ./venv/bin/pip install black isort 2>/dev/null || true
	@cd backend && ./venv/bin/black .
	@cd backend && ./venv/bin/isort .
	@echo "$(GREEN)✅ Python formatado!$(RESET)"

format-frontend: ## ✨ Formata código TypeScript
	@echo "$(BLUE)✨ Formatando código TypeScript...$(RESET)"
	@cd frontend && npm run format || echo "$(YELLOW)⚠️ Configure Prettier$(RESET)"

run-backend: ## 🚀 Inicia servidor backend
	@echo "$(BLUE)🚀 Iniciando backend em http://localhost:8000$(RESET)"
	@echo "$(BLUE)📚 Documentação em http://localhost:8000/docs$(RESET)"
	@cd backend && ./venv/bin/uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-frontend: ## 🚀 Inicia servidor frontend
	@echo "$(BLUE)🚀 Iniciando frontend em http://localhost:5173$(RESET)"
	@cd frontend && npm run dev

clean: ## 🧹 Remove arquivos gerados e caches
	@echo "$(BLUE)🧹 Limpando caches e arquivos gerados...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@rm -rf backend/htmlcov/ 2>/dev/null || true
	@rm -rf frontend/dist/ 2>/dev/null || true
	@rm -rf frontend/node_modules/.cache/ 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(RESET)"

.DEFAULT_GOAL := help