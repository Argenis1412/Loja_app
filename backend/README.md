# Loja App — Backend (Payments API)

![CI](https://github.com/Argenis1412/Loja_app/actions/workflows/backend-ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

This is the core of the Loja App, implementing the business logic, payment calculations, and transaction persistence using a **Clean Architecture** (DDD) approach.

---

## 🏛 Architecture & Principles

- **Framework**: FastAPI (Python 3.12)
- **Persistence**: PostgreSQL (SQLAlchemy + Alembic)
- **Design**: Layered architecture (Domain, Service, Infrastructure, API)
- **Calculations**: Centralized in `domain/calculadora.py`, framework-agnostic.

### Key Features
- **Exact Total splitting**: Last installment adjusted to ensure zero rounding errors.
- **Domain-Driven Validation**: Custom exceptions (e.g., `ValorInvalidoError`) for business rules.
- **API First**: Automatic documentation via Swagger and ReDoc.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+ (Note: `pydantic-core` requires 3.12 for pre-built wheels)
- PostgreSQL (or SQLite for local testing)

### Setup
1.  **Environment**: `python -m venv venv`
2.  **Activate**: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
3.  **Install**: `pip install -r requirements.txt`
4.  **Database**: `alembic upgrade head`
5.  **Run**: `uvicorn api.main:app --reload`

---

## 📂 Project Structure

```text
backend/
├── api/            # API Layer (FastAPI, DTOs, Routes)
├── domain/         # Business Logic (Calculadora, Entities, Exceptions)
├── services/       # Use Cases (PagamentoService)
├── infrastructure/ # DB Drivers, Repositories, Migrations
└── tests/          # Pytest suite (Unit & Integration)
```

---

## 🧪 Testing

The backend maintains high test coverage using **Pytest**.

```bash
# Run all tests (uses SQLite in-memory for speed)
pytest

# Run with coverage report
pytest --cov=. --cov-report=html
```

---

## 🔌 API Endpoints Summary

- `POST /pagamentos/` — Create and persist a payment.
- `POST /pagamentos/simular` — Simulate payment without saving.
- `GET /pagamentos/` — List transaction history.
- `GET /saude` — Basic health check.

For detailed request/response schemas, refer to the local Swagger UI at `/docs`.

---

## 📄 License
Licensed under the **MIT License**.