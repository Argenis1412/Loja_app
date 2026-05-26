## Descripción de los cambios
Este PR cierra la **Fase 2: Calidad y Testing** del epic #13 (Stabilizing Agent-Lab). El objetivo principal fue transformar la suite de pruebas de scripts de validación manual a una suite profesional basada en `pytest` con asserts determinísticos y mocks, garantizando la estabilidad del contrato entre agentes.

## Cambios clave
- **Configuración de Pytest**: Se habilitó `[tool.pytest.ini_options]` en `pyproject.toml` con `pythonpath = ["."]`.
- **Infrastructure de Tests**: Creación de `tests/conftest.py` con fixtures para aislamiento de SDKs.
- **Suite de Tests**: Implementación de 5 módulos de prueba (`test_scout`, `test_architect`, `test_executor`, `test_validator`, `test_schemas`) reemplazando el legado `test_signatures.py`.
- **Calidad**: Inclusión de `QUALITY_GATE.md` como checklist obligatorio pre-merge.
- **Resolución de Bloqueos**: Creación de `schemas/pipeline_run.py` para corregir errores de importación en el pipeline.

## Checklist de validación
- [x] `ruff check .` pasa sin errores.
- [x] `pytest tests/ -m unit` (suite completa operativa).
- [x] Schema `pipeline_run` implementado y testeado.
- [x] Eliminada deuda técnica de `test_signatures.py`.

## Impacto
Mejora sustancial en la detectabilidad de fallos en el contrato entre agentes. Cualquier cambio futuro que rompa los esquemas Pydantic será detectado inmediatamente en CI.
