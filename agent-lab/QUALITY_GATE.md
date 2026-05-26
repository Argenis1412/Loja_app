# Quality Gate — Pre-Merge Checklist

## Comandos obligatorios (deben pasar todos)

### 1. Lint
```bash
ruff check .
```

### 2. Type check (schemas)
```bash
python -c "from schemas.scout_output import ScoutOutput; from schemas.architect_output import ArchitectOutput; from schemas.executor_output import ExecutorOutput; from schemas.validator_output import ValidatorOutput; print('OK')"
```

### 3. Unit tests
```bash
pytest tests/ -m unit -v
```

## Criterios de aprobación
- [ ] `ruff check .` → 0 errores
- [ ] `pytest tests/ -m unit` → 100% pass
- [ ] Ningún `print("PASS")` ni `print("FAIL")` en tests
- [ ] Todo agente retorna `tuple[Output, dict]` con meta completo
