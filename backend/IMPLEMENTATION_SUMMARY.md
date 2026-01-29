# PostgreSQL Persistence — Implementation Summary

## Overview

This document summarizes the final implementation of **PostgreSQL persistence** in the **Loja App backend**, using:

- **SQLAlchemy 2.x**
- **Alembic migrations**
- **FastAPI dependency injection**
- **Pytest with real database integration**

This branch (`Criar_PostgreSQL`) consolidates the backend as an **API-first system**, with a clean separation between domain, services, infrastructure, and delivery layers.

---

## Goals Achieved

- Persist receipts (`recibos`) in **PostgreSQL**
- Enforce schema consistency via **Alembic**
- Keep domain rules independent from infrastructure
- Support full integration testing with database isolation
- Ensure CI stability with deterministic DB initialization

All goals were met and validated by automated tests.

---

## Dependencies

### `requirements.txt`

Key persistence-related dependencies:

- `sqlalchemy>=2.0`
- `psycopg[binary]>=3.0`
- `alembic`
- `fastapi`
- `pytest`

The dependency list intentionally mixes runtime and test tools, as this is a learning/lab repository.

---

## Database Architecture

### 1. SQLAlchemy Core

#### `infrastructure/database.py`

Responsibilities:

- Resolve `DATABASE_URL` from environment
- Create SQLAlchemy `engine` and `SessionLocal`
- Provide session factory for repositories and services
- Detect test/CI context to avoid fatal import-time crashes
- Act as the single source of DB configuration

This module is imported early and intentionally fails fast **outside test/CI contexts** if the database is misconfigured.

---

### 2. ORM Models

#### `infrastructure/db/models/recibo_model.py`

Defines the `recibos` table schema:

| Column | Type | Notes |
|------|------|------|
| `id` | Integer | Primary key |
| `total` | Float | Final calculated amount |
| `metodo` | String(50) | Payment method |
| `parcelas` | Integer | Number of installments |
| `informacoes_adicionais` | Text | Optional |
| `valor_parcela` | Float | Calculated installment value |
| `created_at` | Timestamp | Default: `now()` |

The ORM model mirrors the domain entity but remains infrastructure-specific.

---

### 3. Alembic Migrations

#### `alembic/`

- Schema changes are managed **exclusively via Alembic**
- No runtime `create_all()` calls are used
- Migrations are mandatory for both development and tests

Example:

```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
This guarantees schema reproducibility and test determinism.

### Repository Layer

#### `services/recibo_repository.py`

Defines the repository interface used by the application layer.
No infrastructure details leak into services or domain.

---

### `infrastructure/storage.py`
Implements:
- `PostgresReciboRepository`

Responsibilities:

- Persist Recibo domain objects
- Map between domain and ORM model
- Commit transactions explicitly
- Return fully hydrated domain entities

There is **no file-based or fallback repository** in this branch.

## API Integration

### Dependency Injection
#### `api/deps.py`
- Wires **PostgresReciboRepository** into the application
- Builds **PagamentoService** with explicit dependencies
- Keeps FastAPI routes thin and declarative

### API Layer
#### `api/pagamentos_api.py`
Endpoints:
- `POST /pagamentos/` — required (contract-driven)
- `GET /pagamentos/` — optional (listing persisted receipts)

Responsibilities:
- Input validation via Pydantic DTOs
- Delegation to application services
- Explicit response models (DTOs)

### Testing Strategy

### Test Databases

- Tests run against a **real PostgreSQL schema**
- A dedicated **test database** is required (`loja_test_db`)
- Alembic migrations are applied automatically during tests
- Tables are truncated between test cases

### Test Coverage Summary

| Test Group | Purpose |
|---|---|
| `test_calculadora` | Pure domain rules |
| `test_pagamento_service` | Application use cases |
| `test_postgres_repository` | Repository behavior |
| `test_integration_postgres` | Full stack (API + DB) |
| `test_api_pagamentos` | HTTP contract validation |
| `test_recibo` | Domain entity correctness |

Result:

- Total tests: 24
- Passing: 24
- Failing: 0

### CI Considerations
### Import-Time Database Validation

**Problem**

Database configuration is validated during module import, but CI environments do not define `DATABASE_URL` by default.

**Solution**

The database bootstrap detects test/CI contexts.
In these contexts, a safe default test URL is used.
In real runtime, missing `DATABASE_URL` still raises an error.

This preserves correctness without weakening safety guarantees.

### Current State Summary

| ***Area*** | ***Status*** |
|---|---|
| Domain rules | ✅ Stable |
| PostgreSQL persistence | ✅ Implemented |
| Alembic migrations | ✅ Active |
| API endpoints | ✅ Stable |
| Dependency injection | ✅ Explicit |
| Automated tests | ✅ Passing |
| CI pipeline | ✅ Green |

This branch has **reached its intended conclusion.**

### Non-Goals (Explicitly Out of Scope)

- Frontend or UI implementation
- Authentication / authorization
- Async database drivers
- Query optimization or pagination
- Production hardening (pool tuning, retries, etc.)

These concerns are intentionally deferred.

### Conclusion

The PostgreSQL persistence layer is fully implemented, tested, and integrated.

The backend now represents a **clean, deterministic, API-first architecture** suitable for:

- Further backend extensions
- Frontend consumption via HTTP
- Educational reference for layered design with FastAPI + SQLAlchemy + Alembic

This branch can be considered complete and closed.