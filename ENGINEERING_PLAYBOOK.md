# 📜 Engineering Playbook

> Standards are only useful when you understand why they exist. 
> Every rule here was born from a failure or a hard-learned lesson in system reliability.

---

## 1. Commit Protocol (Atomic & Conventional)

**Format**: `type(scope): description` — [Conventional Commits](https://www.conventionalcommits.org/)

| Type | When to use |
|:---|:---|
| `feat` | New capability visible to users or API consumers |
| `fix` | Corrects broken behavior (e.g., INC-001) |
| `perf` | Measurable performance improvement |
| `refactor` | Internal restructuring with no behavior change |
| `test` | Tests only — no production code |
| `docs` | Documentation only |
| `ci` | CI/CD pipeline changes |

**Atomic commits**: One logical change per commit. Never mix a feature with a refactor. 

**`ci:` commits are prioritized above all other work.** A broken pipeline is a blocked project.

---

## 2. Branch Naming Convention

**Pattern**: `type/short-description` — lowercase, hyphens only.

```text
feat/pagination-support
fix/api-404-versioning
refactor/repository-pattern
docs/add-adr-idempotency
```

---

## 3. CI/CD — Green Pipeline Requirement

No merge to `main` without passing:

1. **`lint`** — `ruff` + `mypy`. Style is automated, not debated in reviews.
2. **`test`** — Full suite with 90%+ coverage threshold enforced.
3. **`build`** — Docker build succeeds. Proves the artifact is deployable.

**Why this matters**: In financial apps, a missing column in a production migration can crash the entire payment flow. The `build` and `test` steps ensure the schema and code are perfectly synced.

---

## 4. Architecture & Design

**Clean Architecture layers**: `Domain → Services → Infrastructure`.

- **The Rule**: Business logic (Domain) MUST NOT import from infrastructure (SQLAlchemy, FastAPI).
- **The Proof**: We can swap SQLite for Postgres or an In-Memory Repo for tests without changing a single line in `domain/recibo.py`.

---

## 5. API Design Contract

**Versioning from Day 1**: All routes at `/api/v1/...`. 
**Why**: INC-001 showed that unversioned changes break frontend consumers. Versioning allows for safe evolution.

**Consistent Error Schema**:
```json
{
  "error": {
    "code": "PAYMENT_FAILED",
    "message": "Detailed message for humans",
    "trace_id": "unique-request-uuid"
  }
}
```
Never return raw strings. Standard schemas allow the frontend to implement a single, robust error handling strategy.

---

## 6. Financial Integrity (Idempotency)

**Mutating endpoints** (POST for payments) must accept an `Idempotency-Key` header.
- **Decision**: Duplicate requests with the same key return the original response without creating a second record.
- **Why**: Prevents double-charging a user if their internet drops during a transaction and the browser retries the request.

---

## 7. Performance & Pagination

**No unbounded lists**. Every listing endpoint must support `limit` and `offset`.
- **Defaults**: `limit=20`, `max=100`.
- **Why**: Returning 10,000 records from a single request causes memory exhaustion in the backend and freezes the frontend.

---

## 8. Definition of Done (DoD)

A task is **NOT DONE** until:
- [ ] Passes `ruff` and `pytest` locally.
- [ ] New logic has unit tests covering success and failure scenarios.
- [ ] `CHANGELOG.md` updated if behavior changed.
- [ ] `ARCHITECTURE.md` or ADRs updated for non-obvious decisions.
- [ ] No placeholders, no `TODO` comments in committed code.

---

## 9. Incident Protocol

Every significant production failure generates an entry in `CHANGELOG.md` under `🔥 Production Incidents`.
- **Format**: What happened, Root Cause, Resolution, and Accepted Side Effects.
- **Goal**: Technical honesty. We don't hide failures; we document them so they never happen again.

---

*Last updated: 2026-04-30 (v1.1.0)*
