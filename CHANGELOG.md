# 📊 CHANGELOG

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) with semantic versioning.

This changelog separates three categories:
- 🔥 **Production Incidents** — events that affected system behavior or availability.
- 🚀 **Releases** — versioned feature and improvement history.
- 🔧 **Hardening** — internal improvements (refactors, CI/CD, documentation).

---

## 🔥 Production Incidents

### INC-001 · API Simulation Failure (404 Not Found)
**Period**: v1.0.0 → v1.1.0 (Refactoring Phase)
**Affected**: `POST /api/pagamentos/simular` — Frontend simulation flow.

**What happened**
The backend was refactored to enforce API versioning (`/api/v1/`). However, the frontend configuration in `api.ts` was not synchronized. The frontend continued to call `/api/pagamentos/simular`, resulting in `404 Not Found` errors in production/development environments.

**How it was discovered**
Discovered via backend logs and a user report showing a broken "Confirmar pagamento" screen where simulation data was missing.

**What was tried first (didn't work)**
Attempted to add a temporary redirect at the server level. This was rejected because it would hide the architectural inconsistency rather than fixing it.

**Root cause**
Lack of synchronized deployment between backend route changes and frontend configuration.

**Resolution (v1.1.0)**
Updated `API_BASE_URL` in `frontend/src/config/api.ts` to include the `/v1` prefix. Synchronized all frontend services to match the new versioned path.

**Accepted side effect**
Existing external clients (if any) using the unversioned `/api/` path will remain broken. This is an intentional breaking change to enforce versioning standards.

---

## 🚀 Releases

### [1.1.0] - 2026-04-30
#### Added
- **API Pagination**: Implemented `limit` and `offset` in all listing endpoints (`/api/v1/pagamentos/`). Default limit set to 20.
- **Idempotency Support**: Added `Idempotency-Key` header validation for payment creation. Prevents duplicate transactions on network retries.
- **Structured Error Schema**: All API errors now return a standard `{ error: { code, message, trace_id } }` object.

#### Fixed
- **INC-001: Redundant API Prefix (404 Error)**: 
  - **Symptom**: Requests were being sent to `/api/api/v1/` instead of `/api/v1/`.
  - **Root Cause**: Legacy configuration in `.env.local` (`VITE_API_URL=.../api`) clashed with a naive URL resilience logic that appended `/api/v1` blindly.
  - **Fix**: Implemented `getBaseApiUrl` normalization in `frontend/src/config/api.ts` that intelligently detects existing prefixes (`/api`, `/api/v1`) before appending, making the frontend resilient to environment variable variations.
- **Missing Database Column**: Applied missing Alembic migration to add `idempotency_key` to local SQLite database.
- **PowerShell Syntax**: Fixed `make.ps1` encoding and path resolution issues using `$PSScriptRoot`.
- **Frontend Error Parsing**: Updated UI to gracefully display structured error messages from the backend.

---

## 🔧 Hardening
- **ADR-0002**: Documented Idempotency and Pagination strategies.
- **Test Suite Expansion**: Reached 94% total coverage with new tests for pagination and idempotency.
- **Git Branching**: Standardized branch naming convention (e.g., `feat/pagination-idempotency-sync`).

---

## [1.0.0] - 2026-04-15
### Initial Release
- Basic payment simulation and persistence.
- SQLite support for local development.
- Initial frontend with React and TailwindCSS.
- Basic test suite with 80% coverage.
