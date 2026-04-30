# ADR 0002: Idempotency and Pagination Implementation

## Status
Proposed

## Context
As the Loja App scales and integrates with frontends and external systems, it is critical to ensure:
1. **Reliability**: Avoiding duplicate payments if a request is retried (Idempotency).
2. **Performance**: Preventing large data transfers and backend strain when listing records (Pagination).

## Decision
We decided to implement:
1. **Idempotency**: Using an `Idempotency-Key` header in `POST` requests. This key is stored in the `recibos` table. Before processing a new payment, the system checks if a record with the same key exists. If it does, the existing record is returned without re-calculating or re-persisting.
2. **Pagination**: Implementing `limit` and `offset` parameters in all list endpoints. The default limit is set to 20, and the maximum is 100 (as per Engineering Playbook).

## Consequences
- The `recibos` table now has an `idempotency_key` column with a unique index.
- API clients must now handle paginated responses (if they want more than 20 records).
- Duplicate requests with the same key are safely handled, returning the original receipt.
