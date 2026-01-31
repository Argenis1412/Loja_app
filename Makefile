.PHONY: install test run clean

install:
	pip install -r backend/requirements.txt

test:
	pytest -c backend/pytest.ini

run:
	uvicorn backend.api.main:app --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage