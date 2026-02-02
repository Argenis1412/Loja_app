.PHONY: install test run clean lint format

install:
	pip install -e backend/.[dev]

test:
	cd backend && pytest

run:
	uvicorn backend.api.main:app --reload

lint:
	cd backend && flake8 .
	cd backend && black --check .
	cd backend && isort --check .
	cd backend && mypy .

format:
	cd backend && black .
	cd backend && isort .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage