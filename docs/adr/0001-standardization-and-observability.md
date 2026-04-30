# ADR 0001: Standardization and Observability

## Status
Accepted

## Context
The Loja App needed to improve its production readiness by addressing technical debt in logging, error handling, and API versioning. The original implementation used simple `print()` statements, had inconsistent error responses, and lacked a versioned API structure, which made it difficult to maintain and scale.

## Decision
We decided to implement a set of core observability and standardization features:

1.  **API Versioning**: Transitioned all API endpoints to a `/api/v1` prefix to allow for future breaking changes without affecting existing clients.
2.  **Structured Logging**: Replaced standard prints with `structlog`, using JSON rendering for production environments.
3.  **Request Tracing**: Added a middleware to inject a unique `Trace ID` (UUID) into every request, returned via the `X-Trace-Id` header.
4.  **Standardized Errors**: Implemented a global exception handling schema that returns a consistent JSON object including an error code, message, and the associated trace ID.
5.  **Soft Deletes**: Added a `deleted_at` column to the database models to allow for logical deletion of records, preserving data integrity and audit trails.
6.  **Robust Rate Limiting**: Replaced custom in-memory rate limiting with `slowapi` to provide a more reliable and configurable protection mechanism.

## Consequences
- **Positive**: Improved debugging capabilities through trace IDs and structured logs. Consistent API contracts for clients. Data safety via soft deletes.
- **Neutral**: Added new dependencies (`structlog`, `slowapi`).
- **Negative**: Clients must update their base URL to include the `/v1` prefix.
