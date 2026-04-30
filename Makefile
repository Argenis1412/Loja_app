.PHONY: help dev back front test test-back test-front lint clean

# Cores
BLUE := \033[36m
GREEN := \033[32m
RESET := \033[0m

help: ## 📋 Mostra este menu de ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[32m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## 🚀 Executa tudo (Backend + Frontend)
	@echo "$(BLUE)Iniciando ambiente completo...$(RESET)"
	@make -j 2 back front

back: ## 🐍 Executa Backend (localhost:8000)
	@echo "$(BLUE)Iniciando Backend...$(RESET)"
	@cd backend && ./venv/Scripts/python -m uvicorn api.main:app --reload

front: ## 📦 Executa Frontend (localhost:5173)
	@echo "$(BLUE)Iniciando Frontend...$(RESET)"
	@cd frontend && npm run dev

test: test-back test-front ## 🧪 Roda todos os testes

test-back: ## 🐍 Tests Backend
	@cd backend && ./venv/Scripts/python -m pytest

test-front: ## 📦 Tests Frontend
	@cd frontend && npm test -- --run

lint: ## 🔍 Linting
	@cd backend && ./venv/Scripts/python -m ruff check .
	@cd frontend && npm run lint

clean: ## 🧹 Limpeza
	@rm -rf backend/.pytest_cache frontend/dist node_modules
	@find . -type d -name "__pycache__" -exec rm -rf {} +