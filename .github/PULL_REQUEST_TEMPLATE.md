## What & Why

<!-- What changed and why. 
     If this fixes a bug: Closes INC-XXX or link to issue.
     If this is a feature: Describe the value for the user. -->

## Type of change

- [ ] `feat` · [ ] `fix` · [ ] `perf` · [ ] `refactor` · [ ] `chore` · [ ] `docs` · [ ] `ci`

## Definition of Done Checklist

- [ ] `lint` / `ruff` passes locally.
- [ ] New logic has unit tests (`test_<unit>_<scenario>_<expected_result>`).
- [ ] `CHANGELOG.md` updated if behavior changed.
- [ ] ADRs updated if an architectural decision was made.
- [ ] No placeholder values or TODOs.

## How to test

<!-- Describe how to verify this change. Include endpoints and payloads. -->

```bash
# Example test command
curl -X POST http://localhost:8000/api/v1/pagamentos/ \
  -H "Idempotency-Key: test-key-1" \
  -d '{"opcao": 1, "valor": 100.0, "parcelas": 1}'
```

## Trade-offs and Consequences

<!-- What did you choose NOT to do? What are the side effects? 
     Example: "Used in-memory store for idempotency which won't scale across workers without Redis." -->

## Screenshots / Evidence

<!-- Add screenshots for UI changes or terminal output for backend changes. -->
