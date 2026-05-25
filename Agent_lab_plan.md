# Agent Lab — Plan de Implementación
> Estado actual: Scout ✅ | Architect (Gemini) ✅ | Architect (Claude) ❌ (Error 404) | Executor ⏳ | Validator ⏳

---

## 1. Contexto

Laboratorio de aprendizaje para construir un pipeline multi-agente de análisis y refactoring de código.
Proyecto objetivo: **Loja App** — sistema de pagos construido con FastAPI + React.

**Objetivo del lab:**
- Aprender orchestration de agentes AI sin frameworks
- Validar el patrón Scout → Architect → Executor → Validator
- Controlar costos usando modelos baratos para tareas de exploración y modelos premium solo para razonamiento

---

## 2. Arquitectura del Pipeline

```
┌─────────────┐     JSON      ┌─────────────┐     Plan JSON   ┌─────────────┐
│    SCOUT    │ ────────────► │  ARCHITECT  │ ──────────────► │  EXECUTOR   │
│ Gemini Flash│               │ Claude Sonnet│                 │   DeepSeek  │
└─────────────┘               └─────────────┘                 └──────┬──────┘
  Read-only                    Valida, prioriza                       │
  Observa, clasifica           Detecta edge cases              ┌──────▼──────┐
  Output: JSON schema          NO implementa                   │  VALIDATOR  │
                                                               │scripts reales│
                                                               │+ LLM summary│
                                                               └──────┬──────┘
                                                                      │
                                                               ┌──────▼──────┐
                                                               │   REVIEWER  │
                                                               │Claude Sonnet│
                                                               │SOLO si diff │
                                                               │es delicado  │
                                                               └─────────────┘
```

### Responsabilidades por capa

| Agente | Modelo | Puede escribir archivos | Responsabilidad |
|---|---|---|---|
| Scout | Gemini Flash | ❌ NUNCA | Scan, clasificar, generar JSON |
| Architect | Claude Sonnet | ❌ NUNCA | Validar findings, priorizar, diseñar orden |
| Executor | DeepSeek / Qwen | ✅ solo tareas aprobadas | Cambios mecánicos de bajo riesgo |
| Validator | Scripts reales + LLM summary | ❌ | lint, tests, typecheck, stderr summary |
| Reviewer | Claude Sonnet | ❌ | Solo en diffs de alto riesgo |

---

## 3. Regla de Oro: El Scout NUNCA implementa

```python
class ScoutAgent:
    ALLOWED_TOOLS   = ["read_file", "list_dir", "grep"]
    FORBIDDEN_TOOLS = ["write_file", "run_command", "delete_file"]
```

Si el Scout tiene permiso de escribir, el pipeline pierde su punto de control.
Esto no es confianza en el modelo — es constraint de diseño.

---

## 4. Risk Policy (Routing del Executor)

```
RIESGO BAJO → Executor (DeepSeek/Qwen)
  - rename de variables
  - agregar type hints
  - mover imports
  - formateo de código
  - eliminar console.log / print debug
  - fix de linting (noqa, line length)

RIESGO MEDIO → Claude Executor
  - refactor de función con side effects
  - cambio de interfaz interna
  - alteración de middleware no crítico

RIESGO ALTO → Claude + human review obligatorio
  - cualquier cosa que toca migrations
  - cambios en auth / payments
  - alteración de contratos de API
  - lógica financiera (recibo.py, calculadora.py)
```

---

## 5. Estructura del Proyecto

```
agent-lab/
├── .env                        # API keys — nunca commitear
├── pipeline.py                 # orquestración manual (pendiente)
├── logger.py                   # logging de todas las llamadas
├── schemas/
│   ├── __init__.py
│   ├── scout_output.py         # ✅ implementado
│   └── architect_output.py     # ⏳ pendiente
├── agents/
│   ├── __init__.py
│   ├── scout.py                # ✅ Gemini Flash — dos pasadas
│   ├── architect.py            # ⚠️  corrió con Gemini, pendiente Claude
│   ├── executor.py             # ⏳ pendiente
│   └── validator.py            # ⏳ pendiente
├── logs/
│   ├── scout_pass1.log
│   ├── scout_pass2.log
│   └── architect.log
└── targets/
    └── loja_app/               # repo objetivo
```

---

## 6. Schemas Implementados

### ScoutOutput (`schemas/scout_output.py`) ✅

```python
from pydantic import BaseModel
from typing import Literal

class Hotspot(BaseModel):
    file: str
    issue: str
    severity: Literal["low", "medium", "high"]
    risk_level: Literal["low", "medium", "high"]
    dependencies: list[str]

class ScoutOutput(BaseModel):
    hotspots: list[Hotspot]
    recommended_order: list[str]
    risks: list[str]
    summary: str
```

### ArchitectOutput (`schemas/architect_output.py`) ⏳ pendiente

```python
from pydantic import BaseModel
from typing import Literal

class Task(BaseModel):
    task_id: str
    title: str
    description: str
    files_to_modify: list[str]
    priority: Literal["low", "medium", "high"]
    effort: Literal["low", "medium", "high"]
    risk_level: Literal["low", "medium", "high"]
    dependencies: list[str]

class ArchitectOutput(BaseModel):
    validated_findings: list[str]
    false_positives: list[str]
    systemic_risks: list[str]
    implementation_plan: list[Task]
    blockers: list[str]
```

---

## 7. Estado actual de implementación

### ✅ Scout — Completo

- Estrategia de dos pasadas (árbol → selección → análisis)
- Pasada 1: solo file tree, < 5K tokens, costo ~$0.001
- Pasada 2: lee 8-12 archivos seleccionados, costo ~$0.003
- Retry automático en 429 (rate limit)
- Logging de tokens y costo por pasada
- Protección contra loop infinito en Windows (os.walk)
- SDK: `google-genai` (nuevo, no deprecado)

**Costo real del Scout en Loja App: ~$0.004**

### ⚠️ Architect — Parcialmente completo

**Lo que corrió:** Gemini Flash

**Resultados obtenidos (logs en `agent-lab/logs/`):**
- Gemini Flash ejecutó con éxito.
- Costo: $0.00039.
- Validación de esquema: OK.

**Problemas:**
- Claude Sonnet falló (Error 404: model not found). Se intentó con `claude-3-5-sonnet-20241022` y `claude-3-5-sonnet-20240620`. Verificar acceso a la API o nombre del modelo.

**Lo que falta:**
- Solucionar error 404 de Claude Sonnet.
- Correr Claude sobre `scout_output_sample.json`.
- Comparar outputs.

### ⏳ Executor — Pendiente

- Implementar routing por risk_level
- DeepSeek para tareas LOW
- Claude para tareas MEDIUM/HIGH
- Nunca ejecutar sin output validado del Architect

### ⏳ Validator — Pendiente

- Scripts reales primero: `pytest`, `ruff`, `tsc --noEmit`
- LLM solo resume stderr — no ejecuta herramientas directamente
- Output: pass/fail + categorización de errores

---

## 8. Lecciones aprendidas hasta ahora

| Problema encontrado | Causa real | Solución aplicada |
|---|---|---|
| Loop infinito en Windows | `rglob` atraviesa junctions antes de filtrar | Cambiar a `os.walk` con IGNORE_DIRS |
| 429 con 50 líneas por archivo | Payload > 250K tokens free tier | Estrategia dos pasadas (árbol → selección) |
| SDK deprecado `google.generativeai` | Google migró a `google-genai` | `uv remove google-generativeai && uv add google-genai` |
| Architect corrió en Gemini no Claude | Cambio sin documentar | Documentado aquí — pendiente comparación |
| JSON con markdown fences | Gemini añade ```json a veces | Strip explícito antes de `json.loads` |

---

## 9. Costos reales vs estimados

| Agente | Modelo | Costo estimado/llamada | Costo real observado |
|---|---|---|---|
| Scout (2 pasadas) | Gemini Flash | ~$0.004 | **$0.004** ✅ |
| Architect | Claude Sonnet | ~$0.013 | pendiente |
| Executor (low risk) | DeepSeek | ~$0.001 | pendiente |
| Validator | Scripts + LLM | ~$0.002 | pendiente |

**Budget Claude disponible: ~$2.50**
**Llamadas Architect posibles: ~190**

---

## 10. Próximos pasos en orden

```
[✅] 1. Crear schemas/architect_output.py con Pydantic
[✅] 2. Reescribir architect.py para usar Claude Sonnet
[❌] 3. Correr Claude sobre scout_output_sample.json (Error 404)
[ ] 4. Comparar output Claude vs output Gemini del Architect
[ ] 5. Documentar diferencias — eso valida el modelo correcto por capa
[ ] 6. Implementar executor.py con routing por risk_level
[ ] 7. Implementar validator.py con scripts reales
[ ] 8. Conectar pipeline.py end-to-end
[ ] 9. Correr pipeline completo sobre loja_app
[ ] 10. Documentar como ADR los patrones que funcionaron
```

---

## 11. Reglas del laboratorio

1. **Scout es read-only.** Sin excepciones.
2. **Logging desde el día 1.** Prompt, response, tokens, latency, costo.
3. **Schema primero.** Define el contrato entre agentes antes de escribir el agente.
4. **Validator usa scripts reales.** LLM solo resume stderr.
5. **Claude entra como reviewer, no como explorer.**
6. **Cualquier cambio de modelo se documenta.** No cambiar Gemini↔Claude sin registrarlo.
7. **Retry policy explícita por agente.** JSON inválido → 1 retry. Path alucinado → reject.

---

## 12. APIs configuradas

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...    # Claude Sonnet — Architect + Reviewer
GOOGLE_API_KEY=...               # Gemini Flash — Scout
DEEPSEEK_API_KEY=...             # DeepSeek — Executor
```

**SDKs instalados:**
```toml
anthropic = "*"
google-genai = "*"
pydantic = "*"
python-dotenv = "*"
httpx = "*"
```