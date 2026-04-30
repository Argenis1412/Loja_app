.PHONY: help dev back front test test-back test-front lint clean

# Colors
BLUE := \033[36m
GREEN := \033[32m
RESET := \033[0m

help: ## 📋 Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[32m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## 🚀 Run everything (Backend + Frontend)
	@echo "$(BLUE)Starting full environment...$(RESET)"
	@make -j 2 back front

back: ## 🐍 Run Backend (localhost:8000)
	@echo "$(BLUE)Starting Backend...$(RESET)"
	@cd backend && ./venv/Scripts/python -m uvicorn api.main:app --reload

front: ## 📦 Run Frontend (localhost:5173)
	@echo "$(BLUE)Starting Frontend...$(RESET)"
	@cd frontend && npm run dev

test: test-back test-front ## 🧪 Run all tests

test-back: ## 🐍 Backend Tests
	@cd backend && ./venv/Scripts/python -m pytest

test-front: ## 📦 Frontend Tests
	@cd frontend && npm test -- --run

lint: ## 🔍 Linting
	@cd backend && ./venv/Scripts/python -m ruff check .
	@cd frontend && npm run lint

clean: ## 🧹 Cleanup
	@rm -rf backend/.pytest_cache frontend/dist node_modules
	@find . -type d -name "__pycache__" -exec rm -rf {} +