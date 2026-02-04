# 🛍️ Loja App — Backend (Payments API)

![CI](https://github.com/argenis972/Loja_app/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20REST-009688?style=flat&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Automated%20Tests-brightgreen?style=flat)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-336791?style=flat&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **Scope note:** This is a learning / lab project focused on backend architecture, financial logic, and testing.

## 🧠 Architecture & Purpose

This backend is an API-first payment system built as a learning laboratory. Its goal is not to maximize features but to maximize clarity, correctness, and architectural reasoning.

The backend is responsible for:

- Enforcing all business rules
- Validating user input and edge cases
- Calculating payment totals and installments
- Persisting transactions reliably
- Exposing a clean, documented REST API
- Being testable, explainable, and evolvable

The frontend is treated as a consumer, never as a source of truth.

<!-- Author and License are declared in the repository root README -->

Each layer has one responsibility and no shortcuts.

---

## 🧮 Domain & Business Rules

All payment rules live exclusively in the domain layer. They are framework-agnostic, deterministic, and unit-tested.

### Supported Payment Modes

| Mode         | Condition           | Rule Applied      |
|--------------|---------------------|-------------------|
| Cash (upfront)   | Immediate payment    | 10% discount      |
| Debit card (upfront) | Immediate payment    | 5% discount       |
| Short installments  | 2x – 6x              | No interest       |
| Card with interest  | 2x – 12x             | Fixed 10% increase|

> **Note:** "Debit card" and "credit card" are treated as distinct options. "Card" is never ambiguous in the API contract. This distinction avoids implicit assumptions common in simplified payment examples.

### Validation Rules

- Installments > 12 are invalid (for any method)
- Invalid business inputs raise domain exceptions (not HTTP errors)
- No rule is duplicated outside the domain

This guarantees consistency across API, tests, and future interfaces.

---

## 🌐 API Layer (FastAPI)

The API layer is intentionally thin. Responsibilities:

- Parse and validate HTTP requests
- Map DTOs to domain inputs
- Translate domain errors into HTTP responses
- Return clean, explicit responses

### Why FastAPI?

- Native async support
- Excellent request validation
- Automatic OpenAPI / Swagger docs
- Minimal boilerplate

### Example Endpoint

**POST /pagamentos/**

Request:
```json
{
  "opcao": 3,
  "valor": 100.00,
  "parcelas": 6
}
```

Response:
```json
{
  "total": 100.00,
  "valor_parcela": 16.67,
  "parcelas": 6,
  "taxas": "0% (Sem juros)",
  "status": "aprovado"
}
```

### `opcao` mapping

The API accepts an internal `opcao` integer that identifies the payment mode. The frontend maps user-friendly payment methods to these IDs.

| `opcao` | Meaning |
|--------:|---------|
| 1 | À vista (cash) — 10% discount |
| 2 | Débito (debit card) — 5% discount |
| 3 | Parcelado sem juros (short installments, 2–6x) — no interest |
| 4 | Cartão com juros (installments, 2–12x) — fixed increase |

> **Note:** "Debit card" (opcao 2) is not "credit card". Credit and debit are always separated in the contract.

### Notes

- `opcao` is an internal domain mapping (payment option identifier), not a user-facing concept. The UI translates user selections into the appropriate `opcao` value before calling the API.
- API contract: The API contract is intentionally explicit and treated as stable. Breaking changes are considered architectural decisions and should be versioned and communicated.

---

## 🗄️ Persistence Layer (PostgreSQL)

PostgreSQL is used as a realistic persistence layer for integration tests and architectural validation, not as a full production schema.

Persistence is implemented using:

- PostgreSQL — realistic production-grade database
- SQLAlchemy — ORM and transaction handling
- Alembic — schema migrations

### Why PostgreSQL (even for a lab)?

- Forces realistic data modeling
- Avoids misleading in-memory shortcuts
- Enables real integration tests
- Mirrors production constraints

### Databases Used

- `loja_db` → development
- `loja_test_db` → automated tests (isolated)

Migrations ensure schema evolution is explicit and reproducible.

---

## 📁 Project Structure (backend)

A short, developer-focused view of the `backend/` layout and responsibilities.

```
backend/
├── api/                     # FastAPI entrypoints, routes and DTOs
│   ├── main.py              # app factory and server entry
│   ├── pagamentos_api.py    # pagamentos HTTP handlers
│   ├── deps.py              # request dependencies and DI helpers
│   └── dtos/                # request/response DTOs (pydantic)
├── config/                  # runtime config and static tax tables
│   └── settings.py
├── domain/                  # business logic (pure, testable)
│   ├── calculadora.py       # payment calculation rules
│   ├── recibo.py            # domain model for receipts
│   └── exceptions.py        # domain-specific exceptions
├── infrastructure/          # adapters and infra concerns
│   ├── database.py          # engine / session setup           
│   ├── db/                  # DB-specific modules (models, mappers)
│   │   ├── base.py
│   │   ├── models/
│   │   └── mappers/
│   └── repositories/        # repository implementations (Postgres)
├── services/                # application services / use-cases
│   └── pagamento_service.py
├── alembic/                 # migrations (managed by Alembic)
├── tests/                   # unit and integration tests
│   ├── conftest.py
│   ├── services/
│   |── unit/   # domain-level unit tests (e.g. test_calculadora.py)
│   └── ...
├── Makefile                 # Command runner (install, test, run, lint)
├── pyproject.toml           # Project dependencies and tool config
└── README.md
```

**Notes:**

- Keep business rules inside `domain/` — that folder is the source of truth.
- `api/dtos` must match `frontend/src/types` when the public API contract changes.
- Integration tests use `loja_test_db` and run migrations via `alembic`.

---

## ⚠️ Error Handling Strategy

This project makes a clear distinction between domain errors (business rule violations) and API/transport errors (validation, parsing).

- **Domain Errors:** invalid installments, unsupported payment options — raised as custom domain exceptions
- **API Errors:** invalid JSON, missing fields, wrong data types — handled by FastAPI validation

This separation avoids mixing business logic with transport concerns.

---

## 🧪 Testing Strategy

**Unit tests** target domain services and rules — no DB, no HTTP (fast and deterministic).

**Integration tests** use the `loja_test_db`, run migrations via Alembic, and exercise real API endpoints.

This combination provides high confidence without over-mocking.

---

## 🧠 Configuration & CI Considerations

The backend validates `DATABASE_URL` at import time. In CI environments this variable may be missing.

**Mitigation strategy:**

- Detect CI/test context and use a safe default test URL where appropriate. CI detection is done via environment variables (e.g. `CI=true`) to avoid implicit configuration.
- Keep explicit runtime failure when real configuration is missing

This behavior is intentional to surface configuration errors early.

---

## 🚀 Running the Backend

### Requirements

- Python 3.11+
- PostgreSQL 14+

### Install & Run

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn api.main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

---

## 🔮 What Would Change in Production?

In production you would typically add:

- Authentication & authorization
- Idempotency keys
- Message queues for async payments
- Observability (logs, metrics, tracing)
- Rate limiting
- Background workers

The architecture supports these changes without refactoring the domain.

---

## 🎯 Summary

- Clean Architecture in practice
- Explicit business rules
- Real persistence
- Meaningful tests
- Clear error boundaries
- API-first thinking

**Designed to be read, reasoned about, and defended.**

---

<!-- Author and License are declared in the repository root README -->