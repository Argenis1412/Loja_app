# Handoff: Pipeline de Análisis y Refactoring

| Agente | Estado | Descripción |
|---|---|---|
| Scout | ✅ Completo | Gemini Flash (2 pasadas), read-only, JSON output. |
| Architect | ✅ Completo | Claude Sonnet, validador de findings, planificador. |
| Executor | ⏳ Pendiente | Routing por risk_level, implementación de cambios. |
| Validator | ✅ Completo | ruff + pytest + tsc, Gemini summary de errores. |
| Reviewer | ⏳ Pendiente | Claude Sonnet, revisión final en cambios de alto riesgo. |
