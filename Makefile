.PHONY: install test run clean

install:
	pip install -e backend/.[dev]

test:
	cd backend && pytest

run:
	uvicorn backend.api.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage