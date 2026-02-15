# Loja App — Backend (Payments API)

![CI](https://github.com/argenis972/Loja_app/actions/workflows/backend-ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Automated%20Tests-brightgreen?style=flat)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DB-336791?style=flat&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

This is the backend component of Loja App, a learning laboratory focused on backend architecture, payment logic, and testing.

---

## Architecture and Purpose

This backend is an API-first payment system built as a learning laboratory. The goal is to maximize clarity, correctness, and architectural reasoning.

The backend is responsible for:

- Enforcing all business rules
- Validating user input and edge cases
- Calculating payment totals and installments with exact precision
- Persisting transactions to database
- Exposing a documented REST API

The domain layer contains no framework dependencies and can be executed in isolation.
Application services orchestrate use cases without embedding business rules.
The frontend is treated as a consumer, never as a source of truth.

### Project Structure

```
backend/
├── alembic/              # Database migrations
│   ├── versions/         # Migration scripts
│   └── env.py            # Alembic configuration
├── api/                  # REST API layer
│   ├── dtos/             # Request/Response models
│   ├── deps.py           # Dependency injection
│   ├── main.py           # FastAPI application
│   └── pagamentos_api.py # Payment endpoints
├── config/               # Configuration
│   ├── settings.py       # Application settings
│   └── taxas.json        # Tax rates configuration
├── domain/               # Business logic (framework-agnostic)
│   ├── calculadora.py    # Payment calculator
│   ├── exceptions.py     # Domain exceptions
│   ├── recibo.py         # Receipt entity
│   └── recibo_repository.py # Repository interface
├── infrastructure/       # External dependencies
│   ├── db/               # Database models and mappers
│   ├── repositories/     # Repository implementations
│   └── database.py       # Database connection
├── services/             # Application services
│   └── pagamento_service.py # Payment use cases
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   ├── services/         # Service tests
│   └── conftest.py       # Pytest fixtures
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Python project configuration
└── alembic.ini           # Alembic configuration
```

---

## Domain and Business Rules

All payment rules live exclusively in the `Calculadora` class (`domain/calculadora.py`). They are framework-agnostic and unit-tested.

### Payment Options

| opcao | Mode | Condition | Rule Applied |
|:-----:|------|-----------|--------------|
| 1 | Cash (À vista) | Immediate payment | 10% discount (configurable via `desconto_vista`) |
| 2 | Debit card (Débito à vista) | Immediate payment | 5% fixed discount |
| 3 | Installments without interest (Parcelado sem juros) | 2 to 6 installments | No interest, exact total |
| 4 | Card with interest (Cartão com juros) | 12 to 24 installments | 10% interest (configurable via `juros_parcelamento`) |

**Note:** Options 3 and 4 have non-overlapping installment ranges (2-6 vs 12-24) to maintain clear separation between no-interest and interest-bearing installment plans.

### Exact Total Calculation

When payments are split into installments, the system automatically calculates the last installment value to ensure the total is exact:

- **Example**: R$ 100.00 in 6 installments
  - 5 installments of R$ 16.67
  - 1 last installment of R$ 16.65
  - **Total**: R$ 100.00 (exactly)

### Validation Rules

| Condition | Exception Raised |
|-----------|------------------|
| `valor <= 0` | Domain exceptions (derived from `DomainError`) or validation errors raised by domain entities. |
| `opcao` not in [1, 2, 3, 4] | Domain exceptions (derived from `DomainError`) or validation errors raised by domain entities. |
| `opcao=3` with `parcelas < 2` or `parcelas > 6` | Domain exceptions (derived from `DomainError`) or validation errors raised by domain entities. |
| `opcao=4` with `parcelas < 12` or `parcelas > 24` | Domain exceptions (derived from `DomainError`) or validation errors raised by domain entities. |

---

## Domain Exceptions

Defined in `domain/exceptions.py`:

| Exception | Description |
|-----------|-------------|
| `DomainError` | Base class for all domain errors |
| `OpcaoInvalidaError` | Invalid payment option |
| `ValorInvalidoError` | Invalid value or installments |
| `RegraPagamentoInvalida` | Invalid payment rule (used by Calculadora) |

The `Calculadora` class uses domain exceptions for all validation errors.

---

## API Layer

### Endpoints

Defined in `api/main.py` and `api/pagamentos_api.py`:

| Method | Path | Description | Status Code |
|--------|------|-------------|-------------|
| POST | `/pagamentos/` | Create and persist a payment | 201 |
| POST | `/pagamentos/simular` | Simulate payment without persistence | 200 |
| GET | `/pagamentos/` | List all persisted payments | 200 |
| GET | `/saude` | Health check | 200 |

### Request DTO

`PagamentoRequest` (from `api/dtos/pagamento_request.py`):

| Field | Type | Required |
|-------|------|----------|
| `opcao` | int | Yes |
| `valor` | float | Yes |
| `parcelas` | int or None | No (defaults to 1 if None) |

### Response DTO

`PagamentoResponse` (from `api/dtos/pagamento_response.py`):

| Field | Type |
|-------|------|
| `id` | int or None |
| `metodo` | str |
| `total` | float |
| `parcelas` | int |
| `valor_parcela` | float |
| `informacoes_adicionais` | str or None |
| `taxa` | float (default 0.0) |
| `tipo_taxa` | str or None |
| `created_at` | datetime or None |

### Error Handling

`DomainError` exceptions are caught by a global handler in `api/main.py` and return HTTP 400:

```python
@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )
```

---

## Service Layer

Defined in `services/pagamento_service.py`:

### Classes

| Class | Description |
|-------|-------------|
| `ProcessarPagamentoUseCase` | Calculates payment and optionally persists via repository |
| `ListarPagamentosUseCase` | Lists all payments from repository |
| `PagamentoService` | Facade that orchestrates use cases |

### PagamentoService

The service is initialized with:
- `repository`: Optional `ReciboRepository` for persistence
- `calculadora`: Optional `Calculadora` instance (defaults to new instance)
- `taxas`: Optional dict with `desconto_vista` and `juros_parcelamento` (defaults to 10.0 each)

Methods:
- `criar_pagamento(opcao, valor, parcelas)` - Creates and persists a payment
- `listar_pagamentos()` - Returns all persisted payments

The service enriches receipts with `taxa` and `tipo_taxa` fields for frontend consumption.

---

## Persistence Layer

### Configuration

Defined in `config/settings.py` using Pydantic Settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_USER` | `loja_user` | Database user |
| `DB_PASSWORD` | `loja_password` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |
| `DB_NAME` | `loja_db` | Database name |
| `DATABASE_URL` | None | Override full connection string |

If `DATABASE_URL` is set, it takes precedence. Otherwise, the URL is built from individual components as `postgresql+psycopg://...`.

### Database Model

`ReciboModel` (from `infrastructure/db/models/recibo_models.py`):

| Column | Type | Nullable |
|--------|------|----------|
| `id` | Integer (PK) | No |
| `total` | Float | No |
| `metodo` | String(50) | No |
| `parcelas` | Integer | No |
| `valor_parcela` | Float | No |
| `informacoes_adicionais` | String | Yes |
| `created_at` | DateTime | No (server default) |

### Repository

`PostgresReciboRepository` (from `infrastructure/repositories/postgres_recibo_repository.py`) implements `ReciboRepository`:

- `salvar(recibo: Recibo) -> Recibo` - Persists a Recibo and returns it with ID
- `listar() -> List[Recibo]` - Returns all receipts ordered by ID descending

### Session Management

`get_db()` in `infrastructure/database.py` provides a session per request with automatic commit on success and rollback on error.

Tables are created on application startup via `create_db_and_tables()`.

---

## Project Structure

```
backend/
├── api/
│   ├── main.py                 # FastAPI app, exception handler, health endpoint
│   ├── pagamentos_api.py       # Payment endpoints
│   ├── deps.py                 # Dependency injection
│   └── dtos/
│       ├── pagamento_request.py
│       └── pagamento_response.py
│
├── config/
│   └── settings.py             # Pydantic Settings configuration
│
├── domain/
│   ├── calculadora.py          # Payment calculation rules
│   ├── recibo.py               # Receipt domain entity
│   ├── recibo_repository.py    # Abstract repository interface
│   └── exceptions.py           # Domain exceptions
│
├── infrastructure/
│   ├── database.py             # Engine, SessionLocal, get_db()
│   ├── db/
│   │   ├── base.py             # SQLAlchemy Base
│   │   └── models/
│   │       └── recibo_models.py
│   └── repositories/
│       └── postgres_recibo_repository.py
│
├── services/
│   └── pagamento_service.py    # Use cases and service facade
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   └── test_calculadora.py
|   ├── services/
│   │   └── test_pagamento_service.py
│   ├── test_recibo.py
│   ├── test_pagamento_service.py
│   ├── test_api_pagamentos.py
│   ├── test_api_pagamentos_errors.py
│   ├─  test_postgres_repository.py
│   ├── test_integration_postgres.py
│   └── test_health.py
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Testing Strategy

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--cov=.", "--cov-report=term-missing", "--cov-report=html"]
```

### Test Files

| File | Type | Description |
|------|------|-------------|
| `unit/test_calculadora.py` | Unit | Domain calculation rules |
| `test_recibo.py` | Unit | Receipt entity validation |
| `test_pagamento_service.py` | Unit | Service with injected rates |
| `test_api_pagamentos.py` | Integration | API endpoint tests |
| `test_api_pagamentos_errors.py` | Integration | Error handling tests |
| `test_postgres_repository.py` | Integration | Repository tests |
| `test_integration_postgres.py` | Integration | Repository integration tests |
| `test_health.py` | Integration | Health endpoint test |

Integration tests use SQLite in-memory databases to avoid requiring a running PostgreSQL instance.

### Running Tests

```bash
cd backend
pytest
```

---

## Running the Backend

### Requirements

- Python 3.11+
- Primary database: PostgreSQL
- Tests and development may use SQLite

### Install and Run

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux / Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn api.main:app --reload
```

### Available URLs

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |
| `http://127.0.0.1:8000/saude` | Health check |

---

## Production Considerations

This is a learning project. In production, you would typically add:

- Authentication and authorization
- Rate limiting
- Structured logging
- Migrations
- Observability

The architecture supports these additions without refactoring the domain layer.

---

## Summary

| Aspect | Implementation |
|--------|----------------|
| Architecture | Layered with domain isolation |
| Business rules | Centralized in `domain/calculadora.py` |
| Persistence | SQLAlchemy with repository pattern |
| Testing | Unit and integration tests with SQLite in-memory |
| Error handling | Domain exceptions mapped to HTTP 400 |
| API design | REST with Pydantic DTOs |

---

<!-- Author and License are declared in the repository root README -->