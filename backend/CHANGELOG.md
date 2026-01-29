## CHANGELOG

All notable technical changes to this repository are documented in this file.  
This project follows a **learning-driven evolution**, not semantic versioning.

---

### [Unreleased] — Current State

- Backend consolidated as **API-first**
- PostgreSQL persistence fully implemented
- Test suite stable and deterministic
- Branch `Criar_PostgreSQL` considered **complete**

---

### [2026-01] — PostgreSQL Persistence Refactor (`Criar_PostgreSQL`)

#### Added

- PostgreSQL persistence using **SQLAlchemy 2.x**
- Alembic migrations for schema management
- Repository abstraction (`ReciboRepository`)
- Concrete implementation: `PostgresReciboRepository`
- Dependency Injection via FastAPI (`api/deps.py`)
- Real database integration tests
- CI-safe database bootstrap logic
- Explicit test database (`loja_test_db`)
- Migration-based test setup (no `create_all`)

#### Changed

- Application architecture refactored into clear layers:
  - `domain`
  - `services`
  - `infrastructure`
  - `api`
- Business logic isolated from infrastructure
- API endpoints became the primary execution path
- Database validation moved to controlled bootstrap logic
- Tests now run against real PostgreSQL instead of mocks

#### Removed

- Local CLI-style execution flow
- Experimental `ui/` folder
- File-based or fallback repositories
- Implicit database initialization
- Tight coupling between execution and persistence

#### Rationale

This refactor was performed to:
- practice clean backend architecture,
- enforce persistence correctness,
- improve test reliability,
- shift from exploratory scripts to a structured backend system.

---

### [Earlier Iterations] — Exploration Phase

#### Characteristics

- Simple `main.py` execution
- Local UI for manual interaction
- File-based persistence
- Minimal test coverage
- Fast iteration over structure

#### Outcome

These iterations were valuable for learning but became limiting once:
- persistence was introduced,
- API contracts mattered,
- automated testing became a priority.

They were intentionally removed to reduce architectural noise.

---

### Notes

- This repository is **not versioned for production use**
- Changes reflect **learning milestones**, not releases
- Frontend/UI is intentionally out of scope
- Future work may include:
  - separate frontend project
  - additional API features
  - architectural experiments

---

### Status

Backend refactor complete.  
Branch `Criar_PostgreSQL` closed by design.
